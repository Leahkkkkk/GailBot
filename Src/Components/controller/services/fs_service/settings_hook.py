# Standard imports
from typing import Dict, Callable
# Local imports
from ....io import IO
from ....organizer import Settings

class SettingsHook:

    def __init__(self, settins_profile_name : str,
            parent_dir_path : str, settings_profile_extension : str) -> None:
        ## Objects
        self.listeners = {
            "save" : [], "load" : [], "cleanup" : []}
        self.io = IO()
        if not self.io.is_directory(parent_dir_path):
            raise Exception("Parent directory invalid")
        ## Vars.
        self.settings_profile_name = settins_profile_name
        self.parent_dir_path = parent_dir_path
        self.settings_profile_extension = settings_profile_extension

    ################################## MODIFIERS #############################

    def save(self, settings : Settings) -> bool:
        self._execute_callables("save")
        path = self._get_profile_path()
        return settings.save_to_file(
            lambda data: self.io.write(path,data,True))

    def load(self) -> Dict:
        self._execute_callables("load")
        path = self._get_profile_path()
        if not self.io.is_file(path):
            return {}
        success, data = self.io.read(path)
        if not success:
            return {}
        return data

    def cleanup(self) -> None:
        self._execute_callables("cleanup")
        self.io.delete(self._get_profile_path())

    def register_listener(self, listener_type,
            callable : Callable[[str],None]) -> bool:
        if not listener_type in self.listeners:
            return False
        self.listeners[listener_type].append(callable)
        return True

    ################################## GETTERS ###############################

    def is_saved(self) -> bool:
        return self.io.is_file(
            self._get_profile_path())

    def get_parent_dir_path(self) -> str:
        return self.parent_dir_path

    def get_profile_path(self) -> str:
        return self._get_profile_path()

    ############################### PRIVATE METHODS ##########################

    def _get_profile_path(self) -> str:
        return "{}/{}.{}".format(self.parent_dir_path,
            self.settings_profile_name,self.settings_profile_extension)

    def _execute_callables(self, listener_type : str) -> None:
        callables = self.listeners[listener_type]
        for method in callables:
            try:
                method(self.settings_profile_name)
            except:
                pass
