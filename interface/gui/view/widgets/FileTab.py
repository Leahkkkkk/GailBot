from heapq import merge
from typing import Dict, List, TypedDict
import sys 

from view.widgets.TabPages import (
    OpenFile, 
    ChooseOutPut, 
    ChooseSet)
from view.style.Background import initBackground
from view.style.styleValues import Color


from PyQt6.QtWidgets import (
    QTabWidget, 
    QWidget, 
    QVBoxLayout, 
    QDialog)

from PyQt6.QtCore import QObject, pyqtSignal, QSize

class Signals(QObject):
    sendFile = pyqtSignal(dict)
    sendStatus = pyqtSignal(int)

class fileObject(TypedDict):
    Name: str
    Type: str
    Profile: str
    Status: str
    Date: str
    Size: int
    Output: str
    FullPath: str
    
class Tab(QTabWidget):
    def __init__(
        self, 
        header:str,
        tabs: Dict[str, QWidget],
        *args,
        **kwargs
        ):
    
        super().__init__(*args, **kwargs)
        self.tabsList = []
        self.curPage = 0
        self.setFixedSize(QSize(300,300))
        for label, tab in tabs.items():
            self.addTab(tab, label)
            self.tabsList.append(tab)
            initBackground(tab,Color.BLUEWHITE )
            tab.signals.nextPage.connect(self._toNextPage)
            tab.signals.close.connect(self.close)
            
        self.setWindowTitle(header)
        self.setTabPosition(QTabWidget.TabPosition.West)
        for i in range (1 , self.count()):
            self.setTabEnabled(i, False)
    
    def _toNextPage(self, idx):
        if idx < self.count():
            self.curPage  = idx
            self.setTabEnabled(self.curPage, True)
            self.setCurrentIndex(self.curPage)

            
class TabWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        
        tab1 = OpenFile()
        tab2 = ChooseSet(["coffee study", "default"])
        tab3 = ChooseOutPut()
        
        mainTab = Tab("Add New File", {"add file": tab1,
                                       "choose setting": tab2,
                                       "select output": tab3})
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(mainTab) 
    
class ChooseFileTab(QDialog):
    def __init__(self, settings:List[str], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.signals = Signals()
        self.chooseFileTab = OpenFile()
        self.chooseSetTab = ChooseSet(settings)
        self.chooseOutPutTab = ChooseOutPut()
        self.chooseOutPutTab.signals.close.connect(self.addFile)
        
        mainTab = Tab("Add New File", 
                      {"add file": self.chooseFileTab,
                       "choose setting": self.chooseSetTab,
                       "select output": self.chooseOutPutTab}
                      )

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


