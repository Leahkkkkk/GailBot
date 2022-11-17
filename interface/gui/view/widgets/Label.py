'''
File: Label.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 1:44:09 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: implement a label widget with customized style
'''
import os
import logging


from util.Style import Color,  FontFamily, FontSource

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
        font   = FontFamily.OTHER, 
        color  =  Color.MAIN_TEXT, 
        others = None, 
        link   = False,
        *args, 
        **kwargs
    ): 
        """initialize label class"""
        super().__init__(*args, **kwargs)
        self.setText(text)
        
        if font == FontFamily.MAIN:
            self.loadHeaderFont()
        elif font == FontFamily.CLOCK:
            self.loadClockFont()
        if link:
            self.setOpenExternalLinks(True)
            
        self.setStyleSheet(f"font-size: {size};" 
                           f"padding:0;" 
                           f"color:{color};"
                           f"background-color:none;"
                           f"{others};")
       
        
    def loadHeaderFont(self):
        """loads font for header label (since it's not default)"""
        id = QFontDatabase.addApplicationFont(os.path.join
                                                   (Path.getProjectRoot(), 
                                                    FontSource.headerFont))
        if id < 0 : logging.warn("Font cannot be loaded")
        Raleway =  QFontDatabase.applicationFontFamilies(id)
        self.setFont(QFont(Raleway[0], weight=800))
    
    def loadClockFont(self):
        id = QFontDatabase.addApplicationFont(os.path.join (Path.getProjectRoot(),
                                                            FontSource.clockFont))
        if id < 0 : logging.warn("Font cannot be loaded")
        Cockfont =  QFontDatabase.applicationFontFamilies(id)
        self.setFont(QFont(Cockfont[0], weight=600))

    def changeText(self, text):
        """ changes the current text
        Args: text (str): text to set current value to
        """
        self.setText(text)