# Standard library imports
from typing import List, Callable, Dict
from copy import deepcopy

# Local imports

# Third party imports

class ObjectManager:

    def __init__(self) -> None:
        self.objects = dict()

    ############################# MODIFIERS ##################################

    def add_object(self, object_name : str, obj : object,
            overwrite_existing : bool = False) -> bool:
        if not overwrite_existing and object_name in self.objects:
            return False
        self.objects[object_name] = obj
        return True

    def remove_object(self, object_name : str) -> bool:
        if object_name in self.objects:
            del self.objects[object_name]
            return True
        return False

    def clear_objects(self) -> bool:
        self.objects.clear()
        return True

    ################################ GETTERS #################################

    def is_object(self, object_name : str) -> bool:
        return object_name in self.objects

    def get_object_names(self) -> List[str]:
        return list(self.objects.keys())

    def get_object(self, object_name : str, deep_copy : bool = False) -> object:
        if not self.is_object(object_name):
            return
        if deep_copy:
            return deepcopy(self.objects[object_name])
        return self.objects[object_name]

    def get_filtered_objects(self, func : Callable[[str,object],bool]) -> Dict[str,object]:
        filtered_objects = dict()
        for name,obj in self.objects.items():
            try:
                if func(name,obj):
                    filtered_objects[name] = obj
            except:
                pass
        return filtered_objects

    def get_all_objects(self) -> Dict[str,object]:
        return self.get_filtered_objects(
            lambda name, obj: name in self.objects.keys())


    ############################# SETTERS ####################################


    ############################# PRIVATE METHODS #############################
