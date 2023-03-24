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
class ERR:
    """structured error formatters"""
    ERROR_WHEN_DUETO = "ERROR: an error occurred when {0} due to {1}"
    DEFAULT_ERROR    = "Error from {source}, error message: {msg}"
    THREAD_RESOURCE     = "ERROR: Thread Resource temporarily unavailable"
    TRANSCRIBE_ERROR = "Error from {source}, file name {name}, error message: {msg}"
    FAIL_TRANSCRIBE  = "ERROR: fail to transcribe {0}"
    
    ### error for file organizer
    FILE_ERROR       = "Error from {source}, file name {name}, error message: {msg}"
    FILE_KEY_ERR         = "ERROR: File key not found"
    DUPLICATE_FILE_KEY      = "ERROR: Duplicate file key"
    POST_FILE_ERROR         = "ERROR: Fail to add file to database"
    GET_FILE_ERROR          = "ERROR: Fail to get data"
    EDIT_FILE_ERROR         = "ERROR: Fail to edit the data"
    DELETE_FILE_ERROR        = "ERROR: Unable to delete data"
    
    
    ## error for profile organizer
    PROFILE_ERROR    = "Error from {source}, profile name {name}, error message: {msg}"
    PLUGIN_ERROR     = "Error from {source}, plugin name {name}, error message: {msg}"
    INVALID_FILE     = "ERROR: {0} is an invalid file"
    DUPLICATED_NAME  = "ERROR: the name {0} has been taken"
    DELETE_DEFAULT    = "Default setting cannot be deleted"
    INVALID_PROFILE   = "ERROR: {0} is an invalid profile"
    SAVE_PROFILE      = "ERROR: fail to save profile {0} locally"
    DELETE_PROFILE    = "ERROR: fail to delete profile {0}"
    GET_PROFILE       = "ERROR: fail to get profile data {0}"
    PROFILE_NOT_FOUND = "ERROR: profile {0} not found"
    PROFILE_EDIT      = "ERROR: fail to update profile {0}"
