from typing import List, Dict
from .FormWidget import FormWidget
from view.widgets.Label import Label
from view.config.Style import FontSize
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QCheckBox
from .CheckBox import CheckBox
from PyQt6.QtCore import Qt

class MultipleSelect(QWidget, FormWidget):
    def __init__(self, label: str,  choices: List[str]) -> None:
        super().__init__()
        self.choices = choices 
        self.labeltxt = label
        self.choicesDict: Dict[str, CheckBox] = {c: CheckBox(c, False) for c in self.choices}
        self.initUI()
        
    def initUI(self):
        self._layout = QVBoxLayout()
        self.labelwidget = Label(self.labeltxt, FontSize.BODY)
        self.setLayout(self._layout)
        self._layout.addWidget(self.labelwidget)
        for c in self.choicesDict.values():
            self._layout.addWidget(c, alignment=Qt.AlignmentFlag.AlignTop)
            self._layout.addSpacing(10)
        self._layout.addStretch()
    
    def getValue(self) -> List[str]:
        res = []
        for choice, box in self.choicesDict.items():
            if box.isChecked():
                res.append(choice)

    
    def setValue(self, choices: List[str]):
        choiceSet = set(choices)
        for choice, box in self.choicesDict.items():
            if choice in choiceSet:
                box.setValue(True)
            else:
                box.setValue(False)

    def addChoice(self, newChoice:str):
        newBox = CheckBox(newChoice, False)
        self.choicesDict[newChoice] = newBox 
        self._layout.addWidget(newBox)