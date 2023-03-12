'''
File: PostSetPage.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 11:08:27 am
Modified By:  Siara Small  & Vivian Li
-----
'''

from view.widgets import SettingForm
from view.widgets.MsgBox import WarnBox
from view.config.Text import ProfilePageText as Text 
from view.config.Text import PostSettingForm as Form
from util.Logger import makeLogger

from PyQt6.QtWidgets import QWidget, QVBoxLayout

class PostSettingPage(QWidget):
    """ class for the post-transcription settings page """
    def __init__(self, *args, **kwargs) -> None:
        """ initializes class """
        super().__init__(*args, **kwargs)
        self.logger  = makeLogger("F")
        self.setForm = SettingForm.SettingForm(
        Text.postSetHeader, Form, Text.postSetCaption)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        """ adds widget to layout """
        self.layout.addWidget(self.setForm)
    
    def setValue(self, values:dict):
        """ set the value of the setting form
        """
        try:
            self.setForm.setValue(values)
        except:
            WarnBox("An error occurred when loading the post transcription profile data")
    
    def getValue(self) -> dict:
        """ get the value in the setting form """
        try:
            return self.setForm.getValue()
        except :
            WarnBox("An error occurred when retrieving post transcription profile data")
        
    