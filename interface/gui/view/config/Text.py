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


text   = toml.load(os.path.join(FRONTEND_CONFIG_ROOT, TextDataPath.string))
forms  = toml.load(os.path.join(FRONTEND_CONFIG_ROOT, TextDataPath.form))
about  = toml.load(os.path.join(FRONTEND_CONFIG_ROOT, TextDataPath.about))


#############################  about data ################################
year = datetime.date.today().strftime("%Y")
copyRightText = f"Copyright {year} © HI Lab"

@dataclass 
class Workspace:
    workspaceName = "GailBot"

@dataclass
class About :
    """class holding data about GailBot; e.g. version, title, etc."""
    version              = "Version 0.0.1"
    APP_TITTLE           = "GailBot"
    copyRight            = copyRightText
    
####################### Text Data ########################################
@dataclass 
class WelcomePageText :
    """class holding the text for the welcome page"""
    audioInstructionText      = "1. Add audio / video\n sources or record live"
    settingsInstructionText   = "2. Select a Settings Profile"
    transcribeInstructionText = "3. Transcribe"
    fileInstructionText       = "4. Review transcriptions"
    editInstructionText       = "5. Edit settings \n or retranscribe"
    welcomeText               = "Welcome to GailBot"
    captionText               = "GailBot is the world's first automated transcription system capable\n" \
                                "of generating customized Conversation Analytic transcripts at scale."
    startBtnText           = "Get Started"
    instructionText        = "How GailBot Works"
    resourcesText          = "Resources"
    tutorialText           = "User Manual"
    guideText              = "Documentation"
    gbLinkText             = "Tufts Human Interaction Laboratory"
    moreInfoText           = "For more information, visit:"
    confirmBtn    = "Confirm"
    changeDirBtn  = "Change Directory"
    email         = "hil@elist.tufts.edu"
    zipFileName   = "gailbot_log_file"
    sendZipMsg    = "You can send the zipped log file to us through the email:"
    saveLogPrompt = "Select the path the log files will be saved to"
    saveLogPath   = "Log files saved to:"
    

@dataclass 
class FileUploadPageText:
    """class holding the text for the file upload pop-up"""
    header                = "Files to Transcribe"
    returnMainText        = "Return to Main Menu"
    recordBtnText         = "Record Live"
    uploadBtnText         = "Add From Device"
    transcribeBtnText     = "Transcribe"
    removeBtnText         = "Remove All"
    ## unicode for settings gear
    settingBtnText        = "\u2699"
    dropText              = "Drop file to upload"
    chooseLocalText       = "Choose from local"
    chooseSetHeader       = "Select Setting Profile"
    selectSetText         = "Select Settings"
    selectPlaceHolderText = "None"
    selectFolderText      = "Select Folder"
    chooseOutPutText      = "Choose Output Directory"
    fileFilter            = "audio file (*.wav)"
    removeWarnText        = "Remove all files?"
    tabAddfile            = "Add File"
    tabAddFolder          = "Add Folder"
    uploadInstruction      = "Drop audio files below (Only wav files are supported)"
    ## unicode for an audio icon
    audioLogo = "\U0001F50A"
    ## unicode for a file folder icon
    directoryLogo = "\U0001F4C1"
    delete = "\u274C"

@dataclass
class RecordPageText:
    """class holding the text for the record page"""
    basic    = "Basic"
    filename = "Filename"
    mp3      = "MP3"
    wav      = "WAV"
    format   = "Audio Format"
    advanced = "Advanced"
    rate     = "Recording Rate (Hertz)"
    duration = "Max Recording Duration"
    cancel   = "Cancel"
    start    = "Start Recording"
    test     = "Test MicroPhone"
    recSet   = "Recording Settings"
    record   = "Record Audio File"
    end      = "End Recording"
    
@dataclass 
class RecordPageProgressText:
    """class holding the text for the record in progress page"""
    start  = "Start Recording"
    cancel = "Cancel"
    end    = "End Recording"


