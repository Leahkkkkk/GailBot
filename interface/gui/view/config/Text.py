"""
File: Config.py
Project: GailBot GUI
File Created: Tuesday, 1st November 2022 3:59:15 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Tuesday, 1st November 2022 5:04:12 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: Dataclasses that stores the static string for frontend interface 
"""


import datetime
import toml
import os
from dataclasses import dataclass
from view.config.Style import Color
from dict_to_dataclass import DataclassFromDict, field_from_dict
from config_frontend.ConfigPath import TextDataPath, FRONTEND_CONFIG_ROOT


forms = toml.load(os.path.join(FRONTEND_CONFIG_ROOT, TextDataPath.form))
link  = toml.load(os.path.join(FRONTEND_CONFIG_ROOT, TextDataPath.link))

#############################  about data ################################
year = datetime.date.today().strftime("%Y")


@dataclass 
class LINKS(DataclassFromDict): 
    """ interface for links data """
    HILAB                   : str = field_from_dict()
    USER_MANUAL             : str = field_from_dict()
    TECHNICAL_DOCUMENT      : str = field_from_dict()
    BUG_REPORT              : str = field_from_dict()
    EMAIL                   : str = field_from_dict()
    



@dataclass
class ABOUT:
    """class holding data about GailBot; e.g. version, title, etc."""
    VERSION = "Version 0.0.1a1"
    VERSION_NAME = "Version Name: Sivian"
    APP_TITTLE = "GailBot"
    COPYRIGHT = f"Copyright {year} © HI Lab"


############################ Text Data by Pages ##############################
@dataclass
class WELCOME_PAGE:
    """class holding the text for the welcome page"""
    AUDIO_INST = "1. Add audio / video\n sources or record live"
    SETTING_INS = "2. Select a Settings Profile"
    TRANSCRIBE_INS = "3. Transcribe"
    FILE_INS = "4. Review transcriptions"
    EDIT_INS = "5. Edit settings \n or retranscribe"
    WELCOME_TEXT = "Welcome to GailBot"
    START = (
        "GailBot is the world's first automated transcription system capable\n"
        "of generating customized Conversation Analytic transcripts at scale."
    )
    START_BTN = "Get Started"
    INSTRUCTION_HEADER = "How GailBot Works"
    RESOURCE_HEADER = "Resources"
    USER_MANUAL = "User Manual"
    GUIDE = "Documentation"
    WEB_LINK = "Tufts Human Interaction Laboratory"
    MORE_INFO = "For more information, visit:"


@dataclass
class FILEUPLOAD_PAGE:
    """class holding the text for the file upload pop-up"""

    HEADER = "Files to Transcribe"
    SELECT_OUTDIR = "Select output directory"
    RETURN_MAIN = "Return to Main Menu"
    RECORD = "Record Live"
    UPLOAD = "Add Source"
    TRANSCRIBE = "Transcribe"
    REMOVE_ALL = "Remove All"
    ## unicode for settings gear
    SETTING_BTN = "\u2699"
    CHOOSE_SET_TAB_HEADER = "Select Setting Profile"
    FILE_FILTER = "audio file (*.wav)"
    REMOVE_CONFIRM = "Remove all files?"
    FROM_FILE = "From File"
    FROM_FOLDER = "From Folder"
    DROP_FILE = "Drop audio files below"
    ## unicode for an audio icon
    AUDIO_LOGO = "\U0001F50A"
    ## unicode for a file folder icon
    DIR_LOGO = "\U0001F4C1"
    URL_LOGO = "\U0001F517"
    DELETE_LOGO = "\u274C"


@dataclass
class RECORD_PAGE:
    """class holding the text for the record page"""
    wav = "WAV"
    format = "Audio Format"
    advanced = "Advanced"
    rate = "Recording Rate (Hertz)"
    duration = "Max Recording Duration"
    cancel = "Cancel"
    start = "Start Recording"
    test = "Test MicroPhone"
    recSet = "Recording Settings"
    record = "Record Audio File"
    end = "End Recording"

@dataclass
class PLUGIN_PAGE:
    HEADER = "Available Plugin Suites"
    CAPTION = "These plugins are available in GailBot"
    CREATE_NEW = "Upload Plugin Suite"


