'''
File: UploadFileTab.py
Project: GailBot GUI
File Created: Sunday, 23rd October 2022 10:57:19 am
Author: Siara Small  & Vivian Li
-----
Last Modified: Sunday, 23rd October 2022 11:06:50 am
Modified By:  Siara Small  & Vivian Li
-----
Description: implementation of a pop up dialog that allow user to upload 
             new file
'''
from typing import List

from util.Logger import makeLogger
from config.Text import ChooseFileTabText
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
   
class UploadFileTab(QDialog):
    def __init__(self, settings:List[str], *args, **kwargs) -> None:
        """ A tab with multiple pages for user to upload a new file.
            when uploading the file, the user will go through the process of:
            1. upload file from local directory 
            2. choose profile setting 
            3. choose the output path of the file

        Constructor Args:
            settings (List[str]): a list of profile name that is currently 
                                  available for user to choose when they upload 
                                  a new file 
    
        """
        super().__init__(*args, **kwargs)
        self.logger = makeLogger("F")
        self.signals = Signals()
        self.uploadFileTab = OpenFile()
        self.chooseSetTab = ChooseSet(settings)
        self.chooseOutPutTab = ChooseOutPut()
        self.setWindowTitle("Upload File")
        mainTab = Tab(ChooseFileTabText.WindowTitle, 
                      {ChooseFileTabText.TabHeader1: self.uploadFileTab,
                       ChooseFileTabText.TabHeader2: self.chooseSetTab,
                       ChooseFileTabText.TabHeader3: self.chooseOutPutTab})
        mainTab.signals.closeTab.connect(self._addFile)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(mainTab) 
        self.logger.info("")
    
    def _addFile(self) -> None: 
        """ emit a signal that contains the file data """
        fileList = self.uploadFileTab.getFile()
        profile = self.chooseSetTab.getProfile()
        outputPath = self.chooseOutPutTab.getOutputPath()
        
        status = {
            "Status": "Not Transcribed", 
            "Progress": "None", 
            "SelectedAction": "Transcribe"}
        try: 
            assert fileList
            for fileObj in fileList:
                fileData = {**fileObj, **profile, **outputPath, **status}
                self.signals.postFile.emit(fileData)
                self.logger.info("File added")
                self.logger.info(fileData)
        except Exception as e: 
            self.logger.error(e)
        self.close()

