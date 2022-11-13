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
from util.Style import Color, Asset, Dimension, GetDynamicAsset
from view.widgets import Image
from util import Path
from PyQt6.QtCore import  Qt
from PyQt6.QtGui import (
    QBrush, 
    QColor, 
    QPalette,
    QImage,
    QTransform
)
from PyQt6.QtWidgets import QWidget, QVBoxLayout


class Background(QBrush):
    """ a QBrush object that creates a white background """
    def __init__(self,color, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setColor(QColor(color))
        self.setStyle(Qt.BrushStyle.SolidPattern) 


def _initBackground(widget:QWidget, color=Color.MAIN_BACKRGOUND):
    """ make the widget background as white """
    widget.setAutoFillBackground(True)
    bg = Background(color)
    palette = widget.palette()
    palette.setBrush(QPalette.ColorRole.Window, bg)
    widget.setPalette(palette)


def _initImgBackground(widget:QWidget, background: str = Asset.homeBackground):
    """  initialize the image background for a widget
    Args:
    widget (QWidget): a QWidget object 
    background (str): the background image name
    """
    widget.setAutoFillBackground(True)
    palette = widget.palette()
    brush = QBrush()
    
    brush.setTextureImage(QImage(os.path.join(Path.getProjectRoot(), 
                                      f"view/asset/{background}")))
    backgroundTransform = QTransform()
    brush.setTransform(backgroundTransform.scale(1,1))
    palette.setBrush(QPalette.ColorRole.Window, brush) 
    widget.setPalette(palette)
    
def initHomePageBackground(widget:QWidget):
    """initialize the home page background with image"""
    Asset  = GetDynamicAsset()
    _initImgBackground(widget, Asset.homeBackground)

def initSubpageBackgorund(widget:QWidget):
    """ initialize the sub pages background with image"""
    Asset  = GetDynamicAsset()
    _initImgBackground(widget, Asset.subPageBackground)

def initSideBarBackground(widget:QWidget):
    """ initialize the side bar background with image"""
    Asset  = GetDynamicAsset()
    _initImgBackground(widget, Asset.sideBarBackground)
    
def initPrimaryColorBackground(widget:QWidget):
    """ fill the widget with primary color background"""
    _initBackground(widget, Color.MAIN_BACKRGOUND)

def initSecondaryColorBackground(widget:QWidget):
    """ fill the widget with secondary color background"""
    _initBackground(widget, Color.SUB_BACKGROUND)


def addLogo(layout: QVBoxLayout):
    """ add the logo to the top left corner on the layout """
    logo = Image.Image(
        Asset.hilLabLogo, (Dimension.LOGO_WIDTH, Dimension.LOGO_HEIGHT))
    layout.addWidget(
        logo, alignment=Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignRight)
    logo.setContentsMargins(0,0,0,0)
    