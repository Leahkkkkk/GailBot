from typing import List, Dict

from PyQt6 import QtCore
from .FormWidget import FormWidget
from ..Label import Label
from view.config.Style import STYLE_DATA
from gbLogger import makeLogger
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStyle
from .CheckBox import CheckBox
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QRadioButton, QLabel


class SingleSelect(QWidget):
    def __init__(self, header, options, parent=None):
        super().__init__(parent)

        # Create a layout for the widget
        layout = QVBoxLayout(self)

        # Create a label for the header
        label = QLabel(header)
        layout.addWidget(label)
        self.setFixedHeight((len(options) + 1) * STYLE_DATA.Dimension.BTNHEIGHT)

        # Create radio buttons for each option
        self.buttons: List[QRadioButton] = []
        for option in options:
            button = QRadioButton(option)
            self.buttons.append(button)
            layout.addWidget(button)

        # Connect the radio buttons to a function to update the selected value
        for button in self.buttons:
            button.toggled.connect(self._update_value)

        # Set the default value to the first option
        self.value = options[0]
        self.buttons[0].setChecked(True)

    # Function to update the selected value when a radio button is clicked
    def _update_value(self, checked):
        if checked:
            for button in self.buttons:
                if button.isChecked():
                    self.value = button.text()
                    break

    # Function to get the currently selected value
    def getValue(self):
        return self.value

    # Function to set the currently selected value
    def setValue(self, value):
        for button in self.buttons:
            if button.text() == value:
                button.setChecked(True)
                self.value = value
                break
