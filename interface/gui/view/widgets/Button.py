'''
File: Button.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 1:43:41 pm
Modified By:  Siara Small  & Vivian Li
-----
'''
import os
from typing import List
from util.Config import FontSize, Dimension, Color, StyleSheet
from util.Config import BtnText as Text
from util.SytemSet import SysColor, SysFontSize
from util.StyleGenerator import colorScale
from view.style.Background import initBackground
from util import Path

from PyQt6.QtWidgets import (
    QPushButton, 
    QWidget, 
    QHBoxLayout, 
    QVBoxLayout,
    QLabel
)

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon

class ColoredBtn(QPushButton):
    """ a button widget with colored background and white button text

    Args:
        label (str): button text
        color (str): hex color in string 
        fontsize (str, optional): represented in string, unit is pixel 
                                  Defaults to FontSize.BTN.
    """
    def __init__(
        self,
        label:str, 
        color:str, 
        fontsize:str = FontSize.BTN , 
        other:str = None,
        borderRadius:int =5,
        *args, 
        **kwargs
    ):
        """"" define and initialize class for colored button """""
        super().__init__(*args, **kwargs)
        self.setText(label)
        self.origColor = color
        self.pressColor = colorScale(color, 0.7)
        self.borderRadius = borderRadius
        self.fontsize = fontsize
        self.other = other
        self.setFixedSize(Dimension.BTNWIDTH, Dimension.BTNHEIGHT)
        self.defaultStyle = f"border-radius:{self.borderRadius};"\
                            f"padding:1;"\
                            f"color:#fff;"\
                            f"font-size:{self.fontsize};"\
                            f"{self.other};"
        self.pressed.connect(self._pressStyle)
        self.released.connect(self._releaseStyle)
        self._releaseStyle()
    
    def _pressStyle(self):
        """ set the button color to be darker  """
        self.setStyleSheet(self.defaultStyle + 
                           f"background-color:{self.pressColor}")
    def _releaseStyle(self):
        """ set the button color to original color """
        self.setStyleSheet(self.defaultStyle + 
                           f"background-color:{self.origColor};")
        
class BorderBtn(QPushButton):
    """ a button widget with colored border and text 
        and white background

    Args:
        label (str): button text
        color (str): hex color in string 
        fontsize (str, optional): represented in string, unit is pixel 
                                  Defaults to FontSize.BTN 
        borderRadius (int): botton border
        other (str): other additional style
    """
    def __init__(
        self, 
        label:str, 
        color:str,
        fontSize:str = FontSize.BTN, 
        borderRadius:int = 5,
        other:str = None,
        *args, 
        **kwargs
    ):
        """"define and initialize class for border button"""
        super().__init__(*args, **kwargs)
    
        self.setText(label)
        self.color = color 
        self.borderRadius = borderRadius
        self.fontSize = fontSize
        self.other = other 
        self.setFixedSize(Dimension.BTNWIDTH, Dimension.BTNHEIGHT)
        self.defaultStyle =f"border: 1px solid {self.color};"\
                           f"color:{self.color};"\
                           f"border-radius:{self.borderRadius};"\
                           f"padding:1;"\
                           f"font-size:{self.fontSize};"\
                           f"{self.other};"
        self.setDefaultStyle()
        

    def setDefaultStyle(self):
        self.setStyleSheet(self.defaultStyle)
    
    def setActiveStyle(self, color: str):
        self.setStyleSheet(self.defaultStyle + f"background-color:{color}")
    
        
    
class ToggleBtn(QPushButton):
    """ A toggle button that display different lable when being toggled 
    
    Args:
        label(tuple(str), optional): the name of the icon image being displayed
        text: the text next to the icon on the toggle lable
        sate: the initial state of the toggle bar, default to False
    """
    def __init__(
        self, 
        label: tuple = (Text.right, Text.down), 
        text:str = "", 
        state:bool = False, 
        *args, 
        **kwargs):
        super().__init__(*args, **kwargs)
        self.text = text
        self.setText(self.text)
        self.rightIcon = QIcon(os.path.join(
            Path.getProjectRoot(), 
            f"view/asset/{label[0]}"))
        self.downIcon = QIcon(os.path.join(
            Path.getProjectRoot(), 
            f"view/asset/{label[1]}"))
        # initBackground(self)
        self.setCheckable(True)
        self.clicked.connect(self._changeSymbol)
        self.state = state
        self._changeSymbol()
        self.update()
        self.show()

    def _changeSymbol(self):
        """ to change the button symbol """
        if self.state:
            self.setIcon(self.downIcon)
        else:
            self.setIcon(self.rightIcon)
        self.state = not self.state

    

