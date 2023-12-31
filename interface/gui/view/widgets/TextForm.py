"""
File: TextForm.py
Project: GailBot GUI
File Created: Friday, 4th November 2022 1:01:27 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Friday, 4th November 2022 5:57:10 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: a form widget that implement a form that takes in user input 
"""
from dataclasses import dataclass
from typing import Dict

from view.widgets import Label, ToggleView
from .Label import Label
from .ToggleView import ToggleView
from .Form.TextInput import TextInput
from .Form.ComBoInput import InputCombo
from .Form.FileUpload import UploadFile
from .Form.FormWidget import FormWidget
from .Form.OnOffButton import onOffButton
from .Form.MultiSelect import MultipleSelect
from .Form.SingleSelect import SingleSelect
from ..config.Style import STYLE_DATA
from view.widgets.Background import initSecondaryColorBackground, initBackground
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)
from PyQt6.QtCore import Qt


@dataclass
class InputFormat:
    BOOL = " bool"
    COMBO = " combo"
    DEPENDENT_COMBO = " dependent combo"
    FILE = " file upload"
    MULTI_CHOICE = " multiple choice"
    SINGLE_CHOICE = " single select"

class TextForm(QWidget):
    def __init__(
        self,
        data: Dict[str, Dict[str, str]],
        background: bool = True,
        showSubtittle = False,
        *args,
        **kwargs,
    ) -> None:
        """Displays a form

        Constructor Args:
            data (Dict[str, str]): a dictionary that stores the form
                                   and initial values of the form
            backgroundColor (bool)  : if true, the background is auto filled
                                      with default color

        Public Functions:
        1. enableForm(self) -> None
        2. disableForm(self) -> None
        3. getValue(self) -> Dict[str, str]
        4. setValues(self, data: Dict[str, str])
        """
        super().__init__(*args, **kwargs)
        self.data: Dict[str, Dict[str, str]] = data
        self.inputDict: Dict[str, FormWidget] = dict()
        self.showSubtittle = showSubtittle
        self.setFixedHeight(STYLE_DATA.Dimension.ENGINE_FORM_HEIGHT)
        self.setFixedWidth(STYLE_DATA.Dimension.ENGINE_FORM_WIDTH)
        self._initWidget()
        self._initLayout()
        self._connectSignal()
        if background:
            self._initStyle()

    def _connectSignal(self):
        STYLE_DATA.signal.changeColor.connect(self.changeColor)

    def changeColor(self):
        initBackground(self, color=STYLE_DATA.Color.LOW_CONTRAST2)

    def enableForm(self) -> None:
        """public function that enable the form edit"""
        for key, input in self.inputDict.items():
            input.enable()
            input.setStyleSheet("color:black;")

    def disableForm(self) -> None:
        """public function that disable the form edit"""
        for key, input in self.inputDict.items():
            input.disable()
            input.setStyleSheet("color:grey;")

    def getValue(self) -> Dict[str, str]:
        """public function that return the result of the form in a dictionary

        Returns:
            Dict[str, str] a dictionary that stores the form values from the user
        """
        value = dict()
        for key, input in self.inputDict.items():
            value[key] = input.getValue()
        return value

    def setValues(self, data: Dict[str, str]) -> None:
        """public function to update the widget values

        Args:
            data (Dict[str, str]): a dictionary that stores the values to be
                                   updated
        """
        for key, input in self.inputDict.items():
            input.setValue(data[key])

    def _initWidget(self):
        """initializes the widgets"""
        self.mainVertical = QVBoxLayout()
        self.mainVertical.setAlignment(Qt.AlignmentFlag.AlignLeft)

        for tittleKey, items in self.data.items():
            """adding spacing"""

            """ create additional layout if the form elements are 
                displayed in a toggle view """

            """ create the label  """
            tittleKey = tittleKey.split(". ")[-1]
            if self.showSubtittle:
                newLabel = Label(
                    tittleKey, STYLE_DATA.FontSize.BTN, STYLE_DATA.FontFamily.MAIN
                )
                self.mainVertical.addWidget(newLabel)

            """ create the form component element """
            for key, value in items.items():
                if InputFormat.BOOL in key:
                    key = key.replace(InputFormat.BOOL, "").split(". ")[-1]
                    newInput = onOffButton(key, state=value)

                elif InputFormat.COMBO in key:
                    key = key.replace(InputFormat.COMBO, "").split(". ")[-1]
                    newInput = InputCombo(label=key, selections=value)

                elif InputFormat.FILE in key:
                    key = key.replace(InputFormat.FILE, "").split(". ")[-1]
                    newInput = UploadFile(key)

                elif InputFormat.MULTI_CHOICE in key:
                    key = key.replace(InputFormat.MULTI_CHOICE, "").split(". ")[-1]
                    newInput = MultipleSelect(key, value)

                elif InputFormat.SINGLE_CHOICE in key:
                    key = key.replace(InputFormat.SINGLE_CHOICE, "").split(". ")[-1]
                    newInput = SingleSelect(key, value)
                else:
                    key = key.split(". ")[-1]
                    newInput = TextInput(key, inputText=value, vertical=False)

                """ add element to the layout """
                self.mainVertical.addWidget(newInput)
                self.inputDict[key] = newInput

        self.mainVertical.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.mainVertical.addStretch()
        self.mainVertical.addSpacing(STYLE_DATA.Dimension.LARGE_SPACING)

    def _initLayout(self):
        """initialize the layout"""
        self.setLayout(self.mainVertical)

    def _initStyle(self):
        """initializes the widget style"""
        initBackground(self, color=STYLE_DATA.Color.LOW_CONTRAST2)

    def addWidget(self, widget, alignment=Qt.AlignmentFlag.AlignLeft):
        """add widget to the Text form under the same column"""
        self.mainVertical.addWidget(widget, alignment=alignment)
