from typing import Dict, Tuple 
from copy import deepcopy
from view.config.Style import Color, Dimension, FontSize 
from ..Label import Label 
from ..ComboBox import ComboBox 
from ..TextForm import TextForm
from .FormWidget import FormWidget
from PyQt6.QtCore import Qt 
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout, 
)

class MultipleCombo(QWidget, FormWidget):
    def __init__(self, formData: Dict[str, dict], *args, **kwargs) -> None:
        """ create a list of combobox 

        Args:
            formData (Dict[str, dict]): the form data stored in a dictionary 
        """
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
        self.mainForm = TextForm(self.formData, toggle = True)
        self.verticalLayout.addWidget(self.mainForm)
    
    def getValue(self):
        return self.mainForm.getValue()
    
    def setValue(self, data: Dict[str, dict]):
        super().setValue(data)
        self.mainForm.setValues(data)

class DependentCombo(QWidget, FormWidget):
    def __init__(self, data: Dict[str, dict], label, pivotKey, *args, **kwargs) -> None:
        """ a dependent combobox form which can dynamically change the form 
            based on the user's choices of the first combobox 

        Args:
            data (Dict[str, dict]): a dictionary that stores the form values 
            label (str): the label of the combo input 
            pivotKey (str): the rest of the form will depends on the value in the pivot key. Defaults to None.
        """
        super().__init__(*args, **kwargs)
        self.form = data 
        self.label = label 
        self.value = None
        self.pivotKey = pivotKey
        self._initUI()
        self._connectSignal()
        self._updateComboBox(self.mainCombo.currentIndex())
    
    def setValue(self, value: Dict[str, Dict[str, str]]):
        """ given a dictionary that stores the form input as key 
            value pair, set the dependent combobox widget to the 
            given value 

        Args:
            value (Dict[str, Dict[str, str]]): _description_
        
        Raises:
            raises a key error if the provided data dictionary does
            not include the pivotKey 
        """
        d =  deepcopy(value)
        temp: Dict[str, Dict[str, str]] = dict()
        pivotValue = d.pop(self.pivotKey, "invalid")
        if pivotValue != "invalid":
            temp[pivotValue] = dict()
            temp[pivotValue].update(d)
            self.mainCombo.setCurrentText(pivotValue)
            self.toggleList.setValue(temp[pivotValue])
        else:
            raise KeyError(self.pivotKey)
    
    def getValue(self) -> Dict[str, str]:
        """get the value of the user input in the form of a 
           dictionary with only one level  

        Returns:
            Dict[str, str]: stores the key value pairs to represent form  
                            input 
        """
        value = dict()
        mainComboValue = self.mainCombo.currentText()
        value[self.pivotKey] = mainComboValue
        value.update(self.toggleList.getValue())
        return value 

    def _initUI(self): 
        self.mainLabel = Label(self.label, FontSize.BODY)
        self.mainCombo = ComboBox(self)
        self.mainCombo.setMaximumWidth(Dimension.TOGGLEBARMINWIDTH)
        self.toggleList = None 
        for key, value in self.form.items():
            self.mainCombo.addItem(key, value)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.setLayout(self.verticalLayout)
        self.verticalLayout.addWidget(self.mainLabel)
        self.verticalLayout.addWidget(self.mainCombo)
    
    def _updateComboBox(self, idx: int):
        """ private function called to update the form content based 
            on the choice of the mainCombo

        Args:
            idx (int): the index of the current mainCombo value
        """
        data = self.mainCombo.itemData(idx)
        if self.toggleList:
            self.verticalLayout.removeWidget(self.toggleList)
            self.toggleList.hide()
            self.toggleList.deleteLater()
        self.toggleList = MultipleCombo(data)
        self.toggleList.setContentsMargins(0,0,0,0)
        self.verticalLayout.addWidget(self.toggleList)
    
    def _connectSignal(self):
        """ 
        private function called to connect signal
        """
        self.mainCombo.currentIndexChanged.connect(self._updateComboBox)
    