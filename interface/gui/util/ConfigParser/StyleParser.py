

from dataclasses import dataclass
from typing import List 
import datetime
# from util.Path import getProjectRoot
from os.path import exists
from dict_to_dataclass import DataclassFromDict, field_from_dict

"""accesses style configuration values from given dictionaries"""

################################## style data #############################
@dataclass 
class ColorData(DataclassFromDict): 
    """ class to access the color data from the currently loaded theme """
    SECONDARY_BUTTON : str = field_from_dict()
    CANCEL_QUIT      : str = field_from_dict()
    HIGHLIGHT        : str = field_from_dict()
    TABLE_HEADER     : str = field_from_dict()
    PRIMARY_BUTTON   : str = field_from_dict()
    PRIMARY_INTENSE  : str = field_from_dict()
    LOW_CONTRAST     : str = field_from_dict()
    LOW_CONTRAST2    : str = field_from_dict()
    OUTLINE          : str = field_from_dict()
    BORDER           : str = field_from_dict()
    SCORLL_BAR       : str = field_from_dict()
    MAIN_TEXT        : str = field_from_dict()
    MAIN_BACKRGOUND  : str = field_from_dict()
    SUB_BACKGROUND   : str = field_from_dict()
    WHITE            : str = field_from_dict()
    GREYDARK         : str = field_from_dict()
    GREYEXTRALIGHT   : str = field_from_dict()
    TABLE_BORDER     : str = field_from_dict()
    INPUT_TEXT       : str = field_from_dict()
    INPUT_BORDER     : str = field_from_dict()
    INPUT_BACKGROUND : str = field_from_dict()
    
    
@dataclass 
class FontSource(DataclassFromDict): 
    """ class to access the font data from the currently loaded theme """
    headerFont: str = field_from_dict()
    clockFont : str = field_from_dict()
    
    
@dataclass
class FontSizeData(DataclassFromDict): 
    """ class to access the font size data from the currently loaded theme """
    BODY               : str = field_from_dict()
    TEXT_FIELD         : str = field_from_dict()
    SMALL              : str = field_from_dict()
    LINK               : str = field_from_dict()
    HEADER1            : str = field_from_dict()
    HEADER2            : str = field_from_dict()
    HEADER3            : str = field_from_dict()
    TABLE_ROW          : str = field_from_dict()
    DESCRIPTION        : str = field_from_dict()
    INSTRUCTION_CAPTION: str = field_from_dict()
    BTN                : str = field_from_dict()
    SETTINGICON        : str = field_from_dict()
    
@dataclass
class FontFamilyData(DataclassFromDict): 
    """ class to access the color font family from the currently loaded theme """
    MAIN : str = field_from_dict()
    OTHER: str = field_from_dict()
    CLOCK: str = field_from_dict()
    
