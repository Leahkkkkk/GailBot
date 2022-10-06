'''
File: Background.py
Project: GailBot GUI
File Created: Thursday, 6th October 2022 12:50:59 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 12:59:28 pm
Modified By:  Siara Small  & Vivian Li
-----
'''

from PyQt6.QtCore import  Qt
from PyQt6.QtGui import (
    QBrush, 
    QColor, 
    QPalette
)
from PyQt6.QtWidgets import QWidget

class Background(QBrush):
    """ a Qbrush object that craeates a white background """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setColor(QColor("#FFFFFF"))
        self.setStyle(Qt.BrushStyle.SolidPattern) 

def initBackground(widget:QWidget):
    """ make the widget background as white """
    widget.setAutoFillBackground(True)
    bg = Background()
    palette = widget.palette()
    palette.setBrush(QPalette.ColorRole.Window, bg)
    widget.setPalette(palette)