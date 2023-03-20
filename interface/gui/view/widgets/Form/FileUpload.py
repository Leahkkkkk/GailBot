
from .FormWidget import FormWidget
from view.widgets import Label, Button, MsgBox
from view.config.Style import Color, FontSize, Dimension
from view.widgets.Form.TextInput import InputField
from copy import deepcopy
from PyQt6.QtWidgets import (
    QGridLayout, 
    QVBoxLayout, 
    QWidget, 
    QFileDialog, 
    QLineEdit,
    QPushButton)
from gbLogger import makeLogger


class UploadFile(QWidget, FormWidget):
    def __init__(self, label: str) -> None:
        super().__init__()
        self.label = deepcopy(label)
        self.logger = makeLogger("FileUpload")
        self.initUI()
        self.selectFileBtn.clicked.connect(self.uploadFile)
    
    def initUI(self):
        self._layout = QGridLayout()
        self.label = "Upload file for " + self.label.replace("_", " ")
        self.labelWidget = Label.Label(self.label, FontSize.BODY)
        self.pathDisplay = InputField()
        self.selectFileBtn = Button.BorderBtn("···", Color.PRIMARY_BUTTON, FontSize.HEADER1)
        self.selectFileBtn.setFixedWidth(70)
        self.selectFileBtn.setFixedHeight(Dimension.INPUTHEIGHT)
        self.setLayout(self._layout)
        self._layout.addWidget(self.labelWidget, 0, 0)
        self._layout.addWidget(self.pathDisplay, 1, 0)
        self._layout.addWidget(self.selectFileBtn, 1, 1)
        
    def uploadFile(self):
        try: 
            dialog = QFileDialog()
            file = dialog.getOpenFileName()
            if file:
                path, type = file 
                self.value = path 
                self.pathDisplay.setText(path)
            else:
                MsgBox.WarnBox("No file is uploaded by user")
        except Exception as e:
            MsgBox.WarnBox("An error occurred when uploading file")
            self.logger.error(exc_info=e)

    def getValue(self):
        return self.value 
    
    def setValue(self, value: str):
        self.value = value
        self.pathDisplay.setText(value)