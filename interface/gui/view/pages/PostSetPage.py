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
import tomli 

from view.widgets import InputBox, Button, Label,TextForm, SettingForm
from view.style.styleValues import FontFamily, FontSize, Color
from view.style.Background import initBackground

from PyQt6.QtWidgets import QWidget, QVBoxLayout,QScrollArea
from PyQt6.QtCore import Qt


class PostSetPage(QWidget):
    """ post-transcription settings page """
    def __init__(self, data, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.data = data
        self.header  = "Post-Transcription Settings"
        self.caption = "These settings are applied after the file is created."
        self.setForm = SettingForm.SettingForm(self.header, self.data, self.caption)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        """ add widget to layout """
        self.layout.addWidget(self.setForm)
    
    def setValue(self, values:dict):
        self.setForm.setValue(values)
    
    def getValue(self) -> dict:
        return self.setForm.getValue()
        
    def _initConfig(self):
        with open("controller/interface.toml", mode="rb") as fp:
            self.config = tomli.load(fp)
    