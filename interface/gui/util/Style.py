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

from util.Path import getProjectRoot
from config.ConfigPath import StyleDataPath
from util.ConfigParser import StyleParser


basedir = getProjectRoot()

# reading data from toml files
color = toml.load(os.path.join (basedir, StyleDataPath.currentColor))
fontSize = toml.load(os.path.join (basedir, StyleDataPath.currentFontSize))
dimension = toml.load(os.path.join(basedir, StyleDataPath.dimension))
fontFamily  = toml.load(os.path.join (basedir, StyleDataPath.fontFamily))



# parse toml files to dataclass object
Color = StyleParser.ColorData.from_dict(color["colors"])
FontSize = StyleParser.FontSizeData.from_dict(
    fontSize["fontSizes"])
Dimension = StyleParser.DimensionData.from_dict(
    dimension["dimension"])
StyleSheet = StyleParser.StyleSheet.from_dict(
    color["styleSheet"])
Asset = StyleParser.Asset.from_dict(color["asset"])
FileTableDimension = StyleParser.FileTableDimension.from_dict(
    dimension["filetable"]["dimension"])
FontFamily = StyleParser.FontFamilyData.from_dict(fontFamily ["fontFamily"])
FontSource = StyleParser.FontSource.from_dict(fontFamily ["fontSource"])


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
                    
    ButtonInactive = f"background-color:{Color.LOW_CONTRAST};\
                    color:white;\
                    border-radius:5;\
                    font-size:{FontSize.BTN}"
                    