@dataclass 
class ProfilePageText:
    """class holding the text for the profile page"""
    cancelBtn          = "Cancel"
    saveBtn            = "Save and Exit"
    deleteBtn          = "Delete Profile"
    newProfileBtn      = "Create New Profile"
    reuquiredSetBtn    = "Required Settings"
    postSetBtn         = "Post-Transcription Settings"
    newPluginBtn       = "Add New Plugin"
    pluginSetBtn       = "Plugin Settings"
    engineSettingHeader  = "Speech to Text Settings"
    engineSettingCaption = "These settings are applied to the selected settings profile and are required for transcription"
    pluginHeader       = "Choose Plugins"
    pluginCaption      = "These plugins are applied to the transcription process"
    tempMessage        = "This page has been temporarily disabled to allow for further updates and developments. Please check back later."
    confirmDelete      = "Confirm deleting the profile: "

@dataclass 
class SystemSetPageText:
    """class holding the text for the system settings page"""
    header        = "System Settings"
    caption       = "Control various aspects of the graphical interface"
    cancelBtn     = "Cancel"
    saveBtn       = "Save and Exit"
    confirmChange = """The changes applied require GailBot to relaunch. All uploaded \
                    files will be removed. Do you wish to proceed?"""
    changeError   = "System settings change failed"
    clearLog      = "Clear all log files"
    confirmClear  = "All log files will be removed. Proceed?"
    changeWorkSpace = "Change GailBot workspace"

class ConfirmTranscribeText:
    """class holding the text for the confirm transcription popup"""
    confirmLabel = "Confirm Files and Settings"
    confirm      = "Confirm"
    cancel       = "Cancel"

@dataclass 
class CreateNewProfilePageText:
    """class holding the text for the create new settings profile page"""
    profileName           = "Profile Name"
    confirmProfileNameBtn = "Start"
    emptyNameMsg          = "A profile name must be specified"
    emptyUserMsg          = "Please enter user name and password"
    engineSettingHeader   = "Speech to Text Settings"
    outputSettingHeader   = "Output format settings"
    cofirmBtn             = "Confirm"

@dataclass
class ChooseFileTabText:
    """class holding the text for the choose file tab functionality"""
    WindowTitle = "Upload File"
    TabTitle    = "Add New File"
    TabHeader1  = "Add File"
    TabHeader2  = "Choose Settings"
    TabHeader3  = "Select Output"

@dataclass 
class CreateNewProfileTabText:
    """class holding the text for the create new profile tab"""
    WindowTitle  = "Create New Profile"
    TabTitle     = "Create New Profile"
    TabHeader1   = "Profile Name"
    TabHeader2   = "Engine Settings"
    TabHeader3   = "Plugin Settings"
    pluginFilter = "json file (*.json) zip file (*.zip)"

@dataclass 
class MainStackText:
    """class holding the text for the main stack"""
    profilesetting = "profile settings"
    systemsetting  = "system settings"
    
@dataclass 
class MenuBarText:
    """class holding the text for the menu bar"""
    console    = "Console"
    open       = "Open"
    close      = "Close"
    help       = "Help"
    contact    = "Contact Us"
    bugreport  = "Report Bug"
    buglink    = "https://docs.google.com/forms/d/e/1FAIpQLSey-yx8gj2k5n-pdoSqBzBRU9q1aqWfK6laiQCxTimvuGU0hg/viewform"
    email      = "mailto:hil@elist.tufts.edu"
    mailFailed = "Cannot open mail application on your computer, \
                  please contact us by sending email to: hil@elist.tufts.edu"

@dataclass 
class BtnText:
    """class holding the text for the buttons widget"""
    on    = "ON"
    off   = "OFF"
    icon  = "iconButton"
    right = "right.png"
    down  = "down.png"

