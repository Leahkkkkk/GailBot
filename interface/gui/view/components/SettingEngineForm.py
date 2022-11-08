'''
File: DynamicNDependentCombo.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 1:44:39 pm
Modified By:  Siara Small  & Vivian Li
-----
'''

from typing import Dict

from util.Logger import makeLogger
from util.Text import EngineSettingForm
from view.widgets.MultipleCombo import ToggleCombo
from PyQt6.QtWidgets import (
    QComboBox, 
    QWidget, 
    QVBoxLayout, 
    QLabel, 
)


class SettingEngineForm(QWidget):
    """ Generate a dynamic list of combobox
    
    Args:
        data (dict): a dictionary that stores the dependent logic 
    
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
        print(engineName)
        self.logger.info(engineName)
        self.mainCombo.setCurrentText(engineName)
        self.toggleList.setValue(data[engineName])
        
    def _initWidget(self):
        """ initialize the widget """
        self.label = QLabel("Speech to Text Engine")
        self.mainCombo = QComboBox(self)
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
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.addStretch()
    
  
        



        
