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
import datetime
import toml 
import logging
from view.widgets import Label, Button, MsgBox
from view.widgets.MsgBox import WarnBox
from view.util.io import zip_file, is_directory, copy
from PyQt6.QtWidgets import QDialog, QFileDialog, QVBoxLayout
from config_frontend.ConfigPath import WorkSpaceConfigPath, PROJECT_ROOT, FRONTEND_CONFIG_ROOT
from view.config.Style import Color, FontFamily, FontSize, Dimension
from view.config.Text import WelcomePageText as TEXT 
from gbLogger import makeLogger
from config_frontend import getWorkPath, getWorkBasePath
from PyQt6.QtCore import QSize, Qt
import userpaths
center = Qt.AlignmentFlag.AlignHCenter
USER_ROOT_NAME = "GailBot"
BACKEND_LOG_NAME = "BackendLogFiles"

class WorkSpaceDialog(QDialog):
    def __init__(self, *arg, **kwargs) -> None:
        super().__init__(*arg, **kwargs)
        self.userRoot = os.path.join(userpaths.get_profile(), USER_ROOT_NAME)
        self.workSpaceSaved = False
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
            TEXT.firstLaunchHeader, FontSize.HEADER2, FontFamily.MAIN)
        self.label = Label.Label(
            TEXT.firstLaunchInstruction, FontSize.BODY, others="text-align:center;")
        self.label.setWordWrap(True)
        self.displayPath = Label.Label(
            f"{TEXT.workspacePath}: {self.userRoot}", 
            FontSize.BODY, FontFamily.MAIN, 
            others=f"border: 1px solid {Color.MAIN_TEXT}; text-align:center;")
        self.confirm = Button.ColoredBtn(TEXT.confirmBtn, Color.SECONDARY_BUTTON)
        self.choose  = Button.ColoredBtn(TEXT.changeDirBtn, Color.PRIMARY_BUTTON)
    
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
                f"{TEXT.workspacePath} {self.userRoot}")
            
    def saveWorkspace(self) -> bool:
        workSpace = { "userRoot" : self.userRoot}
        try:
            with open(
                os.path.join(FRONTEND_CONFIG_ROOT, WorkSpaceConfigPath.userRoot), "w+") as f:
                toml.dump(workSpace, f)
             
            if not os.path.isdir(self.userRoot):
                os.mkdir(self.userRoot)
            return True
        except Exception as e:
            WarnBox(f"cannot find the file path: " 
                    f"{os.path.join(FRONTEND_CONFIG_ROOT, WorkSpaceConfigPath.userRoot)}"
                    f"error: {e}")
            return False
        
    def _onConfirm(self):
        if self.saveWorkspace():
            self.workSpaceSaved = True 
            self.close()
        else:
            self.workSpaceSaved = False
            self.userRoot = os.path.join(userpaths.get_profile(), USER_ROOT_NAME)
    
    def _initStyle(self):
        """ initialize the style """
        self.setStyleSheet(f"background-color:{Color.MAIN_BACKGROUND}")
        self.setFixedSize(QSize(600,450))

class SaveLogFile(WorkSpaceDialog):
    """ 
    open a dialog that ask user to select a space to store zipped log files 
    """
    def __init__(self, *arg, **kwargs) -> None:
        super().__init__(*arg, **kwargs)
        self.userRoot = userpaths.get_desktop()
        self.logger = makeLogger("F")
        
    def _initWidget(self):
        self.userRoot = userpaths.get_desktop()
        self.workDir = getWorkBasePath()
        self.header = Label.Label(
           TEXT.saveLogPrompt, FontSize.HEADER3, FontFamily.MAIN)
        linkFormat = "<a style='color:{0};' href='mailto: {1}'> {2} \n {1}</a>"
        self.label = Label.Label(
            linkFormat.format(Color.MAIN_TEXT, TEXT.email, TEXT.sendZipMsg), FontSize.BODY, link=True)
        self.displayPath = Label.Label(
            f"{TEXT.saveLogPath}: {self.userRoot}", 
            FontSize.BODY, FontFamily.MAIN, 
            others=f"border: 1px solid {Color.MAIN_TEXT}; text-align:center;")
        self.confirm = Button.ColoredBtn(TEXT.confirmBtn, Color.SECONDARY_BUTTON)
        self.choose  = Button.ColoredBtn(TEXT.changeDirBtn, Color.PRIMARY_BUTTON)
   
    def _initStyle(self):
        """ initialize the style """
        self.setStyleSheet(f"background-color:{Color.MAIN_BACKGROUND}")
        self.setFixedSize(QSize(500,350))
    
    def _openDialog(self):
        dialog = QFileDialog() 
        dialog.setDirectory(userpaths.get_profile())
        selectedFolder = dialog.getExistingDirectory()
        if selectedFolder:
            self.userRoot = selectedFolder
            self.displayPath.setText(
                f"{TEXT.saveLogPath}: {self.userRoot}")
        
    def _onConfirm(self):
        """ 
            On confirm, output the zipped log file to the directory selected 
            by user
        """
        try:
            """ TODO: find better implementation if we were to move 
                      the backend log files 
            """
            backendLog = getWorkPath().backendLogFiles
            if is_directory(os.path.join(PROJECT_ROOT, BACKEND_LOG_NAME)):
                copy(os.path.join(PROJECT_ROOT, BACKEND_LOG_NAME), backendLog)
            logdir = getWorkBasePath()
            zip_file(logdir, 
                     os.path.join(self.userRoot, f"{TEXT.zipFileName}-{datetime.datetime.now()}.zip"),
                     ".log")
            self.close()
        except Exception as e:
            self.logger.error(e)

class ChangeWorkSpace(WorkSpaceDialog):
    """  a subclass of the original workspace dialog, with changed labels """
    def __init__(self, *arg, **kwargs) -> None:
        super().__init__(*arg, **kwargs)
        self.oldRoot = self.userRoot
        self.logger = makeLogger("F")
        self.logger.info(f"old work space root {self.oldRoot}")
        
    def _initWidget(self):
        """ initialize the widget """
        self.workDir = getWorkBasePath()
        self.header = Label.Label(
          TEXT.changeWorkDir, FontSize.HEADER3, FontFamily.MAIN)
        self.label = Label.Label(
            " ", FontSize.BODY, others="text-align:center;")
        self.displayPath = Label.Label(
            f"{TEXT.workspacePath}: {self.workDir}", 
            FontSize.BODY, FontFamily.MAIN, 
            others=f"border: 1px solid {Color.MAIN_TEXT}; text-align:center;")
        self.confirm = Button.ColoredBtn(TEXT.confirmBtn, Color.SECONDARY_BUTTON)
        self.choose  = Button.ColoredBtn(TEXT.changeDirBtn, Color.PRIMARY_BUTTON)

    def _initStyle(self):
        """ initialize the style """
        self.setStyleSheet(f"background-color:{Color.MAIN_BACKGROUND}")
        self.setFixedSize(QSize(500,350))
    
    def _onConfirm(self):
        workSpace = { "userRoot" : self.userRoot}
        try:
            with open(
                os.path.join(FRONTEND_CONFIG_ROOT, WorkSpaceConfigPath.newUserRoot), "w+") as f:
                toml.dump(workSpace, f)
        except Exception as e:
            self.logger.info(f"error when creating file to store user workspace {e}")
            WarnBox(f"cannot find the file path: " 
                    f"{os.path.join(FRONTEND_CONFIG_ROOT, WorkSpaceConfigPath.newUserRoot)}")
        WarnBox("The change to workspace will be applied when relaunching GailBot")
        self.close()