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
from view.widgets import ToggleView, Label, Button

from PyQt6.QtWidgets import (
    QComboBox, 
    QWidget, 
    QVBoxLayout, 
    QGridLayout,
    QLineEdit,
    QLabel, 
)

class DynamicNDependentCombo(QWidget):
    """ Generate a dynamic list of combobox
    
    Args:
        data (dict): a dictionary that stores settings with depended logic 
                     between key setting and values 
    
    """
    def __init__(self, data:dict, *args, **kwargs) -> None:
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
            self.toggleList.deleteLater()
            
        self.toggleList = ToggleList(data)
        self.layout.addWidget(self.toggleList)
        
        
class ToggleList(QWidget):
    """ generate a list of toggle view, 
        Arg: 
            data(dict): a dictionary that stores  the toggle view data
                        the key is the label, the value is another dictionay
                        that will be used to construct a combolist
    """
    def __init__(self, data:dict, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.data = data 
        self._initWidget()
        self._initLayout()

    def _initWidget(self):
        """ initialize the widget """
        self.userForm = UserForm()
        self.basicSet = ToggleView.ToggleView("basic setting", self.userForm)
        self.toggleList = []
        for key, item in self.data.items():
            newCombo = ComboList(item)
            newToggle = ToggleView.ToggleView(key, newCombo)
            self.toggleList.append(newToggle)

    def _initLayout(self):
        """ initialize layout """
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.basicSet)
        for toggleView in self.toggleList:
            self.layout.addWidget(toggleView)
            
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
        

class ComboList(QWidget):
    """ generalise a list of combobox
    
    Args:
        data(dict): a dictionary that stores combobox data
                    the key is a string stores the label
                    the value is a list of string that stores combobox items
    
    """
    def __init__(self, data:dict, *args, **kwargs) -> None:
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
        self.setLayout(self.layout)
        for i in range(len(self.comboList)):
            self.layout.addWidget(self.labelList[i]) 
            self.layout.addWidget(self.comboList[i])





            
