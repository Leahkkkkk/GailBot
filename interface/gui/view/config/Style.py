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
import toml

from config_frontend.ConfigPath import StyleDataPath, FRONTEND_CONFIG_ROOT
from .interface import StyleParser

# reading data from toml files
color      = toml.load(os.path.join (FRONTEND_CONFIG_ROOT, StyleDataPath.currentColor))
fontSize   = toml.load(os.path.join (FRONTEND_CONFIG_ROOT, StyleDataPath.currentFontSize))
dimension  = toml.load(os.path.join(FRONTEND_CONFIG_ROOT, StyleDataPath.dimension))
fontFamily = toml.load(os.path.join (FRONTEND_CONFIG_ROOT, StyleDataPath.fontFamily))

# parse toml files to dataclass object
Color              = StyleParser.ColorData.from_dict(color["colors"])
FontSize           = StyleParser.FontSizeData.from_dict(fontSize["fontSizes"])
Dimension          = StyleParser.DimensionData.from_dict(dimension["dimension"])
StyleSheet         = StyleParser.StyleSheet.from_dict(color["styleSheet"])
Asset              = StyleParser.Asset.from_dict(color["asset"])
FileTableDimension = StyleParser.FileTableDimension.from_dict(dimension["filetable"]["dimension"])
FontFamily         = StyleParser.FontFamilyData.from_dict(fontFamily ["fontFamily"])
FontSource         = StyleParser.FontSource.from_dict(fontFamily ["fontSource"])

@dataclass
class buttonStyle:
    '''class holding style values for buttons, allowing for buttons to toggle 
    between active style and functionality and inactive style and functionality'''
    BASE = "background-color:#fff;\
            border:none;"
    
    ButtonActive = f"background-color:{Color.SECONDARY_BUTTON};\
                    color:white;\
                    border-radius:5;\
                    font-size:{FontSize.BTN}"
                    
    ButtonInactive = f"background-color:{Color.LOW_CONTRAST2};\
                    color:white;\
                    border-radius:5;\
                    font-size:{FontSize.BTN}"
                    



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
    