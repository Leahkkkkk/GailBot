'''
File: TextInput.py
Project: GailBot GUI
File Created: Monday, 9th January 2023 9:57:42 am
Author: Siara Small  & Vivian Li
-----
Last Modified: Monday, 9th January 2023 12:02:32 pm
Modified By:  Siara Small  & Vivian Li
-----
'''

from view.widgets.Form.FormWidget import FormWidget
from view.widgets import Label
from view.style.WidgetStyleSheet import INPUT_TEXT as INPUT_STYLE
from util.Style import FontSize, Dimension


from PyQt6.QtWidgets import QLineEdit, QHBoxLayout, QVBoxLayout, QWidget
from PyQt6.QtCore import QSize

class InputField(QLineEdit, FormWidget):
    def __init__(self, *args, **kwargs):
        super(InputField, self).__init__(*args, **kwargs)
        self.setFixedSize(
            QSize(Dimension.INPUTWIDTH, Dimension.INPUTHEIGHT)
        )
        self.setStyleSheet(INPUT_STYLE)
        
    def mouseDoubleClickEvent(self, a0) -> None:
        super().mouseDoubleClickEvent(a0)
        self.clear()
          
class TextInput(QWidget, FormWidget):
    def __init__(self,
                 label: str, 
                 labelSize = FontSize.BODY, 
                 inputText = None,
                 vertical = False,
                 *args, **kwargs) -> None:
        super(TextInput, self).__init__(*args, **kwargs)
        self.label = label
        self.vertical = vertical
        self.labelSize = labelSize
        self.value = inputText
        self.initUI()
        self.connectSignal()
        
    def initUI(self):
        self.inputLabel = Label.Label(self.label, self.labelSize)
        self.inputField = InputField()
        if self.value:
            self.inputField.setText(str(self.value))
        
        self._layout = QVBoxLayout() 
        self.setLayout(self._layout)
        self._layout.addWidget(self.inputLabel)
        self._layout.addWidget(self.inputField)
        
    def connectSignal(self):
        self.inputField.textChanged.connect(self.updateValue)

    def setValue(self, value):
        self.value = value 
        self.inputField.setText(str(value))
    
    def getValue(self):
        return self.inputField.text()
    