import toml

from util import StyleParser

color = toml.load("config/color.toml")
dimension = toml.load("config/dimension.toml")

Color = StyleParser.ColorData.from_dict(color["colors"])
FontSize = StyleParser.FontSizeData.from_dict(dimension["fontSizes"])
Dimension = StyleParser.DimensionData.from_dict(dimension["dimension"])
StyleSheet = StyleParser.StyleSheet.from_dict(color["styleSheet"])
Asset = StyleParser.Asset.from_dict(color["asset"])
FileTableDimension = StyleParser.FileTableDimension.from_dict(dimension["filetable"]["dimension"])
FontFamily = StyleParser.FontFamilyData.from_dict(dimension["fontFamily"])
