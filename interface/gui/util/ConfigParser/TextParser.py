"""
File: Config.py
Project: GailBot GUI
File Created: Tuesday, 1st November 2022 3:59:15 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Tuesday, 1st November 2022 5:04:12 pm
Modified By:  Siara Small  & Vivian Li
-----
"""

"""accesses text configuration values from given dictionaries"""

from dataclasses import dataclass
from typing import List 
import datetime
# from util.Path import getProjectRoot
from os.path import exists
from dict_to_dataclass import DataclassFromDict, field_from_dict


""" 
   TODO: load the config file dynamically 
    
    - load either from user toml or interface toml 
    - get the root path 

"""
#############################  about data ################################
year = datetime.date.today().strftime("%Y")
copyRightText = f"copyright {year} © HIL Lab"
@dataclass
class aboutData(DataclassFromDict):
    """class holding data about GailBot; e.g. version, title, etc."""
    version   : str      = field_from_dict()
    APP_TITTLE: str      = field_from_dict()
    copyRight            = copyRightText
    
####################### Text Data ########################################
@dataclass 
class WelcomePageTextData(DataclassFromDict):
    """class holding the text for the welcome page"""
    audioInstructionText     : str = field_from_dict()
    settingsInstructionText  : str = field_from_dict()
    transcribeInstructionText: str = field_from_dict()
    fileInstructionText      : str = field_from_dict()
    editInstructionText      : str = field_from_dict()
    welcomeText              : str = field_from_dict()
    captionText              : str = field_from_dict()
    startBtnText             : str = field_from_dict()
    instructionText          : str = field_from_dict()
    resourcesText            : str = field_from_dict()
    tutorialText             : str = field_from_dict()
    guideText                : str = field_from_dict()
    gbLinkText               : str = field_from_dict()
    moreInfoText             : str = field_from_dict()
    firstLaunchHeader        : str = field_from_dict()
    firstLaunchInstruction   :str  = field_from_dict()
        
@dataclass
class TranscribeSuccessTextData(DataclassFromDict):
    """class holding the text for the transcription success page"""
    mainLabelText       : str = field_from_dict()
    transcribedFilesText: str = field_from_dict()
    moreBtnText         : str = field_from_dict()
    returnBtnText       : str = field_from_dict()
    backgroundImg       : str = "backgroundConfirmPage.png"

@dataclass
class TranscribeProgressTextData(DataclassFromDict):
    """class holding the text for the transcription in progress page"""
    mainLabelText : str = field_from_dict()
    loadingText   : str = field_from_dict()
    inProgressText: str = field_from_dict()
    cancelText    : str = field_from_dict()
    loggerMsg     : str = "Confirm cancellation"
    backgroundImg : str = "backgroundSubPages.png"

@dataclass 
class ProfileSettingData(DataclassFromDict):
    """class holding the text for the setting page"""
    RequiredSetting: dict = field_from_dict()
    PostTranscribe : dict = field_from_dict()
    Plugins        : dict = field_from_dict()

@dataclass 
class EngineSetting(DataclassFromDict):
    """class holding the text for the engine setting page"""
    Engine: dict = field_from_dict()

@dataclass 
class OutputFormatSetting(DataclassFromDict):
    """class holding the text for the output functionality"""
    CorpusSettings: dict      = field_from_dict()
    FileFormat    : List[str] = field_from_dict()
    Language      : List[str] = field_from_dict()
 

@dataclass 
class FileUploadPageTextData(DataclassFromDict):
    """class holding the text for the file upload pop-up"""
    header                : str = field_from_dict()
    returnMainText        : str = field_from_dict()
    recordBtnText         : str = field_from_dict()
    uploadBtnText         : str = field_from_dict()
    transcribeBtnText     : str = field_from_dict()
    removeBtnText         : str = field_from_dict()
    settingBtnText        : str = field_from_dict()
    dropText              : str = field_from_dict()
    chooseLocalText       : str = field_from_dict()
    chooseSetHeader       : str = field_from_dict()
    selectSetText         : str = field_from_dict()
    selectPlaceHolderText : str = field_from_dict()
    selectFolderText      : str = field_from_dict()
    chooseOutPutText      : str = field_from_dict()
    removeWarnText        : str = field_from_dict()
    fileFilter            : str = field_from_dict()
    tabAddfile            : str = field_from_dict()
    tabAddFolder          : str = field_from_dict()
    audioLogo             : str = field_from_dict()
    directoryLogo         : str = field_from_dict()

@dataclass
class RecordPageTextData(DataclassFromDict):
    """class holding the text for the record page"""
    basic    : str = field_from_dict()
    filename : str  = field_from_dict()
    mp3      : str = field_from_dict()
    wav      : str = field_from_dict()
    format   : str = field_from_dict()
    advanced : str = field_from_dict()
    rate     : str = field_from_dict()
    duration : str = field_from_dict()
    cancel   : str = field_from_dict()
    start    : str = field_from_dict()
    test     : str = field_from_dict()
    recSet   : str = field_from_dict()
    record   : str = field_from_dict()
    end      : str = field_from_dict()

@dataclass 
class RecordPageProgressData(DataclassFromDict):
    """class holding the text for the record in progress page"""
    start  : str = field_from_dict()
    cancel : str = field_from_dict()
    end    : str = field_from_dict()

