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
from typing import Tuple
from view.config.Style import STYLE_DATA 
from view.widgets.Image import Image
from config_frontend import PROJECT_ROOT

from PyQt6.QtCore import  Qt
from PyQt6.QtGui import (
    QBrush, 
    QColor, 
    QPalette,
    QPixmap,
    QResizeEvent
)
from PyQt6.QtWidgets import QWidget, QVBoxLayout



def initBackground(widget:QWidget, color = STYLE_DATA.Color.MAIN_BACKGROUND):
    """ paint the widget's background with a solid color

    Args:
        widget (QWidget): the widget 
        color (str, optional): the color of the background. 
                            Defaults to STYLE_DATA.Color.MAIN_BACKGROUND.
    """
    widget.setAutoFillBackground(True)
    bg = Background(color)
    palette = widget.palette()
    palette.setBrush(QPalette.ColorRole.Window, bg)
    widget.setPalette(palette)

def initHomePageBackground(widget:QWidget):
    """initialize the home page background with image"""
    _initImgBackground(widget, STYLE_DATA.Asset.homeBackground)


def initSubPageBackground(widget:QWidget):
    """ initialize the sub pages background with image"""
    _initImgBackground(widget, STYLE_DATA.Asset.subPageBackground)


def initSideBarBackground(widget:QWidget):
    """ initialize the side bar background with image"""
    _initImgBackground(widget, STYLE_DATA.Asset.sideBarBackground)

    
def initPrimaryColorBackground(widget:QWidget):
    """ fill the widget with primary color background"""
    initBackground(widget, STYLE_DATA.Color.MAIN_BACKGROUND)

def initSecondaryColorBackground(widget:QWidget):
    """ fill the widget with secondary color background"""
    initBackground(widget, STYLE_DATA.Color.SUB_BACKGROUND)

def addLogo(layout: QVBoxLayout):
    """ add the logo to the top left corner on the layout """
    logo = Image(
        STYLE_DATA.Asset.hilLabLogo, (STYLE_DATA.Dimension.LOGO_WIDTH, STYLE_DATA.Dimension.LOGO_HEIGHT))
    layout.addWidget(
        logo, alignment=Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignRight)
    logo.setContentsMargins(0,0,0,0)

def getLogo() -> Tuple[QWidget, Qt.AlignmentFlag]:
    """ get the logo widget  """
    logo = Image(
        STYLE_DATA.Asset.hilLabLogo, (STYLE_DATA.Dimension.LOGO_WIDTH, STYLE_DATA.Dimension.LOGO_HEIGHT))
    logo.setContentsMargins(0,0,0,0)
    return logo
 
def _resizeEvent(widget: QWidget, event: QResizeEvent, img: str):
    """ scale the background image when the window is resized"""
    size = event.size()
    temp = QPixmap(os.path.join(PROJECT_ROOT, img))
    pixmap = temp.scaled(
        size, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
    # Set the scaled image to the QLabel
    palette = widget.palette()
    brush = QBrush()
    brush.setTexture(pixmap)
    palette.setBrush(QPalette.ColorRole.Window, brush)
    widget.setPalette(palette)
    

def _initImgBackground(widget:QWidget, background: str = STYLE_DATA.Asset.homeBackground):
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
        size, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
    brush = QBrush()
    brush.setTexture(pixmap)
    palette.setBrush(QPalette.ColorRole.Window, brush) 
    widget.setPalette(palette)
    widget.resizeEvent = lambda event : _resizeEvent(widget, event, background)
    
class Background(QBrush):
    def __init__(self,color, *args, **kwargs) -> None:
        """a QBrush object that creates a background 

        Args:
            color (str): the color of the background
        """
        super().__init__(*args, **kwargs)
        self.setColor(QColor(color))
        self.setStyle(Qt.BrushStyle.SolidPattern) 