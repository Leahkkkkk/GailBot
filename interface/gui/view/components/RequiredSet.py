from typing import Dict 

from view.widgets import ToggleView, TextForm, Button
from view.components.SettingEngineForm import SettingEngineForm
from view.components.OutputFormatForm import OutPutFormat
from util.Config import CreateNewProfilePageText as Text 
from util.Config import Dimension


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
        self.engineSet = ToggleView.ToggleView(
            Text.engineSettingHeader,self.engineForm, header = True)
        self.outPutForm = OutPutFormat()
        self.outPutFormatForm = ToggleView.ToggleView(
            Text.outputSettingHeader, self.outPutForm, header = True)
        self.outPutFormatForm.setScrollHeight(Dimension.DEFAULTTABHEIGHT)
        
    def _initLayout(self):
        """initialize layout"""
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        self.verticalLayout.addWidget(
            self.engineSet, alignment=Qt.AlignmentFlag.AlignTop)
        self.verticalLayout.addWidget(
            self.outPutFormatForm, stretch = 2, alignment=Qt.AlignmentFlag.AlignTop)  
    
    def setValue(self, data: Dict [str, dict]):
        """ a public function to set the form value

        Args:
            data (Dict[str, Dict[str, dict]]): a dictionary that stores the 
                                               profile values
        """
        self.engineForm.setValue(data["Engine"])
        # self.outPutForm.setValue(data["Output Form Data"])
    
    def getValue(self) ->  Dict [str, dict]:
        """ a plublic function that get the file value

        Returns:
            dict: retuns a dictionary that stores the profile values
        """
        profile = dict() 
        profile["Engine"] = self.engineForm.getValue()
        profile["Output Form Data"] = self.outPutForm.getValue()
        return profile