@dataclass 
class DimensionData(DataclassFromDict): 
    """ class to access the dimension data from the currently loaded theme """
    WINMAXWIDTH         : int = field_from_dict()
    WINMAXHEIGHT        : int = field_from_dict()
    BTNWIDTH            : int = field_from_dict()
    BTNHEIGHT           : int = field_from_dict()
    SBTNWIDTH           : int = field_from_dict()
    SBTNHEIGHT          : int = field_from_dict()
    LBTNWIDTH           : int = field_from_dict()
    CONSOLEWIDTH        : int = field_from_dict()
    CONSOLEHEIGHT       : int = field_from_dict()
    STATUSWIDTH         : int = field_from_dict()
    STATUSHEIGHT        : int = field_from_dict()
    INPUTWIDTH          : int = field_from_dict()
    INPUTHEIGHT         : int = field_from_dict()
    ICONBTN             : int = field_from_dict()
    SMALLICONBTN        : int = field_from_dict()
    TABLEWIDTH          : int = field_from_dict()
    TABLEMINHEIGHT      : int = field_from_dict()
    TABLECONTAINERWIDTH : int = field_from_dict()
    PROGRESSBARWIDTH    : int = field_from_dict()
    PROGRESSBARHEIGHT   : int = field_from_dict()
    LARGEDIALOGWIDTH    : int = field_from_dict()
    LARGEDIALOGHEIGHT   : int = field_from_dict()
    TOGGLEBARMAXWIDTH   : int = field_from_dict()
    TOGGLEBARMINWIDTH   : int = field_from_dict()
    TOGGLEVIEWOFFSET    : int = field_from_dict()
    STANDARDSPACING     : int = field_from_dict()
    SIDEBAR             : int = field_from_dict()
    FORMWIDTH           : int = field_from_dict()
    FORMMINHEIGHT       : int = field_from_dict()
    FORMMAXHEIGHT       : int = field_from_dict()
    DEFAULTTABHEIGHT    : int = field_from_dict()
    DEFAULTTABWIDTH     : int = field_from_dict()
    LOGO_WIDTH          : int = field_from_dict()
    LOGO_HEIGHT         : int = field_from_dict()
    SMALL_TABLE_WIDTH   : int = field_from_dict()
    SMALL_TABLE_HEIGHT  : int = field_from_dict()
    SMALL_SPACING       : int = field_from_dict()
    MEDIUM_SPACING      : int = field_from_dict()
    LARGE_SPACING       : int = field_from_dict()
    LARGE_ICON          : int = field_from_dict()
    WIN_MIN_WIDTH       : int = field_from_dict()
    WIN_MIN_HEIGHT      : int = field_from_dict()
    OUTPUT_FORM_HEIGHT  : int = field_from_dict()

@dataclass 
class Asset(DataclassFromDict): 
    """class to access the asset data from the currently loaded theme"""
    arrowImg              : str = field_from_dict()
    trashImg              : str = field_from_dict()
    sidebarColor          : str = field_from_dict()
    tabSettings           : str = field_from_dict()
    tabTrash              : str = field_from_dict()
    tabDisk               : str = field_from_dict()
    fileIcon              : str = field_from_dict()
    instructionSound      : str = field_from_dict()
    instructionSetting    : str = field_from_dict()
    instructionTranscribe : str = field_from_dict()
    instructionFile       : str = field_from_dict()
    instructionEdit       : str = field_from_dict()
    recordStop            : str = field_from_dict()
    recordPlay            : str = field_from_dict()
    homeBackground        : str = field_from_dict()
    subPageBackground     : str = field_from_dict()
    sideBarBackground     : str = field_from_dict()
    downImg               :str  = field_from_dict()
    rightImg              : str = field_from_dict()
    hilLabLogo            : str = field_from_dict()
    transcribing          : str = field_from_dict()
    endRecording          : str = field_from_dict()


@dataclass 
class FileTableDimension(DataclassFromDict): 
    """class to access the file table dimension data from the currently loaded theme"""
    fileUploadPage: List[float] = field_from_dict()
    confirmPage   : List[float] = field_from_dict()
    transcribePage: List[float] = field_from_dict()
    successPage   : List[float] = field_from_dict()

@dataclass 
class StyleSheet(DataclassFromDict): 
    """class to access the style sheet data from the currently loaded theme"""
    goToMain          : str = field_from_dict()
    settingStackID    : str = field_from_dict()
    settingStack      : str = field_from_dict()
    sysSettingStackID : str = field_from_dict()
    sysSettingStack   : str = field_from_dict()
    noSideBorder      : str = field_from_dict()
    boldTopBorder     : str = field_from_dict()
    boldBottomBorder  : str = field_from_dict()
    onlyBottomBorder  : str = field_from_dict()
    onlyTopBorder     : str = field_from_dict()
    checkbox          : str = field_from_dict()
    toggleBtnBasic    : str = field_from_dict()
    formBorder        : str = field_from_dict()
    warnText          : str = field_from_dict()
    statusText        : str = field_from_dict()
    errorText         : str = field_from_dict()
    buttonList        : str = field_from_dict()
    dropDownBtn       : str = field_from_dict()
    checkbox          : str = field_from_dict()
    basic             : str = field_from_dict()
    linkStyle         : str = field_from_dict()
    iconBtn           : str = field_from_dict()
