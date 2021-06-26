# Standard library imports
from typing import Any, List, Dict
from abc import ABC, abstractmethod
import imp
# Local imports
from .config import Config
from ..manager import ObjectManager

# Third party imports

class Loader(ABC):

    def __init__(self) -> None:
        ## Objects
        self.manager = ObjectManager()

    ################################# MODIFIERS #############################

    @abstractmethod
    def load_plugin_using_config(self, plugin_config : Config) -> bool:
        """
        Load a plugin using information provided in the Config.

        Args:
            plugin_config (Config)

        Returns:
            (bool): True if successful. False otherwise.
        """
        pass

    ################################# GETTERS ###############################

    def is_plugin_loaded(self, plugin_name : str) -> bool:
        """
        Determine if the plugin is loaded.

        Args:
            plugin_name (str): Name of the plugin.

        Returns:
            (bool): True if successful. False otherwise.
        """
        return self.manager.is_object(plugin_name)

    def get_loaded_plugin_names(self) -> List[str]:
        """
        Obtain the names of all loaded plugins.

        Returns:
            (List[str]): Names of all plugins.
        """
        return self.manager.get_object_names()

    def get_plugin(self, plugin_name : str) -> Any:
        """
        Obtain the specified plugin.

        Args:
            plugin_name (str)

        Returns:
            (Any)
        """
        if not self.is_plugin_loaded(plugin_name):
            return
        return self.manager.get_object(plugin_name)

    def get_all_plugins(self) -> Dict[str,Any]:
        """
        Obtain all plugins.

        Returns:
            (Dict[str,Any]): Mapping from plugin name to object.
        """
        return self.manager.get_all_objects()

    ######################### PRIVATE METHODS ###############################

    def _add_plugin(self, plugin_name : str, plugin : Any) -> bool:
        """
        Add a plugin with the specified name to the manager.
        """
        return self.manager.add_object(plugin_name,plugin,True)

    def _load_class_from_file(self, file_path : str, module_name : str,
            class_name : str, *args, **kwargs) -> object:
        """
        Given a file path, load the specified class in the specified module
        from the path. The class is initialized with *args, **kwargs.
        """
        try:
            module_type = imp.load_source(module_name, file_path)
            clazz = getattr(module_type,class_name)
            instance = clazz(*args,**kwargs)
            return instance
        except Exception as e:
            pass





