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
from util.Path import getProjectRoot
from os.path import exists
import toml 
from dict_to_dataclass import DataclassFromDict, field_from_dict


""" 
   TODO: load the config file dynamically 
    
    - load either from user toml or interface toml 
    - get the root path 

"""



config = toml.load("controller/interface.toml")


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
    
    
@dataclass 
class DimensionData(DataclassFromDict):
    WINMAXWIDTH :int = field_from_dict()
    WINMAXHEIGHT :int = field_from_dict()
    BTNWIDTH:int = field_from_dict()
    BTNHEIGHT :int = field_from_dict()
    SBTNWIDTH :int = field_from_dict()
    SBTNHEIGHT  :int = field_from_dict()
    CONSOLEWIDTH :int = field_from_dict()
    CONSOLEHEIGHT :int = field_from_dict()
    STATUSWIDTH :int = field_from_dict()
    STATUSHEIGHT :int = field_from_dict()
    INPUTWIDTH :int = field_from_dict()
    INPUTHEIGHT:int = field_from_dict()
    ICONBTN :int = field_from_dict()

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

""" style data """
Color = ColorData.from_dict(config["colors"])
FontSize = FontSizeData.from_dict(config["fontSizes"])
WelcomePageText = WelcomePageTextData.from_dict(
    config["text"]["WelcomePageText"])
Dimension = DimensionData.from_dict(config["dimension"])

""" text data """
TranscribeProgressText = TranscribeProgressTextData.from_dict(
    config["text"]["TranscribeProgressText"])
TranscribeSuccessText = TranscribeSuccessTextData.from_dict(
    config["text"]["TranscribeSuccessText"])

""" setting form data  """
ProfileSettingForm = ProfileSettingData.from_dict(config["profile form"])
SystemSettingForm = config["system setting form"]


@dataclass
class Links: 
    link = config["text"]["links"]["HILAB"]
    _linkTemplate = "<a href={0}>{1}</a>"
    tutorialLink = _linkTemplate.format(
        link, WelcomePageText.tutorialText)
    guideLink = _linkTemplate.format(
        link, WelcomePageText.guideText)
    gbWebLink = _linkTemplate.format(
        link, WelcomePageText.gbLinkText)
    gbWebLink = _linkTemplate.format(
        link, WelcomePageText.guideText)










