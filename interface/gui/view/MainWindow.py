import sys
import os
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow, QFileDialog
from view.components import MainStack, StatusBar, MenuBar, Console, MsgBox
from util import Logger 
from util import Path

""" mainwindow object """
class MainWindow(QMainWindow):
    def __init__(self, controller, settingdata, modelObj):
        super().__init__()
        self.setWindowTitle("My App")
        self.resize(900, 700)
        self.setMinimumSize(QSize(700, 600))
        self.setMaximumSize(QSize(1000, 800))
        self.settingdata = settingdata
        self.MainStack = MainStack.MainStack(self.settingdata, parent=self)
        self.setCentralWidget(self.MainStack)
        self.model = modelObj
        self.controller = controller
        self.StatusBar = StatusBar.StatusBar()
        self.setStatusBar(self.StatusBar)
        self.MenuBar = MenuBar.ManuBar()
        self.setMenuBar(self.MenuBar)
        self.Console = Console.Console()
        self.logger = Logger.makeLogger("Frontend")
        
        self._initFileModel()
        self._connectSignal()
        self._connectController()

    """ Functions provided to controller """
    
    def showTranscribeInProgress(self):
        self.MainStack.gotoTranscribeInProgress()
        
    def showTranscribeSuccess(self):
        self.MainStack.gotoTranscribeSuccess()
    
    def showFileUploadPage(self):
        self.MainStack.gotoFileUploadPage()
    
    def busyThreadPool(self):
        self.msgBox = MsgBox.WarnBox("The GailBot is too busy to receive your request!")
    
    def showStatusMsg(self, msg, time=None):
        self.StatusBar.showStatusMsg(msg, time)
    
    def freeThread(self):
        self.StatusBar.clearMessage()
    
    def TranscribeFailed(self, err:str):
        self.msgBox = MsgBox.WarnBox(f"Transcription Failed, error: {err}", self.showFileUploadPage)
        self.MainStack.TranscribeProgressPage.IconImg.stop()
        
    """ private function """
    
    def _connectSignal(self):
        self.MenuBar.OpenConsole.triggered.connect(lambda: self.Console.show())
        self.MenuBar.CloseConsole.triggered.connect(lambda: self.Console.hide())
        
    def _initFileModel(self):
        self.MainStack.FileUploadPage.fileTable.setModel(self.model.FileModel)
        
    def _connectController(self):
        self.MainStack.FileUploadPage.uploadFileBtn.clicked.connect(self._addfile)
        self.MainStack.ConfirmTranscribePage.confirmBtn.clicked.connect(self._transcribe)
    
    def _addfile(self):
        filedialog = QFileDialog(self)
        file_filter = "*.txt *.pdf *.wav *.png"
        filedialog.setNameFilter(file_filter)
        if filedialog.exec():
            filenamefull = filedialog.selectedFiles()
            if filenamefull:
                path = filedialog.directoryUrl().toString()
                path_arr = filenamefull[0].split("/")
                filename = path_arr[- 1]
                filepath = path[7:]
                filesize = round(os.stat(filenamefull[0]).st_size /(1024**2),2)
                fileObj = [[filename, filepath, f"{filesize}mb", "untranscribed"]]
                self.controller.addfile(fileObj)
            else:
                return None
    
    def _transcribe(self):
        indices = self.MainStack.FileUploadPage.fileTable.selectedIndexes()
        if indices:
            key = indices[0].row()
            self.controller.runGailBot(key)
        self.logger.info("")

    """ functions provided to mainstack"""
    def confirmCancel(self):
        self.logger.info("")
        self.controller.cancelGailBot()