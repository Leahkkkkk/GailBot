from typing import Dict, Tuple, TypedDict

from view.style.styleValues import Color
from view.widgets import ToggleView

from PyQt6.QtWidgets import (
    QComboBox, 
    QWidget, 
    QVBoxLayout,
    QLabel, 
    QGridLayout,
    QLineEdit
)



class ToggleCombo(QWidget):
    """ generate a list of toggle view, 
        Arg: 
            data(dict): a dictionary that stores  the toggle view data
                        the key is the label, the value is another dictionay
                        that will be used to construct a combolist
    """
    def __init__(self, 
                 data:Dict[str, dict],  
                 showBasicSet:bool = True, 
                 *args, 
                 **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.data = data 
        self.showBasicSet = showBasicSet
        self.comboListDict = dict()
        self._initWidget()

    def _initWidget(self):
        """ initialize the widget """
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        if self.showBasicSet:
            self.userForm = UserForm()
            self.basicSet = ToggleView.ToggleView("basic setting", 
                                                self.userForm, 
                                                headercolor="#fff", 
                                                viewcolor=Color.GREYLIGHT)
            self.layout.addWidget(self.basicSet)
        for key, item in self.data.items():
            newCombo = ComboList(item)
            newToggle = ToggleView.ToggleView(key, 
                                              newCombo, 
                                              headercolor="#fff",
                                              viewcolor=Color.GREYLIGHT)
            self.layout.addWidget(newToggle)
            self.comboListDict[key] = newCombo
        self.layout.addStretch()
    
    def getValue(self) -> Dict[str, dict]:
        value = dict()
        for key, comboList in self.comboListDict.items():
            value[key] = comboList.getValue()
        return value

    def setValue(self, data : Dict[str, dict]):
        for key, values in data.items():
            self.comboListDict[key].setValue(values)
    
class ComboList(QWidget):
    """ generalise a list of combobox
    
    Args:
        data(dict): a dictionary that stores combobox data
                    the key is a string stores the label
                    the value is a list of string that stores combobox items
    
    """
    def __init__(self, data:Dict[str, str], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.data = data
        self._initWidget()
    
    def _initWidget(self):
        """ initialize the widget """
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.comboBoxes = dict()
        self.labels = dict()
        
        for key, items in self.data.items():
            newlabel = QLabel(key)
            newCombo = QComboBox(self)
            newCombo.addItems(items)
            newCombo.setCurrentIndex(0)
            self.labels[key] = newlabel
            self.comboBoxes[key] = newCombo
            self.layout.addWidget(newlabel)
            self.layout.addWidget(newCombo)
        self.layout.addStretch()

    def getValue(self) -> dict:
        values = dict() 
        for key, combo in self.comboBoxes.items():
            values[key] = combo.currentText()
        return values
    
    def setValue(self, data:Dict[str,str]) -> None:
        for key, value in data.items():
            print(value)
            self.comboBoxes[key].setCurrentText(value)
            
        
class UserForm(QWidget):
    """ class for user form """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.layout = QGridLayout()
        self.userlabel = QLabel("Username")
        self.layout.addWidget(self.userlabel, 0,0)
        self.nameInput = QLineEdit(self)
        self.layout.addWidget(self.nameInput, 1,0)
        self.passwordLabel = QLabel("Password")
        self.layout.addWidget(self.passwordLabel, 0,1)
        self.passwordInput = QLineEdit(self)
        self.layout.addWidget(self.passwordInput, 1,1)
        self.setLayout(self.layout)
        self.setFixedHeight(100)
    
            
    def getValue(self)-> Tuple[str, str]:
        return (self.nameInput.text(), self.passwordInput.text())
    
    def setValue(self, data:dict):
        self.nameInput.setText(data["username"])
        self.passwordInput.setText(data["password"])
    
    