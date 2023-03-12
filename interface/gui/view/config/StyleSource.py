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
from config_frontend.ConfigPath import StyleDataPath

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
    
    
    