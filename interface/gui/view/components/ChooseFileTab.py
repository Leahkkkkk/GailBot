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

from util.Logger import makeLogger
from util.Text import ChooseFileTabText
from view.widgets.PopUpTab import Tab
from view.pages.FileUploadTabPages import (
    OpenFile, 
    ChooseOutPut, 
    ChooseSet
)

from PyQt6.QtWidgets import (
    QVBoxLayout, 
    QDialog,
)
from PyQt6.QtCore import QObject, pyqtSignal


class Signals(QObject):
    """ signal object for sending file data """
    postFile = pyqtSignal(dict)
    sendStatus = pyqtSignal(int)
   
class ChooseFileTab(QDialog):
    def __init__(self, settings:List[str], *args, **kwargs) -> None:
        """ a pop up tab for uploading new file

        Args:
            settings (List[str]): _description_
        """
        super().__init__(*args, **kwargs)
        self.logger = makeLogger("F")
        self.signals = Signals()
        self.chooseFileTab = OpenFile()
        self.chooseSetTab = ChooseSet(settings)
        self.chooseOutPutTab = ChooseOutPut()
        self.setWindowTitle("Upload File")
        mainTab = Tab(ChooseFileTabText.WindowTitle, 
                      {ChooseFileTabText.TabHeader1: self.chooseFileTab,
                       ChooseFileTabText.TabHeader2: self.chooseSetTab,
                       ChooseFileTabText.TabHeader3: self.chooseOutPutTab})
        mainTab.signals.closeTab.connect(self._addFile)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(mainTab) 
        self.logger.info("")
    
    def _addFile(self) -> None: 
        """ emit a signal that contains the file data """
        fileList = self.chooseFileTab.getFile()
        profile = self.chooseSetTab.getProfile()
        outputPath = self.chooseOutPutTab.getOutputPath()
        
        status = {
            "Status": "Not Transcribed", 
            "Progress": "None", 
            "SelectedAction": "Transcribe"}
        
        for fileObj in fileList:
            fileData = {**fileObj, **profile, **outputPath, **status}
            self.signals.postFile.emit(fileData)
            self.logger.info("file added")
            self.logger.info(fileData)

        self.close()

