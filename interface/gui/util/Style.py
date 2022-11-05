import toml

from util import StyleParser

config = toml.load("config/style.toml")

Color = StyleParser.ColorData.from_dict(config["colors"])
FontSize = StyleParser.FontSizeData.from_dict(config["fontSizes"])
Dimension = StyleParser.DimensionData.from_dict(config["dimension"])
StyleSheet = StyleParser.StyleSheet.from_dict(config["styleSheet"])
Asset = StyleParser.Asset.from_dict(config["asset"])
FileTableDimension = StyleParser.FileTableDimension.from_dict(config["filetable"]["dimension"])
FontFamily = StyleParser.FontFamilyData.from_dict(config["fontFamily"])
