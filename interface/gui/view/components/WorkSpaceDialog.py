'''
File: WorkSpaceDialog.py
Project: GailBot GUI
File Created: Tuesday, 22nd November 2022 2:09:54 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Tuesday, 29th November 2022 8:34:12 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: a pop up dialogue that opens during the first launch of the 
             app to ask user for the path the gailbot work directory
'''

import os 
import toml 
from view.widgets import Label, Button, MsgBox
from view.widgets.MsgBox import WarnBox
from PyQt6.QtWidgets import QDialog, QFileDialog, QVBoxLayout
from config_gui.ConfigPath import BackEndDataPath
from config.Style import Color, FontFamily, FontSize, Dimension
from config.Path import getProjectRoot
from config.Text import WelcomePageText as Text 
from util.Logger import makeLogger
from util.io import copy, delete
from config.GailBotData import getWorkBasePath
from PyQt6.QtCore import QSize, Qt
import userpaths

center = Qt.AlignmentFlag.AlignHCenter
USER_ROOT_NAME = "GailBot"
class WorkSpaceDialog(QDialog):
    def __init__(self, *arg, **kwargs) -> None:
        super().__init__(*arg, **kwargs)
        self.userRoot = os.path.join(userpaths.get_profile(), USER_ROOT_NAME)
        self.logger = makeLogger("F")
        self._initWidget()
        self._initLayout()
        self._connectSignal()
        self._initStyle()
    
    def getUserRoot(self) -> str:
        return self.userRoot
          
    def _connectSignal(self):
        self.choose.clicked.connect(self._openDialog)
        self.confirm.clicked.connect(self._onConfirm)
        
    def _initWidget(self):
        """ initialize the widget """
        self.header = Label.Label(
            Text.firstLaunchHeader, FontSize.HEADER2, FontFamily.MAIN)
        self.label = Label.Label(
            Text.firstLaunchInstruction, FontSize.BODY, others="text-align:center;")
        self.label.setWordWrap(True)
        self.displayPath = Label.Label(
            f"GailBot Work Space Path: {self.userRoot}", 
            FontSize.BODY, FontFamily.MAIN, 
            others=f"border: 1px solid {Color.MAIN_TEXT}; text-align:center;")
        self.confirm = Button.ColoredBtn("Confirm", Color.SECONDARY_BUTTON)
        self.choose  = Button.ColoredBtn("Change Directory", Color.PRIMARY_BUTTON)
    
    def _initLayout(self):
        """ initialize the layout """
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
        dialog.setDirectory(userpaths.get_profile())
        selectedFolder = dialog.getExistingDirectory()
        if selectedFolder:
            self.userRoot = os.path.join(selectedFolder, USER_ROOT_NAME)
            self.displayPath.setText(
                f"GailBot Work Space Path: {self.userRoot}")
    
    def _onConfirm(self):
        basedir = getProjectRoot()
        print(basedir)
        workSpace = { "WORK_SPACE_BASE_DIRECTORY" : self.userRoot}
        print(os.path.join(basedir, BackEndDataPath.workSpaceData))
        try:
            with open(
                os.path.join(basedir, BackEndDataPath.workSpaceData), "w+") as f:
                toml.dump(workSpace, f)
             
            if not os.path.isdir(self.userRoot):
                os.mkdir(self.userRoot)
       
        except Exception as e:
            self.logger("error when creating file to store user workspace {e}")
            WarnBox(f"cannot find the file path: " 
                    f"{os.path.join(basedir, BackEndDataPath.workSpaceData)}")
        self.close()
    
    def _initStyle(self):
        """ initialize the style """
        self.setStyleSheet(f"background-color:{Color.MAIN_BACKGROUND}")
        self.setFixedSize(QSize(600,450))

class ChangeWorkSpace(WorkSpaceDialog):
    """  a subclass of the original workspace dialog, with changed labels """
    def __init__(self, *arg, **kwargs) -> None:
        super().__init__(*arg, **kwargs)
        self.oldRoot = self.userRoot
        self.logger.info(f"old work space root {self.oldRoot}")
        
    def _initWidget(self):
        """ initialize the widget """
        self.workDir = getWorkBasePath()
        self.header = Label.Label(
           "Change Path to GailBot Work Space", FontSize.HEADER3, FontFamily.MAIN)
        self.label = Label.Label(
            " ", FontSize.BODY, others="text-align:center;")
        self.displayPath = Label.Label(
            f"GailBot Work Space Path: {self.workDir}", 
            FontSize.BODY, FontFamily.MAIN, 
            others=f"border: 1px solid {Color.MAIN_TEXT}; text-align:center;")
        self.confirm = Button.ColoredBtn("Confirm", Color.SECONDARY_BUTTON)
        self.choose  = Button.ColoredBtn("Change Directory", Color.PRIMARY_BUTTON)

    def _initStyle(self):
        """ initialize the style """
        self.setStyleSheet(f"background-color:{Color.MAIN_BACKGROUND}")
        self.setFixedSize(QSize(500,350))
    
    def _onConfirm(self):
        super()._onConfirm()
        try:
            copy(self.oldRoot, self.userRoot)
            delete(self.oldRoot)
        except Exception as e:
            self.logger.error(f"Error in moving GailBot folder {e}")