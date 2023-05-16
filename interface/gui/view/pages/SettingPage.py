'''
File: SettingPage.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 11:11:19 am
Modified By:  Siara Small  & Vivian Li
-----
'''

""" TODO:
make the button into a list for modularity 
"""
from enum import Enum
from typing import List, Dict, List, Tuple
from view.config.Style import STYLE_DATA
from view.config.Text import PROFILE_PAGE as Text
from view.config.Style import StyleSheet as STYLE 
from gbLogger import makeLogger

from view.pages import (
    ProfilePage, 
    PluginPage,
    SysSetPage, 
    EnginePage
)
from view.util.ErrorMsg import  ERR
from view.widgets import (
    ColoredBtn,
    BorderBtn,
    SideBar,
)

from PyQt6.QtWidgets import (
    QWidget, 
    QStackedWidget, 
    QHBoxLayout,
    QVBoxLayout
)
from PyQt6 import QtCore

center = QtCore.Qt.AlignmentFlag.AlignHCenter
bottom = QtCore.Qt.AlignmentFlag.AlignBottom


class SET_STATE(Enum):
    REQUIRED = 0
    PLUGIN = 1
    
class SettingPage(QWidget):
    """ class for settings page """
    def __init__(
        self, 
        *args, 
        **kwargs) -> None:
        """ initializes class """
        super().__init__(*args, **kwargs)
        self.logger = makeLogger()
        self._initWidget()
        self._initLayout()
        self._connectSignal()
    
    def addAvailableSettings(self, profiles: List[Tuple[str, Dict]]):
        """ add a list of profile keys """
        for profile in profiles:
            self.ProfilePage.addSucceed(profile)
    
    def addAvailableEngines(self, engines:List[Tuple[str, Dict]]):
        for engine in engines:
            self.EngineSetPage.addSucceed(engine)
     
    def addAvailablePluginSuites(self, pluginSuites: List[Tuple[str, Dict[str, str], str]]):
        for suite in pluginSuites:
            self.PluginPage.addSucceed(suite)
    
    def _initWidget(self):
        self.HIGH_LIGHT = STYLE_DATA.Color.HIGHLIGHT
        """ initializes widgets"""
        self.sideBar = SideBar()
        
        # button on the sidebar
        self.transcibeSetBtn = BorderBtn(
            Text.PROFILES_BTN, STYLE_DATA.Color.GREYDARK, STYLE_DATA.FontSize.BTN, 0, 
            STYLE.onlyBottomBorder, width=STYLE_DATA.Dimension.LBTNWIDTH)

        self.engineSetBtn = BorderBtn(
            Text.ENGINE_BTN, STYLE_DATA.Color.GREYDARK, STYLE_DATA.FontSize.BTN, 0, 
            STYLE.onlyBottomBorder, width=STYLE_DATA.Dimension.LBTNWIDTH )
       
        self.pluginSetBtn = BorderBtn(
            Text.PLUGIN_BTN, STYLE_DATA.Color.GREYDARK, STYLE_DATA.FontSize.BTN, 0, 
            STYLE.onlyBottomBorder, width=STYLE_DATA.Dimension.LBTNWIDTH)
        
        self.systemSetBtn = BorderBtn(
            Text.SYSSET_BTN, STYLE_DATA.Color.GREYDARK, STYLE_DATA.FontSize.BTN, 0, 
            STYLE.onlyBottomBorder, width=STYLE_DATA.Dimension.LBTNWIDTH)
        
        self.CANCEL = ColoredBtn(Text.CANCEL, STYLE_DATA.Color.CANCEL_QUIT)
        self.settingStack = QStackedWidget(self)
        self.PluginPage = PluginPage.PluginPage()
        self.SysPage = SysSetPage.SystemSettingPage()
        self.EngineSetPage = EnginePage.EnginePage()
        self.ProfilePage = ProfilePage.ProfilePage()
        self.settingStack.addWidget(self.ProfilePage)
        self.settingStack.addWidget(self.PluginPage)
        self.settingStack.addWidget(self.SysPage)
        self.settingStack.addWidget(self.EngineSetPage)
        self.settingStack.setCurrentWidget(self.ProfilePage)
         
    def _initLayout(self):
        """initializes layout"""
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0,0,0,0)
        self.horizontalLayout.setSpacing(0)
        self.setLayout(self.horizontalLayout)
        self.topSelectionContainer = QWidget()
        self.topSelectionContainer.setContentsMargins(0,0,0,0)
        self.sidebarTopLayout = QVBoxLayout()
        self.sidebarTopLayout.setContentsMargins(0,0,0,0)
        self.topSelectionContainer.setLayout(self.sidebarTopLayout)
        """ adds widgets to layout """
        self.sidebarTopLayout.addWidget(self.transcibeSetBtn)
        self.sidebarTopLayout.addWidget(self.engineSetBtn)
        self.sidebarTopLayout.addWidget(self.pluginSetBtn)
        self.sidebarTopLayout.addWidget(self.systemSetBtn)
        self.sidebarTopLayout.setSpacing(0)
        self.sideBar.addTopWidget(self.topSelectionContainer)
        self.sideBar.addMidWidget(self.CANCEL)
        self.horizontalLayout.addWidget(self.sideBar)
        self.horizontalLayout.addWidget(self.settingStack)
        self.settingStack.setContentsMargins(0,0,0,0)
   
    def _connectSignal(self):
        """ connects profileSignal upon button clicks """
        self.transcibeSetBtn.clicked.connect(self._activeRequiredSet)
        self.engineSetBtn.clicked.connect(self._activateEngineSet)
        self.pluginSetBtn.clicked.connect(self._activatePlugin)
        self.systemSetBtn.clicked.connect(self._activateSystemSet)

        self.PluginPage.signal.addSucceed.connect(self.ProfilePage.addPluginSuite)
        self.PluginPage.signal.deleteSucceed.connect(self.ProfilePage.deletePlugin)
        self.EngineSetPage.signal.addSucceed.connect(self.ProfilePage.addEngineSetting)
        self.EngineSetPage.signal.deleteSucceed.connect(self.ProfilePage.deleteEngine)
        
        STYLE_DATA.signal.changeColor.connect(self.colorchange)
        STYLE_DATA.signal.changeFont.connect(self.fontchange)
        
    def _activeRequiredSet(self):
        """ switches current page from post transcription settings page to required settings page """
        self._setBtnDefault()
        self.transcibeSetBtn.setActiveStyle(self.HIGH_LIGHT)
        self.settingStack.setCurrentWidget(self.ProfilePage)
    
    def _activateEngineSet(self):
        self._setBtnDefault()
        self.engineSetBtn.setActiveStyle(self.HIGH_LIGHT)
        self.settingStack.setCurrentWidget(self.EngineSetPage)
    
    def _activatePlugin(self):
        """ switches current page to plugin page """
        self._setBtnDefault()
        self.pluginSetBtn.setActiveStyle(self.HIGH_LIGHT)
        self.settingStack.setCurrentWidget(self.PluginPage)
    
    def _activateSystemSet(self):
        self._setBtnDefault()
        self.systemSetBtn.setActiveStyle(self.HIGH_LIGHT)
        self.settingStack.setCurrentWidget(self.SysPage)
    
    def _setBtnDefault(self):
        """ private function that sets the default style of the buttons on the page """
        self.transcibeSetBtn.setDefaultStyle()
        self.pluginSetBtn.setDefaultStyle()
        self.systemSetBtn.setDefaultStyle()
        self.engineSetBtn.setDefaultStyle()
    
    def colorchange(self):
        self.transcibeSetBtn.addOtherStyle(STYLE_DATA.StyleSheet.onlyBottomBorder)
        self.engineSetBtn.addOtherStyle(STYLE_DATA.StyleSheet.onlyBottomBorder)
        self.systemSetBtn.addOtherStyle(STYLE_DATA.StyleSheet.onlyBottomBorder)
        self.pluginSetBtn.addOtherStyle(STYLE_DATA.StyleSheet.onlyBottomBorder)
        self.transcibeSetBtn.colorChange(STYLE_DATA.Color.GREYDARK)
        self.engineSetBtn.colorChange(STYLE_DATA.Color.GREYDARK)
        self.systemSetBtn.colorChange(STYLE_DATA.Color.GREYDARK)
        self.pluginSetBtn.colorChange(STYLE_DATA.Color.GREYDARK)
        self.HIGH_LIGHT = STYLE_DATA.Color.HIGHLIGHT
  
    def fontchange(self):
        self.transcibeSetBtn.fontChange(STYLE_DATA.FontSize.BTN)
        self.engineSetBtn.fontChange(STYLE_DATA.FontSize.BTN)
        self.systemSetBtn.fontChange(STYLE_DATA.FontSize.BTN)
        self.pluginSetBtn.fontChange(STYLE_DATA.FontSize.BTN)