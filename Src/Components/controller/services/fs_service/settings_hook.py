# Standard imports
from Src.utils.observer.subscriber import Subscriber
from typing import Dict, Callable, Any
# Local imports
from .....utils.observer import ObserverEventManager, Subscriber
from .....utils.manager import ObjectManager
from ....io import IO
from ....organizer import Settings

class SettingsHook:
    """
    File system hook for a settings profile.
    """

    EVENT_TYPES = ("save", "load", "cleanup")

    def __init__(self, settings_profile_name : str,
            parent_dir_path : str, settings_profile_extension : str) -> None:
        """
        Args:
            settings_profile_name (str)
            parent_dir_path (str): Directory in which the hook is created.
            settings_profile_extension (str): Extension for a settings profile.
        """
        ## Vars.
        self.settings_profile_name = settings_profile_name
        self.parent_dir_path = parent_dir_path
        self.settings_profile_extension = settings_profile_extension
        ## Objects
        self.io = IO()
        self.observers = ObserverEventManager()
        ## Initializing
        self._initialize(
            settings_profile_name, parent_dir_path, settings_profile_extension)

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
        path = self._generate_profile_path(
            self.settings_profile_name, self.parent_dir_path,
            self.settings_profile_extension)
        try:
            if settings.save_to_file(
                    lambda data : self.io.write(path,data,True)):
                self.observers.notify("save",{"settings" : Settings})
                return True
            return False
        except:
            return False

    def load(self) -> Dict[str,Any]:
        """
        Load a settings profile data from the hook.

        Returns:
            (Dict[str,Any])
        """
        path = self._generate_profile_path(
            self.settings_profile_name, self.parent_dir_path,
            self.settings_profile_extension)
        success, data = self.io.read(path)
        if not success:
            return {}
        self.observers.notify("load",{"data" : data})
        return data

    def cleanup(self) -> None:
        """
        Cleanup the hook, removing all files inside the hook.
        """
        path = self._generate_profile_path(
            self.settings_profile_name, self.parent_dir_path,
            self.settings_profile_extension)
        self.io.delete(path)
        self.observers.notify("cleanup",{})

    def register_listener(self, event_type : str,
            subscriber : Subscriber) -> bool:
        """
        Add a listener that takes in the settings hook name and is executed
        when the listener type method successfully finishes execution.

        Args:
            listener_type (str): one of save, load, or cleanup.
            callable ( Callable[[str],None])

        Returns:
            (bool): True if successfully registered, False otherwise.
        """
        if not event_type in self.EVENT_TYPES:
            return
        self.observers.subscribe(event_type, subscriber)

    ################################## GETTERS ###############################

    def is_saved(self) -> bool:
        """
        Determine if the settings is saved to the hook.

        Returns:
            (bool): True if the settings is saved, False otherwise.
        """
        path = self._generate_profile_path(
            self.settings_profile_name, self.parent_dir_path,
            self.settings_profile_extension)
        return self.io.is_file(path)

    ############################### PRIVATE METHODS ##########################

    def _initialize(self, settings_profile_name : str,
                parent_dir_path : str, settings_profile_extension : str) -> None:
        # Must not already exist.
        if not self.io.is_directory(parent_dir_path) or \
                self.io.is_file(self._generate_profile_path(
                    settings_profile_name, parent_dir_path,
                    settings_profile_extension)):
            raise Exception("Unable to configure settings hook")

    def _generate_profile_path(self, settings_profile_name : str,
                parent_dir_path : str, settings_profile_extension : str) -> str:
            return "{}/{}.{}".format(parent_dir_path, settings_profile_name,
                settings_profile_extension)
