'''
File: SettingForm.py
Project: GailBot GUI
File Created: Friday, 4th November 2022 1:01:27 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Friday, 4th November 2022 6:24:06 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: a form page widget that display a page with a form  that accept 
            user input 
'''
from typing import Dict 
from .Label import Label 
from .TextForm import TextForm
from .ScrollArea import ScrollArea
from .Background import initSecondaryColorBackground, initBackground
from ..config.Style import STYLE_DATA 
from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout,
    QScrollArea
)
from PyQt6.QtCore import Qt

center = Qt.AlignmentFlag.AlignHCenter

class SettingForm(QWidget):
    """ class for setting input form with title, caption, and form"""
    def __init__(self, 
                 header:str, 
                 formData: dict, 
                 caption: str = None, 
                 *args, 
                 **kwargs) -> None:
        """  initializes page
        Constructor Args:
            header (str): the header of the page 
            formData (dict): the form data 
            caption (str, optional): a short description of the form 
                                    Defaults to None.
        Public Functions: 
        1. setValue(self, values:dict)
        2. getValue(self) -> Dict[str, str]
        """
        super().__init__(*args, **kwargs)
        
        self.headerText = header 
        self.formData = formData
        self.START = caption
        self._initWidget()
        self._initLayout()
        self._connectSignal()
    
    def _connectSignal(self):
        STYLE_DATA.signal.changeColor.connect(self.colorChange)
        STYLE_DATA.signal.changeFont.connect(self.fontChange)

        
    def setValue(self, values:dict) -> None:
        """ public function to set the values in the form  """
        self.setForm.setValues(values)
    
    def getValue(self) -> Dict[str, str]:
        """ public function to get the values from the form """
        return self.setForm.getValue()

    def _initWidget(self):
        """ initializes the widgets """
        self.header = Label(
            self.headerText, STYLE_DATA.FontSize.HEADER2,STYLE_DATA.FontFamily.MAIN)
        if self.START:
            self.caption = Label(
                self.START, STYLE_DATA.FontSize.DESCRIPTION, STYLE_DATA.FontFamily.MAIN)
        self.setForm = TextForm(self.formData)
        self.setForm.setFixedWidth(STYLE_DATA.Dimension.FORMWIDTH)
        self.setForm.setFixedHeight(STYLE_DATA.Dimension.FORMMINHEIGHT)
    
    def _initLayout(self):
        """ initializes the layout"""
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.verticalLayout.addWidget(self.header, alignment = center)
        if self.START:
            self.verticalLayout.addWidget(self.caption, alignment = center )
        self.verticalLayout.addWidget(self.setForm, alignment = center)
        self.verticalLayout.addStretch()
        self.verticalLayout.setContentsMargins(0,0,0,0)
    
    def addWidget(self, widget: QWidget):
        self.setForm.addWidget(widget)

    def colorChange(self):
        initBackground(self.setForm, STYLE_DATA.Color.SUB_BACKGROUND)
    
    def fontChange(self):
        self.header.fontChange(STYLE_DATA.FontSize.HEADER2)
        self.caption.fontChange(STYLE_DATA.FontSize.DESCRIPTION)
        

    
        