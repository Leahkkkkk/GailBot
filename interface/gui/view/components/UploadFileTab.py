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

from gbLogger import makeLogger
from view.config.Text import ChooseFileTabText
from view.config.Style import STYLE_DATA
from view.widgets.TabPage import TabDialog
from view.pages.FileUploadTabPages import (
    OpenFile, 
    ChooseOutPut, 
    ChooseSet
)

from PyQt6.QtCore import QObject, pyqtSignal, QSize


class Signals(QObject):
    """ signal object for sending file data """
    postFile = pyqtSignal(dict)
    sendStatus = pyqtSignal(int)
   
class UploadFileTab():
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
        self.mainTab = TabDialog(ChooseFileTabText.WindowTitle, 
                      {ChooseFileTabText.TabHeader1: self.uploadFileTab,
                       ChooseFileTabText.TabHeader2: self.chooseSetTab,
                       ChooseFileTabText.TabHeader3: self.chooseOutPutTab},
                      QSize(550,600))
        
        self.mainTab.finishedBtn.clicked.connect(self._addFile)

    def exec(self):
        self.mainTab.exec()
    
    def _addFile(self) -> None: 
        """ emit a signal that contains the file data """
        fileList = self.uploadFileTab.getFile()
        profile = self.chooseSetTab.getProfile()
        outputPath = self.chooseOutPutTab.getOutputPath()
        
        status = {"Status": "Not Transcribed", "Progress": "None"}
        
        try: 
            assert fileList
            for fileObj in fileList:
                fileData = {**fileObj, **profile, **outputPath, **status}
                self.signals.postFile.emit(fileData)
                self.logger.info("File added")
                self.logger.info(fileData)
        except Exception as e: 
            self.logger.error(e, exc_info=e)

