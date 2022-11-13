'''
File: StyleSource.py
Project: GailBot GUI
File Created: Sunday, 6th November 2022 10:40:00 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Sunday, 6th November 2022 10:42:36 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: contains instances of dataclasses with style data
'''


from dataclasses import dataclass
from config.ConfigPath import StyleDataPath

@dataclass
class StyleSource:
    """ stores file paths to different style theme"""
    DARK_COLOR          = "config/style/color/colorDark.toml"
    LIGHT_COLOR         = "config/style/color/colorLight.toml"
    CURRENT_COLOR       = "config/style/color/color.toml"
    L_FONTSIZE          = "config/style/font/fontSizeL.toml"
    M_FONTSIZE          = "config/style/font/fontSizeM.toml"
    S_FONTSIZE          = "config/style/font/fontSizeM.toml"
    CURRENT_FONTSIZE    = "config/style/font/fontSize.toml"


""" a search table with all style choices and the path to the source"""
StyleTable = {
    "dark mode"     :   StyleDataPath.darkColor,
    "light mode"    :   StyleDataPath.lightColor,
    "default"       :   StyleDataPath.currentColor,
    "small"         :   StyleDataPath.smallFontSize,
    "large"         :   StyleDataPath.largeFontSize,
    "medium"        :   StyleDataPath.mediumFontSize 
}
    
    
    