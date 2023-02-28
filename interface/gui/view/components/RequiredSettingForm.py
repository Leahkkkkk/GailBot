'''
File: RequiredSettingForm.py
Project: GailBot GUI
File Created: Friday, 4th November 2022 1:01:27 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Tuesday, 8th November 2022 4:00:50 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: implementation of the required setting form 
'''

from typing import Dict 

from view.widgets import ToggleView
from view.widgets.Form.DependentComboBox import DependentCombo
from util.Text import EngineSettingForm
from view.components.OutputFormatForm import OutPutFormat
from util.Text import CreateNewProfilePageText as Text 
from util.Style import Dimension
import logging

logger = logging.getLogger()
logger = logging.LoggerAdapter(logger, {"source": "Frontend"})

from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
)
from PyQt6.QtCore import Qt

class RequiredSettingForm(QWidget):
    """ implementation of a form that allow user to create required setting 
    
    Public Functions: 
    1.  getValue() -> Dict[str, dict] 
        get the form value
    2.  setValue(data: Dict[str, dict]) -> None
        taking a dictionary that stores the form values, and load those
        form values
    
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._initWidget()
        self._initLayout()
         
    def _initWidget(self):
        """initialize widgets"""
        self.engineForm = DependentCombo(
            EngineSettingForm.Engine, "Speech to Text Engine")
        self.engineFormView = ToggleView.ToggleView(
            Text.engineSettingHeader, self.engineForm, header = True)
        self.engineFormView.setScrollHeight(Dimension.OUTPUT_FORM_HEIGHT)
        logger.error("the required setting form")
        logger.error(self.getValue())

    def _initLayout(self):
        """initialize layout"""
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        self.verticalLayout.addWidget(
            self.engineFormView, alignment=Qt.AlignmentFlag.AlignTop)
    
    def setValue(self, data: Dict [str, dict]):
        """ a public function to set the form value

        Args:
            data (Dict[str, Dict[str, dict]]): a dictionary that stores the 
                                               profile values
        """
        print(data["Engine"])
        self.engineForm.setValue(data["Engine"])
    
    
    def getValue(self) -> Dict [str, dict]:
        """ a public function that get the file value

        Returns:
            dict: returns a dictionary that stores the profile values
        """
        profile = dict() 
        d = self.engineForm.getValue()
        engine = list(d.keys())[0]
        profile["engine"] = engine
        profile.update(d[engine])
        logger.error(profile)
        return profile
