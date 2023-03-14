'''
File: Error.py
Project: GailBot GUI
File Created: Friday, 4th November 2022 1:01:27 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Sunday, 6th November 2022 1:11:39 pm
Modified By:  Siara Small  & Vivian Li
-----
'''

from dataclasses import dataclass
@dataclass
class ErrorMsg:
    """ error messages """
    KEYERROR          = "File key not found"
    DUPLICATEKEY      = "Duplicate key"
    POSTERROR         = "Fail to add to database"
    GETERROR          = "Fail to get data"
    EDITERROR         = "Fail to edit the data"
    DELETEEROR        = "Unable to delete data"
    RESOURCEERROR     = "Thread Resource temporarily unavailable"
    DELETE_DEFAULT    = "Default setting cannot be deleted"
    PROFILE_NOT_FOUND = "Profile Not Found"

@dataclass
class ErrorFormatter:
    DEFAULT_ERROR = "Error from {source}, error message: {msg}"
    FILE_ERROR = "Error from {source}, file name {name}, error message: {msg}"
    PROFILE_ERROR = "Error from {source}, profile name {name}, error message: {msg}"
    PLUGIN_ERROR = "Error from {source}, plugin name {name}, error message: {msg}"
    TRANSCRIBE_ERROR = "Error from {source}, file name {name}, error message: {msg}"    
    
class DBException(Exception):
    """ exception for database module """
    def __init__(self, msg = None):
        self.msg = msg

class ThreadException(Exception):
    """ exception for thread module """
    def __init__(self, msg = None):
        self.msg = msg