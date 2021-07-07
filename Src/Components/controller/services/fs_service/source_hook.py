# Standard imports
from copy import deepcopy
from typing import Dict, Callable, List
# Local imports
from ....io import IO

class SourceHook:
    """
    File system hook for a source.
    """

    def __init__(self, parent_dir_path : str, source_name : str) -> None:
        """
        Args:
            parent_dir_path (str): Path to the parent directory for this hook.
        """
        ## Objects
        self.io = IO()
         ## Checks
        if not self.io.is_directory(parent_dir_path):
            raise Exception("Source directory invalid")
        ## Vars.
        self.listeners = {
            "add_to_source" : [], "remove_from_source" : [], "cleanup" : []}
        self.permanent_items = dict()
        self.temp_items = dict()
        self.parent_dir_path = parent_dir_path
        self.source_name = source_name
        # Initialize the source dir path
        self.source_dir_path = self._initialize_source_dir(
            parent_dir_path, source_name)
        self.cleanup()

    ################################## MODIFIERS #############################

    def add_to_source(self, identifier : str, path : str,
            is_permanent : bool) -> bool:
        """
        Add an item with the specified identifier to the source.
        The item must be a file or directory that is moved into the source.
        If is_permanent, this item is considered a permanently hooked item,
        otherwise it is a temporary hooked item that is not saved with results.

        Args:
            identifier (str)
            path (str): File or directory path.
            is_permanent (bool)

        Returns:
            (bool): True if added, False otherwise.
        """
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
        """
        Remove the item with the specified identifier if it exists.

        Args:
            identifier (str)

        Returns:
            (bool): True if removed, False otherwise.
        """
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

    def cleanup(self) -> None:
        """
        Cleanup this source hook, removing all items in the hook.
        """
        self.io.delete(self.source_dir_path)
        self.io.create_directory(self.source_dir_path)
        self.permanent_items.clear()
        self.temp_items.clear()
        self._execute_callables("cleanup")

    def register_listener(self, listener_type,
            callable : Callable[[str],None]) -> bool:
        """
        Add a listener that takes in the source hook name and is executed
        when the listener type method successfully finishes execution.

        Args:
            listener_type (str): one of add_to_source, remove_from_source, or
                                cleanup.
            callable ( Callable[[str],None])

        Returns:
            (bool): True if successfully registered, False otherwise.
        """
        if not listener_type in self.listeners:
            return False
        self.listeners[listener_type].append(callable)
        return True

    def copy_permanent_items(self, result_dir_path : str) -> bool:
        """
        Copy all permanent items to the specified directory.
        Directory must exist.

        Args:
            result_dir_path (str)

        Returns:
            (bool): True if copied, False otherwise.
        """
        if not self.io.is_directory(result_dir_path):
            return False
        # Move all permanent paths to this directory.
        for identifier, path in self.get_permanent_hooked_items().items():
            if not self.io.copy(path,result_dir_path):
                return False
        return True

    ################################## GETTERS ###############################

    def is_item(self, identifier : str) -> bool:
        """
        Determine if an item with the given identifier exists.

        Args:
            identifier (str)

        Returns:
            (bool): True if the item exists, False otherwise.
        """
        return identifier in self.permanent_items or \
            identifier in self.temp_items

    def get_path(self) -> str:
        """
        Obtain the path to the source directory.

        Returns:
            (str): Path to the directory
        """
        return self.source_dir_path

    def get_item_path(self, identifier : str) -> str:
        """
        Get path to the item if it exists.

        Args:
            identifier (str)

        Returns:
            (str): Item path if it exists, None otherwise.
        """
        if identifier in self.permanent_items:
            return self.permanent_items[identifier]
        elif identifier in self.temp_items:
            return self.temp_items[identifier]
        return None

    def get_hooked_items(self) -> Dict[str,str]:
        """
        Obtain a mapping from hooked items to their paths.

        Returns:
            (Dict[str,str]): Identifier to path map
        """
        hooked_items = dict()
        for identifier, path in self.permanent_items.items():
            hooked_items[identifier] = path
        for identifier, path in self.temp_items.items():
            hooked_items[identifier] = path
        return hooked_items

    def get_permanent_hooked_items(self) -> Dict[str,str]:
        """
        Obtain a mapping from identifier to path for permanent hooked items.

        Returns:
            (Dict[str,str]): Identifier to path map
        """
        return deepcopy(self.permanent_items)

    def get_temporary_hooked_items(self) -> Dict[str,str]:
        """
        Obtain a mapping from identifier to path for temporary hooked items.

        Returns:
            (Dict[str,str]): Identifier to path map
        """
        return deepcopy(self.temp_items)

    ############################### PRIVATE METHODS ##########################

    def _execute_callables(self, listener_type : str) -> None:
        """
        Execute listener of the specified type.
        """
        callables = self.listeners[listener_type]
        for method in callables:
            try:
                method(self.source_name)
            except:
                pass

    def _delete_paths(self, paths : List[str]) -> bool:
        """
        Delete all the paths.
        """
        return all([self.io.delete(path) for path in paths ])

    def _initialize_source_dir(self, parent_dir_path : str, \
            source_name : str) -> str:
        """
        Initialize the source directory.
        """
        dir_path =  "{}/{}".format(parent_dir_path, source_name)
        self.io.create_directory(dir_path)
        return dir_path