@dataclass
class PROFILE_PAGE:
    """class holding the text for the profile page"""

    ## sidebar 
    CANCEL = "Exit"
    PROFILES_BTN = "Profiles"
    SYSSET_BTN = "Settings"
    ENGINE_BTN = "Engines"
    PLUGIN_BTN = "Plugins"
    TABLE_HEADER  = ["Profile Name", "Applied Engine", "Applied Plugin Suite", "Actions"]
    TABLE_DIMENSION = [0.24, 0.24, 0.24, 0.255]
    HEADER = "Profile Settings"
    CAPTION = "Available profile settings for GailBot"
    CREATE_NEW = "Create New Profile"


@dataclass
class SYSTEM_SET_PAGE:
    """class holding the text for the system settings page"""
    HEADER = "System Settings"
    CAPTION = "Control various aspects of the graphical interface"
    CANCEL = "Exit"
    SAVE = "Save"
    CONFIRM_CHANGE = "Confirm changing GailBot system setting?"
    CHANGE_ERROR = "System settings change failed"
    CONFIRM_CLEAR = "All log files will be removed. Proceed?"
    RESTORE = "Restore Defaults"
    RESTORE_BTN = "Restore"
    CLEAR_LOG = "Clear Logs"
    CLEAR_LOG_BTN = "Clear"
    SAVE_LOG = "Save Logs"
    SAVE_LOG_BTN = "Save"
    CLEAR_CACHE = "Clear Cache"
    CLEAR_CACHE_BTN = "Clear"
    CONFIRM_CLEAR = "Confirm clearing cache?"


class CONFIRM_PAGE:
    """class holding the text for the confirm transcription popup"""
    HEADER = "Confirm Files and Settings"
    CONFIRM = "Confirm"
    CANCEL = "Cancel"



@dataclass
class PROGRESS_PAGE:
    HEADER = "Transcription in progress"
    LOADING = "Transcribing files..."

@dataclass
class SUCCESS_PAGE:
    HEADER = "Transcription complete"
    MORE_BTN = "Process additional files"
    RETURN_BTN = "Return to main menu"


############################ Text Data by Component ############################
@dataclass
class CREATE_NEW_PROFILE:
    """class holding the text for the create new settings profile page"""
    PROFILE_NAME = "Profile Name"
    ENGINE_SETTING = "Choose Engine Setting"
    PLUGIN_SETTING = "Plugin Setting"
    HEADER = "Create New Profile"


@dataclass
class ChooseFileTabText:
    """class holding the text for the choose file tab functionality"""
    WindowTitle = "Upload File"
    TabTitle = "Add New File"
    TabHeader1 = "Add File"
    TabHeader2 = "Choose Settings"
    TabHeader3 = "Select Output"


@dataclass
class CreateNewProfileTabText:
    """class holding the text for the create new profile tab"""
    WindowTitle = "Create New Profile"
    TabTitle = "Create New Profile"
    TabHeader1 = "Profile Name"
    TabHeader2 = "Engine Settings"
    TabHeader3 = "Plugin Settings"
    pluginFilter = "json file (*.json) zip file (*.zip)"


@dataclass
class ENGINE_TAB_TEXT:
    CREATE_TITTLE = "Create New Engine Setting"
    NAME_TAB = "Engine Setting Name"
    SELECT_ENGINE = "Select Speech to Text Engine"
    ENGINE_SETTING = "Speech to Text Engine Setting"






@dataclass
class BTN_TEXT:
    """class holding the text for the buttons widget"""
    ON = "ON"
    OFF = "OFF"
    ICON_BTN = "iconButton"
    right = "right.png"
    down = "down.png"


@dataclass
class FILE_TABLE:
    """class holding the text for the file table widget"""
    COMPLETE = "\u2705 Completed"


@dataclass
class POPUP_TAB:
    """class holding the text for the pop-up component"""
    ## unicode of right pointing arrow
    START = "Start"
    PREVIOUS = "Previous"
    NEXT = "Next"
    FINISH = "Finish"

