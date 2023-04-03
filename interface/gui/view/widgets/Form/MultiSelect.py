from typing import List, Dict
from .FormWidget import FormWidget
from ..Label import Label
from view.config.Style import FontSize
from gbLogger import makeLogger
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStyle
from .CheckBox import CheckBox
from PyQt6.QtCore import Qt

CHECKBOX_STYLE = "font-size:18px"


class MultipleSelect(QWidget, FormWidget):
    def __init__(self, label: str,  choices: List[str]) -> None:
        super().__init__()
        self.logger = makeLogger("F")
        self.choices = choices 
        self.labeltxt = label
        self.choicesDict: Dict[str, CheckBox] = dict()
        self.initUI()
        for choice in choices: 
            self.addChoice(choice)
        
    def initUI(self):
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.labelwidget = Label(self.labeltxt, FontSize.BODY)
        self.setLayout(self._layout)
        self._layout.addWidget(self.labelwidget, alignment=Qt.AlignmentFlag.AlignTop)
        
    def getValue(self) -> List[str]:
        res = []
        for choice, box in self.choicesDict.items():
            if box.isChecked():
                res.append(choice)
        self.logger.info(f"return the plugin setting {res}")
        return res
    
    def setValue(self, choices: List[str]):
        choiceSet = set(choices)
        for choice, box in self.choicesDict.items():
            if choice in choiceSet:
                box.setValue(True)
            else:
                box.setValue(False)

    def addChoice(self, newChoice:str):
        newBox = CheckBox(newChoice, False)
        self.logger.info(CHECKBOX_STYLE)
        newBox.setStyleSheet(CHECKBOX_STYLE)
        self.choicesDict[newChoice] = newBox 
        self._layout.addWidget(newBox, alignment=Qt.AlignmentFlag.AlignTop)
        
    
    
    def removeChoice(self,choice: str):
        if choice in self.choicesDict:
            try:
                self.choicesDict[choice].hide()
            except Exception as e:
                self.logger.error(e, exc_info=e)