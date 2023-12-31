'''
File: MultiSelect.py
Project: GailBot GUI
File Created: 2023/04/01
Author: Siara Small  & Vivian Li
-----
Last Modified:2023/05/23
Modified By:  Siara Small  & Vivian Li
-----
Description: implement a widget that allow user to select multiple options 
            
'''
from typing import List, Dict
from .FormWidget import FormWidget
from ..Label import Label
from view.config.Style import STYLE_DATA
from gbLogger import makeLogger
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from .CheckBox import CheckBox
from PyQt6.QtCore import Qt


class MultipleSelect(QWidget, FormWidget):
    def __init__(self, label: str, choices: List[str]) -> None:
        super().__init__()
        self.logger = makeLogger()
        self.choices = choices
        self.labeltxt = label
        self.choicesDict: Dict[str, CheckBox] = dict()
        self.initUI()
        for choice in choices:
            self.addChoice(choice)

    def initUI(self):
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.labelwidget = Label(
            self.labeltxt, STYLE_DATA.FontSize.HEADER4, STYLE_DATA.FontFamily.MAIN
        )
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

    def addChoice(self, newChoice: str):
        newBox = CheckBox(newChoice, False)
        self.choicesDict[newChoice] = newBox
        self._layout.addWidget(newBox, alignment=Qt.AlignmentFlag.AlignTop)

    def removeChoice(self, choice: str):
        if choice in self.choicesDict:
            try:
                self.choicesDict[choice].hide()
            except Exception as e:
                self.logger.error(e, exc_info=e)

    def changeFont(self):
        self.labelwidget.changeFont(STYLE_DATA.FontSize.HEADER4)
