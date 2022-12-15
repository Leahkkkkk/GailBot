'''
File: RequiredSetPage.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 11:08:43 am
Modified By:  Siara Small  & Vivian Li
-----
'''
 
from util.Style import FontSize,FontFamily
from util.Text import ProfilePageText as Text
from view.widgets import  Label
from view.components import RequiredSettingForm
from view.widgets.MsgBox import WarnBox

from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
)
from PyQt6.QtCore import Qt

center = Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter

class RequiredSettingPage(QWidget):
    """ class for the required settings page """
    def __init__(self, *args, **kwargs) -> None:
        """ initializes the page """
        super().__init__(*args, **kwargs)
        self._initWidget()
        self._initLayout()

    def setValue(self, data:dict):
        """ sets the value of data
        Args: data:dict: dictionary that is passed in to be updated
        """
        try:
            self.form.setValue(data)
        except:
            raise ValueError("Set Required Setting Data Error")
    
    def getValue(self) -> dict:
        """ gets the value of data """
        try:
            return self.form.getValue()
        except:
            raise ValueError("Get Required Setting Data Error")
        
    def _initWidget(self):
        """ initializes the widgets on the page """
        self.label = Label.Label(
            Text.requiredSetHeader, FontSize.HEADER2, FontFamily.MAIN )
        self.description = Label.Label(
            Text.requiredSetCaption, FontSize.DESCRIPTION, FontFamily.MAIN )
        self.form = RequiredSettingForm.RequiredSettingForm()
    
    def _initLayout(self):
        """ initializes the layout of the page """
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.label,
                              alignment=center)
        self.layout.addWidget(self.description,
                              alignment=center)
        self.layout.addWidget(self.form, 
                              alignment=center)
        self.layout.addStretch()

        
