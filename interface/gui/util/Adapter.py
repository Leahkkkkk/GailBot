'''
File: Config.py
Project: GailBot GUI
File Created: Tuesday, 1st November 2022 3:59:15 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Tuesday, 1st November 2022 5:04:12 pm
Modified By:  Siara Small  & Vivian Li
-----
'''


from dataclasses import dataclass
from typing import List 
import datetime
# from util.Path import getProjectRoot
from os.path import exists
import toml 
from dict_to_dataclass import DataclassFromDict, field_from_dict


""" 
   TODO: load the config file dynamically 
    
    - load either from user toml or interface toml 
    - get the root path 

"""


#############################  about data ################################
year = datetime.date.today().strftime("%Y")
copyRightText = f"{year} © HIL Lab"
@dataclass
class aboutData(DataclassFromDict):
    version: str = field_from_dict()
    copyRight = copyRightText
    
################################## style data #############################
@dataclass 
class ColorData(DataclassFromDict):
    GREEN: str = field_from_dict()
    ORANGE: str = field_from_dict()
    BLUEWHITE: str =  field_from_dict()
    BLUELIGHT: str =  field_from_dict()
    BLUEMEDIUM: str =  field_from_dict()
    BLUEDARK: str =  field_from_dict()
    GREYLIGHT: str =  field_from_dict()
    GREYMEDIUM1: str =  field_from_dict()
    GREYMEDIUM2: str =  field_from_dict()
    GREYDARK: str =  field_from_dict()
    BORDERGREY: str =  field_from_dict()
    BLACK: str =  field_from_dict()
    WHITE: str =  field_from_dict()
    GREYEXTRALIGHT: str =  field_from_dict()

@dataclass
class FontSizeData(DataclassFromDict):
    BODY: str =  field_from_dict()
    TEXT_FIELD: str =  field_from_dict()
    SMALL: str =  field_from_dict()
    LINK: str =  field_from_dict()
    HEADER1: str =  field_from_dict()
    HEADER2: str =  field_from_dict()
    HEADER3: str =  field_from_dict()
    TABLE_ROW: str =  field_from_dict()
    DESCRIPTION: str =  field_from_dict()
    INSTRUCTION_CAPTION: str =  field_from_dict()
    BTN: str =  field_from_dict()
    SETTINGICON: str = field_from_dict()
    
@dataclass
class FontFamilyData(DataclassFromDict):
    MAIN: str = field_from_dict()
    OTHER: str = field_from_dict()
    
@dataclass 
class DimensionData(DataclassFromDict):
    WINMAXWIDTH : int = field_from_dict()
    WINMAXHEIGHT :int = field_from_dict()
    BTNWIDTH: int = field_from_dict()
    BTNHEIGHT :int = field_from_dict()
    SBTNWIDTH :int = field_from_dict()
    SBTNHEIGHT  :int = field_from_dict()
    LBTNWIDTH: int = field_from_dict()
    CONSOLEWIDTH :int = field_from_dict()
    CONSOLEHEIGHT :int = field_from_dict()
    STATUSWIDTH :int = field_from_dict()
    STATUSHEIGHT :int = field_from_dict()
    INPUTWIDTH :int = field_from_dict()
    INPUTHEIGHT:int = field_from_dict()
    ICONBTN :int = field_from_dict()
    SMALLICONBTN: int = field_from_dict()
    TABLEWIDTH: int = field_from_dict()
    TABLEMINHEIGHT: int = field_from_dict()
    TABLECONTAINERWIDTH :int = field_from_dict()
    PROGRESSBARWIDTH :int = field_from_dict()
    PROGRESSBARHEIGHT :int = field_from_dict()
    LARGEDIALOGWIDTH:int = field_from_dict()
    LARGEDIALOGHEIGHT:int = field_from_dict()
    TOGGLEBARMAXWIDTH:int = field_from_dict()
    TOGGLEBARMINWIDTH:int = field_from_dict()
    TOGGLEVIEWOFFSET:int = field_from_dict()
    STANDARDSPACING: int = field_from_dict()
    SIDEBAR: int = field_from_dict()
    FORMWIDTH: int = field_from_dict()
    FORMMINHEIGHT: int = field_from_dict()
    FORMMAXHEIGHT: int = field_from_dict()
    DEFAULTTABHEIGHT: int = field_from_dict()
    DEFAULTTABWIDTH : int = field_from_dict()



