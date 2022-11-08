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


import toml
from util import StyleParser
from util.StyleSource import StyleSource

color = toml.load(StyleSource.CURRENT_COLOR)
fontSize = toml.load(StyleSource.CURRENT_FONTSIZE)
dimension = toml.load("config/style/dimension.toml")
fontfamily = toml.load("config/style/font/fontFamily.toml")
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
FontFamily = StyleParser.FontFamilyData.from_dict(fontfamily["fontFamily"])
FontSource = StyleParser.FontSource.from_dict(fontfamily["fontSource"])

