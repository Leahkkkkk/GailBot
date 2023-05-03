from dataclasses import dataclass
from typing import Dict
from .Style import STYLE_DATA

@dataclass 
class INSTRUCTION:
    ICON_MARKER = "icon"
    REMOVE_PLUGIN = {ICON_MARKER + STYLE_DATA.Asset.tableRemove:
                    "Remove the plugin suite and the source file from GailBot, official plugin suite cannot be removed"}
    REMOVE_FILE = {ICON_MARKER + STYLE_DATA.Asset.tableRemove: 
                    "Remove the audio file from the transcription queue, the original file will not be removed"}
    REMOVE = {ICON_MARKER + STYLE_DATA.Asset.tableRemove: 
                    "Remove the source from GailBot"}
    REMOVE_PROFILE = {ICON_MARKER + STYLE_DATA.Asset.tableRemove: 
                    "Remove the profile from GailBot"}
    REMOVE_ENGINE = {ICON_MARKER + STYLE_DATA.Asset.tableRemove: 
                    "Remove the engine setting from GailBot"}
    EDIT_ENGINE = {ICON_MARKER + STYLE_DATA.Asset.tableEdit: 
                    "Edit the engine setting"}
    EDIT_PROFILE = {ICON_MARKER + STYLE_DATA.Asset.tableEdit: 
                    "Edit profile setting"}
    EDIT_FILE_PROFILE = {ICON_MARKER + STYLE_DATA.Asset.tableEdit: 
                    "Edit the file's profile setting"}
    EDIT_BTN = {ICON_MARKER + STYLE_DATA.Asset.tableEdit: 
                    "Edit setting"}
    ENGINE_DETAIL = {ICON_MARKER + STYLE_DATA.Asset.tableDetail: 
                    "Open a pop up for displaying the engine setting details"}
    PROFILE_DETAIL = {ICON_MARKER + STYLE_DATA.Asset.tableDetail: 
                    "Open a pop up for displaying the profile setting details"}
    PLUGIN_DETAIL = {ICON_MARKER + STYLE_DATA.Asset.tableDetail: 
                    "Open a pop up for displaying the plugin suite detail"}
    SOURCE_BTN = {ICON_MARKER + STYLE_DATA.Asset.tableSource: 
                    "View the source file"}
    OUTPUT_BTN = {ICON_MARKER + STYLE_DATA.Asset.tableOutput: 
                    "View the output of transcription"}
    TRANSCRIBE_BTN = {"Transcribe": "Transcribe the files that are selected on the table"}
    CONFIRM_BTN = {"Confirm ": ""}
    SETTING_BTN = {"Settings": "Opens the application's system settings"}
    ENGINE_BTN = {"Engine": "Opens application's page for displaying and editing engine setting"}
    PLUGIN_BTN = {"Plugin": "Opens application's page for displaying and adding new plugin suite"}
    Profile = {"Profile": "Opens application's page for displaying and editing profile setting "}
    REMOVE_ALL = {"Remove All": "Remove all the audio files from table and transcription queue"}
    FONT_SIZE = {"Font size": "Lets the user adjust the font size in the application"}
    CHANGE_COLOR = {"Color mode": "Enables the user to switch between different color modes in the application."}
    LOG_AUTO_DELETE = {"Log file auto \ndeletion time": "Sets the time interval for automatic deletion of log files."}
    RESTORE = {"Restore Default": "Restores all settings to their default values."}
    SAVELOG = {"Save Log Files": "Saves the application's log files to a specified location."}
    CLEARLOG = {"Clear Log Files": "Clears all log files from the application."}
    CLEARCACHE = {"Clear Cache": "Clears the application's cache"}
    
    SOURCE_TABLE_INS = REMOVE | EDIT_FILE_PROFILE | PROFILE_DETAIL
    ENGINE_TABLE_INS = EDIT_ENGINE | ENGINE_DETAIL | REMOVE_ENGINE
    PROFILE_TABLE_INS = EDIT_PROFILE | PROFILE_DETAIL | REMOVE_PROFILE
    PLUGIN_TABLE_INS = REMOVE_PLUGIN | PLUGIN_DETAIL |  SOURCE_BTN
    FILE_UPLOAD_INS = REMOVE_FILE | EDIT_PROFILE | PROFILE_DETAIL | TRANSCRIBE_BTN | REMOVE_ALL
    CONFIRM_IN = CONFIRM_BTN | PROFILE_DETAIL
    SUCCESS_IN = CONFIRM_BTN | PROFILE_DETAIL
    TRANSCRIBE_IN = TRANSCRIBE_BTN 
    SETTING_FORM_INS = FONT_SIZE | CHANGE_COLOR | LOG_AUTO_DELETE | CLEARLOG | CLEARCACHE | RESTORE | SAVELOG 