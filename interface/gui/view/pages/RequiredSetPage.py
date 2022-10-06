'''
File: RequiredSetPage.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 11:08:43 am
Modified By:  Siara Small  & Vivian Li
-----
'''

from view.widgets import DynamicNDependentCombo, ToggleView
from view.components import MsgBox

from PyQt6.QtWidgets import (
    QWidget, 
    QLabel, 
    QVBoxLayout, 
    QGridLayout, 
    QComboBox,
    QLineEdit
)
from PyQt6.QtCore import Qt

class RequiredSetPage(QWidget):
    """ required settings page"""
    
    def __init__(self, data, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.data = data
        self._initWidget()
        self._initLayout()
        
    def _initWidget(self):
        """initialize widgets"""
        self.label = QLabel("Required Setting")
        self.userForm = UserForm(self)
        self.header1 = QLabel("Speech to text settings")
        self.header1.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.basicSet = ToggleView.ToggleView("Basic Setting", self.userForm)
        self.comboBox = DynamicNDependentCombo.DynamicNDependentCombo(self.data,parent=self)
        self.engineset = ToggleView.ToggleView("Speech to text engine", self.comboBox)
        self.outPut = OutPutFormat()
        self.outPutSet = ToggleView.ToggleView("Output File Format Settings", self.outPut)
        
    def _initLayout(self):
        """initialize layout"""
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.header1)
        self.verticalLayout.addWidget(self.basicSet)
        self.verticalLayout.addWidget(self.engineset)
        self.verticalLayout.addWidget(self.outPutSet)
        
    def submitForm(self):
        """function to submit username and password form"""
        res = dict()
        if self.userForm.nameInput.text() == "":
            self.msgbox = MsgBox.WarnBox("Please Enter User name")
            return 
        elif self.userForm.passwordInput.text() == "":
            self.msgbox = MsgBox.WarnBox("Please Enter Passward")
            return
        else:
            res["userName"] = self.userForm.nameInput.text()
            res["password"] = self.userForm.passwordInput.text()
        return res
            
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

class OutPutFormat(QWidget):
    """class for output form"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.layout = QVBoxLayout(self)
        self.header1 = QLabel("Output File Format")
        self.layout.addWidget(self.header1)
        self.formatCombo = QComboBox()
        self.formatCombo.addItems([".TXT", ".CHAT", ".RTF"])
        self.layout.addWidget(self.formatCombo)
        self.headerForm = HeaderForm()
        self.fileheader = ToggleView.ToggleView("File Header Views", self.headerForm)
        self.layout.addWidget(self.headerForm)

class HeaderForm(QWidget):
    """class for header form"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.header = QLabel("General")
        self.layout.addWidget(self.header)
        self.speakerCombolist = []
        self.speakerLabelList = []
        
        self.label1 = QLabel("language")
        self.layout.addWidget(self.label1)
        
        self.lanCombo = QComboBox(self)
        self.lanCombo.addItems(["English", "Spanish", "Gernman", "French"])
        self.layout.addWidget(self.lanCombo)
        
        self.label2 = QLabel("Number of Speaker")
        self.layout.addWidget(self.label2)
        self.numCombo = QComboBox(self)
        self.numCombo.addItems(["1", "2", "3"])
        self.numCombo.currentIndexChanged.connect(self._updateNumCombo)
        self.layout.addWidget(self.numCombo)
        
        for i in range(3):
            newLabel = QLabel(f"Speaker {i + 1} Gender")
            self.speakerLabelList.append(newLabel)
            self.layout.addWidget(newLabel)
            newCombo = QComboBox()
            newCombo.addItems(["Female", "Male"])
            self.speakerCombolist.append(newCombo)
            self.layout.addWidget(newCombo)
            
        self._updateNumCombo(self.numCombo.currentIndex())
    
    def _updateNumCombo(self,index):
        for i in range(index+1):
            self.speakerCombolist[i].show()
            self.speakerLabelList[i].show()
        
        for i in range(index+1, 3):
            self.speakerCombolist[i].hide()
            self.speakerLabelList[i].hide()

        
            