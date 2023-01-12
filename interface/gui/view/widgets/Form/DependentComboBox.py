from typing import Dict, Tuple 

from util.Style import Color, Dimension, FontSize 
from util.Text import MultipleComboText as Text 
from view.widgets import  Label, ComboBox, TextForm
from view.widgets.Form.FormWidget import FormWidget 

from PyQt6.QtCore import QSize, Qt 
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout, 
)

class MultipleCombo(QWidget, FormWidget):
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
        self.mainForm = TextForm.TextForm(self.formData, toggle = True)
        self.verticalLayout.addWidget(self.mainForm)
    
    def getValue(self):
        return self.mainForm.getValue()
    
    def setValue(self, data: Dict[str, dict]):
        super().setValue(data)
        self.mainForm.setValues(data)

class DependentCombo(QWidget, FormWidget):
    def __init__(self, data: Dict[str, dict], label, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.form = data 
        self.label = label 
        self.value = None
        self.initUI()
        self.connectSignal()
        self.updateComboBox(self.mainCombo.currentIndex())
    
    def initUI(self): 
        self.mainLabel = Label.Label(self.label, FontSize.BODY)
        self.mainCombo = ComboBox.ComboBox(self)
        self.mainCombo.setMaximumWidth(Dimension.TOGGLEBARMINWIDTH)
        self.toggleList = None 
        for key, value in self.form.items():
            self.mainCombo.addItem(key, value)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.setLayout(self.verticalLayout)
        self.verticalLayout.addWidget(self.mainLabel)
        self.verticalLayout.addWidget(self.mainCombo)
    
    def updateComboBox(self, idx: int):
        data = self.mainCombo.itemData(idx)
        if self.toggleList:
            self.verticalLayout.removeWidget(self.toggleList)
            self.toggleList.hide()
            self.toggleList.deleteLater()
        self.toggleList = MultipleCombo(data)
        self.toggleList.setContentsMargins(0,0,0,0)
        self.verticalLayout.addWidget(self.toggleList)
        self.verticalLayout.addStretch()
    
    def connectSignal(self):
        self.mainCombo.currentIndexChanged.connect(self.updateComboBox)
    
    def setValue(self, value: Dict[str, Dict[str, dict]]):
        super().setValue(value)
        mainComboValue = list(value)[0]
        self.mainCombo.setCurrentText(mainComboValue)
        self.toggleList.setValue(value[mainComboValue])
    
    def getValue(self):
        value = dict()
        mainComboValue = self.mainCombo.currentText()
        value[mainComboValue] = self.toggleList.getValue()
        return value 