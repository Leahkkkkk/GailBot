from PyQt6.QtWidgets import QLabel, QWidget, QHBoxLayout, QLineEdit
from PyQt6.QtGui import QStandardItemModel
from PyQt6.QtCore import QSize
from view.style import style

""" an input box widget
param: 
    @label: input_field label 
"""
class InputBox(QWidget):
    def __init__(self, label:str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.label = label
        self._initWidget()
        self._initLayout()
        self._connectSignal()

    """ public function to ge the value of the input """
    def value(self):
        return self.inputFeild.text()
    
    def _initWidget(self):
        self.inputlabel = QLabel(self.label)
        self.inputFeild = InputField(self) 
        self.inputFeild.setMaximumSize(200,50)
    
    def _initLayout(self):
        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)
        self.layout.addWidget(self.inputlabel) 
        self.layout.addWidget(self.inputFeild)
    
    def _connectSignal(self):
        pass


class InputField(QLineEdit):
    def __init__(self, label:str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setStyleSheet(f"font-size: {style.FontSize.TEXT_FIELD};"
                           f"padding:0;"
                           f"border: 1px solid {style.Color.BORDERGREY} ")
        self.setFixedSize(QSize(style.Dimension.INPUTFIELD_WIDTH, 
                                style.Dimension.INPUTFIELD_HEIGHT))
        