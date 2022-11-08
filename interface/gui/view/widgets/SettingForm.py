'''
File: SettingForm.py
Project: GailBot GUI
File Created: Friday, 4th November 2022 1:01:27 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Friday, 4th November 2022 6:24:06 pm
Modified By:  Siara Small  & Vivian Li
-----
'''
from typing import Dict 

from view.widgets import Label,TextForm
from view.style.Background import initSecondaryColorBackground
from util.Style import (
    FontFamily, 
    FontSize, 
    Dimension
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
        Args:
            header (str): the header of the page 
            formData (dict): the form data 
            caption (str, optional): a short discription of the form 
                                    Defaults to None.
        """
        super().__init__(*args, **kwargs)
        
        self.headerText = header 
        self.formData = formData
        self.captionText = caption
        self._initWidget()
        self._initLayout()

    def setValue(self, values:dict):
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
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(
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