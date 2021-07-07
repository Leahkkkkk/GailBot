# Standard imports
from typing import Dict, Callable, Any
# Local imports
from ....io import IO
from ....organizer import Settings

class SettingsHook:
    """
    File system hook for a settings profile.
    """

    def __init__(self, settins_profile_name : str,
            parent_dir_path : str, settings_profile_extension : str) -> None:
        """
        Args:
            settings_profile_name (str)
            parent_dir_path (str): Directory in which the hook is created.
            settings_profile_extension (str): Extension for a settings profile.
        """
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
        """
        Save the given settings object to the hook.
        Must have a settings.save_to_file method.

        Args:
            settings (Settings)

        Returns:
            (bool): True if successfully saved. False otherwise.
        """
        self._execute_callables("save")
        path = self._get_profile_path()
        return settings.save_to_file(
            lambda data: self.io.write(path,data,True))

    def load(self) -> Dict[str,Any]:
        """
        Load a settings profile data from the hook.

        Returns:
            (Dict[str,Any])
        """
        self._execute_callables("load")
        path = self._get_profile_path()
        if not self.io.is_file(path):
            return {}
        success, data = self.io.read(path)
        if not success:
            return {}
        return data

    def cleanup(self) -> None:
        """
        Cleanup the hook, removing all files inside the hook.
        """
        self._execute_callables("cleanup")
        self.io.delete(self._get_profile_path())

    def register_listener(self, listener_type : str,
            callable : Callable[[str],None]) -> bool:
        """
        Add a listener that takes in the settings hook name and is executed
        when the listener type method successfully finishes execution.

        Args:
            listener_type (str): one of save, load, or cleanup.
            callable ( Callable[[str],None])

        Returns:
            (bool): True if successfully registered, False otherwise.
        """
        if not listener_type in self.listeners:
            return False
        self.listeners[listener_type].append(callable)
        return True

    ################################## GETTERS ###############################

    def is_saved(self) -> bool:
        """
        Determine if the settings is saved to the hook.

        Returns:
            (bool): True if the settings is saved, False otherwise.
        """
        return self.io.is_file(
            self._get_profile_path())

    def get_parent_dir_path(self) -> str:
        """
        Obtain the path to the parent directory for this hook.

        Returns:
            (str): Parent dir path.
        """
        return self.parent_dir_path

    def get_profile_path(self) -> str:
        """
        Obtain the path to the settings profile file.

        Returns:
            (str): Path to the settings profile file.
        """
        return self._get_profile_path()

    ############################### PRIVATE METHODS ##########################

    def _get_profile_path(self) -> str:
        """
        Generate path for the settings profile file.
        """
        return "{}/{}.{}".format(self.parent_dir_path,
            self.settings_profile_name,self.settings_profile_extension)

    def _execute_callables(self, listener_type : str) -> None:
        """
        Execute a callable of the specified listener type.
        """
        callables = self.listeners[listener_type]
        for method in callables:
            try:
                method(self.settings_profile_name)
            except:
                pass