@dataclass 
class ProfilePageTextData(DataclassFromDict):
    """class holding the text for the profile page"""
    cancelBtn          : str  = field_from_dict()
    saveBtn            : str  = field_from_dict()
    newProfileBtn      : str  = field_from_dict()
    reuquiredSetBtn    : str  = field_from_dict()
    postSetBtn         : str  = field_from_dict()
    newPluginBtn       : str  = field_from_dict()
    pluginSetBtn       : str  = field_from_dict()
    postSetHeader      : str  = field_from_dict()
    postSetCaption     : str  = field_from_dict()
    requiredSetHeader  : str  = field_from_dict()
    requiredSetCaption : str  = field_from_dict()
    pluginHeader       : str  = field_from_dict()
    pluginCaption      : str  = field_from_dict()
    tempMessage        : str  = field_from_dict()

@dataclass 
class SystemSetPageTextData(DataclassFromDict):
    """class holding the text for the system settings page"""
    header        : str  = field_from_dict()
    caption       : str  = field_from_dict()
    cancelBtn     : str  = field_from_dict()
    saveBtn       : str  = field_from_dict()
    confirmChange : str  = field_from_dict()
    changeError   : str  = field_from_dict()
    clearLog      : str  = field_from_dict()
    confirmClear  : str  = field_from_dict()
    changeWorkSpace: str  = field_from_dict()
    
@dataclass
class ConfirmTranscribeTextData(DataclassFromDict):
    """class holding the text for the confirm transcription popup"""
    confirmLabel: str = field_from_dict()
    confirm: str = field_from_dict()
    cancel: str = field_from_dict()

@dataclass 
class CreateNewProfileTextData(DataclassFromDict):
    """class holding the text for the create new settings profile page"""
    profileName: str = field_from_dict()
    confirmProfileNameBtn: str = field_from_dict()
    emptyNameMsg :str = field_from_dict()
    emptyUserMsg : str = field_from_dict()
    engineSettingHeader: str = field_from_dict()
    outputSettingHeader: str = field_from_dict()
    cofirmBtn : str = field_from_dict()
    
@dataclass
class ChooseFileTabTextData(DataclassFromDict):
    """class holding the text for the choose file tab functionality"""
    WindowTitle : str = field_from_dict()
    TabTitle : str = field_from_dict()
    TabHeader1 : str = field_from_dict()
    TabHeader2 : str = field_from_dict()
    TabHeader3 : str = field_from_dict()

@dataclass 
class CreateNewProfileTabTextData(DataclassFromDict):
    """class holding the text for the create new profile tab"""
    WindowTitle : str = field_from_dict()
    TabTitle    : str = field_from_dict()
    TabHeader1  : str = field_from_dict()
    TabHeader2  : str = field_from_dict()
    TabHeader3  : str = field_from_dict()
    TabHeader4  : str = field_from_dict()
    TabHeader5  : str = field_from_dict()
    TabHeader6  : str = field_from_dict()
    pluginFilter : str = field_from_dict()

@dataclass 
class MainStackTextData(DataclassFromDict):
    """class holding the text for the main stack"""
    ProfileSetting : str = field_from_dict()
    SystemSetting  : str = field_from_dict()

@dataclass 
class MenuBarText(DataclassFromDict):
    """class holding the text for the menu bar"""
    console: str = field_from_dict()
    open: str = field_from_dict()
    close : str = field_from_dict()

@dataclass
class OutputFormatFormData(DataclassFromDict):
    """class holding the text for the output functionality"""
    header : str = field_from_dict()
    CorpuFormHeader  : str = field_from_dict()
    LanguageHeader   : str = field_from_dict()
    FileFormatHeader : str = field_from_dict()
    SpeakerHeader    : str = field_from_dict()
    TextWrap         : str = field_from_dict()
    FileHeaderView   : str = field_from_dict()

@dataclass 
class BtnText(DataclassFromDict):
    """class holding the text for the buttons widget"""
    on : str = field_from_dict()
    off : str = field_from_dict()
    icon  : str = field_from_dict()
    right : str = field_from_dict()
    down : str = field_from_dict()


@dataclass
class FileTableText(DataclassFromDict):
    """class holding the text for the file table widget"""
    default : str = field_from_dict()
    delete : str = field_from_dict()
    changeSet : str = field_from_dict()
    profileDet : str = field_from_dict()

@dataclass 
class MultipleComboText(DataclassFromDict):
    """class holding the text for the combo box widget"""
    username : str = field_from_dict()
    password : str = field_from_dict()
    
@dataclass
class WindowTitleData(DataclassFromDict):
    """class holding the text for the window title component"""
    consoleWindow : str = field_from_dict()

@dataclass
class PopUpText(DataclassFromDict):
    """class holding the text for the pop-up component"""
    leftArr : str = field_from_dict()
    rightArr : str = field_from_dict()
    finish : str = field_from_dict()
    window : str = field_from_dict()

@dataclass
class TableText(DataclassFromDict):
    """class holding the text for the table component"""
    location : str = field_from_dict()
    postSettings : str = field_from_dict()
    save : str = field_from_dict()
    transBy : str = field_from_dict()
    transOn : str = field_from_dict()
    inDir : str = field_from_dict()
    abtDir : str = field_from_dict()

@dataclass
class FiletableHeader(DataclassFromDict):
    """class holding the text for the file table headers"""
    fileUploadPage: List[str] = field_from_dict()
    confirmPage: List[str] = field_from_dict()
    successPage:  List[str] = field_from_dict()
    transcribePage: List[str] = field_from_dict()


@dataclass
class TableWidgetOptions(DataclassFromDict):
    """class holding the text for options of the table widget component"""
    fileDetails: str = field_from_dict()
    

@dataclass 
class ProfileField(DataclassFromDict):
    """class holding the text for the profile field component"""
    user: str = field_from_dict()
    engine : str = field_from_dict()
    outPutFormat: str = field_from_dict()
    postTranscribe : str = field_from_dict()
    reuquiredSetting : str = field_from_dict()
    plugin: str = field_from_dict()