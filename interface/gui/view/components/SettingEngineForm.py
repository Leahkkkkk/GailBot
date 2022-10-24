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

"""
    TODO: create functions to disable editing 
"""
from typing import Dict

from util.Logger import makeLogger
from view.widgets.MultipleCombo import ToggleCombo
from PyQt6.QtWidgets import (
    QComboBox, 
    QWidget, 
    QVBoxLayout, 
    QLabel, 
)

myLogger = makeLogger("Frontend")

class SettingEngineForm(QWidget):
    """ Generate a dynamic list of combobox
    
    Args:
        data (dict): a dictionary that stores the dependent logic 
    
    """
    def __init__(self, data:Dict[str, dict], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.data = data
        self._initWidget()
        self._initLayout()
        self._connectSignal()
        self._updateCombo(self.mainCombo.currentIndex())
        
    def _initWidget(self):
        """ initialize the widget """
        self.label = QLabel("Speech to Text Engine")
        self.mainCombo = QComboBox(self)
        self.toggleList = None
        for key, value in self.data.items():
            self.mainCombo.addItem(key, value)
    
    def _initLayout(self):
        """ initialize the layout """
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.mainCombo)
         
    def _connectSignal(self):
        """ connect the signal  """
        self.mainCombo.currentIndexChanged.connect(self._updateCombo)
    
    def _updateCombo(self, index):
        """ function to update the combobox """
        data = self.mainCombo.itemData(index)
        if self.toggleList:
            self.layout.removeWidget(self.toggleList)
            self.toggleList.deleteLater()
            
        self.toggleList = ToggleCombo(data)
        self.toggleList.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.toggleList)
        self.layout.setSpacing(0)
        self.layout.addStretch()
        
    def setValue(self, data: Dict[str, Dict[str, dict]]):
        engineName = list(data)[0]
        print(engineName)
        myLogger.info(engineName)
        self.mainCombo.setCurrentText(engineName)
        self.toggleList.setValue(data[engineName])
        
        



        
