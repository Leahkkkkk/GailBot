# Standard library imports 
from typing import Any, Tuple, List
import os 
import glob
import json
import yaml
import shutil
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
            readers (Dict): Mapping from file extensions to read functions.
            writers (Dict): Mapping from file extensions to write functions.
        """
        self.readers = {
            "JSON" : self._read_json,
            "TXT" : self._read_text,
            "YML" : self._read_yaml,
            "YAML" : self._read_yaml} 
        self.writers = {
            "JSON" : self._write_json,
            "TXT" : self._write_text,
            "YML" : self._write_yaml,
            "YAML" : self._write_yaml}

    ############################## INSPECTORS ###############################

    def is_directory(self, dir_path : str) -> bool:
        """
        Determine if the given path is a directory.

        Args:
            dir_path (str): Path to directory.
        
        Returns:
            (bool): True if path is a directory. False otherwise.
        """
        return os.path.isdir(dir_path) 

    def is_file(self, file_path : str) -> bool:
        """
        Determine if the given path is a file.

        Args:
            file_path (str): Path to file.
        
        Returns:
            (bool): True if path is a file. False otherwise.
        """
        return os.path.isfile(file_path)

    def number_of_files_in_directory(self, dir_path : str ,
            extensions : List[str] = ["*"], 
            check_subdirectories : bool = False) -> Tuple[bool,int]:
        """
        Determine the number of files in the directory.

        Args:
            dir_path (str): Path to directory.
            extensions (List[str]): Specific file extensions to look for. 
                        Ex: ["pdf"]. '*' is a wildcard and considers all 
                        extensions. default = ["*"]
            check_subdirectories (bool): True to check subdirectories. 
                                False otherwise. default = False 
        
        Returns:   
            (Tuple[bool,int]): True + number of files if successful.
                                False + None if unsuccessful.
        """
        success, paths = self.names_of_file_in_directory(
            dir_path,extensions,check_subdirectories)
        if success:
            return (True,len(paths))
        else:
            return (False, None)

    def names_of_file_in_directory(self, dir_path : str ,
            extensions : List[str] = ["*"],
            check_subdirectories : bool = False ) -> Tuple[bool,List[str]]:
        """
        Determine the names of files in the directory.

        Args:
            dir_path (str): Path to directory.
            extensions (List[str]): Specific file extensions to look for. 
                        Ex: ["pdf"]. '*' is a wildcard and considers all 
                        extensions. default = ["*"]
            check_subdirectories (bool): True to check subdirectories. 
                                        False otherwise. default = False 
        
        Returns:   
            (Tuple[bool,List[str]]): True + names of files if successful.
                                False + None if unsuccessful.
        """
        # Check if it is directory
        if not self.is_directory(dir_path):
            return (False, [])
        paths = list()
        for extension in extensions:
            # Determining the type of file.
            if extension == "*":
                file_type = "{}".format(extension)
            else:
                file_type = "*.{}".format(extension)
            # Generating the glob query.
            if check_subdirectories:
                query = "{}/**/{}".format(dir_path,file_type)
            else:
                query = "{}/{}".format(dir_path,file_type)
            paths.extend(glob.glob(query,recursive=True))
        return (True,paths)   

    def is_readable(self, file_path : str) -> bool:
        """
        Determine if the file at the given path is readable by GeneralIO.

        Args:
            file_path (str)
        
        Returns:
            (bool): True if the file is readable. False otherwise.
        """
        return self.is_file(file_path) and \
            self.get_file_extension(file_path) in self.readers.keys()

    def get_file_extension(self, file_path : str) -> str:
        """
        Obtain file extension /format, which is the substring after the right-
        most "." character.

        Args:
            file_path (str)
        
        Returns:
            (str): File extension / format.
        """
        return os.path.splitext(file_path.strip())[1][1:]

    ############################## ACTIONS #################################

    def read_file(self, file_path : str) -> Tuple[bool,Any]:
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
        if not self.is_file(file_path) or \
                not self.get_file_extension(file_path).upper() \
                    in self.readers.keys():
            return (False, None)
        # Readers handle exceptions 
        file_format = self.get_file_extension(file_path)
        return self.readers[file_format.upper()](file_path)
    
    def write_to_file(self, file_path : str, data : Any, overwrite : bool) \
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
        if not file_format.upper() in self.writers.keys() or \
                file_format != self.get_file_extension(file_path):
            return False
        # The writers should handle exceptions 
        return self.writers[file_format.upper()](
                file_path, data, overwrite)

    def create_directory(self, dir_path : str) -> bool:
        """
        Create a new directory with the given path.

        Args:
            dir_path (str): Path of the new directory.

        Returns:
            (bool): True if successful. False otherwise.
        """
        try:
            os.makedirs(dir_path)
            return True
        except:
            return False 

    def move_file(self, src_file_path : str, dst_dir_path : str) -> bool:
        """
        Move a source file to the destination directory.
        
        Args:
            src_file_path (str): Source file or directory path
            dst_dir_path (str): Path to destination directory. Must be an 
                                existing directory.
    
        Returns:
            (bool): True if successful. False otherwise.
        """
        if not self.is_file(src_file_path) or \
                not self.is_directory(dst_dir_path):
            return False 
        try:
            shutil.move(src_file_path,dst_dir_path)
            return True
        except:
            return False 

    def copy(self, src_path : str, dst_path : str) -> bool:
        """
        Copy the source file or directory to the destination file or directory.

        Args:
            src_path (str): Path of source file / directory 
            dst_path (str): Path of destination file / directory 
            
        Returns:
            (bool): True if successful. False otherwise.
        """
        if self.is_file(src_path):
            try:
                shutil.copy(src_path,dst_path)
            except:
                return False 
        elif self.is_directory(src_path) \
                and not self.is_directory(dst_path):
            try:
                shutil.copytree(src_path,dst_path)
            except:
                return False 
        else:
            return False 
        return True

    def rename(self, src_path : str, new_name : str) -> bool:
        """
        Rename the source file or directory.

        Args:
            src_path (str): Path to the source file / directory.
            new_name (str): New names 
        
        Returns:
            (bool): True if successful. False otherwise.
        """
        if not self.is_file(src_path) and not self.is_directory(src_path):
            return False 
        try:
            os.rename(src_path,new_name)
            return True 
        except:
            return False  
    
    def delete(self, path : str) -> bool:
        """
        Delete the given file or directory. For a directory, deletes all 
        sub-directories as well.

        Args:
            path (str): Path of file / directory to delete .
        
        Returns:
           (bool): True if successful. False otherwise  
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

    ################################### PRIVATE METHODS ######################

    def _read_json(self, file_path : str) -> Tuple[bool,Any]:
        """
        Read a json file at the given path.

        Args:
            file_path (str)
        
        Returns:
            (Tuple[bool,Any]): True + Data read from file is successful.
                            False + None if unsuccessful.
        """
        try:
            with open(file_path,"r") as f:
                return (True,json.load(f))
        except:
            return (False, None)

    def _write_json(self, file_path : str, data : Any, overwrite : bool) \
            -> bool:
        """
        Write the given data to a json file.

        Args:
            file_path (str): Path of new file.
            data (Any): Data being written to file.
            overwrite (bool): If True, any existing file with the same name is
                            overwritten.
        
        Returns:
            (bool): True if successful. False otherwise  
        """
        try:
            if not overwrite:
                previous_data = self._read_json(file_path)
                previous_data.update(data) 
                data = deepcopy(previous_data)
            with open(file_path,"w") as f:
                    json.dump(data,f)
            return True
        except:
            return False 

    def _read_text(self, file_path : str) -> Tuple[bool,Any]:
        """
        Read a text file at the given path.

        Args:
            file_path (str)
        
        Returns:
            (Tuple[bool,Any]): True + data read from file if successful.
                                False + None if unsuccessful.
        """
        try:
            return (True,open(file_path,"r").read())
        except:
            return (False, None )

    def _write_text(self, file_path : str, data : Any, overwrite : bool) \
            -> bool:
        """
        Write the given data to a text file.

        Args:
            file_path (str): Path of new file.
            data (Any): Data being written to file.
            overwrite (bool): If True, any existing file with the same name is
                            overwritten.
        
        Returns:
            (bool): True if successful. False otherwise  
        """
        try:
            mode = 'w' if overwrite else "a"
            with open(file_path,mode) as f:
                f.write(data)
            return True 
        except:
            return False 

    def _read_yaml(self, file_path : str) -> Tuple[bool,Any]:
        """
        Read a yaml file at the given path.

        Args:
            file_path (str)
        
        Returns:
            (Tuple[bool,Any]): True + data read from file if successful.
                                False + None if unsuccessful.
        """
        try:
            with open(file_path,'r') as f:
                return (True ,yaml.load(f))
        except:
            return (False, None )

    def _write_yaml(self, file_path : str, data : Any, overwrite : bool) \
            -> bool:
        """
        Write the given data to a yaml file.

        Args:
            file_path (str): Path of new file.
            data (Any): Data being written to file.
            overwrite (bool): If True, any existing file with the same name is
                            overwritten.
        
        Returns:
            (bool): True if successful. False otherwise  
        """
        try:
            if not overwrite:
                previous_data = yaml.load(file_path)
                previous_data.update(data)
                data = deepcopy(previous_data)
            with open(file_path,"w") as f:
                yaml.dump(data,f)
            return True 
        except:
            return False 

     





