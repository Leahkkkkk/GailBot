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

from view.widgets import Label,TextForm, ScrollArea
from view.widgets.Background import initSecondaryColorBackground
from ..config.Style import (
    FontFamily, 
    FontSize, 
    Dimension,
    Color
)
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
        self.captionText = caption
        self._initWidget()
        self._initLayout()

    def setValue(self, values:dict) -> None:
        """ public function to set the values in the form  """
        self.setForm.setValues(values)
    
    def getValue(self) -> Dict[str, str]:
        """ public function to get the values from the form """
        return self.setForm.getValue()

    def _initWidget(self):
        """ initializes the widgets """
        self.header = Label.Label(
            self.headerText, FontSize.HEADER2,FontFamily.MAIN)
        if self.captionText:
            self.caption = Label.Label(
                self.captionText, FontSize.DESCRIPTION, FontFamily.MAIN)
        self.setForm = TextForm.TextForm(self.formData)
        self.scroll = ScrollArea.ScrollArea()
        self.scroll.setWidgetResizable(False)
        self.scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setWidget(self.setForm)
        self.scroll.setFixedWidth(Dimension.FORMWIDTH)
        self.scroll.setFixedHeight(Dimension.FORMMINHEIGHT)
        initSecondaryColorBackground(self.scroll)
    
    def _initLayout(self):
        """ initializes the layout"""
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.verticalLayout.addWidget(self.header, alignment = center)
        if self.captionText:
            self.verticalLayout.addWidget(self.caption, alignment = center )
        self.verticalLayout.addWidget(self.scroll, alignment = center)
        self.verticalLayout.addStretch()
    
    def addWidget(self, widget: QWidget):
        self.setForm.addWidget(widget)
    
    def addWidgetTotheSide(self, widget: QWidget):
        self.setForm.addWidgetToSide(widget)

    
        