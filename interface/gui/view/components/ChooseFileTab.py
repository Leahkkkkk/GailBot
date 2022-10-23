'''
File: ChooseFileTab.py
Project: GailBot GUI
File Created: Sunday, 23rd October 2022 10:57:19 am
Author: Siara Small  & Vivian Li
-----
Last Modified: Sunday, 23rd October 2022 11:06:50 am
Modified By:  Siara Small  & Vivian Li
-----
'''

from typing import List

from view.widgets.PopUpTab import Tab
from view.pages.FileUploadTabPages import (
    OpenFile, 
    ChooseOutPut, 
    ChooseSet)
from PyQt6.QtWidgets import (
    QVBoxLayout, 
    QDialog,
)

from PyQt6.QtCore import QObject, pyqtSignal


class Signals(QObject):
    sendFile = pyqtSignal(dict)
    sendStatus = pyqtSignal(int)
   
class ChooseFileTab(QDialog):
    def __init__(self, settings:List[str], *args, **kwargs) -> None:
        """ a pop up tab for uploading new file

        Args:
            settings (List[str]): _description_
        """
        super().__init__(*args, **kwargs)
        self.signals = Signals()
        self.chooseFileTab = OpenFile()
        self.chooseSetTab = ChooseSet(settings)
        self.chooseOutPutTab = ChooseOutPut()
        self.setWindowTitle("Upload File")
        mainTab = Tab("Add New File", 
                      {"add file": self.chooseFileTab,
                       "choose setting": self.chooseSetTab,
                       "select output": self.chooseOutPutTab}
                      )
        mainTab.signals.closeTab.connect(self.addFile)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(mainTab) 
    
    def addFile(self) -> None: 
        fileObj = self.chooseFileTab.getFile()
        profileObj = self.chooseSetTab.getProfile()
        print("file profile", profileObj)
        outputPathObj = self.chooseOutPutTab.getOutputPath()
        statusObj = {"Status": "Not Transcribed"}
        fileData = {**fileObj, **profileObj, **outputPathObj, **statusObj}
        self.signals.sendFile.emit(fileData)
        self.signals.sendStatus.emit(200)
        self.close()
