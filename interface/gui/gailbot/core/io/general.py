# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2021-11-30 17:58:28
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2021-12-07 18:05:53
# Standard library imports
from typing import Any, Callable, Tuple, List, Dict
import os
import glob
import json
import yaml
import shutil
from pathlib import Path
# Local imports
# Third party imports
from copy import deepcopy


class GeneralIO:
    """
    Provides methods that deal with reading and writing non-media files and
    interacting with the file system.
    """

    def __init__(self) -> None:
        """
        Params:
            readers (Dict[str,Callable]):
                Mapping from file extensions to read functions.
            writers (Dict[str,Callable]):
                Mapping from file extensions to write functions.
        """
        self.readers = {
            "JSON": self._read_json,
            "TXT": self._read_text,
            "YML": self._read_yaml,
            "YAML": self._read_yaml,
            "*": self._read_text}
        self.writers = {
            "JSON": self._write_json,
            "TXT": self._write_text,
            "YML": self._write_yaml,
            "YAML": self._write_yaml,
            "*": self._write_text}

    ############################## INSPECTORS ###############################

    def is_directory(self, dir_path: str) -> bool:
        """
        Determine if the given path is a directory.
        """
        return os.path.isdir(dir_path)

    def is_file(self, file_path: str) -> bool:
        """
        Determine if the given path is a file.
        """
        try:
            return os.path.isfile(file_path)
        except:
            return False

    def number_of_files_in_directory(
            self, dir_path: str,
            extensions: List[str] = ["*"],
            check_subdirectories: bool = False) -> Tuple[bool, int]:
        """
        Determine the number of files in the directory.

        Args:
            dir_path (str): Path to directory.
            extensions (List[str]): Specific file extensions to look for.
                        Ex: ["pdf"]. '*' is a wildcard and considers all
                        extensions. Does not consider sub-directories.
                        default = ["*"]
            check_subdirectories (bool): True to check subdirectories.
                                False otherwise. default = False

        Returns:
            (Tuple[bool,int]): True + number of files if successful.
                                False + None if unsuccessful.
        """
        success, paths = self.path_of_files_in_directory(
            dir_path, extensions, check_subdirectories)
        if success:
            return (True, len(paths))
        else:
            return (False, None)

    def path_of_files_in_directory(
            self, dir_path: str,
            extensions: List[str] = ["*"],
            check_subdirectories: bool = False) -> Tuple[bool, List[str]]:
        """
        Determine the paths, relative to dir_path, of files in the directory.

        Args:
            dir_path (str): Path to directory.
            extensions (List[str]): Specific file extensions to look for.
                        Ex: ["pdf"]. '*' is a wildcard and considers all file
                        extensions. Does not consider sub-directories.
                        default = ["*"]
            check_subdirectories (bool): True to check subdirectories.
                                        False otherwise. default = False

        Returns:
            (Tuple[bool,List[str]]):
                True + paths relative to directory of files if successful.
                False + None if unsuccessful.
        """
        # Check if it is directory
        if not self.is_directory(dir_path):
            return (False, [])
        paths = list()
        for extension in extensions:
            # Determining the type of file.
            if extension == "*.":
                file_type = "{}".format(extension)
            else:
                file_type = "*.{}".format(extension)
            # Generating the glob query.
            if check_subdirectories:
                query = "{}/**/{}".format(dir_path, file_type)
            else:
                query = "{}/{}".format(dir_path, file_type)
            paths.extend(glob.glob(query, recursive=True))
        return (True, paths)

    def number_of_subdirectories(self, dir_path: str) -> Tuple[bool, int]:
        """
        Obtain the number of subdirectories in a ditrectory

        Args:
            dir_path (str): path to the directory.

        Returns:
            (Tuple[bool,int]):
                True + number of subdirectories if successful.
                False + None if unsuccessful.
        """
        success, paths = self.paths_of_subdirectories(dir_path)
        if success:
            return (True, len(paths))
        return (False, None)

    def paths_of_subdirectories(self, dir_path: str) -> Tuple[bool, List[str]]:
        """
        Obtain the paths of all subdirectories in a directory.

        Args:
            dir_path (str): path to the directory.

        Returns:
            (Tuple[bool,List[str]]):
                True + paths of subdirectories if successful.
                False + None if unsuccessful.
        """
        if not self.is_directory(dir_path):
            return (False, None)
        paths = list()
        for it in os.scandir(dir_path):
            if it.is_dir():
                paths.append(it.path)
        return (True, paths)

    def is_readable(self, file_path: str) -> bool:
        """
        Determine if the file at the given path is readable.

        Args:
            file_path (str): Path to the file.

        Returns:
            (bool): True if the file is readable. False otherwise.
        """
        return self.is_file(file_path) and \
            self.get_file_extension(file_path).upper() in self.readers.keys()

    def get_file_extension(self, file_path: str) -> str:
        """
        Obtain file extension /format, which is the substring after the right-
        most "." character.

        Args:
            file_path (str): Must be a valid file path.

        Returns:
            (str): File extension / format.
        """
        return os.path.splitext(file_path.strip())[1][1:]

    def get_name(self, path: str) -> str:
        """
        Attempts to extract the name of the file or directory from the given
        path. The name is defined as anything to the right of the right-most
        backslash in the path, and does NOT include the extension (if exists).

        Args:
            path (str): Path to a file or directory.

        Returns:
            (str): Name of the file or directory, without extension
        """
        if self.is_file(path):
            return path[path.rfind("/")+1:path.rfind(".")]
        elif self.is_directory(path):
            return path[path.rfind("/")+1:]
        return ""

    def get_parent_directory(self, path: str) -> str:
        """
        Obtain the absolute path of the parent directory given a path to a file or
        directory.

        Args:
            path (str): Path to file or directory.

        Returns:
            (str): Absolute parent directory path for the given file or directory.
                    Empty string if parent directory cannot be determined.
        """
        if not self.is_directory(path) and not self.is_file(path):
            return ""
        path = Path(path)
        return path.parent.absolute()

    def get_size(self, path: str) -> Tuple[bool, bytes]:
        """
        Obtain the size of the file or directory in bytes.
        For a directory, the total size is the size of all items in the
        directory, including any sub-directories.

        Args:
            path (str): Path to a file or directory.

        Returns:
            (Tuple[bool, bytes]):
                True + Size of the file or directory in bytes if successful.
                False + None if unsuccessful.
        """
        if self.is_file(path):
            return (True, os.path.getsize(path))
        elif self.is_directory(path):
            total_size = 0
            all_paths_list = self.path_of_files_in_directory(
                path, ["*"], True)[1]
            for file_path in all_paths_list:
                total_size += os.path.getsize(file_path)
            return (True, total_size)
        return (False, None)

    ############################## ACTIONS #################################

    def read_file(self, file_path: str) -> Tuple[bool, Any]:
        """
        Read the file at the given path. The file must be readable.

        Args:
            file_path (str): Path to file

        Returns:
           (Tuple[bool,Any]):
                True + file data if successful.
                False + None otherwise.
        """
        # Determine the file format using extension
        if not self.is_file(file_path):
            return (False, None)
        if not self.get_file_extension(file_path).upper() \
                in self.readers.keys():
            return self.readers["*"](file_path)
        # Readers handle exceptions
        file_format = self.get_file_extension(file_path)
        return self.readers[file_format.upper()](file_path)

    def write_to_file(self, file_path: str, data: Any, overwrite: bool) \
            -> bool:
        """
        Write the data in a file of the specified format at the given path.

        Args:
            file_path (str): Complete path to file, including filename and
                            extension.
            data (Any): Data to write in the file.
            overwrite (bool): True to overrite the file if it exists.
                            False to append to the file

        Returns:
           (bool): True if successful. False otherwise
        """
        # Determine the file format using extension
        file_format = self.get_file_extension(file_path)
        if file_format.upper() in self.writers.keys():
            # The writers should handle exceptions
            return self.writers[file_format.upper()](
                file_path, data, overwrite)
        else:
            return self.writers["*"](
                file_path, data, overwrite)

    def create_directory(self, dir_path: str) -> bool:
        """
        Create a new directory with the given path.
        """
        try:
            os.makedirs(dir_path)
            return True
        except:
            return False

    def move_file(self, src_file_path: str, dst_dir_path: str) \
            -> Tuple[bool, str]:
        """
        Move a source file to the destination directory.

        Args:
            src_file_path (str): Source file or directory path
            dst_dir_path (str): Path to destination directory. Must be an
                                existing directory.
        """
        if not self.is_directory(dst_dir_path):
            return False, None
        try:
            # Generate the moved path.
            if self.is_file(src_file_path):
                moved_file_path = "{}/{}.{}".format(
                    dst_dir_path, self.get_name(
                        src_file_path), self.get_file_extension(src_file_path))
            else:
                moved_file_path = "{}/{}".format(
                    dst_dir_path, self.get_name(src_file_path))
            shutil.move(src_file_path, dst_dir_path)
            return True, moved_file_path
        except:
            return False, None

    def copy(self, src_path: str, dst_path: str) -> Tuple[bool, str]:
        """
        Copy the source file or directory to the destination file or directory.

        Args:
            src_path (str): Path of source file / directory
            dst_path (str): Path of destination file / directory

        Returns:
            (bool): True if successful. False otherwise.
        """
        try:
            if self.is_file(src_path):
                try:
                    moved_path = "{}/{}.{}".format(dst_path, self.get_name(
                        src_path), self.get_file_extension(src_path))
                    shutil.copy(src_path, dst_path)
                except:
                    return False, None
            elif self.is_directory(src_path) \
                    and not self.is_directory(dst_path):
                try:
                    moved_path = "{}/{}".format(dst_path,
                                                self.get_name(src_path))
                    shutil.copytree(src_path, dst_path)

                except:
                    return False, None
            else:
                return False, None
            return True, moved_path
        except Exception as e:
            print(e)

    def rename(self, src_path: str, new_name: str) -> Tuple[bool, str]:
        """
        Rename the source file or directory.

        Args:
            src_path (str): Path to the source file / directory.
            new_name (str): name of the new file or directpry only, NOT
                            the complete path. Should not contain extension or
                            backslashes.

        Returns:
            (bool): True if successful. False otherwise.
        """
        if not self.is_file(src_path) and not self.is_directory(src_path):
            return False, None
        try:
            if self.is_file(src_path):
                ext = self.get_file_extension(src_path)
                parent_dir_path = src_path[:src_path.rfind("/")]
                new_path = "{}/{}.{}".format(parent_dir_path, new_name, ext)
            else:
                parent_dir_path = src_path[:src_path.rfind("/")]
                new_path = "{}/{}".format(parent_dir_path, new_name)
            os.rename(src_path, new_path)
            return self.is_file(new_path) or self.is_directory(new_path), new_path
        except:
            return False, None

    def delete(self, path: str) -> bool:
        """
        Delete the given file or directory. For a directory, deletes all
        sub-directories as well.
        """
        if self.is_file(path):
            try:
                os.remove(path)
            except:
                return False
        elif self.is_directory(path):
            try:
                shutil.rmtree(path)
            except:
                return False
        else:
            return False
        return True

    def clear_directory(self, dir_path: str) -> bool:
        if not self.is_directory(dir_path):
            return False
        return self.delete(dir_path) and \
            self.create_directory(dir_path)

    ################################### PRIVATE METHODS ######################

    def _read_json(self, file_path: str) -> Tuple[bool, Any]:
        """
        Read a json file at the given path.
        Raises an exception if the file data cannot be converted to a
        dictionary.

        Returns:
            (Tuple[bool,Any]): True + Data read from file is successful.
                            False + None if unsuccessful.
        """
        try:
            with open(file_path, "r") as f:
                # Data must be a dictionary when read from a json file.
                data = json.load(f)
                if not type(data) == dict:
                    raise Exception
                return (True, data)
        except:
            return (False, None)

    def _write_json(self, file_path: str, data: Dict, overwrite: bool) \
            -> bool:
        """
        Write the given data to a json file.

        Args:
            file_path (str): Path of new file.
            data (Dict): Data being written to file.
            overwrite (bool): If True, any existing file with the same name is
                            overwritten.
        """
        try:
            # Data must be convertable to a dictionary to be written to json
            data = dict(data)
            if not overwrite:
                _, previous_data = self._read_json(file_path)
                if previous_data != None:
                    previous_data.update(data)
                    data = deepcopy(previous_data)
            with open(file_path, "w") as f:
                json.dump(data, f)
            return True
        except:
            return False

    def _read_text(self, file_path: str) -> Tuple[bool, Any]:
        """
        Read a text file at the given path.
        """
        try:
            return (True, open(file_path, "r").read())
        except:
            return (False, None)

    def _write_text(self, file_path: str, data: str, overwrite: bool) \
            -> bool:
        """
        Write the given data to a text file.

        Args:
            file_path (str): Path of new file.
            data (str): Data being written to file.
            overwrite (bool): If True, any existing file with the same name is
                            overwritten.
        """
        try:
            # Anything written to a text file must be a string
            data = str(data)
            mode = 'w' if overwrite else "a"
            with open(file_path, mode) as f:
                f.write(data)
            return True
        except:
            return False

    def _read_yaml(self, file_path: str) -> Tuple[bool, Any]:
        """
        Read a yaml file at the given path.
        Raises an exception if the file data cannot be converted to a
        dictionary.

        """
        try:
            with open(file_path, 'r') as f:
                data = yaml.load(f)
                # Data loaded must be a dictionary
                if not type(data) == dict:
                    raise Exception
                return (True, data)
        except:
            return (False, None)

    def _write_yaml(self, file_path: str, data: Dict, overwrite: bool) \
            -> bool:
        """
        Write the given data to a yaml file.

        Args:
            file_path (str): Path of new file.
            data (Dict): Data being written to file.
            overwrite (bool): If True, any existing file with the same name is
                            overwritten.
        """
        try:
            data = dict(data)
            if not overwrite:
                _, previous_data = self._read_yaml(file_path)
                if previous_data != None:
                    previous_data.update(data)
                    data = deepcopy(previous_data)
            with open(file_path, "w") as f:
                # Data must be convertable to a dictionary object to be written to
                # a yaml file.
                yaml.dump(data, f)
            return True
        except:
            return False
