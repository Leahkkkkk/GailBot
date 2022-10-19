from heapq import merge
from pickle import FALSE
from typing import Dict, List, TypedDict
import sys


from view.widgets import Button
from view.widgets.TabPages import (
    OpenFile, 
    ChooseOutPut, 
    ChooseSet)
from view.widgets.Button import ColoredBtn
from view.style.widgetStyleSheet import buttonStyle
from view.style.Background import initBackground
from view.style.styleValues import Color, FontFamily, FontSize


from PyQt6.QtWidgets import (
    QTabWidget, 
    QWidget, 
    QVBoxLayout, 
    QDialog,
    QHBoxLayout,
    QGridLayout)

from PyQt6.QtCore import QObject, pyqtSignal, QSize, Qt

class Signals(QObject):
    sendFile = pyqtSignal(dict)
    sendStatus = pyqtSignal(int)
    closeTab = pyqtSignal()

class fileObject(TypedDict):
    Name: str
    Type: str
    Profile: str
    Status: str
    Date: str
    Size: int
    Output: str
    FullPath: str
    
class Tab(QWidget):
    def __init__(
        self, 
        header:str,
        tabs: Dict[str, QWidget],
        *args,
        **kwargs
        ):
    
        super().__init__(*args, **kwargs)
        self.tabsState = []
        self.curPageIdx = 0
        self.header = header 
        self.tabs = tabs
        self.signals = Signals()
        self.setFixedSize(QSize(600,300))
        self._initWidget()
        self._initLayout()
        initBackground(self,Color.BLUEWHITE)

        
    def _initWidget(self):
        self.MainTab = QTabWidget(self)
        self.MainTab.setTabPosition(QTabWidget.TabPosition.West)
        
        """ iintialiale the control button """
        self.changePageBtn = changePageBtn()
        self.changePageBtn.nextBtn.clicked.connect(self._toNextPage)
        self.changePageBtn.prevBtn.clicked.connect(self._toPreviousPage)
        self.changePageBtn.finishBtn.clicked.connect(lambda: 
                                                self.signals.closeTab.emit())
       
        """ initialize the pages on the tab """
        for label, tab in self.tabs.items():
            self.MainTab.addTab(tab, label)
            self.tabsState.append(False)
            initBackground(tab,Color.BLUEWHITE)
            """ setting the page logic """
            tab.signals.nextPage.connect(self._enableBtn)
            tab.signals.close.connect(lambda: self.changePageBtn.finishBtn.show())
        
        for i in range (1 , self.MainTab.count()):
            self.MainTab.setTabEnabled(i, False)
            
    
        
        self.setWindowTitle(self.header)
        self.MainTab.currentChanged.connect(self._setButtonState)
        
    def _setButtonState(self, index):
        if self.tabsState[index]:
            self.changePageBtn.activateNextButton()
        else:
            self.changePageBtn.deactivateNextButton()
        
        if index == 0:
            self.changePageBtn.deactivatePrevButton()
        else:
            self.changePageBtn.activatePrevButton()
            
        if index == self.MainTab.count() - 1:
            self.changePageBtn.finishBtn.hide()
            
        
    def _initLayout(self):
        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)
        self.layout.addWidget(self.MainTab)
        self.layout.addWidget(self.changePageBtn)
    
    
    def _enableBtn(self):
        self.tabsState[self.MainTab.currentIndex()] = True
        self._setButtonState(self.MainTab.currentIndex())
        
    
    def _toNextPage(self):
        if self.curPageIdx + 1 < self.MainTab.count():
            self.curPageIdx += 1
            self.MainTab.setCurrentIndex(self.curPageIdx)
            self.MainTab.setTabEnabled(self.curPageIdx, True)
            
    
    def _toPreviousPage(self):
        if self.curPageIdx > 0 :
            self.curPageIdx -= 1
            self.MainTab.setCurrentIndex(self.curPageIdx)

            
            
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


class changePageBtn(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.horizontaLayout = QHBoxLayout(self)
        self.verticalLayout = QVBoxLayout(self)
        self.subContainer = QWidget(self)
        self.subContainer.setLayout(self.horizontaLayout)
        self.setLayout(self.verticalLayout)
        self.nextBtn = Button.BorderBtn("▶",Color.GREYDARK)
        self.prevBtn = Button.BorderBtn("◀", Color.GREYDARK)
        self.nextBtn.setFixedSize(QSize(20,20))
        self.prevBtn.setFixedSize(QSize(20,20))
        self.finishBtn = Button.ColoredBtn("Finish", Color.BLUEMEDIUM)
        self.finishBtn.setFixedSize(80,40)
        self.deactivateNextButton()
        self.deactivatePrevButton()
        self.horizontaLayout.addWidget(self.prevBtn)
        self.horizontaLayout.addWidget(self.nextBtn)
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(self.subContainer)
        self.verticalLayout.addWidget(self.finishBtn)
        self.finishBtn.hide()
    
    def activateNextButton(self):
        self.nextBtn.setStyleSheet(buttonStyle.ButtonActive)
        self.nextBtn.setEnabled(True)

    def deactivateNextButton(self):
        self.nextBtn.setStyleSheet(buttonStyle.ButtonInactive)
        self.nextBtn.setEnabled(False)
        
    def activatePrevButton(self):
        self.prevBtn.setStyleSheet(buttonStyle.ButtonActive)
        self.prevBtn.setEnabled(True)
    
    def deactivatePrevButton(self):
        self.prevBtn.setEnabled(False)
        self.prevBtn.setStyleSheet(buttonStyle.ButtonInactive)
    
   