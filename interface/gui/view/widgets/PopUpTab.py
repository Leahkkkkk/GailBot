'''
File: PopUpTab.py
Project: GailBot GUI
File Created: Friday, 4th November 2022 1:01:27 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Sunday, 13th November 2022 2:51:26 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: implement tab widgets that take in different page widget as child
             elements, and display those pages in a tab 
'''
from typing import Dict

from .Button import ColoredBtn, BorderBtn
from .ScrollArea import ScrollArea
from .TabPage import TabPage
from .Background import initPrimaryColorBackground
from view.config.Text import PopUpText as Text

from PyQt6.QtWidgets import (
    QTabWidget, 
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout)
from PyQt6.QtCore import QObject, pyqtSignal, QSize, Qt

""" default tab size """

#### controlling style changes 
from view.config.Style import STYLE_DATA, buttonStyle
######################
TabSize = QSize(STYLE_DATA.Dimension.DEFAULTTABWIDTH, STYLE_DATA.Dimension.DEFAULTTABHEIGHT)
class Signals(QObject):
    """ a close tab signal """
    closeTab = pyqtSignal()

class Tab(QWidget):
    def __init__(
        self, 
        header:str,
        tabs: Dict[str, TabPage],
        size: QSize = TabSize,
        *args,
        **kwargs
        ):
        """  A tab with the built-in logic of sequential dependencies among 
            different pages 

        Args:
            header (str): the window header of the tab 
            tabs (Dict[str, TabPage]): the key of dictionary is the the header 
                                       of each tab page, and the value 
                                       is a TabPage widget
        """
        super().__init__(*args, **kwargs)
        self.tabsState = []   
        self.curPageIdx = 0
        self.header = header 
        self.tabs = tabs
        self.signals = Signals()
        self.setFixedSize(size)
        self._initWidget()
        self._initLayout()
        initPrimaryColorBackground(self)
    
    def setSize (self, size: QSize):
        self.setSize(size)
        
    def _initWidget(self):
        """ initialize the widget """
        self.MainTab = QTabWidget(self)
        initPrimaryColorBackground(self.MainTab)
        self.MainTab.setTabPosition(QTabWidget.TabPosition.West)
        
        """ initialize the control button """
        self.changePageBtn = _ChangePageBtn()
        self.changePageBtn.nextBtn.clicked.connect(self._toNextPage)
        self.changePageBtn.prevBtn.clicked.connect(self._toPreviousPage)
        self.changePageBtn.finishBtn.clicked.connect(lambda: 
                                                self.signals.closeTab.emit())
       
        """ initialize the pages on the tab """
        for label, tab in self.tabs.items():
            self.MainTab.addTab(tab, label)
            self.tabsState.append(False)
            initPrimaryColorBackground(tab)
            """ setting the page logic """
            tab.signals.nextPage.connect(self._enableBtn)
            tab.signals.goToNextPage.connect(self._toNextPage)
            tab.signals.close.connect(
                lambda: self.changePageBtn.finishBtn.show())
        
        for i in range (1 , self.MainTab.count()):
            self.MainTab.setTabEnabled(i, False)
        
        self.setWindowTitle(self.header)
        self.MainTab.currentChanged.connect(self._setButtonState)
        self.MainTab.currentChanged.connect(self._setCurrentIdx)
        
    def _setButtonState(self, index):
        """ change the next and prev button states  based on the signal 
            from the current page"""
        if self.tabsState[index]:
            self.changePageBtn.activateNextButton()
        else:
            self.changePageBtn.deactivateNextButton()
        
        if index == 0:
            self.changePageBtn.deactivatePrevButton()
        else:
            self.changePageBtn.activatePrevButton()
         
    def _initLayout(self):
        """ initialize the layout """
        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)
        self.layout.addWidget(self.MainTab)
        self.layout.addWidget(self.changePageBtn)
    
    def _enableBtn(self):
        """ enabled the button """
        self.tabsState[self.MainTab.currentIndex()] = True
        self._setButtonState(self.MainTab.currentIndex())
        
    
    def _toNextPage(self):
        """ activate and redirect to the next page"""
        if self.curPageIdx + 1 < self.MainTab.count():
            self.curPageIdx += 1
            self.MainTab.setCurrentIndex(self.curPageIdx)
            self.MainTab.setTabEnabled(self.curPageIdx, True)
            
    def _toPreviousPage(self):
        """ redirect to the previous page """
        if self.curPageIdx > 0 :
            self.curPageIdx -= 1
            self.MainTab.setCurrentIndex(self.curPageIdx)
    
    def _setCurrentIdx(self, idx):
        """ track the current index of the tab """
        self.curPageIdx = idx

        