@dataclass 
class Asset(DataclassFromDict):
    arrowImg: str =  field_from_dict()
    subPageBackgorund: str =  field_from_dict()
    trashImg: str  =  field_from_dict()
    mainBackground: str  =  field_from_dict()
    headerFont : str  =  field_from_dict()
    sidebarColor: str  =  field_from_dict()
    tabSettings: str  =  field_from_dict()
    tabTrash: str  =  field_from_dict()
    tabDisk: str  =  field_from_dict()
    fileIcon: str  =  field_from_dict()
    instructionSound: str  =  field_from_dict()
    instructionSetting: str  =  field_from_dict()
    instructionTranscribe: str  =  field_from_dict()
    instructionFile: str  =  field_from_dict()
    instructionEdit: str  =  field_from_dict()
    recordStop: str  =  field_from_dict()
    recordPlay: str  =  field_from_dict()

@dataclass 
class FileTableDimension(DataclassFromDict):
    fileUploadPage: List[float] = field_from_dict()
    confirmPage: List[float] = field_from_dict()


@dataclass 
class StyleSheet(DataclassFromDict):
    goToMain: str =  field_from_dict()
    settingStackID: str = field_from_dict()
    settingStack: str = field_from_dict()
    sysSettingStackID: str = field_from_dict()
    sysSettingStack: str = field_from_dict()
    noSideBorder: str = field_from_dict()
    boldTopBorder: str = field_from_dict()
    boldBottomBorder: str = field_from_dict()
    onlyBottomBorder: str = field_from_dict()
    onlyTopBorder: str = field_from_dict()
    checkbox : str = field_from_dict()
    toggleBtnBasic: str = field_from_dict()
    formBorder: str = field_from_dict()
    warnText: str = field_from_dict()
    statusText:  str = field_from_dict()
    errorText :  str = field_from_dict()

@dataclass 
class FontFamilyData(DataclassFromDict):
    MAIN: str = field_from_dict()
    OTHER: str = field_from_dict()
    
####################### Text Data ########################################
@dataclass 
class WelcomePageTextData(DataclassFromDict):
    audioInstructionText: str =  field_from_dict()
    settingsInstructionText: str =  field_from_dict()
    transcribeInstructionText: str =  field_from_dict()
    fileInstructionText: str =  field_from_dict()
    editInstructionText: str =  field_from_dict()
    welcomeText: str =  field_from_dict()
    captionText: str =  field_from_dict()
    startBtnText: str =  field_from_dict()
    instructionText: str =  field_from_dict()
    resourcesText: str =  field_from_dict()
    tutorialText: str =  field_from_dict()
    guideText: str =  field_from_dict()
    gbLinkText: str =  field_from_dict()
    moreInfoText: str =  field_from_dict()
        
@dataclass
class TranscribeSuccessTextData(DataclassFromDict):
    mainLabelText: str =  field_from_dict()
    transcribedFilesText: str =  field_from_dict()
    moreBtnText: str =  field_from_dict()
    returnBtnText: str =  field_from_dict()
    backgroundImg: str = "backgroundConfirmPage.png"

@dataclass
class TranscribeProgressTextData(DataclassFromDict):
    mainLabelText: str =  field_from_dict()
    loadingText: str =  field_from_dict()
    inProgressText: str =  field_from_dict()
    cancelText: str =  field_from_dict()
    loggerMsg: str = "Confirm cancellation"
    backgroundImg: str = "backgroundSubPages.png"

@dataclass 
class ProfileSettingData(DataclassFromDict):
    RequiredSetting: dict = field_from_dict()
    PostTranscribe: dict = field_from_dict()
    Plugins: dict = field_from_dict()

@dataclass 
class EngineSetting(DataclassFromDict):
    Engine: dict = field_from_dict()

@dataclass 
class OutputFormatSetting(DataclassFromDict):
    CorpusSettings: dict = field_from_dict()
    FileFormat: List[str] = field_from_dict()
    Language: List[str] = field_from_dict()

@dataclass 
class FileUploadPageTextData(DataclassFromDict):
    header: str =  field_from_dict()
    returnMainText: str = field_from_dict()
    recordBtnText: str =  field_from_dict()
    uploadBtnText : str =  field_from_dict()
    transcribeBtnText : str =  field_from_dict()
    removeBtnText : str =  field_from_dict()
    settingBtnText : str =  field_from_dict()
    dropText: str =  field_from_dict()
    chooseLocalText : str =  field_from_dict()
    chooseSetHeader : str =  field_from_dict()
    selectSetText: str =  field_from_dict()
    selectPlaceHolderText : str =  field_from_dict()
    selectFolderText: str =  field_from_dict()
    chooseOutPutText: str =  field_from_dict()
    removeWarnText: str =  field_from_dict()
    fileFilter: List[str] =  field_from_dict()

@dataclass
class RecordPageTextData(DataclassFromDict):
    basic: str = field_from_dict()
    filename: str = field_from_dict()
    mp3: str = field_from_dict()
    wav: str = field_from_dict()
    format: str = field_from_dict()
    advanced: str = field_from_dict()
    rate: str = field_from_dict()
    duration: str = field_from_dict()
    cancel: str = field_from_dict()
    start: str = field_from_dict()
    test: str = field_from_dict()
    recSet: str = field_from_dict()
    record: str = field_from_dict()
    end : str = field_from_dict()

