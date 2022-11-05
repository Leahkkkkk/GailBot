from typing import Dict 

from view.widgets import ToggleView, TextForm, Button
from util.Config import OutputFormatForm, OutputFormatFormText,Color


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
        self.header1 = QLabel(OutputFormatFormText.header)
        self.layout.addWidget(self.header1)
        self.formatCombo = QComboBox()
        self.formatCombo.addItems(OutputFormatForm.FileFormat)
        self.layout.addWidget(self.formatCombo)
        self.headerForm = HeaderForm(
            {OutputFormatFormText.CorpuFormHeader: OutputFormatForm.CorpusSettings})
        self.fileHeader = ToggleView.ToggleView(
            OutputFormatFormText.FileHeaderView, 
            self.headerForm,
            headercolor= Color.WHITE,
            viewcolor=Color.GREYLIGHT)
        self.layout.addWidget(self.fileHeader)
        self.textWrap = Button.onOffButton(OutputFormatFormText.TextWrap)
        self.textWrapField = ToggleView.ToggleView(
            OutputFormatFormText.FileFormatHeader, 
            self.textWrap,
            headercolor= Color.WHITE,
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
        
        self.label1 = QLabel(OutputFormatFormText.LanguageHeader)
        self.layout.addWidget(self.label1)
            
        self.lanCombo = QComboBox(self)
        self.lanCombo.addItems(OutputFormatForm.Language)
        self.layout.addWidget(self.lanCombo)
        self.label2 = QLabel(OutputFormatFormText.SpeakerHeader)
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
        """ dynamically change the number of combo box """
        for i in range(index + 1):
            self.speakerCombolist[i].show()
            self.speakerLabelList[i].show()
        
        for i in range(index + 1, 3):
            self.speakerCombolist[i].hide()
            self.speakerLabelList[i].hide()
    
    def getValue(self):
        """ public function to get the form value """
        value = dict()
        value["language"] = self.lanCombo.currentText()
        value["Number of speaker"] = self.numCombo.currentText()
        for i in range(len(self.speakerCombolist)):
            value[f"gender{i}"] = self.speakerCombolist[i].currentText()
        
        corpusValue = self.corpusForm.getValue()
        value["Corpus Settings"] = corpusValue
        return value 

    def setValue(self, data: Dict[str, str]):
        """ public function to set the form value
        
        Args: 
            data (Dict[str, str]): a dutionary that stores the data value
        """
        self.lanCombo.setCurrentText(data["language"])
        self.numCombo.setCurrentIndex(data["Number of speaker"])
        for i in range(len(self.speakerCombolist)):
            self.speakerCombolist[i].setCurrentText(data[f"gender{i}"])
        self.corpusForm.setValues(data["Corpus Settings"])
            