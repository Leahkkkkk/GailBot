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
import os
from util.SytemSet import SysImage
from util import Path
from PyQt6.QtCore import  Qt
from PyQt6.QtGui import (
    QBrush, 
    QColor, 
    QPalette,
    QImage,
    QTransform
)
from PyQt6.QtWidgets import QWidget

class Background(QBrush):
    """ a Qbrush object that craeates a white background """
    def __init__(self,color, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setColor(QColor(color))
        self.setStyle(Qt.BrushStyle.SolidPattern) 



def initBackground(widget:QWidget, color="#FFFFFF"):
    """ make the widget background as white """
    widget.setAutoFillBackground(True)
    bg = Background(color)
    palette = widget.palette()
    palette.setBrush(QPalette.ColorRole.Window, bg)
    widget.setPalette(palette)


def initImgBackground(widget:QWidget, background: str = SysImage.homeBackground):
    widget.setAutoFillBackground(True)
    palette = widget.palette()
    brush = QBrush()
    
    brush.setTextureImage(QImage(os.path.join(Path.getProjectRoot(), 
                                      f"view/asset/{background}")))
    backgroundTransform = QTransform()
    brush.setTransform(backgroundTransform.scale(1,1))
    palette.setBrush(QPalette.ColorRole.Window, brush) 
    widget.setPalette(palette)