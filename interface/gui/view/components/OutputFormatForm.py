from typing import Dict 

from view.widgets import ToggleView, TextForm, Button
from view.style.styleValues import FontFamily, FontSize, Color
from util.Config import OutputFormatForm

from PyQt6.QtWidgets import (
    QWidget, 
    QLabel, 
    QVBoxLayout, 
    QComboBox,
)
from PyQt6.QtCore import Qt

class OutPutFormat(QWidget):
    """class for output form"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.layout = QVBoxLayout(self)
        self.header1 = QLabel("Output File Format")
        self.layout.addWidget(self.header1)
        self.formatCombo = QComboBox()
        self.formatCombo.addItems(OutputFormatForm.FileFormat)
        self.layout.addWidget(self.formatCombo)
        self.headerForm = HeaderForm({"Corpus Settings": OutputFormatForm.CorpusSettings})
        self.fileHeader = ToggleView.ToggleView("File Header Views", 
                                                self.headerForm,
                                                headercolor= "#fff",
                                                 viewcolor=Color.GREYLIGHT)
        self.layout.addWidget(self.fileHeader)
        self.textWrap = Button.onOffButton("Text-Wrapping")
        self.textWrapField = ToggleView.ToggleView("File Format", 
                                                   self.textWrap,
                                                    headercolor= "#fff",
                                                    viewcolor= Color.GREYLIGHT)
        self.layout.addWidget(self.textWrapField)
        
    def getValue(self):
        value = self.headerForm.getValue()
        value["Output File Format"] = self.formatCombo.currentText()
        return value
    
    def setValue(self, data:dict):
        self.formatCombo.setCurrentText(data["Output File Format"])
        
class HeaderForm(QWidget):
    """class for header form"""
    def __init__(self, data, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.speakerCombolist = []
        self.speakerLabelList = []
        
        self.label1 = QLabel("language")
        self.layout.addWidget(self.label1)
            
        self.lanCombo = QComboBox(self)
        self.lanCombo.addItems(OutputFormatForm.Language)
        self.layout.addWidget(self.lanCombo)
        self.label2 = QLabel("Number of Speaker")
        self.layout.addWidget(self.label2)
        self.numCombo = QComboBox(self)
        self.numCombo.addItems(["1", "2", "3"])
        self.layout.addWidget(self.numCombo)
        self.corpusForm = TextForm.TextForm(data, Color.GREYLIGHT)
    
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
        self.layout.addWidget(self.corpusForm)
    
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
        
        corpusValue = self.corpusForm.getValue()
        value["Corpus Settings"] = corpusValue
        return value 

    def setValue(self, data:dict):
        self.lanCombo.setCurrentText(data["language"])
        self.numCombo.setCurrentIndex(data["Number of speaker"])
        for i in range(len(self.speakerCombolist)):
            self.speakerCombolist[i].setCurrentText(data[f"gender{i}"])
        self.corpusForm.updateValues(data["Corpus Settings"])
            