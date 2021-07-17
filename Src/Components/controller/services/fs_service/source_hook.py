# Standard imports
from dataclasses import dataclass
from typing import Dict, Callable, List, Any
# Local imports
from .....utils.observer import ObserverEventManager, Subscriber
from .....utils.manager import ObjectManager
from ....io import IO

@dataclass
class HookedItem:
    identifier : str
    path : str
    item_type : str

class SourceHook:
    """
    File system hook for a source.
    """

    ITEM_TYPES = ("permanent", "temporary","workspace")
    EVENT_TYPES = (
        "add_to_source", "remove_from_source","cleanup",
        "save_to_directory", "destroy")

    def __init__(self, parent_dir_path : str, source_name : str,
            result_dir_path : str) -> None:
        ## Objects
        self.io = IO()
        self.observers = ObserverEventManager()
        self.hooked_items = ObjectManager()
        ## Vars.
        self.parent_dir_path = parent_dir_path
        self.result_dir_path = self._generate_result_dir_path(
            result_dir_path,source_name)
        self.source_name = source_name
        self.source_dir_path = None
        self.permanant_dir_path = None
        self.temp_dir_path = None
        self.ws_dir_path = None

        # Initializing the source directory.
        self._initialize_source_directory(
            parent_dir_path, source_name)


    ################################# MODIFIERS #############################

    def add_to_source(self, identifier : str, path : str,
            item_type : str, copy : bool = False) -> bool:
        """
        Add an item with the specified identifier to the source.

        Args:
            identifier (str)
            path (str): File or directory path.
            item_type (str)

        Returns:
            (bool): True if added, False otherwise.
        """
        # Ensure item exists
        if (not self.io.is_directory(path) and not self.io.is_file(path)) or \
                self.is_contained(identifier) or \
                not item_type in self.ITEM_TYPES:
            return False
        # Generate a new path for the item
        move_dir_path = self._generate_move_dir_path(item_type)
        save_path = self._generate_save_path(path,item_type)
        # Generate a HookedItem objects
        item = HookedItem(identifier, save_path, item_type)
        # Same file cannot already exist.
        if self.io.is_file(save_path) or self.io.is_directory(save_path):
            self.io.delete(save_path)
        # Move the file to the new location
        if copy:
            success = self.io.copy(path,move_dir_path)
        else:
            success = self.io.move_file(path,move_dir_path)
        if success:
            # Add to hooked items
            self.hooked_items.add_object(identifier,item)
            # Notify the subscribers
            data = {
                "identifier" : identifier,
                "path" : save_path,
                "item_type" : item_type}
            self.observers.notify("add_to_source",data)
            return True
        return False

    def write_to_file(self, identifier : str, item_type : str, file_name : str,
            extension : str, data : Any, overwrite : bool = False) -> bool:
        """
        Write a file with the specified identifier, file_name, extension,
        and data to the results for this specific source.

        Args:
            identifier (str): Unique identifier for the file or directory.
            file_name (str): Name of the file.
            extension (str): Extension of the file.
            overwrite (bool): If True, any existing file with the same name
                            or extension is overwritten.

        Returns:
            (bool): True if successfully written, False otherwise.
        """
        # Generate the save path.
        save_path = "{}/{}.{}".format(
            self._generate_move_dir_path(item_type),file_name,extension)
        # Attempt to write the data to this file.
        try:
            # Only save identifier if successful.
            if self.io.write(save_path,data,overwrite):
                item = HookedItem(identifier,save_path,item_type)
                if self.hooked_items.is_object(identifier):
                    self.hooked_items.remove_object(identifier)
                self.hooked_items.add_object(identifier,item)
                return True
            return False
        except:
            return False

    def change_item_type(self, identifier : str, new_item_type : str) -> bool:
        """
        Change the type of the specified identifier.
        The identifier and the type must exist.

        Args:
            identifier (str)
            new_item_type (str): One of 'permanent', 'temporary', or 'workspace'
        """
        if not self.is_contained(identifier) or \
                not new_item_type in self.ITEM_TYPES:
            return False
        # Get the item, remove, and re-add as new type.
        item : HookedItem = self.hooked_items.get_object(identifier)
        self.hooked_items.remove_object(identifier)
        return self.add_to_source(identifier,item.path,new_item_type)

    def remove_from_source(self, identifier : str) -> bool:
        """
        Remove the item with the specified identifier if it exists.

        Args:
            identifier (str)

        Returns:
            (bool): True if removed, False otherwise.
        """
        if self.hooked_items.remove_object(identifier):
            self.observers.notify(
                "remove_from_source", {"identifier" : identifier})
            return True
        return False

    def cleanup(self) -> None:
        """
        Cleanup this source hook, removing all items in the hook.
        """
        self._delete_all_in_directory(self.permanant_dir_path)
        self._delete_all_in_directory(self.temp_dir_path)
        self._delete_all_in_directory(self.ws_dir_path)
        self.observers.notify("cleanup", {})

    def destroy(self) -> None:
        """
        Remove the source directory.
        It is expected that the source hook will not be used after this call.
        """
        if self.io.is_directory(self.source_dir_path):
            self.io.delete(self.source_dir_path)
        self.observers.notify("destroy", {})

    def save_to_directory(self) -> bool:
        """
        Copy all permanent items to the specified directory.

        Args:
            result_dir_path (str)

        Returns:
            (bool): True if copied, False otherwise.
        """
        saved = list()
        if not self.io.is_directory(self.result_dir_path) and \
                not self.io.create_directory(self.result_dir_path):
            return False
        paths = self._get_paths_of_objects_in_directory(
            self.permanant_dir_path)
        for path in paths:
            if self.io.move_file(path, self.result_dir_path):
                saved.append(path)
        self.observers.notify("save_to_directory",{"saved" : saved})
        return True

    def register_listener(self, event_type, subscriber : Subscriber) -> None:
        """
        Add a listener that takes in the source hook name and is executed
        when the listener type method successfully finishes execution.

        Args:
            event_type (str): one of add_to_source, remove_from_source, or
                                cleanup.
            callable ( Callable[[str],None])

        Returns:
            (bool): True if successfully registered, False otherwise.
        """
        if not event_type in self.EVENT_TYPES:
            return
        self.observers.subscribe(event_type, subscriber)

    ################################## GETTERS ###############################

    def is_contained(self, identifier : str) -> bool:
        """
        Determine if the specified identifier exists.

        Args:
            identifier (str)

        Returns:
            (bool): True if the identifier exists, False otherwise.
        """
        if self.hooked_items.is_object(identifier):
            hooked_item : HookedItem = self.hooked_items.get_object(identifier)
            path = hooked_item.path
            return self.io.is_directory(path) or \
                self.io.is_file(path)
        return False

    def get_item_type(self, identifier : str) -> str:
        """
        Obtain the type of this item.

        Args:
            identifier (str)

        Returns:
            (str): Type
        """
        if self.hooked_items.is_object(identifier):
            hooked_item : HookedItem = self.hooked_items.get_object(identifier)
            return hooked_item.item_type

    def get_hooked_paths(self, item_type : str) -> Dict[str,str]:
        """
        Obtain a mapping from identifier to path for items of the specified type

        Args:
            item_type (str)

        Returns:
            (Dict[str,str]): Identifier to its path mapping.
        """
        paths = dict()
        if item_type in self.ITEM_TYPES:
            items = self.hooked_items.get_filtered_objects(
                lambda name, obj: obj.item_type == item_type)
            for identifier, item in items.items():
                item : HookedItem
                paths[identifier] = item.path
        return paths

    def get_workspace_path(self) -> str:
        """
        Obtain a path to the workspace.
        """
        return self.ws_dir_path

    def get_result_directory_path(self) -> str:
        """
        Obtain the result directory path.
        """
        return self.result_dir_path

    ############################### PRIVATE METHODS ##########################

    def _initialize_source_directory(self, parent_dir_path : str,
            source_name : str) -> None:
        # Generate source dir paths.
        self.source_dir_path = "{}/{}".format(parent_dir_path, source_name)
        self.permanant_dir_path = "{}/{}".format(
            self.source_dir_path,"permanent")
        self.temp_dir_path = "{}/{}".format(self.source_dir_path,"temp")
        self.ws_dir_path = "{}/{}".format(self.source_dir_path,"ws")
        # Initialize a permanent, temp, and workspace directory in this path
        self.io.delete(self.source_dir_path)
        if not self.io.create_directory(self.source_dir_path) or \
                not self.io.create_directory(self.permanant_dir_path) or \
                not self.io.create_directory(self.temp_dir_path) or \
                not self.io.create_directory(self.ws_dir_path):
            raise Exception("Unable to initialize source hook")
        return self.source_dir_path

    def _initialize_save_directory(self) -> None:
        self.io.create_directory(self.get_save_directory_path())

    def _generate_move_dir_path(self,item_type : str ) -> str:
        if item_type == "permanent":
            return self.permanant_dir_path
        elif item_type == "temporary":
           return  self.temp_dir_path
        return self.ws_dir_path

    def _generate_save_path(self, path : str, item_type : str) -> str:
        if self.io.is_directory(path):
            return "{}/{}".format(
                self._generate_move_dir_path(item_type), self.io.get_name(path))
        elif self.io.is_file(path):
            return "{}/{}.{}".format(
                self._generate_move_dir_path(item_type), self.io.get_name(path),
                self.io.get_file_extension(path)[1])
        else:
            raise Exception()

    def _generate_result_dir_path(self, dir_path : str, source_name : str) \
            -> str:
        if not self.io.is_directory(dir_path):
            if not self.io.create_directory(dir_path):
                raise Exception("Unable to create result directory")
        count = 0
        while True:

            path = "{}/{}_{}".format(dir_path,source_name,count)
            if self.io.is_directory(path):
                count += 1
            else:
                self.io.create_directory(path)
                break
        return path

    def _get_paths_of_objects_in_directory(self , dir_path : str) -> List[str]:
        paths = list()
        if self.io.is_directory(dir_path):
            _, file_paths = self.io.path_of_files_in_directory(
                dir_path,["*"], False)
            _, dir_paths = self.io.paths_of_subdirectories(dir_path)
            paths.extend(file_paths)
            paths.extend(dir_paths)
        return paths

    def _delete_all_in_directory(self, dir_path : str) -> None:
        paths = self._get_paths_of_objects_in_directory(dir_path)
        for path in paths:
            self.io.delete(path)