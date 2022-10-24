from typing import Dict 

from view.widgets import ToggleView, Label
from view.components.SettingEngineForm import SettingEngineForm
from view.style.styleValues import FontFamily, FontSize, Color

from PyQt6.QtWidgets import (
    QWidget, 
    QLabel, 
    QVBoxLayout, 
    QComboBox,
)
from PyQt6.QtCore import Qt

class RequiredSet(QWidget):
    """ required settings page"""
    def __init__(self, data, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.data = data
        self._initWidget()
        self._initLayout()
         
    def _initWidget(self):
        """initialize widgets"""
        self.engineForm = SettingEngineForm(self.data,parent=self)
        self.engineSet = ToggleView.ToggleView("Speech to text settings", 
                                               self.engineForm, 
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
        self.verticalLayout.addWidget(self.engineSet, alignment=Qt.AlignmentFlag.AlignTop)
        self.verticalLayout.addWidget(self.outPutSet, alignment=Qt.AlignmentFlag.AlignTop)  
        self.verticalLayout.addStretch()
    
    def submitForm(self):
        """ TODO: add user validation """
        pass
        """function to submit username and password form"""
    
    def setValue(self, data: Dict[str, Dict[str, dict]]):
        self.engineForm.setValue(data)


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
        self.fileHeader = ToggleView.ToggleView("File Header Views", 
                                                self.headerForm, 
                                                headercolor="#fff")
        self.fileHeader.resizeViewHeight(200)
        self.layout.addWidget(self.fileHeader)
        
    def getValue(self):
        value = self.headerForm.getValue()
        value["Output File Format"] = self.formatCombo.currentText()
        return value
        


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
    
    def getValue(self):
        value = dict()
        value["language"] = self.lanCombo.currentText()
        value["Number of speaker"] = self.numCombo.currentText()
        for i in range(len(self.speakerCombolist)):
            value[f"gender{i}"] = self.speakerCombolist[i].currentText()
        
        return value 

        
            