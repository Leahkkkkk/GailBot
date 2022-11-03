from typing import Dict 

from view.widgets import ToggleView, TextForm, Button
from view.components.SettingEngineForm import SettingEngineForm
from view.components.OutputFormatForm import OutPutFormat
from view.style.styleValues import FontFamily, FontSize, Color


from PyQt6.QtWidgets import (
    QWidget, 
    QLabel, 
    QVBoxLayout, 
    QComboBox,
)
from PyQt6.QtCore import Qt

class RequiredSet(QWidget):
    """ required settings page"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._initWidget()
        self._initLayout()
         
    def _initWidget(self):
        """initialize widgets"""
        self.engineForm = SettingEngineForm()
        self.engineSet = ToggleView.ToggleView("Speech to text settings", 
                                               self.engineForm, 
                                               header = True)
        self.outPutForm = OutPutFormat()
        self.outPutFormatForm = ToggleView.ToggleView("Output File Format Settings", 
                                               self.outPutForm,
                                               header = True)
        self.outPutFormatForm.setScrollHeight(450)
        
    def _initLayout(self):
        """initialize layout"""
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        self.verticalLayout.addWidget(
            self.engineSet, alignment=Qt.AlignmentFlag.AlignTop)
        self.verticalLayout.addWidget(
            self.outPutFormatForm, stretch=2, alignment=Qt.AlignmentFlag.AlignTop)  
    
    def submitForm(self):
        """ TODO: add user validation """
        pass
        """function to submit username and password form"""
    
    def setValue(self, data: Dict[str, Dict[str, dict]]):
        self.engineForm.setValue(data["Engine"])
        # self.outPutForm.setValue(data["Output Form Data"])
    
    def getValue(self)->dict:
        profile = dict() 
        profile["Engine"] = self.engineForm.getValue()
        profile["Output Form Data"] = self.outPutForm.getValue()
        return profile
