from typing import Dict, Tuple

from util.Style import Color, Dimension
from util.Text import MultipleComboText as Text
from view.widgets import ToggleView

from PyQt6.QtWidgets import (
    QComboBox, 
    QWidget, 
    QVBoxLayout,
    QLabel, 
    QGridLayout,
    QLineEdit,
)
from PyQt6.QtCore import QSize

class ToggleCombo(QWidget):
    """ generate a list of toggle view, 
        Arg: 
            data(dict): a dictionary that stores  the toggle view data
                        the key is the label, the value is another dictionay
                        that will be used to construct a combolist
            showBasicSet(bool): 
    """
    def __init__(self, 
                 data:Dict[str, dict],  
                 showBasicSet:bool = True, 
                 header = "basic setting", 
                 *args, 
                 **kwargs) -> None:
        """_summary_

        Args:
            data (Dict[str, dict]): a dictionary that stores form data,
                                    the key is the label, the value is another dictionay
                                    that stores tha value in each sub-form
            showBasicSet (bool, optional): if true, shows the user form 
            header (str, optional): header of the entire form, Defaults to "basic setting".
        """
        super().__init__(*args, **kwargs)
        
        self.data = data 
        self.header = header
        self.showBasicSet = showBasicSet
        self.comboListDict = dict()
        self._initWidget()
    
    def getValue(self) -> Dict[str, dict]:
        """ a public function to get the form value """
        value = dict()
        for key, comboList in self.comboListDict.items():
            value[key] = comboList.getValue()
        return value

    def setValue(self, data : Dict[str, dict]):
        """ a public function to set the form value """
        for key, values in data.items():
            self.comboListDict[key].setValue(values)

    def _initWidget(self):
        """ initialize the widget """
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        if self.showBasicSet:
            self.userForm = UserForm()
            self.basicSet = ToggleView.ToggleView(
            self.header, self.userForm, 
            headercolor = Color.WHITE, viewcolor =Color.LOW_CONTRAST)
            self.basicSet.setContentsMargins(0,0,0,0)
            self.layout.addWidget(self.basicSet)
            
        for key, item in self.data.items():
            newCombo = ComboList(item)
            newToggle = ToggleView.ToggleView(
            key, newCombo, 
            headercolor = Color.WHITE, viewcolor = Color.LOW_CONTRAST)
            self.layout.addWidget(newToggle)
            newToggle.setContentsMargins(0,0,0,0)
            self.comboListDict[key] = newCombo
            
        self.layout.addStretch()
    
    
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
    
    
    def getValue(self) -> Dict[str, str]:
        """ a public function to get the form value """
        values = dict() 
        for key, combo in self.comboBoxes.items():
            values[key] = combo.currentText()
        return values
    
    def setValue(self, data:Dict[str,str]) -> None:
        """ a public function to set the form value """
        for key, value in data.items():
            print(value)
            self.comboBoxes[key].setCurrentText(value)
    
    def _initWidget(self):
        """ initialize the widget """
        self.layout = QVBoxLayout()
        self.layout.setSpacing(5)
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
            
        
class UserForm(QWidget):
    """ class for user form """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.layout = QGridLayout()
        self.userlabel = QLabel(Text.username)
        self.layout.addWidget(self.userlabel, 0,0)
        self.nameInput = QLineEdit(self)
        self.nameInput.setFixedSize(
            QSize(Dimension.INPUTWIDTH,Dimension.INPUTHEIGHT))
        self.layout.addWidget(self.nameInput, 1,0)
        self.passwordLabel = QLabel(Text.password)
        self.layout.addWidget(self.passwordLabel, 0,1)
        self.passwordInput = QLineEdit(self)
        self.passwordInput.setFixedSize(
            QSize(Dimension.INPUTWIDTH, Dimension.INPUTHEIGHT))
        
        self.layout.addWidget(self.passwordInput, 1,1)
        self.setLayout(self.layout)
        self.setFixedHeight(100)
    
    def getValue(self)-> Tuple[str, str]:
        """ a public function to get the form value """
        return (self.nameInput.text(), self.passwordInput.text())
    
    def setValue(self, data: dict):
        """ a public function to set the form value """
        self.nameInput.setText(data["username"])
        self.passwordInput.setText(data["password"])
    
    