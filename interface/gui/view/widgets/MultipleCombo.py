from typing import Dict

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
        self._initWidget()
        self._initLayout()

    def _initWidget(self):
        """ initialize the widget """
        self.userForm = UserForm()
        self.basicSet = ToggleView.ToggleView("basic setting", 
                                              self.userForm, 
                                              headercolor="#fff", 
                                              viewcolor=Color.GREYLIGHT)
        self.toggleList = []
        for key, item in self.data.items():
            newCombo = ComboList(item)
            newToggle = ToggleView.ToggleView(key, 
                                              newCombo, 
                                              headercolor="#fff",
                                              viewcolor=Color.GREYLIGHT)
            self.toggleList.append(newToggle)

    def _initLayout(self):
        """ initialize layout """
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        if self.showBasicSet:
            self.layout.addWidget(self.basicSet)
        for toggleView in self.toggleList:
            self.layout.addWidget(toggleView)
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
        self._initLayout()
    
    def _initWidget(self):
        """ initialize the widget """
        self.comboList = []
        self.labelList = []
        for key, items in self.data.items():
            newlabel = QLabel(key)
            self.labelList.append(newlabel)
            newCombo = QComboBox(self)
            newCombo.addItems(items)
            newCombo.setCurrentIndex(0)
            self.comboList.append(newCombo)

    def _initLayout(self):
        """ initialize layout """
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        for i in range(len(self.comboList)):
            self.layout.addWidget(self.labelList[i]) 
            self.layout.addWidget(self.comboList[i])
        self.layout.addStretch()


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