@dataclass
class FILE_TABLE_HEADER:
    """class holding the text for the file table headers"""
    FILE_UPLOAD = ["Select All","Type", "Name", "Profile", "Status",  "Date", "Actions"]
    CONFIRM = ["Type", "Name", "Profile", "Actions"]
    TRANSCRIBE = ["Type", "Name", "Progress"]
    SUCCESS = ["Type", "Name", "Status", "Output", "Actions"]


LINKS_DATA = LINKS.from_dict(link)
@dataclass
class LINK:
    _linkTemplate = "<a style='color:{0}; font-weight: 500;' href={1}>{2}</a>"
    USER_MANUAL = _linkTemplate.format(
        Color.LINK, LINKS_DATA.USER_MANUAL, WELCOME_PAGE.USER_MANUAL
    )
    TECH_DOC = _linkTemplate.format(Color.LINK, LINKS_DATA.TECHNICAL_DOCUMENT, WELCOME_PAGE.GUIDE)
    GB_WEB = _linkTemplate.format(Color.LINK, LINKS_DATA.HILAB, WELCOME_PAGE.WEB_LINK)


@dataclass
class MENU_BAR:
    """class holding the text for the menu bar"""
    CONSOLE = "Console"
    OPEN = "Open"
    CLOSE = "Close"
    HELP = "Help"
    CONTACT = "Contact Us"
    BUG = "Report Bug"
    BUG_LINK = LINKS_DATA.BUG_REPORT
    EMAIL_LINK = LINKS_DATA.EMAIL 
    MAIL_FAILED = "Cannot open mail application on your computer, \
                  please contact us by sending email to: hil@elist.tufts.edu"
@dataclass
class PLUGIN_SUITE_TEXT:
    HEADER = "Upload Plugin Suite"
    SELECT_PLUGIN = "Select Plugin Suites"
    LOAD_DIR = "Load from Directory"
    LOAD_URL = "Load from Cloud"
    REGISTER = "Register Plugin Suite"
    URL = ""

    UPLOAD = "Upload"
    URL_INSTRUCTION = "GailBot currently accepts plugin suite from: "
    SOURCES = [
        "1. Amazon S3 object url storing plugin suite as zip file",
        "2. Amazon S3 Public Bucket Name",
        "3. Github url storing plugin suite as zip file",
    ]
    TABLE_HEADER = ["Plugin Suite Name", "Author", "Version", "Actions"]
    TABLE_DIMENSION = [0.3, 0.22, 0.20, 0.255]
    CONFIRM_DELETE = "Confirm deleting plugin suite {0}"


@dataclass
class ENGINE_SETTING_TEXT:
    TABLE_HEADER = ["Engine Setting Name", "Speech to Text Engine", "Actions"]
    CONFIRM_DELETE = "Confirm deleting engine setting {0}"
    HEADER = "Engine Settings"
    CAPTION = "Available Speech to Text Engine Setting"
    TABLE_DIMENSION = [0.36, 0.36, 0.255]
    CREATE_NEW = "Create New Engine"


@dataclass
class ENGINE_SETTING_FORM(DataclassFromDict):
    google: dict = field_from_dict()
    whisper: dict = field_from_dict()
    watson: dict = field_from_dict()


@dataclass
class PATH_DIALOG: 
    CONFIRM = "Confirm"
    CHANGE_DIR = "Change Directory"
    EMAIL = "hil@elist.tufts.edu"
    ZIP_FILE = "gailbot_log_file"
    SEND_ZIP = "You can send the zipped log file to us through the email:"
    SAVE_LOG = "Select the path the log files will be saved to"
    SAVE_LOG_LABEL = "Log files saved to:"
    SAVE_SOURCE = "Select path to save the source"
    SAVE_SOURCE_CAPTION = "A copy of the source will be saved to the selected path for access"
    SAVE_SOURCE_LABEL = "Select Path: "


@dataclass 
class SETTING_TABLE:
    SETTING_DETAIL_TABLE_HEADER = ["Setting Options", "Value"]
    PLUGIN_DISPLAY_HEADER = ["Applied Plugin Suite"]
    
    
ENGINE_FORM = ENGINE_SETTING_FORM.from_dict(forms["EngineForm"])
LOG_DELETE = forms["log deletion"]
RECORD_FORM = forms["record form"]
