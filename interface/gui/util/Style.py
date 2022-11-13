'''
File: Style.py
Project: GailBot GUI
File Created: Saturday, 5th November 2022 6:16:59 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Sunday, 6th November 2022 1:13:58 pm
Modified By:  Siara Small  & Vivian Li
-----
'''

from dataclasses import dataclass
import toml
from util.StyleSource import StyleSource
from util.ConfigParser import StyleParser
print("reload settings")
# reading data from toml files
color = toml.load(StyleSource.CURRENT_COLOR)
fontSize = toml.load(StyleSource.CURRENT_FONTSIZE)
dimension = toml.load("config/style/dimension.toml")
fontfamily = toml.load("config/style/font/fontFamily.toml")
Color = StyleParser.ColorData.from_dict(color["colors"])

# parse toml files to dataclass object
FontSize = StyleParser.FontSizeData.from_dict(
    fontSize["fontSizes"])
Dimension = StyleParser.DimensionData.from_dict(
    dimension["dimension"])
StyleSheet = StyleParser.StyleSheet.from_dict(
    color["styleSheet"])
Asset = StyleParser.Asset.from_dict(color["asset"])
FileTableDimension = StyleParser.FileTableDimension.from_dict(
    dimension["filetable"]["dimension"])
FontFamily = StyleParser.FontFamilyData.from_dict(fontfamily["fontFamily"])
FontSource = StyleParser.FontSource.from_dict(fontfamily["fontSource"])


@dataclass
class buttonStyle:
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
                    
                    
def GetDynamicAsset() -> StyleParser.Asset : 
   print("reload")
   colordy = toml.load(StyleSource.CURRENT_COLOR)
   return StyleParser.Asset.from_dict(colordy["asset"]) 