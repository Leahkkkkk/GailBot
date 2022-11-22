import os 
import toml 

from view.widgets import Label, Button
from view.widgets.MsgBox import WarnBox
from PyQt6.QtWidgets import QDialog, QFileDialog, QVBoxLayout
from config.ConfigPath import BackEndDataPath
from util.Style import Color, FontFamily, FontSize, Dimension
from util.Path import getProjectRoot
from PyQt6.QtCore import QSize, Qt

import userpaths

center = Qt.AlignmentFlag.AlignHCenter

class WorkSpaceDialog(QDialog):
    def __init__(self, *arg, **kwargs) -> None:
        super().__init__(*arg, **kwargs)
        self.workDir = f"{userpaths.get_my_documents()}"
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
                                 "workspace directory on your computer.\n This will be where the "
                                 "file generated during transcription stored in", FontSize.BODY, others="text-align:center;")
        self.displayPath = Label.Label(f"GailBot Work Space Path: {self.workDir}/GailBot", FontSize.BODY, FontFamily.MAIN, others=f"border: 1px solid {Color.MAIN_TEXT}; text-align:center;")
        self.confirm = Button.ColoredBtn("Confirm", Color.SECONDARY_BUTTON)
        self.choose  = Button.ColoredBtn("Change Directory", Color.PRIMARY_BUTTON)
    
    def _initLayout(self):
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.verticalLayout.addWidget(self.header, alignment=center)
        self.verticalLayout.addWidget(self.label, alignment=center)
        self.verticalLayout.addWidget(self.displayPath)
        self.verticalLayout.addSpacing(Dimension.MEDIUM_SPACING)
        self.verticalLayout.addWidget(self.choose, alignment=center)
        self.verticalLayout.addWidget(self.confirm, alignment=center)
    
    def _openDialog(self):
        dialog = QFileDialog() 
        dialog.setDirectory(self.workDir)
        selectedFolder = dialog.getExistingDirectory()
        if selectedFolder:
            self.workDir = selectedFolder
            self.displayPath.setText(f"GailBot Work Space Path:\n {self.workDir}/GailBot")
    
    def _onConfirm(self):
        basedir = getProjectRoot()
        try:
            workSpace = { "WORK_SPACE_BASE_DIRECTORY" : self.workDir }
            with open(
                os.path.join(basedir, BackEndDataPath.workSpaceData), "w") as f:
                toml.dump(workSpace, f)
            if not os.path.isdir(f"{self.workDir}/GailBot"):
                os.mkdir(f"{self.workDir}/GailBot")
            if not os.path.isdir(f"{self.workDir}/GailBot/Frontend"):
                os.mkdir(f"{self.workDir}/GailBot/Frontend")
        except :
            WarnBox("cannot find the valid file path")
        
        self.close()
    
    def _initStyle(self):
        self.setStyleSheet(f"background-color:{Color.MAIN_BACKRGOUND}")
        self.setFixedSize(QSize(600,450))

