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
    ERROR_WHEN_DUETO = "ERROR: An error occurred when {0} due to {1}."
    THREAD_RESOURCE     = "ERROR: Thread Resource temporarily unavailable"
    FAIL_TRANSCRIBE  = "ERROR: fail to transcribe {0}"
    
    ### error for file organizer
    FILE_KEY_ERR        = "ERROR: File key not found."
    DUPLICATE_FILE_KEY  = "ERROR: Duplicate file key."
    DUPLICATE_FILE_NAME = "ERROR: Duplicate file name."
    POST_FILE_ERROR     = "ERROR: Fail to add file to database."
    GET_FILE_ERROR      = "ERROR: Fail to get data."
    EDIT_FILE_ERROR     = "ERROR: Fail to edit the data."
    DELETE_FILE_ERROR   = "ERROR: Unable to delete data."
    
    
    ## error for profile organizer
    INVALID_FILE      = "ERROR: {0} is an invalid file."
    DUPLICATED_NAME   = "ERROR: The name {0} has been taken."
    DELETE_DEFAULT    = "Default setting cannot be deleted."
    INVALID_PROFILE   = "ERROR: {0} is an invalid profile."
    SAVE_PROFILE      = "ERROR: Fail to save profile {0} locally."
    DELETE_PROFILE    = "ERROR: Fail to delete profile {0}."
    GET_PROFILE       = "ERROR: Fail to get profile data {0}."
    PROFILE_NOT_FOUND = "ERROR: Profile {0} not found."
    PROFILE_EDIT      = "ERROR: Fail to update profile {0}."
    PROFILE_IN_USE    = "ERROR: profile {0} is in use"
 
    ## error for plugin organizer
    PLUGIN_IN_USE    = "ERROR: plugin {0} is in use"