class _ChangePageBtn(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        """ a private class for Tab class to allow user to switch between 
            pages through button"""
        super().__init__(*args, **kwargs)
        self.horizontaLayout = QHBoxLayout()
        self.verticalLayout = QVBoxLayout()
        self.subContainer = QWidget()
        self.subContainer.setLayout(self.horizontaLayout)
        self.setLayout(self.verticalLayout)
        self.nextBtn = BorderBtn(Text.leftArr, STYLE_DATA.Color.GREYDARK)
        self.prevBtn = BorderBtn(Text.rightArr, STYLE_DATA.Color.GREYDARK)
        self.nextBtn.setFixedSize(
            QSize(STYLE_DATA.Dimension.SMALLICONBTN,STYLE_DATA.Dimension.SMALLICONBTN))
        self.prevBtn.setFixedSize(
            QSize(STYLE_DATA.Dimension.SMALLICONBTN,STYLE_DATA.Dimension.SMALLICONBTN))
        self.finishBtn = ColoredBtn(Text.finish, STYLE_DATA.Color.PRIMARY_BUTTON)
        self.finishBtn.setFixedWidth(STYLE_DATA.Dimension.SBTNWIDTH)
        self.deactivateNextButton()
        self.deactivatePrevButton()
        self.horizontaLayout.addWidget(self.prevBtn)
        self.horizontaLayout.addWidget(self.nextBtn)
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(self.subContainer)
        self.verticalLayout.addWidget(self.finishBtn)
        self.finishBtn.hide()
    
    def activateNextButton(self):
        """ activate the next button  """
        self.nextBtn.setStyleSheet(buttonStyle.ButtonActive)
        self.nextBtn.setEnabled(True)

    def deactivateNextButton(self):
        """ deactivate the next button  """
        self.nextBtn.setStyleSheet(buttonStyle.ButtonInactive)
        self.nextBtn.setEnabled(False)
        
    def activatePrevButton(self):
        """ activate the previous button  """
        self.prevBtn.setStyleSheet(buttonStyle.ButtonActive)
        self.prevBtn.setEnabled(True)
    
    def deactivatePrevButton(self):
        """ deactivate the previous bytton """
        self.prevBtn.setEnabled(False)
        self.prevBtn.setStyleSheet(buttonStyle.ButtonInactive)
    
class NoControlTab(QWidget): 
    def __init__(
        self, 
        header:str,
        tabs: Dict[str, QWidget],
        *args,
        **kwargs
        ):
        """ a simple tab widget that can store different pages but does 
            not have the logic of page dependencies 

        Args:
            header (str): the window header of the pop up tab  
            tabs (Dict[str, QWidget]): the key of dictionary is the the header 
                                       of each tab page, and the value 
                                       is a QWidget that implement the page
        """
        super().__init__(*args, **kwargs)
        self.tabs = tabs
        self.header = header 
        self.setFixedSize(TabSize)
        self._initWidget()
        initPrimaryColorBackground(self)

    def _initWidget(self):
        """ initializes widgets """
        self.MainTab = QTabWidget(self)
        initPrimaryColorBackground(self.MainTab)
        self.MainTab.setTabPosition(QTabWidget.TabPosition.North)
        """ initialize the pages on the tab """
        for label, tab in self.tabs.items():
            container  = QWidget()
            layout = QVBoxLayout()
            container.setLayout(layout)
            scroll = ScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setWidget(tab)
            scroll.setVerticalScrollBarPolicy(
                Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
            layout.addWidget(scroll)
            self.MainTab.addTab(container, label)
            initPrimaryColorBackground(tab)
        self.setWindowTitle(self.header)

        
            