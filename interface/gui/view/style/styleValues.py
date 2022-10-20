'''
File: style.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 11:14:51 am
Modified By:  Siara Small  & Vivian Li
-----
'''

from dataclasses import dataclass

from PyQt6.QtCore import QSize, QRect


dataclass
class Color:
    """ store all colors, type string """
    GREEN = "#6E9B87"
    ORANGE = "#EE6C4D"
    BLUEWHITE = "#F0F6F9"
    BLUELIGHT = "#D2E4EE"
    BLUEMEDIUM = "#3D4A80"
    BLUEDARK = "#293241"
    GREYLIGHT = "#EBEBEB"
    GREYMEDIUM1 = "#91969D" 
    GREYMEDIUM2 = "#767C85"
    GREYDARK = "#545B67"
    BORDERGREY ="#797979"

dataclass
class FontSize:
    """ store all font size, unit px, type string"""
    BODY = "13px"
    TEXT_FIELD = "12px"
    SMALL="11px"
    LINK = "15px"
    HEADER1 = "32px"
    HEADER2  = "24px"
    HEADER3  = "18px"
    TABLE_ROW = "13px"
    DESCRIPTION = "12px"
    INSTRUCTION_CAPTION = "14px"
    BTN = "14px"

dataclass
class Dimension:
    """ store all dimention, unit px """
    WIN_MAXSIZE = QSize(1100, 900)
    MARGIN_HORIZONTAL = "20px" 
    MARGIN_VERTICAL = "5px"
    BGBUTTON = QSize(140, 40)
    RBUTTON = QSize(130, 40)
    MEDIUMBUTTON = QSize(100, 30)
    ICONBUTTON = QSize(50, 50)
    SMALLICONBUTTON = QSize(30,30)
    INPUTFIELD = QSize(200, 23)
    CONSOLE = QSize(1000, 300)
    STATUSBAR = QSize(900, 30)
    ACTION = QSize(100,35)
    MEDIUMDIALOG = QSize(400,110)
    LARGEDIALOG = QSize(400, 600)

dataclass
class Geometry:
    """ store all geomery, type QRect """
    CONSOLE = QRect(300, 700, 1000, 300)
    MENUBAR = QRect(0, 0, 900, 37)
    
    
dataclass   
class FontFamily:
    """ store all font familt, type string """
    MAIN = "Raleway"
    OTHER = "Helvetica"




    
        
        