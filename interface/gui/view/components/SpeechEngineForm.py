'''
File: SettingEngineForm.py
Project: GailBot GUI
File Created: Friday, 4th November 2022 1:01:27 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Tuesday, 8th November 2022 4:00:59 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: implementation of a speech to engine form 
'''

from typing import Dict
from util.Style import FontSize
from util.Logger import makeLogger
from util.Text import EngineSettingForm
from view.widgets.MultipleCombo import ToggleCombo
from view.widgets.Label import Label
from view.widgets.ComboBox import ComboBox
from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
)
from PyQt6.QtCore import Qt

center = Qt.AlignmentFlag.AlignHCenter

class SpeechEngineForm(QWidget):
    """ Generate a dynamic list of combobox to implement the 
        setting form that allow user to create speech to engine setting 
    
    Args:
        data (dict): a dictionary that stores the dependent logic 
        
    Public Functions: 
    1.  getValue() -> Dict[str, dict] 
        get the form value
    2.  setValue(data: Dict[str, dict]) -> None
        taking a dictionary that stores the form values, and load those
        form values
    
    """
    def __init__(self, showBasicSet:bool = True,*args, **kwargs) -> None:
        super().__init__( *args, **kwargs)
        self.logger = makeLogger("Frontend")
        self.data = EngineSettingForm.Engine
        self.showBasicSet = showBasicSet
        self._initWidget()
        self._initLayout()
        self._connectSignal()
        self._updateCombo(self.mainCombo.currentIndex())
    
    def getValue(self) -> dict:
        """ public function to get engine form value """
        engine = self.mainCombo.currentText()
        return {engine: self.toggleList.getValue()}
    
    def setValue(self, data: Dict[str, Dict[str, dict]]):
        """ public function to set the engine form value """
        engineName = list(data)[0]
        self.logger.info(engineName)
        self.mainCombo.setCurrentText(engineName)
        self.toggleList.setValue(data[engineName])
        
    def _initWidget(self):
        """ initialize the widget """
        self.label = Label("Speech to Text Engine", FontSize.BODY)
        self.mainCombo = ComboBox(self)
        self.toggleList = None
        for key, value in self.data.items():
            self.mainCombo.addItem(key, value)
    
    def _initLayout(self):
        """ initialize the layout """
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.setLayout(self.verticalLayout)
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.mainCombo)
         
    def _connectSignal(self):
        """ connect the signal  """
        self.mainCombo.currentIndexChanged.connect(self._updateCombo)
    
    def _updateCombo(self, index):
        """ function to update the combobox """
        data = self.mainCombo.itemData(index)
        if self.toggleList:
            self.verticalLayout.removeWidget(self.toggleList)
            self.toggleList.hide()
            self.toggleList.deleteLater()
            
        self.toggleList = ToggleCombo(data, self.showBasicSet)
        self.toggleList.setContentsMargins(0,0,0,0)
        self.verticalLayout.addWidget(self.toggleList)
 
    
  
        



        
