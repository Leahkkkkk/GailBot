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

from view.style.styleValues import FontSize, Dimension, Color
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
    """ a rusable button widget with colored background and white button text

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
        fontsize=FontSize.BTN, 
        other="",
        borderRadius=5,
        *args, 
        **kwargs
    ):
        """"" define and initialize class for colored button """""
        super().__init__(*args, **kwargs)
        self.setText(label)
        self.setStyleSheet(f"background-color:{color};"
                           f"color:#fff;"
                           f"border-radius:{borderRadius};"
                           f"padding:1;"
                           f"font-size:{fontsize};"
                           f"{other}")
        self.setMaximumSize(Dimension.BGBUTTON)
      
        
class BorderBtn(QPushButton):
    """ a rusable button widget with colored border and text 
        and white background

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
        fontsize=FontSize.BTN, 
        *args, 
        **kwargs
    ):
        """"define and initialize class for border button"""
        super().__init__(*args, **kwargs)
    
        self.setText(label)
        self.setStyleSheet(f"border: 1px solid {color};"
                           f"color:{color};"
                           f"border-radius:5;"
                           f"padding:1;"
                           f"font-size:{fontsize}")
        self.setMaximumSize(Dimension.BGBUTTON)


""" TODO: use a button icon instead of unicode, 
          add style 
"""
class ToggleBtn(QPushButton):
    """ A toggle button that display different lable when being toggled 
    
    Args:
        label(tuple(str), optional): text being displayed on button
    """
    def __init__(
        self, 
        label: tuple = ("right.png", "down.png"), 
        text = "", 
        state= False, 
        minHeight = 30,
        *args, 
        **kwargs):
        super().__init__(*args, **kwargs)
        self.text = text
        self.setText(self.text)
        self.rightIcon = QIcon(os.path.join(Path.getProjectRoot(), f"view/asset/{label[0]}"))
        self.downIcon = QIcon(os.path.join(Path.getProjectRoot(), f"view/asset/{label[1]}"))
        self.setMinimumSize(QSize(500, minHeight))
        self.setMaximumSize(QSize(700, minHeight))
        self.setCheckable(True)
        self.state = state
        self.clicked.connect(self._changeSymbol)
        self.setStyleSheet("background-color:#fff;border:none")
        # self.setContentsMargins(0,0,0,0)
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
            self.onOffBtn = QPushButton("ON")
        else:
            self.onOffBtn = QPushButton("OFF")
        self.onOffBtn.setMaximumSize(40, 100)
    
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
            self.onOffBtn.setText("OFF")
        else:
            self.state = True 
            self.onOffBtn.setText("ON")

    def value(self):
        """access state of on-off select"""
        return self.state


class iconBtn(QPushButton):
    """ A button with icon """
    def __init__(self, icon:str, label:str=None,*args, **kwargs):
      super().__init__(*args, **kwargs)
      icon = QIcon(os.path.join(Path.getProjectRoot(), f"view/asset/{icon}"))
      self.setIcon(icon)
      self.setObjectName("iconButton")
      if label:
          self.setText(label)
  
      
class dropDownButton(QWidget):
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
                              "margin-top:0px;border-radius:0px;padding:5px")
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


class buttonList(QWidget):
    def __init__(self, labels: list, btnFuns:list = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.btnList = []
        self.layout  = QVBoxLayout(self)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        
        for i in range(len(labels)):
            newButton = ColoredBtn(labels[i],
                                   Color.BLUEMEDIUM, 
                                   FontSize.SMALL,
                                    "margin-top:0px;border-radius:0px;border:1px solid #fff; padding:3px 0px")
            self.btnList.append(newButton)
            if btnFuns:
                self.btnList[i].clicked.connect(btnFuns[i])
            self.layout.addWidget(newButton)