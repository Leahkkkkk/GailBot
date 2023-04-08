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

from enum import Enum
from typing import List, Dict, List, Tuple
from view.config.Style import STYLE_DATA
from view.config.Text import ProfilePageText as Text
from view.config.Style import StyleSheet as STYLE 
from view.Signals import GlobalStyleSignal
from gbLogger import makeLogger

from view.Signals import ProfileSignals, PluginSignals
from view.pages import (
    TranscriptionSetPage, 
    PluginPage,
    SysSetPage
)
from view.util.ErrorMsg import  ERR
from view.widgets import (
    ColoredBtn,
    BorderBtn,
    ComboBox, 
    SideBar,
)

from view.components.CreateNewSettingTab import CreateNewSetting
from view.components.UploadPluginDialog import UploadPlugin
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
        profileSignal: ProfileSignals,
        pluginSignal: PluginSignals,
        *args, 
        **kwargs) -> None:
        """ initializes class """
        super().__init__(*args, **kwargs)
        self.profileSignal = profileSignal 
        self.pluginSignal = pluginSignal
        self.logger = makeLogger("F")
        self._initWidget()
        self._initLayout()
        self._connectSignal()
    
    def addAvailableSetting(self, profileKeys: List[str]):
        """ add a list of profile keys """
        self.TranscriptionSetPage.addAvailableSetting(profileKeys)
     
    def _initWidget(self):
        self.HIGH_LIGHT = STYLE_DATA.Color.HIGHLIGHT
        """ initializes widgets"""
        self.sideBar = SideBar()
        # button on the sidebar
        self.transcibeSetBtn = BorderBtn(
            Text.reuquiredSetBtn, STYLE_DATA.Color.GREYDARK, STYLE_DATA.FontSize.BTN, 0, 
            STYLE.onlyBottomBorder, width=STYLE_DATA.Dimension.LBTNWIDTH)
       
        self.pluginSetBtn = BorderBtn(
            Text.pluginSetBtn, STYLE_DATA.Color.GREYDARK, STYLE_DATA.FontSize.BTN, 0, 
            STYLE.onlyBottomBorder, width=STYLE_DATA.Dimension.LBTNWIDTH)
        
        self.systemSetBtn = BorderBtn(
            Text.sysSetBtn, STYLE_DATA.Color.GREYDARK, STYLE_DATA.FontSize.BTN, 0, 
            STYLE.onlyBottomBorder, width=STYLE_DATA.Dimension.LBTNWIDTH)
        
        self.cancelBtn = ColoredBtn(Text.cancelBtn, STYLE_DATA.Color.CANCEL_QUIT)
        self.settingStack = QStackedWidget(self)
        self.TranscriptionSetPage = TranscriptionSetPage.TranscriptionSetPage(self.profileSignal)
        self.PluginPage = PluginPage.PluginPage(self.pluginSignal)
        self.SysPage = SysSetPage.SystemSettingPage()
        self.settingStack.addWidget(self.TranscriptionSetPage)
        self.settingStack.addWidget(self.PluginPage)
        self.settingStack.addWidget(self.SysPage)
        self.settingStack.setCurrentWidget(self.TranscriptionSetPage)
         
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
        self.sidebarTopLayout.addWidget(self.pluginSetBtn)
        self.sidebarTopLayout.addWidget(self.systemSetBtn)
        self.sidebarTopLayout.setSpacing(0)
        self.sideBar.addTopWidget(self.topSelectionContainer)
        self.sideBar.addMidWidget(self.cancelBtn)
        self.horizontalLayout.addWidget(self.sideBar)
        self.horizontalLayout.addWidget(self.settingStack)
        self.settingStack.setContentsMargins(0,0,0,0)
   
    def _connectSignal(self):
        """ connects profileSignal upon button clicks """
        self.transcibeSetBtn.clicked.connect(self._activeRequiredSet)
        self.pluginSetBtn.clicked.connect(self._activatePlugin)
        self.systemSetBtn.clicked.connect(self._activateSystemSet)
        self.PluginPage.signal.pluginAdded.connect(self.TranscriptionSetPage.addPluginSuite)
        self.PluginPage.signal.pluginDeleted.connect(self.TranscriptionSetPage.deletePlugin)
        STYLE_DATA.signal.changeColor.connect(self.colorchange)
        STYLE_DATA.signal.changeFont.connect(self.fontchange)
        
    def _activeRequiredSet(self):
        """ switches current page from post transcription settings page to required settings page """
        self._setBtnDefault()
        self.transcibeSetBtn.setActiveStyle(self.HIGH_LIGHT)
        self.settingStack.setCurrentWidget(self.TranscriptionSetPage)
    
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
    
    def colorchange(self, colormode = None):
        self.transcibeSetBtn.addOtherStyle(STYLE_DATA.StyleSheet.onlyBottomBorder)
        self.systemSetBtn.addOtherStyle(STYLE_DATA.StyleSheet.onlyBottomBorder)
        self.pluginSetBtn.addOtherStyle(STYLE_DATA.StyleSheet.onlyBottomBorder)
        self.transcibeSetBtn.colorChange(STYLE_DATA.Color.GREYDARK)
        self.systemSetBtn.colorChange(STYLE_DATA.Color.GREYDARK)
        self.pluginSetBtn.colorChange(STYLE_DATA.Color.GREYDARK)
        self.HIGH_LIGHT = STYLE_DATA.Color.HIGHLIGHT
  
    def fontchange(self, fontchange = None):
        self.transcibeSetBtn.fontChange(STYLE_DATA.FontSize.BTN)
        self.systemSetBtn.fontChange(STYLE_DATA.FontSize.BTN)
        self.pluginSetBtn.fontChange(STYLE_DATA.FontSize.BTN)
    
    def deleteProfileConfirmed(self, deleted: bool):
        """ if deleted, remove the current setting name from available setting"""
        # self.TranscriptionSetPage.deleteProfileConfirmed(deleted) 
        pass
        
    def loadProfile(self, profile:tuple):
        """ loads the profile data to be presented onto the table """
        # self.TranscriptionSetPage.loadProfile(profile)
        pass
         
    def addProfile (self, profileName:str):
        """ adding a new profile option to the settings page 
        Arg:
            profileName(str): name to be added as profile name to the new profile entry
        """
        self.TranscriptionSetPage.createSucceed(profileName) 
        
    def addPluginHandler(self, pluginSuite: Tuple[str, Dict[str, str]]):
        name , info = pluginSuite
        # self.TranscriptionSetPage.addPluginSuite(name)
        self.PluginPage.addPluginSuiteConfirmed(pluginSuite)