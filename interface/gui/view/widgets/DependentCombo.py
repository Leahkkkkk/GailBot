'''
File: DependentCombo.py
Project: GailBot GUI
File Created: Thursday, 29th December 2022 4:53:21 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 29th December 2022 9:42:16 pm
Modified By:  Siara Small  & Vivian Li
-----
'''


from typing import Dict, Tuple

from util.Style import Dimension, FontSize
from util.Text import MultipleComboText as Text 
from view.widgets import ToggleView, Label, ComboBox, TextForm

from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout)
from PyQt6.QtCore import QSize, Qt

class DependentCombo(QWidget):
    def __init__(self, data: Dict[str, dict], label, *args, **kwargs) -> None:
        super().__init__(*args, *kwargs)
        self.data = data 
        self.label = label
        self._initWidget()
        self._initLayout()
        self._connectSignal()
        self._updateContent(self.mainCombo.currentIndex())
    
    def getValue(self) -> Dict[str, Dict[str, dict]]:
        value = dict()
        mainComboValue = self.mainCombo.currentText()
        value[mainComboValue] = self.toggleList.getValue()
        return value 

    def setValue(self, data: Dict[str, Dict[str, dict]]):
        mainComboValue = list(data)[0]
        self.mainCombo.setCurrentText(mainComboValue)
        self.toggleList.setValue(data[mainComboValue])
        
    def _initWidget(self):
        self.mainLabel = Label.Label(self.label, FontSize.BODY)
        self.mainCombo = ComboBox.ComboBox(self)
        self.mainCombo.setMaximumWidth(Dimension.TOGGLEBARMINWIDTH + 20)
        self.toggleList = None 
        for key, value in self.data.items():
            self.mainCombo.addItem(key, value)
    
    def _initLayout(self):
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.addSpacing(0)
        self.setLayout(self.verticalLayout)
        self.verticalLayout.addWidget(self.mainLabel)
        self.verticalLayout.addWidget(self.mainCombo)
    
    def _connectSignal(self):
        self.mainCombo.currentIndexChanged.connect(self._updateContent)
        
    def _updateContent(self, index):
        data = self.mainCombo.itemData(index)
        if self.toggleList:
            self.verticalLayout.removeWidget(self.toggleList)
            self.toggleList.hide()
            self.toggleList.deleteLater()
        self.toggleList = MultipleCombo(data)
        self.toggleList.setContentsMargins(0,0,0,0)
        self.verticalLayout.addWidget(self.toggleList)
        
class MultipleCombo(QWidget):
    def __init__(self, formData: Dict[str, dict], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.formData = formData
        self.formWidgets = dict()
        self._initWidget()
    
    def _initWidget(self):
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setContentsMargins(0,0,0,0)
        self.verticalLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.verticalLayout.setSpacing(0)
        self.setLayout(self.verticalLayout)
        self.mainForm = TextForm.TextForm(self.formData, toggle=True)
        self.mainForm.setMinimumHeight(1400)
        self.verticalLayout.addWidget(self.mainForm)
    
    def getValue(self):
        return self.mainForm.getValue()
    
    def setValue(self, data: Dict[str, dict]):
        self.mainForm.setValues(data)
