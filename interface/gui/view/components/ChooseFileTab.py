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

from util.Config import ChooseFileTabText
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
    
    def _addFile(self) -> None: 
        """ emit a signal that contains the file data """
        fileObjList = self.chooseFileTab.getFile()
        profileObj = self.chooseSetTab.getProfile()
        outputPathObj = self.chooseOutPutTab.getOutputPath()
        
        statusObj = {
            "Status": "Not Transcribed", 
            "Progress": "Transcribing", 
            "SelectedAction": "Transcribe"}
        
        for fileObj in fileObjList:
            fileData = {**fileObj, **profileObj, **outputPathObj, **statusObj}
            self.signals.postFile.emit(fileData)
        self.close()