class onOffButton(QWidget):
    """ a toggle button that displays "on" or "off" text while being toggled
    
    Args: 
        label(str): a line of text above the button 
        childWidget(QWidget, optional): contains the content that can be hidden
                                        or shown will the button is toggled
    """
    def __init__(
        self, 
        label: str, 
        state = True,
        *args, 
        **kwargs
    ) -> None:
        
        super().__init__(*args, **kwargs)
        self.label = label
        self.state = state
        self._initWidget()
        self._initLayout()
        self._connectSignal()
        
    def _initWidget(self):
        """initialize widgets for on-off select"""
        self.label =  QLabel(self.label)
        if self.state:
            self.onOffBtn = QPushButton(Text.on)
        else:
            self.onOffBtn = QPushButton(Text.off)
        self.onOffBtn.setMinimumSize(35, 25)
        self.onOffBtn.setMaximumSize(40, 30)
    
    def _initLayout(self):
        """initialize layout for on-off select"""
        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.onOffBtn, alignment=Qt.AlignmentFlag.AlignLeft) 
        
    def _connectSignal(self):
        """marked signal as clicked"""
        self.onOffBtn.clicked.connect(self._updateStatus)

    def _updateStatus(self):
        """update status of on-off select"""
        if self.state:
            self.state = False
            self.onOffBtn.setText(Text.off)
        else:
            self.state = True 
            self.onOffBtn.setText(Text.on)

    def value(self):
        """ access state of on-off select """
        return self.onOffBtn.text()
    
    def setText(self, text):
        if text == "ON":
            self.state = True 
            self.onOffBtn.setText(Text.on)
        else:
            self.state = False 
            self.onOffBtn.setText(Text.off)


class iconBtn(QPushButton):
    """ A button with icon
    icon (str): a string that indcate the icon file name
    label  (str, optional): the tex to be displayed on the icon 
    """
    def __init__(self, icon:str, label:str=None,*args, **kwargs):
      super().__init__(*args, **kwargs)
      icon = QIcon(os.path.join(Path.getProjectRoot(), f"view/asset/{icon}"))
      self.setIcon(icon)
      self.setObjectName(Text.icon)
      if label:
          self.setText(label)
  
   
   
   
   
""" NOTE: currently unused in the interface  """  
class dropDownButton(QWidget):
    """ a dropdown button widget, when the button is clicked,
        there is a dropdown of a list of buttons
    """
    def __init__(
        self, 
        label:str, 
        buttons:list, 
        btnFuns:list = None,
        *args, 
        **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.buttonList = buttonList(buttons,btnFuns) 
        self.btn = ColoredBtn(f"▶ {label}", 
                              Color.BLUEMEDIUM,
                              FontSize.SMALL, 
                              StyleSheet.dropDownBtn)
        self.label = label
        self.hideView = True 
        self.setFixedWidth(130)
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.btn)
        self.layout.addWidget(self.buttonList)
        self.buttonList.hide()
        self.btn.clicked.connect(self._toggle)

    
    def _toggle(self):
        if self.hideView == True:
            self.hideView = False
            self.buttonList.show()
            self.btn.setText(f"▼ {self.label}")
        else:
            self.hideView = True 
            self.buttonList.hide()
            self.btn.setText(f"▶ {self.label}")

""" NOTE: currently unused on the frontend interface """
class buttonList(QWidget):
    def __init__(
        self, 
        labels: list, 
        btnFuns: List[callable] = None, 
        *args, 
        **kwargs) -> None:
        """  a widget that implement a list of buttons

        Args:
            labels (list): a list of the button labels 
            btnFuns (list, optional): a list of functions triggered when button 
                                      is pressed
        """
        super().__init__(*args, **kwargs)
        self.btnList = []
        self.layout  = QVBoxLayout(self)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        
        for i in range(len(labels)):
            newButton = ColoredBtn(
                labels[i],
                Color.BLUEMEDIUM, 
                FontSize.SMALL,
                StyleSheet.buttonList)
            self.btnList.append(newButton)
            if btnFuns:
                self.btnList[i].clicked.connect(btnFuns[i])
            self.layout.addWidget(newButton)