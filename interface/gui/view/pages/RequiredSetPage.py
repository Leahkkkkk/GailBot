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

from re import T
from view.widgets import DynamicNDependentCombo, ToggleView
from view.components import MsgBox

from PyQt6.QtWidgets import (
    QWidget, 
    QLabel, 
    QVBoxLayout, 
    QGridLayout, 
    QComboBox,
    QLineEdit,
    QScrollArea
)
from PyQt6.QtCore import Qt, QSize

class RequiredSetPage(QWidget):
    """ required settings page"""
    
    def __init__(self, data, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.data = data
        self._initWidget()
        self._initLayout()
        
    def _initWidget(self):
        """initialize widgets"""
        self.comboBox = DynamicNDependentCombo.DynamicNDependentCombo(self.data,parent=self)
        self.engineSet = ToggleView.ToggleView("Speech to text settings", 
                                               self.comboBox, 
                                               header = True)
        self.outPut = OutPutFormat()
        self.outPutSet = ToggleView.ToggleView("Output File Format Settings", 
                                               self.outPut,
                                               header = True)
        self.outPutSet.resizeViewHeight(350)
        
        
    def _initLayout(self):
        """initialize layout"""
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        self.verticalLayout.addWidget(self.engineSet, 
                                      alignment =Qt.AlignmentFlag.AlignTop
                                                |Qt.AlignmentFlag.AlignAbsolute)
        self.verticalLayout.addWidget(self.outPutSet, 
                                      alignment =Qt.AlignmentFlag.AlignTop
                                                |Qt.AlignmentFlag.AlignAbsolute)     
    
    def submitForm(self):
        """ TODO: add user validation """
        pass
        """function to submit username and password form"""


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
        self.fileHeader = ToggleView.ToggleView("File Header Views", self.headerForm)
        self.fileHeader.resizeViewHeight(200)
        self.layout.addWidget(self.fileHeader)

class HeaderForm(QWidget):
    """class for header form"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
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
        self.layout.addWidget(self.numCombo)
    
        for i in range(3):
            newLabel = QLabel(f"Speaker {i + 1} Gender")
            self.speakerLabelList.append(newLabel)
            self.layout.addWidget(newLabel)
            newCombo = QComboBox()
            newCombo.addItems(["Female", "Male"])
            self.speakerCombolist.append(newCombo)
            self.layout.addWidget(newCombo)
        
        self.numCombo.currentIndexChanged.connect(self._updateNumCombo)
        self._updateNumCombo(self.numCombo.currentIndex())
    
    def _updateNumCombo(self,index):
        for i in range(index + 1):
            self.speakerCombolist[i].show()
            self.speakerLabelList[i].show()
        
        for i in range(index + 1, 3):
            self.speakerCombolist[i].hide()
            self.speakerLabelList[i].hide()

        
            