@dataclass 
class RecordPageProgressData(DataclassFromDict):
    start: str = field_from_dict()
    cancel : str = field_from_dict()
    end: str = field_from_dict()

@dataclass 
class ProfilePageTextData(DataclassFromDict):
    cancelBtn: str = field_from_dict()
    saveBtn : str = field_from_dict()
    newProfileBtn : str = field_from_dict()
    reuquiredSetBtn : str = field_from_dict()
    postSetBtn : str = field_from_dict()
    newPluginBtn : str = field_from_dict()
    pluginSetBtn : str = field_from_dict()
    postSetHeader : str = field_from_dict()
    postSetCaption: str = field_from_dict()
    requiredSetHeader : str = field_from_dict()
    requiredSetCaption : str = field_from_dict()
    pluginHeader:  str = field_from_dict()
    pluginCaption:  str = field_from_dict()

@dataclass 
class SystemSetPageTextData(DataclassFromDict):
    header: str = field_from_dict()
    caption:str = field_from_dict()
    cancelBtn : str = field_from_dict()
    saveBtn : str = field_from_dict()
    
@dataclass
class ConfirmTranscribeTextData(DataclassFromDict):
    confirmLabel: str = field_from_dict()
    confirm: str = field_from_dict()
    cancel: str = field_from_dict()

@dataclass 
class CreateNewProfileTextData(DataclassFromDict):
    confirmProfileNameBtn: str = field_from_dict()
    emptyNameMsg :str = field_from_dict()
    emptyUserMsg : str = field_from_dict()
    engineSettingHeader: str = field_from_dict()
    outputSettingHeader: str = field_from_dict()
    cofirmBtn : str = field_from_dict()
    
    
@dataclass
class ChooseFileTabTextData(DataclassFromDict):
    WindowTitle : str = field_from_dict()
    TabTitle    : str = field_from_dict()
    TabHeader1  : str = field_from_dict()
    TabHeader2  : str = field_from_dict()
    TabHeader3  : str = field_from_dict()

@dataclass 
class CreateNewProfileTabTextData(DataclassFromDict):
    WindowTitle : str = field_from_dict()
    TabTitle    : str = field_from_dict()
    TabHeader1  : str = field_from_dict()
    TabHeader2  : str = field_from_dict()
    TabHeader3  : str = field_from_dict()
    TabHeader4  : str = field_from_dict()
    TabHeader5  : str = field_from_dict()
    TabHeader6  : str = field_from_dict()

@dataclass 
class MainStackTextData(DataclassFromDict):
    ProfileSetting : str = field_from_dict()
    SystemSetting  : str = field_from_dict()

@dataclass 
class MenuBarText(DataclassFromDict):
    console: str = field_from_dict()
    open: str = field_from_dict()
    close : str = field_from_dict()

@dataclass
class OutputFormatFormData(DataclassFromDict):
    header : str = field_from_dict()
    CorpuFormHeader  : str = field_from_dict()
    LanguageHeader   : str = field_from_dict()
    FileFormatHeader : str = field_from_dict()
    SpeakerHeader    : str = field_from_dict()
    TextWrap         : str = field_from_dict()
    FileHeaderView   : str = field_from_dict()

@dataclass 
class BtnText(DataclassFromDict):
    on : str = field_from_dict()
    off : str = field_from_dict()
    icon  : str = field_from_dict()
    right : str = field_from_dict()
    down : str = field_from_dict()



@dataclass
class FileTableText(DataclassFromDict):
    default : str = field_from_dict()
    delete : str = field_from_dict()
    changeSet : str = field_from_dict()
    profileDet : str = field_from_dict()

@dataclass 
class MultipleComboText(DataclassFromDict):
    username : str = field_from_dict()
    password : str = field_from_dict()
    
@dataclass
class WindowTitleData(DataclassFromDict):
    consoleWindow : str = field_from_dict()

@dataclass
class PopUpText(DataclassFromDict):
    leftArr : str = field_from_dict()
    rightArr : str = field_from_dict()
    finish : str = field_from_dict()
    window : str = field_from_dict()

@dataclass
class TableText(DataclassFromDict):
    location : str = field_from_dict()
    postSettings : str = field_from_dict()
    save : str = field_from_dict()
    transBy : str = field_from_dict()
    transOn : str = field_from_dict()
    inDir : str = field_from_dict()
    abtDir : str = field_from_dict()

#####################   config data by widget #########################
@dataclass
class FiletableHeader(DataclassFromDict):
    fileUploadPage: List[str] = field_from_dict()
    confirmPage: List[str] = field_from_dict()
    

