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
        pass

    ################################# GETTERS ###############################

    def is_plugin_loaded(self, plugin_name : str) -> bool:
        return self.manager.is_object(plugin_name)

    def get_loaded_plugin_names(self) -> List[str]:
        return self.manager.get_object_names()

    def get_plugin(self, plugin_name : str) -> Any:
        if not self.is_plugin_loaded(plugin_name):
            return
        return self.manager.get_object(plugin_name)

    def get_all_plugins(self) -> Dict[str,Any]:
        return self.manager.get_all_objects()

    ######################### PRIVATE METHODS ###############################

    def _add_plugin(self, plugin_name : str, plugin : Any) -> bool:
        return self.manager.add_object(plugin_name,plugin,True)

    def _load_class_from_file(self, file_path : str, module_name : str,
            class_name : str, *args, **kwargs) -> object:
        try:
            module_type = imp.load_source(module_name, file_path)
            clazz = getattr(module_type,class_name)
            instance = clazz(*args,**kwargs)
            return instance
        except Exception as e:
            pass





