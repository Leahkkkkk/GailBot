'''
File: Error.py
Project: GailBot GUI
File Created: Friday, 4th November 2022 1:01:27 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Sunday, 6th November 2022 1:11:39 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: data that contains the error message
'''

from dataclasses import dataclass

@dataclass
class ERR:
    """structured error formatters"""
    ERROR_WHEN_DUETO      = "ERROR 001 An error occurred when {0} due to {1}."
    ERROR_THREAD_RESOURCE = "ERROR 002: Thread resource temporarily unavailable. Please see the GailBot user manual for more details."
    ERROR_FAIL_TRANSCRIBE = "ERROR 003: Failed to transcribe {0}. Please see the GailBot user manual for more details."

    ### error for file organizer
    FILE_KEY_ERR          = "ERROR 004: File name not found."
    DUPLICATE_FILE_KEY    = "ERROR 005: Duplicate file key."
    DUPLICATE_FILE_NAME   = "ERROR 006: GailBot does not allow duplicate file names. Please edit the file name and try again."
    POST_FILE_ERROR       = "ERROR 007: Failed to add file to database."
    GET_FILE_ERROR        = "ERROR 008: Failed to get data. Please see the GailBot user manual for more details."
    EDIT_FILE_ERROR       = "ERROR 009: Failed to edit the data. Please see the GailBot user manual for more details."
    DELETE_FILE_ERROR     = "ERROR 010: Unable to delete data. Please see the GailBot user manual for more details."
    GET_FILE_OUTPUT_ERROR = "ERROR 011: Unable to get the path to file output."

    ## error for profile organizer
    INVALID_FILE      = "ERROR 012: {0} is an invalid file."
    DUPLICATED_NAME   = "ERROR 013: The name {0} is already in use."
    DELETE_DEFAULT    = "ERROR 014: The default settings profile cannot be deleted."
    INVALID_PROFILE   = "ERROR 015: {0} is an invalid profile."
    SAVE_PROFILE      = "ERROR 016: Failed to save profile {0} locally. Please see the GailBot user manual for more details."
    DELETE_PROFILE    = "ERROR 017: Failed to delete profile {0}. Please see the GailBot user manual for more details."
    GET_PROFILE       = "ERROR 018: Failed to get profile data {0}. Please see the GailBot user manual for more details."
    PROFILE_NOT_FOUND = "ERROR 019: Profile {0} not found. Please be sure you are trying to access an existing profile."
    PROFILE_EDIT      = "ERROR 020: Failed to update profile {0}. Please see the GailBot user manual for more details."
    PROFILE_IN_USE    = "ERROR 021: Profile {0} cannot be deleted while it is in use."
    PROFILE_SRC_CODE  = "ERROR 022: Failed to open source code for profile source {0} due to error {1}"

    POST_ENGINE      = "ERROR 023: Failed to create engine setting {0}. Please see the GailBot user manual for more details."
    ENGINE_IN_USE    = "ERROR 024: Engine setting {0} cannot be deleted while it is in use"
    ENGINE_EDIT      = "ERROR 025: Failed to update the engine {0}"
    ENGINE_NOT_FOUND = "ERROR 026: Engine setting {0} not found. Please ensure you are using an existing engine settings profile"
    INVALID_ENGINE   = "ERROR 027: {0} is an invalid engine setting."
    DELETE_ENGINE    = "ERROR 028: Failed to delete engine setting {0}."
    GET_ENGINE       = "ERROR 029: Failed to get engine setting data {0}."
    ENGINE_SRC_CODE  = "ERROR 030: Failed to open source code for engine source {0} due to error {1}"

    ## error for plugin organizer
    PLUGIN_IN_USE   = "ERROR 031: Plugin {0} cannot be deleted while it is in use."
    PLUGIN_OFFICIAL = "ERROR 032: Official plugin {0} cannot be deleted."
    PLUGIN_SRC_CODE = "ERROR 033: Failed to open source code for plugin suite {0}. Source code has been deleted. "
    PLUGIN_DETAIL   = "ERROR 034: Failed to display plugin suite details"
    INVALID_PLUGIN  = "ERROR 035: Failed to upload plugin suite, since the plugin suite is invalid"
    DELETE_PLUGIN   = "ERROR 036: Failed to delete plugin suite"
    ## error for transcription 
    FAIL_TRANSCRIBE       = "ERROR 036: Failed to transcribe the following files {0}. "
    INVALID_TRANSCRIBE    = "ERROR 037: The following files are invalid: {0}."
    FAIL_START_TRANSCRIBE = "ERROR 038: Failed to start transcription due to {0}"
    