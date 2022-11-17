import os 
import toml 

from view.widgets import Label, Button
from view.widgets.MsgBox import WarnBox
from PyQt6.QtWidgets import QDialog, QFileDialog, QVBoxLayout
from config.ConfigPath import BackEndDataPath
from util.Style import Color, FontFamily, FontSize, Dimension, buttonStyle

from PyQt6.QtCore import QSize, Qt

center = Qt.AlignmentFlag.AlignHCenter

class WorkSapceDialog(QDialog):
    def __init__(self, *arg, **kwargs) -> None:
        super().__init__(*arg, **kwargs)
        self.workDir = None
        self._initWidget()
        self._initLayout()
        self._connectSignal()
        self._initStyle()
        
    
    def _connectSignal(self):
        self.choose.clicked.connect(self._openDialog)
        self.confirm.clicked.connect(self._onConfirm)
        
    def _initWidget(self):
        self.header = Label.Label("Welcome to the first launch on GailBot", FontSize.HEADER2, FontFamily.MAIN)
        self.label = Label.Label("The first step is to choose the path to GailBot's"
                                 "workspace directory\n on your computer. This will be where the "
                                 "file generated during transcription stored in", FontSize.BODY)
        self.confirm = Button.ColoredBtn("Confirm", Color.SECONDARY_BUTTON)
        self.choose  = Button.ColoredBtn("Choose Directory", Color.PRIMARY_BUTTON)
        self.confirm.setStyleSheet(buttonStyle.ButtonInactive)
        self.confirm.setDisabled(True)
    
    
    def _initLayout(self):
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.verticalLayout.addWidget(self.header, alignment=center)
        self.verticalLayout.addWidget(self.label, alignment=center)
        self.verticalLayout.addWidget(self.choose, alignment=center)
        self.verticalLayout.addWidget(self.confirm, alignment=center)
    
    def _openDialog(self):
        dialog = QFileDialog() 
        selectedFolder = dialog.getExistingDirectory()
        if selectedFolder:
            self.workDir = selectedFolder
            self._activateBtn()
    
    def _onConfirm(self):
        try:
            workSpace = {
                "workSpace": self.workDir, 
                "plugin": f"{self.workDir}/plugin"}
            with open(
                os.path.join(os.path.abspath("."),  BackEndDataPath.workSpaceData), "w") as f:
                toml.dump(workSpace, f)
            self.close()
        except :
            WarnBox("cannot find the valid file path")
    
    def _initStyle(self):
        self.setStyleSheet(f"background-color:{Color.MAIN_BACKRGOUND}")
        self.setFixedSize(QSize(550,300))

    def _activateBtn(self):
        self.confirm.setStyleSheet(buttonStyle.ButtonActive)
        self.confirm.setDisabled(False)