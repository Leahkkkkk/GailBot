'''
File: Label.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 1:44:09 pm
Modified By:  Siara Small  & Vivian Li
-----
'''
import os
import logging

from view.style.styleValues import FontFamily

from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont, QFontDatabase
from util import Path


class Label(QLabel):
    """ Label widget used to display text 
    
    Args:
        text(str): text content
        size(str): font size stored  in string, unit is pixel
        font(str): font family 
        color(str, optional): color of the font, Defaults to Black
        others(str, optional): other styles, Defaults to None
    """
    def __init__(
        self, 
        text:str, 
        size:str, 
        font = FontFamily.OTHER, 
        color = "Black", 
        others = None, 
        link = False,
        *args, 
        **kwargs
    ): 
        """initialize label class"""
        super().__init__(*args, **kwargs)
        self.setText(text)
        
        self.setStyleSheet(f"font-size: {size};" 
                           f"padding:0;" 
                           f"color:{color};"
                           f"{others}")
        if font == FontFamily.MAIN:
            self.loadHeaderFont()
        if link:
            self.setOpenExternalLinks(True)
        
    def loadHeaderFont(self):
        """load font for header label (since it's not default)"""
        id = QFontDatabase.addApplicationFont(os.path.join
                                                   (Path.getProjectRoot(), 
                                                    "view/asset/Raleway.ttf"))
        if id < 0 : logging.warn("font cannot be loaded")
        Raleway =  QFontDatabase.applicationFontFamilies(id)
        self.setFont(QFont(Raleway[0], weight=800))