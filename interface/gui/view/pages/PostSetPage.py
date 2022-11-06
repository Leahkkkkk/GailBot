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
from util.Text import ProfilePageText as Text 
from util.Text import PostSettingForm as Form

from PyQt6.QtWidgets import QWidget, QVBoxLayout

class PostSetPage(QWidget):
    """ class for the post-transcription settings page """
    def __init__(self, *args, **kwargs) -> None:
        """ initializes class """
        super().__init__(*args, **kwargs)
        self.setForm = SettingForm.SettingForm(
        Text.postSetHeader, Form, Text.postSetCaption)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        """ adds widget to layout """
        self.layout.addWidget(self.setForm)
    
    def setValue(self, values:dict):
        """ sets the value of the setting form
        Args: values:dict: TODO
        """
        self.setForm.setValue(values)
    
    def getValue(self) -> dict:
        """ gets the value in the setting form """
        return self.setForm.getValue()
        
    