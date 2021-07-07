# Standard imports
from copy import deepcopy
from typing import Dict, Callable, List
# Local imports
from ....io import IO

class SourceHook:

    def __init__(self, source_dir_path : str) -> None:
        ## Vars.
        self.listeners = {
            "add_to_source" : [], "remove_from_source" : [], "cleanup" : []}
        self.permanent_items = dict()
        self.temp_items = dict()
        self.source_dir_path = source_dir_path
        ## Objects
        self.io = IO()
        ## Checks
        if not self.io.is_directory(source_dir_path):
            raise Exception("Source directory invalid")
        self.cleanup()

    ################################## MODIFIERS #############################

    def add_to_source(self, identifier : str, path : str,
            is_permanent : bool) -> bool:
        # Check type
        if (not self.io.is_directory(path) and not self.io.is_file(path)) or \
                self.is_item(identifier):
            return False
        # Generate the new path.
        if self.io.is_directory(path):
            new_path = "{}/{}".format(
                self.source_dir_path,self.io.get_name(path))
        else:
            new_path = "{}/{}.{}".format(
                self.source_dir_path,self.io.get_name(path),
                self.io.get_file_extension(path)[1])
        # If file is already present, simply add it to hooks.
        if not (self.io.is_file(new_path) or self.io.is_directory(new_path)):
            # TODO: Determine if this should be move or copy.
            if not self.io.copy(path,new_path):
                return False
        if is_permanent:
            self.permanent_items[identifier] = new_path
        else:
            self.temp_items[identifier] = new_path
        # Execute listener on true only.
        self._execute_callables("add_to_source")
        return True

    def remove_from_source(self, identifier : str) -> bool:
        if not self.is_item(identifier):
            return False
        # Delete the item
        if identifier in self.permanent_items:
            path = self.permanent_items[identifier]
            del self.permanent_items[identifier]
        else:
            path = self.temp_items[identifier]
            del self.temp_items[identifier]
        if not self.io.delete(path):
            return False
        self._execute_callables("remove_from_source")
        return True

    def cleanup(self) -> bool:
        self._delete_paths(self.io.paths_of_subdirectories(
            self.source_dir_path)[1])
        self._delete_paths(self.io.path_of_files_in_directory(
            self.source_dir_path,["*"],False)[1])
        self.permanent_items.clear()
        self.temp_items.clear()
        self._execute_callables("cleanup")

    def register_listener(self, listener_type,
            callable : Callable[[str],None]) -> bool:
        if not listener_type in self.listeners:
            return False
        self.listeners[listener_type].append(callable)
        return True

    def copy_permanent_items(self, result_dir_path : str) -> bool:
        if not self.io.is_directory(result_dir_path):
            return False
        # Move all permanent paths to this directory.
        for identifier, path in self.get_permanent_hooked_items().items():
            if not self.io.copy(path,result_dir_path):
                return False
        return True

    ################################## GETTERS ###############################

    def is_item(self, identifier : str) -> bool:
        return identifier in self.permanent_items or \
            identifier in self.temp_items

    def get_path(self) -> str:
        return self.source_dir_path

    def get_item_path(self, identifier : str) -> str:
        if identifier in self.permanent_items:
            return self.permanent_items[identifier]
        elif identifier in self.temp_items:
            return self.temp_items[identifier]
        return None

    def get_hooked_items(self) -> Dict[str,str]:
        hooked_items = dict()
        for identifier, path in self.permanent_items.items():
            hooked_items[identifier] = path
        for identifier, path in self.temp_items.items():
            hooked_items[identifier] = path
        return hooked_items

    def get_permanent_hooked_items(self) -> Dict[str,str]:
        return deepcopy(self.permanent_items)

    def get_temporary_hooked_items(self) -> Dict[str,str]:
        return deepcopy(self.temp_items)

    ############################### PRIVATE METHODS ##########################

    def _execute_callables(self, listener_type : str) -> None:
        callables = self.listeners[listener_type]
        for method in callables:
            try:
                method(self.source_dir_path)
            except:
                pass

    def _delete_paths(self, paths : List[str]) -> bool:
        return all([self.io.delete(path) for path in paths ])