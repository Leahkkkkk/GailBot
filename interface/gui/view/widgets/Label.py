from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont, QFontDatabase
from util import Path
import os
import logging
from view.style.style import FontFamily

""" 
Label widget 
param:
    @text: text content
    @size: font size
    @font: font family 
    @color: font color
"""
class Label(QLabel):
    def __init__(self, text:str, size:str, 
                 font:str, color = "Black", 
                 others = "",
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setText(text)
        
        self.setStyleSheet(f"font-size: {size};" 
                           f"padding:0;" 
                           f"color:{color};"
                           f"{others}")
        if font == FontFamily.MAIN:
            self._load_header_font()
        
    def _load_header_font(self):
        id = QFontDatabase.addApplicationFont(os.path.join
                                                   (Path.get_project_root(), 
                                                    "view/asset/Raleway.ttf"))
        if id < 0 : logging.warn("font cannot be loaded")
        Raleway =  QFontDatabase.applicationFontFamilies(id)
        self.setFont(QFont(Raleway[0], weight=800))