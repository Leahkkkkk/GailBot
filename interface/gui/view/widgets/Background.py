'''
File: Background.py
Project: GailBot GUI
File Created: Thursday, 6th October 2022 12:50:59 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 12:59:28 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: implement function for initialize background for different pages
'''
import os

from view.config.Style import Color, Asset, Dimension
from view.widgets import Image
from config_frontend import PROJECT_ROOT

from PyQt6.QtCore import  Qt, QEvent
from PyQt6.QtGui import (
    QBrush, 
    QColor, 
    QPalette,
    QPixmap,
    QResizeEvent
)
from PyQt6.QtWidgets import QWidget, QVBoxLayout

class Background(QBrush):
    """ a QBrush object that creates a white background """
    def __init__(self,color, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setColor(QColor(color))
        self.setStyle(Qt.BrushStyle.SolidPattern) 


def resizeEvent(widget: QWidget, event: QResizeEvent, img: str):
    size = event.size()
    temp = QPixmap(os.path.join(PROJECT_ROOT, img))
    pixmap = temp.scaled(
        size, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.FastTransformation)
    # Set the scaled image to the QLabel
    palette = widget.palette()
    brush = QBrush()
    brush.setTexture(pixmap)
    palette.setBrush(QPalette.ColorRole.Window, brush)
    widget.setPalette(palette)

def _initBackground(widget:QWidget, color=Color.MAIN_BACKGROUND):
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
    size = widget.size()
    temp = QPixmap(os.path.join(PROJECT_ROOT, background))

    pixmap = temp.scaled(
        size, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.FastTransformation)
    brush = QBrush()
    brush.setTexture(pixmap)
    palette.setBrush(QPalette.ColorRole.Window, brush) 
    widget.setPalette(palette)
    widget.resizeEvent = lambda event : resizeEvent(widget, event, background)
    
def initHomePageBackground(widget:QWidget):
    """initialize the home page background with image"""
    _initImgBackground(widget, Asset.homeBackground)

def initSubPageBackground(widget:QWidget):
    """ initialize the sub pages background with image"""
    _initImgBackground(widget, Asset.subPageBackground)

def initSideBarBackground(widget:QWidget):
    """ initialize the side bar background with image"""
    _initImgBackground(widget, Asset.sideBarBackground)
    
def initPrimaryColorBackground(widget:QWidget):
    """ fill the widget with primary color background"""
    _initBackground(widget, Color.MAIN_BACKGROUND)

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
 