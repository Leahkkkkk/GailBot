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
import tomli

from view.widgets import  Label
from view.style.styleValues import FontFamily, FontSize
from view.components import RequiredSet

from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
)

from PyQt6.QtCore import Qt

class RequiredSetPage(QWidget):
    def __init__(self, data, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.data = data
        self._initConfig()
        self._initWidget()
        self._initLayout()
    
    def submitForm(self):
        self.form.submitForm()
    
    def setValue(self, data:dict):
        self.form.setValue(data)
    
    def getValue(self) -> dict:
        return self.form.getValue()
        
    def _initWidget(self):
        self.label = Label.Label("Required Settings", self.config["fontSizes"]["HEADER2"], 
                                 FontFamily.MAIN )
        self.description = Label.Label("\n"
                                "These settings are required before transcription and cannot be edited after transcription.",
                                 self.config["fontSizes"]["DESCRIPTION"], 
                                 FontFamily.MAIN )
        self.form = RequiredSet.RequiredSet(self.data)
    
    def _initLayout(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.label,
                              alignment=Qt.AlignmentFlag.AlignTop 
                              | Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.description,
                              alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.form, stretch= 10)
        self.layout.setSpacing(0)
        
    def _initConfig(self):
        with open("controller/interface.toml", mode="rb") as fp:
            self.config = tomli.load(fp)
