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

from view.style.styleValues import FontSize, Dimension

from PyQt6.QtWidgets import (
    QPushButton, 
    QWidget, 
    QGridLayout, 
    QLabel
)
from PyQt6.QtCore import QSize

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
        *args, 
        **kwargs
    ):
        """"" define and initialize class for colored button """""
        super().__init__(*args, **kwargs)
        self.setText(label)
        self.setStyleSheet(f"background-color:{color};"
                           f"color:#fff;"
                           f"border-radius:5;"
                           f"padding:1;"
                           f"font-size:{fontsize};")
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
        self.setStyleSheet(f"border: 2px solid {color};"
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
    def __init__(self, label: tuple = ("▶", "▼"), text = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = label
        self.text = text
        self.setText(f"{self.label[0]}  {self.text}")
        self.setMinimumSize(QSize(500, 30))
        self.setMaximumSize(QSize(700, 30))
        self.setCheckable(True)
        self.clicked.connect(self._changeSymbol)
        self.update()
        self.show()

    def _changeSymbol(self):
        """ to change the button symbol """
        if self.isChecked():
            self.setText(f"{self.label[1]}  {self.text}")
        else:
            self.setText(f"{self.label[0]}  {self.text}")
    



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
        *args, 
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.label = label
        self.state = True
        self._initWidget()
        self._initLayout()
        self._connectSignal()
        
    def _initWidget(self):
        """initialize widgets for on-off select"""
        self.label =  QLabel(self.label)
        self.onOffBtn = QPushButton("ON")
        self.onOffBtn.setMaximumSize(40, 100)
    
    def _initLayout(self):
        """initialize layout for on-off select"""
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)
        self.layout.addWidget(self.label,0,0)
        self.layout.addWidget(self.onOffBtn,0,1) 
        
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