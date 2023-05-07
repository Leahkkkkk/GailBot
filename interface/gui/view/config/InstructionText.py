from dataclasses import dataclass
from typing import Dict
from .Style import STYLE_DATA
@dataclass 
class INSTRUCTION:
    ICON_MARKER = "icon"
    REMOVE_PLUGIN = {ICON_MARKER + STYLE_DATA.Asset.tableRemove:
                    "Remove this plugin suite and its source files from GailBot. Official plugin suites cannot be removed."}
    REMOVE_FILE = {ICON_MARKER + STYLE_DATA.Asset.tableRemove: 
                    "Remove this media file from the transcription queue. This file will not be transcribed during the current transcription process. The original source file will not be removed or updated."}
    REMOVE = {ICON_MARKER + STYLE_DATA.Asset.tableRemove: 
                    "Remove this media source file from GailBot."}
    REMOVE_PROFILE = {ICON_MARKER + STYLE_DATA.Asset.tableRemove: 
                    "Remove this settings profile from GailBot."}
    REMOVE_ENGINE = {ICON_MARKER + STYLE_DATA.Asset.tableRemove: 
                    "Remove this engine settings profile from GailBot."}
    EDIT_ENGINE = {ICON_MARKER + STYLE_DATA.Asset.tableEdit: 
                    "Edit this engine's settings profile."}
    EDIT_PROFILE = {ICON_MARKER + STYLE_DATA.Asset.tableEdit: 
                    "Edit this profile's settings."}
    EDIT_FILE_PROFILE = {ICON_MARKER + STYLE_DATA.Asset.tableEdit: 
                    "Edit the profile settings for this file."}
    EDIT_BTN = {ICON_MARKER + STYLE_DATA.Asset.tableEdit: 
                    "Edit the settings profile."}
    ENGINE_DETAIL = {ICON_MARKER + STYLE_DATA.Asset.tableDetail: 
                    "View the details of this engine settings profile."}
    PROFILE_DETAIL = {ICON_MARKER + STYLE_DATA.Asset.tableDetail: 
                    "View the details of this settings profile."}
    PLUGIN_DETAIL = {ICON_MARKER + STYLE_DATA.Asset.tableDetail: 
                    "View the details of this plugin suite."}
    SOURCE_BTN = {ICON_MARKER + STYLE_DATA.Asset.tableSource: 
                    "View this source file on your device."}
    OUTPUT_BTN = {ICON_MARKER + STYLE_DATA.Asset.tableOutput: 
                    "View the GailBot transcription and analysis of this media."}
    TRANSCRIBE_BTN = {"Transcribe": "Transcribe the selected files."}
    CONFIRM_BTN = {"Confirm ": ""}
    SETTING_BTN = {"Settings": "Open the application's system settings."}
    ENGINE_BTN = {"Engine": "View and edit the engine settings profiles."}
    PLUGIN_BTN = {"Plugin": "View, edit, and add plugin suites."}
    Profile = {"Profile": "View and edit the settings profiles."}
    REMOVE_ALL = {"Remove All": "Remove all media files from the table and transcription queue."}
    FONT_SIZE = {"Font size": "Change the font size of the application."}
    CHANGE_COLOR = {"Color mode": "Switch between different color themes in the application."}
    LOG_AUTO_DELETE = {"Log file auto \ndeletion time": "Set the time interval for automatic deletion of logging files."}
    RESTORE = {"Restore Default": "Restore all system settings to their default values."}
    SAVELOG = {"Save Log Files": "Set the location on your device to which log files will be saved."}
    CLEARLOG = {"Clear Log Files": "Clear all log files from the application."}
    CLEARCACHE = {"Clear Cache": "Clear the application's cache."}
    FROM_FILE_BTN = {"From File": "Upload a single audio file."}
    FROM_DIR_BTN = {"From Folder": "Upload a directory of audio files or a directory that has been previously transcribed by GailBot."}
    CLOUD_PLUGIN = {"Load from Cloud": "Register plugin from cloud source"} 
    REGISTER_PLUGIN_SUITE = {"Register Plugin Suite": "Are you sure you want to register this plugin suite?"}
    DIRECTORY_PLUGIN = {"Load from Directory": "Upload a plugin suite from your device."} 
    SELECT_PROFILE = {"Select Profile": "The selected profile setting will be applied during the transcription process."}
    SELECT_OUTPUT = {"Select Output": "The selected output path will be where the transcription result stored"}
    PROFILE_NAME = {"Profile Name": "Create a name for the new profile, the name must not be taken by existing profile"}
    SELECT_ENGINE = {"Engine": "Choose a speech to text engine"}
    SELECT_PLUGIN_SUITE = {"Plugin Suite": "Choose plugin suite to be applied in the transcription, zero or more plugin suite can be applied"}
    ENGINE_NAME = {"Engine Name": "Create a name for the new engine, the name must not be taken by existing profile"}
    STT_ENGINE_SETTING = {"Engine Setting": "Create engine setting"}
    SOURCE_TABLE_INS = REMOVE | EDIT_FILE_PROFILE | PROFILE_DETAIL
    ENGINE_TABLE_INS = EDIT_ENGINE | ENGINE_DETAIL | REMOVE_ENGINE
    PROFILE_TABLE_INS = EDIT_PROFILE | PROFILE_DETAIL | REMOVE_PROFILE
    PLUGIN_TABLE_INS = REMOVE_PLUGIN | PLUGIN_DETAIL |  SOURCE_BTN
    FILE_UPLOAD_INS = REMOVE_FILE | EDIT_PROFILE | PROFILE_DETAIL | TRANSCRIBE_BTN | REMOVE_ALL
    CONFIRM_INS = CONFIRM_BTN | PROFILE_DETAIL
    SUCCESS_INS = OUTPUT_BTN 
    TRANSCRIBE_INS = TRANSCRIBE_BTN 
    SETTING_FORM_INS = FONT_SIZE | CHANGE_COLOR | LOG_AUTO_DELETE | CLEARLOG | CLEARCACHE | RESTORE | SAVELOG 
    FILE_UPLOAD_TAB_INS = FROM_FILE_BTN | FROM_DIR_BTN | SELECT_OUTPUT | SELECT_PROFILE
    SELECT_PROFILE_INS = SELECT_PROFILE
    REGISTER_PLUGIN_SUITE_INS = CLOUD_PLUGIN | DIRECTORY_PLUGIN 
    CREATE_NEW_PROFILE_INS = PROFILE_NAME | SELECT_ENGINE | SELECT_PLUGIN_SUITE
    CREATE_NEW_ENGINE_INS = ENGINE_NAME | STT_ENGINE_SETTING