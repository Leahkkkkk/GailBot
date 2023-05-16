'''
File: TabPage.py
Project: GailBot GUI
File Created: Sunday, 23rd October 2022 10:39:27 am
Author: Siara Small  & Vivian Li
-----
Last Modified: Sunday, 23rd October 2022 10:40:25 am
Modified By:  Siara Small  & Vivian Li
-----
Description: Tab page widget with the signal to support functionalities for 
             control flow 
'''
from typing import Dict, List
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal, QObject
from view.config.Style import STYLE_DATA
from gbLogger import makeLogger
from .Button import ColoredBtn, BorderBtn
from .Background import initPrimaryColorBackground
from view.config.Text import POPUP_TAB as Text
from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout, 
    QDialog,
    QStackedWidget)
from PyQt6.QtCore import QObject, pyqtSignal, QSize, Qt


TabSize = QSize(STYLE_DATA.Dimension.LARGEDIALOGWIDTH, STYLE_DATA.Dimension.LARGEDIALOGHEIGHT)
class Signals(QObject):
    """ contain signals to communicate with the parent tab widget """
    blockNextPage = pyqtSignal()
    nextPage = pyqtSignal()
    goToNextPage = pyqtSignal()
    previousPage = pyqtSignal()
    close = pyqtSignal()
    
class TabPage(QWidget):
    """ the wrapper class for tab pages with signals to redirect pages """
    def __init__(self, blockNext : bool = False, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.blockNext: bool = blockNext
        self.signals = Signals()
        self.logger = makeLogger()
        
    def initState(self):
        self.logger.info(f"init state called, block state set to {self.blockNext}")
        if self.blockNext:
            self.signals.blockNextPage.emit()
            self.blockNext = False
        else:
            self.signals.nextPage.emit()
    
class TabDialog(QDialog):
    def __init__(self, title, tabs: Dict[str, TabPage], size: QSize = TabSize) -> None:
        super().__init__()
        self.logger = makeLogger()
        self.currPage = 0 
        self.setWindowTitle(title)
        self.tabs: List[TabPage] = list(tabs.values())
        self.finalTabIdx = len(self.tabs) - 1
        self.setFixedSize(size)
        self.initUI()
        self.connectSignal()
        self.initStyle()
        self.updatePage()
        
    def initStyle(self):
        initPrimaryColorBackground(self)
        for tab in self.tabs:
            initPrimaryColorBackground(tab)
    
    def initUI(self):
        self._layout = QVBoxLayout()
        
        self.tabStack = QStackedWidget()
        for tab in self.tabs:
            self.tabStack.addWidget(tab)
            
        self.btnContainer = QWidget()
        self.btnLayout = QHBoxLayout()
        self.btnContainer.setLayout(self.btnLayout)
        
        self.startBtn = BorderBtn(Text.NEXT, STYLE_DATA.Color.PRIMARY_BUTTON)
        self.prevBtn = BorderBtn(Text.PREVIOUS, STYLE_DATA.Color.PRIMARY_BUTTON)
        self.nextBtn = BorderBtn(Text.NEXT, STYLE_DATA.Color.PRIMARY_BUTTON)
        self.finishedBtn = BorderBtn(Text.FINISH, STYLE_DATA.Color.PRIMARY_BUTTON)
       
        self.currentBtns: List[BorderBtn] =  [self.startBtn, self.prevBtn, self.nextBtn, self.finishedBtn]
        self.dynamicBtns: List[BorderBtn] = [self.startBtn, self.nextBtn, self.finishedBtn]
        
        self.setLayout(self._layout)
        
        for btn in self.currentBtns:
            self.btnLayout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignHCenter)
            btn.setStyleSheet(STYLE_DATA.buttonStyle.ButtonActive)
        
        self._layout.addWidget(self.tabStack, alignment=Qt.AlignmentFlag.AlignHCenter)
        self._layout.addWidget(self.btnContainer, alignment=Qt.AlignmentFlag.AlignHCenter)
        
    def addWidget(self, widget, alignment):
        self._layout.addWidget(widget, alignment=alignment)
        
    def connectSignal(self):
        self.startBtn.clicked.connect(self.gotoNext)
        self.finishedBtn.clicked.connect(self.close)
        self.nextBtn.clicked.connect(self.gotoNext)
        self.prevBtn.clicked.connect(self.gotoPrev)
        for tab in self.tabs:
            tab.signals.blockNextPage.connect(self.deactivateBtn)
            tab.signals.nextPage.connect(self.activateBtn)
     
    def gotoNext(self):
        if self.currPage < self.finalTabIdx:
            self.currPage += 1
            self.updatePage()

    def gotoPrev(self):
        if self.currPage != 0: 
            self.currPage -= 1
            self.updatePage()
    
    def updatePage(self):
        self.tabStack.setCurrentWidget(self.tabs[self.currPage])
        self.tabs[self.currPage].initState()
        for btn in self.currentBtns:
            btn.hide()
        if self.currPage == 0:
            self._showStartBtn()
        elif self.currPage == self.finalTabIdx:
            self._showFinishBtn()
        else:
            self._showPrevNextBtn()
    
    def _showStartBtn(self):
        self.startBtn.show()
        self.currentBtns = [self.startBtn]

    def _showFinishBtn(self):
        self.prevBtn.show()
        self.finishedBtn.show()
        self.currentBtns = [self.prevBtn, self.finishedBtn]

    def _showPrevNextBtn(self):
        self.prevBtn.show()
        self.nextBtn.show()
        self.currentBtns = [self.prevBtn, self.nextBtn]
        
    def deactivateBtn(self):
        self.logger.info("deactivate buttons")
        for btn in self.dynamicBtns:
            btn.setStyleSheet(STYLE_DATA.buttonStyle.ButtonInactive)
            btn.setEnabled(False) 
    
    def activateBtn(self):
        self.logger.info("deactivate buttons")
        for btn in self.dynamicBtns:
            btn.setStyleSheet(STYLE_DATA.buttonStyle.ButtonActive)
            btn.setEnabled(True) 
