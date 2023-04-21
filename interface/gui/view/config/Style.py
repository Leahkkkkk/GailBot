'''
File: Style.py
Project: GailBot GUI
File Created: Saturday, 5th November 2022 6:16:59 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Sunday, 6th November 2022 1:13:58 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: contain instances of dataclass with style data 
'''
import os 
from dataclasses import dataclass
from typing import Dict
import toml

from config_frontend.ConfigPath import StyleDataPath, FRONTEND_CONFIG_ROOT
from .interface import StyleParser
from view.Signals import GlobalStyleSignal
from PyQt6.QtCore import QObject, pyqtSignal

class StyleSignals(QObject):
    changeColor = pyqtSignal()
    changeFont  = pyqtSignal()

# reading data from toml files
color      = toml.load(os.path.join (FRONTEND_CONFIG_ROOT, StyleDataPath.currentColor))
fontSize   = toml.load(os.path.join (FRONTEND_CONFIG_ROOT, StyleDataPath.currentFontSize))
dimension  = toml.load(os.path.join(FRONTEND_CONFIG_ROOT, StyleDataPath.dimension))
fontFamily = toml.load(os.path.join (FRONTEND_CONFIG_ROOT, StyleDataPath.fontFamily))

lightcolor = toml.load(os.path.join(FRONTEND_CONFIG_ROOT, StyleDataPath.lightColor))
darkcolor = toml.load(os.path.join(FRONTEND_CONFIG_ROOT, StyleDataPath.darkColor))


smallfont   = toml.load(os.path.join(FRONTEND_CONFIG_ROOT, StyleDataPath.smallFontSize))
mediumfont  = toml.load(os.path.join(FRONTEND_CONFIG_ROOT, StyleDataPath.mediumFontSize))
largfont   = toml.load(os.path.join(FRONTEND_CONFIG_ROOT, StyleDataPath.largeFontSize))


# parse toml files to dataclass object
Color              = StyleParser.ColorData.from_dict(color["colors"])
FontSize           = StyleParser.FontSizeData.from_dict(fontSize["fontSizes"])
Dimension          = StyleParser.DimensionData.from_dict(dimension["dimension"])
StyleSheet         = StyleParser.StyleSheet.from_dict(color["styleSheet"])
Asset              = StyleParser.Asset.from_dict(color["asset"])
FileTableDimension = StyleParser.FileTableDimension.from_dict(dimension["filetable"]["dimension"])
FontFamily         = StyleParser.FontFamilyData.from_dict(fontFamily ["fontFamily"])
FontSource         = StyleParser.FontSource.from_dict(fontFamily ["fontSource"])

COLOR_DICT : Dict[str, StyleParser.ColorData] = \
    {"Light Mode": StyleParser.ColorData.from_dict(lightcolor["colors"]), 
     "Dark Mode" : StyleParser.ColorData.from_dict(darkcolor["colors"]),
     "Default": Color}

FONT_DICT : Dict[str, StyleParser.FontSizeData] = \
    { "Small" : StyleParser.FontSizeData.from_dict(smallfont["fontSizes"]), 
      "Large" : StyleParser.FontSizeData.from_dict(largfont["fontSizes"]),
      "Medium": StyleParser.FontSizeData.from_dict(mediumfont["fontSizes"]),
      "Default": FontSize}

ASSET_DICT : Dict[str, StyleParser.Asset] = \
    {"Light Mode" : StyleParser.Asset.from_dict(lightcolor["asset"]),
     "Dark Mode"  : StyleParser.Asset.from_dict(darkcolor["asset"]),
     "Default": Asset}

STYLE_DICT : Dict[str, StyleParser.StyleSheet] = \
    {"Light Mode" : StyleParser.StyleSheet.from_dict(lightcolor["styleSheet"]),
     "Dark Mode"  : StyleParser.StyleSheet.from_dict(darkcolor["styleSheet"]),
     "Default": StyleSheet}

@dataclass
class buttonStyle:
    '''class holding style values for buttons, allowing for buttons to toggle 
    between active style and functionality and inactive style and functionality'''
    def __init__(self, color: StyleParser.ColorData):
        self.BASE = "background-color:#fff;\
                border:none;"
        
        self.ButtonActive = f"background-color:{color.SECONDARY_BUTTON};\
                        color:white;\
                        border-radius:5;\
                        font-size:{FontSize.BTN};"
                        
        self.ButtonInactive = f"background-color:{color.LOW_CONTRAST2};\
                        color:white;\
                        border-radius:5;\
                        font-size:{FontSize.BTN};"
@dataclass
class StyleSource:
    """ stores file paths to different style theme"""
    CURRENT_COLOR       = StyleDataPath.currentColor
    CURRENT_FONTSIZE    = StyleDataPath.currentFontSize


""" a search table with all style choices and the path to the source"""
StyleTable = {
    "Dark Mode"     :   StyleDataPath.darkColor,
    "Light Mode"    :   StyleDataPath.lightColor,
    "Small"         :   StyleDataPath.smallFontSize,
    "Large"         :   StyleDataPath.largeFontSize,
    "Medium"        :   StyleDataPath.mediumFontSize 
}

class StyleController():
    def __init__(self) -> None:
        self.StyleSheet: StyleParser.StyleSheet = STYLE_DICT["Default"]
        self.Color: StyleParser.ColorData  = COLOR_DICT["Default"]
        self.Asset: StyleParser.Asset = ASSET_DICT["Default"]
        self.FontSize : StyleParser.FontSizeData = FONT_DICT["Default"]
        self.Dimension = Dimension
        self.FontFamily = FontFamily 
        self.buttonStyle = buttonStyle(self.Color)
        GlobalStyleSignal.changeColor.connect(self.colorchange)
        GlobalStyleSignal.changeFont.connect(self.fontsizeChange)
        
        self.signal = StyleSignals()

    ###### style control
    def colorchange(self, colormode):
        global StyleSheet
        global Color
        global Asset
        self.StyleSheet = STYLE_DICT[colormode]
        self.Color = COLOR_DICT[colormode]
        self.Asset = ASSET_DICT[colormode]
        self.signal.changeColor.emit()
        self.buttonStyle = buttonStyle(self.Color)
    
    def fontsizeChange(self, fontmode):
        self.FontSize = FONT_DICT[fontmode]
        self.signal.changeFont.emit()

#### top level style controller that is responsible to change the color
STYLE_DATA = StyleController()