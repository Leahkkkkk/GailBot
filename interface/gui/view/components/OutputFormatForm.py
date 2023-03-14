'''
File: OutputFormatForm.py
Project: GailBot GUI
File Created: Friday, 4th November 2022 1:01:27 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Tuesday, 8th November 2022 4:01:17 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: implementation of the out put format form 
'''
from typing import Dict 

from view.widgets import ToggleView, TextForm, Button, Label, ComboBox
from view.config.Text import OutputFormatForm, OutputFormatFormText
from view.config.Style import Color, Dimension, FontSize
from gbLogger import makeLogger

from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
)

class OutPutFormat(QWidget):
    """ implementation of a form that allow user to create the profile setting 
        for output format 
        
        Public Functions: 
        1. getValue() -> Dict[str, str] 
            get the form value
        2. setValue(data: Dict[str, str]) -> None
            taking a dictionary that stores the form values, and load those
            form values
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.logger = makeLogger("F")
        self.layout = QVBoxLayout(self)
        self.header1 = Label.Label(OutputFormatFormText.header, FontSize.BODY)
        self.layout.addWidget(self.header1)
        self.formatCombo = ComboBox.ComboBox()
        self.formatCombo.setFixedWidth(Dimension.TOGGLEBARMINWIDTH + 20)
        self.formatCombo.addItems(OutputFormatForm.FileFormat)
        self.layout.addWidget(self.formatCombo)
        self.headerForm = HeaderForm(
            {OutputFormatFormText.CorpuFormHeader: OutputFormatForm.CorpusSettings})
        self.fileHeader = ToggleView.ToggleView(
            OutputFormatFormText.FileHeaderView, 
            self.headerForm,
            headercolor= Color.MAIN_BACKGROUND,
            viewcolor=Color.MAIN_BACKGROUND)
        self.layout.addWidget(self.fileHeader)
        self.textWrap = Button.onOffButton(OutputFormatFormText.TextWrap)
        self.textWrap.setFixedHeight(Dimension.SMALL_TABLE_HEIGHT)
        self.textWrapField = ToggleView.ToggleView(
            OutputFormatFormText.FileFormatHeader, 
            self.textWrap,
            headercolor= Color.MAIN_BACKGROUND,
            viewcolor= Color.MAIN_BACKGROUND)
        self.layout.addWidget(self.textWrapField)
        self.layout.addStretch()
        
    def getValue(self) -> Dict[str, str]:
        """ gets current value of the form data """
        value = self.headerForm.getValue()
        value["Output File Format"] = self.formatCombo.currentText()
        return value
    
    def setValue(self, data: Dict[str, str]) -> None:
        """ gets current value of the form data 
        Args: data:dict: dictionary to update
        """
        self.formatCombo.setCurrentText(data["Output File Format"])
        self.headerForm.setValue(data)
        
class HeaderForm(QWidget):
    """class for header form"""
    def __init__(self, data, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.speakerCombolist = []
        self.speakerLabelList = []
        
        self.label1 = Label.Label(
            OutputFormatFormText.LanguageHeader, FontSize.BODY)
        self.layout.addWidget(self.label1)
            
        self.lanCombo = ComboBox.ComboBox(self)
        self.lanCombo.addItems(OutputFormatForm.Language)
        self.layout.addWidget(self.lanCombo)
        self.label2 = Label.Label(
            OutputFormatFormText.SpeakerHeader, FontSize.BODY)
        self.layout.addWidget(self.label2)
        self.numCombo = ComboBox.ComboBox(self)
        self.numCombo.addItems(["1", "2", "3"])
        self.layout.addWidget(self.numCombo)
        self.corpusForm = TextForm.TextForm(data, background=False)

    
        for i in range(3):
            newLabel = Label.Label(
                f"Speaker {i + 1} Gender", FontSize.BODY)
            self.speakerLabelList.append(newLabel)
            self.layout.addWidget(newLabel)
            newCombo = ComboBox.ComboBox()
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
            data (Dict[str, str]): a dictionary that stores the data value
        """
        self.lanCombo.setCurrentText(data["language"])
        self.numCombo.setCurrentText(data["Number of speaker"])
        for i in range(len(self.speakerCombolist)):
            self.speakerCombolist[i].setCurrentText(data[f"gender{i}"])
        self.corpusForm.setValues(data["Corpus Settings"])
            