@dataclass
class FileTableText:
    """class holding the text for the file table widget"""
    default    = "Default"
    delete     = "Remove"
    changeSet  = "Change Profile"
    profileDet = "Profile Details"
    
@dataclass
class WindowTitle:
    """class holding the text for the window title component"""
    consoleWindow = "Console" 

@dataclass
class PopUpText:
    """class holding the text for the pop-up component"""
    leftArr = "\u25B6"
    ## unicode of right pointing arrow
    rightArr = "\u25C0"
    finish   = "Finish"
    window   = "File Info"

@dataclass
class TableText:
    """class holding the text for the table component"""
    location     = "Change Location"
    postSettings = "Post Transcribe Setting"
    save         = "Save"
    transBy      = "Transcribed by: "
    transOn      = "Trancribed on: "
    inDir        = "In this directory"
    abtDir       = "About this directory"

@dataclass
class TranscribeProgressText:
    mainLabelText  = "Transcription in progress"
    loadingText    = "Transcribing files..."
    inProgressText = "Files in progress:"
    cancelText     = "Cancel"
@dataclass
class FileTableHeader:
    """class holding the text for the file table headers"""
    fileUploadPage = ["Select All", "Type", "Name", "Profile",
                        "Status", "Date", "Size", "Actions"]
    confirmPage    = ["Type", "Name", "Profile", "Action"]
    transcribePage = ["Type", "Name", "Progress"]
    successPage    = ["Type",  "Name", "Status", "Output"]
@dataclass 
class TranscribeSuccessText: 
    mainLabelText        = "Transcription complete"
    transcribedFilesText = "Files summary and locations:"
    moreBtnText          = "Process additional files"
    returnBtnText        = "Return to main menu"

@dataclass
class TableWidgetOptions:
    """class holding the text for options of the table widget component"""
    fileDetails = "details"

@dataclass 
class ProfileField:
    """class holding the text for the profile field component"""
    user             = "User Info"
    engine           = "Engine"
    outPutFormat     = "Output Form Data"
    postTranscribe   = "PostTranscribe"
    reuquiredSetting = "RequiredSetting"
    plugin           = "Plugins"

@dataclass
class ProfileSetting(DataclassFromDict):
    """class holding the text for the setting page"""
    RequiredSetting: dict = field_from_dict()
    PostTranscribe : dict = field_from_dict() 
    Plugins        : dict = field_from_dict()

@dataclass 
class EngineSetting(DataclassFromDict):
    """class holding the text for the engine setting page"""
    Engine: dict = field_from_dict()
    
@dataclass
class Links: 
    HILAB            = "https://sites.tufts.edu/hilab/gailbot-an-automatic-transcription-system-for-conversation-analysis"
    USER_MANUAL      = "https://drive.google.com/file/d/1NnirL5-26j3xnI4yEV7cJVUEqxrFfTm5/view?usp=sharing"
    GUIDE            = "https://drive.google.com/file/d/1t_-NAM0PCFHhjZ4Kpry2LuhLcXZTDG07/view?usp=sharing"
    _linkTemplate    = "<a style='color:{0}; font-weight: 500;' href={1}>{2}</a>"
    tutorialLink     = _linkTemplate.format(Color.LINK, USER_MANUAL, WelcomePageText.tutorialText)
    guideLink        = _linkTemplate.format(Color.LINK, GUIDE, WelcomePageText.guideText)
    gbWebLink        = _linkTemplate.format(Color.LINK, HILAB, WelcomePageText.gbLinkText)
    guideLinkSideBar = _linkTemplate.format(Color.LINK, USER_MANUAL, WelcomePageText.tutorialText)

ProfileSettingForm = ProfileSetting.from_dict(forms["profile form"])
EngineForm  = EngineSetting.from_dict(forms["profile form"]["RequiredSetting"])
SystemSettingForm  = forms["system setting form"]
LogDeleteTimeDict  = forms["log deletion"]
RecordForm         = forms["record form"]