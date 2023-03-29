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
from typing import List

from view.config.Style import Color, Dimension
from view.config.Text import ProfilePageText as Text
from view.config.Style import FontSize 
from view.config.Style import StyleSheet as STYLE 
from view.config.Text import ProfileSettingForm as Form 
from gbLogger import makeLogger

from view.Signals import ProfileSignals
from view.pages import (
    RequiredSettingPage, 
    PluginPage
)
from view.util.ErrorMsg import  ERR
from view.widgets import (
    ColoredBtn,
    BorderBtn,
    ComboBox, 
    SideBar,
    WarnBox,
    ConfirmBox 
)

from view.components.CreateNewSettingTab import CreateNewSetting
from view.components.PluginDialog import PluginDialog
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
class ProfileSettingPage(QWidget):
    """ class for settings page """
    def __init__(
        self, 
        signals: ProfileSignals,
        *args, 
        **kwargs) -> None:
        """ initializes class """
        super().__init__(*args, **kwargs)
        self.setState : SET_STATE = SET_STATE.REQUIRED
        self.signals = signals
        self.plugins = list(Form.Plugins)
        self.logger = makeLogger("F")
        self._initWidget()
        self._initLayout()
        self._connectSignal()
        self._initStyle()
        self._initDimension()
    
    def addAvailableSetting(self, profileKeys: List[str], pluginSuites: List[str]):
        """ add a list of profile keys """
        self.selectSettings.addItems(profileKeys)
        self.RequiredSetPage.pluginForm.addPluginSuites(pluginSuites)
         
    def _initWidget(self):
        """ initializes widgets"""
        self.sideBar = SideBar()
        self.selectSettings = ComboBox()
        self.cancelBtn = ColoredBtn(
            Text.cancelBtn, Color.CANCEL_QUIT)
        self.saveBtn = ColoredBtn(
            Text.saveBtn, Color.SECONDARY_BUTTON)
        self.newSetBtn = ColoredBtn(
            Text.newProfileBtn,Color.PRIMARY_BUTTON)
        self.requiredSetBtn = BorderBtn(
            Text.reuquiredSetBtn, Color.GREYDARK, FontSize.BTN, 0, STYLE.onlyTopBorder)
        self.pluginBtn = BorderBtn(
            Text.pluginSetBtn, Color.GREYDARK, FontSize.BTN, 0, STYLE.onlyBottomBorder)
        self.settingStack = QStackedWidget(self)
        self.RequiredSetPage = RequiredSettingPage.RequiredSettingPage()
        self.PluginPage = PluginPage.PluginPage()
        self.selectSettings.setCurrentIndex(0)     
        self.placeHolder = QWidget()
        self.settingStack.addWidget(self.placeHolder)
        self.settingStack.addWidget(self.RequiredSetPage)
        self.settingStack.addWidget(self.PluginPage)
        self.settingStack.setCurrentWidget(self.RequiredSetPage)
    
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
        self.sidebarTopLayout.addWidget(self.selectSettings)
        self.sidebarTopLayout.addWidget(self.requiredSetBtn)
        self.sidebarTopLayout.addWidget(self.pluginBtn)
        self.sidebarTopLayout.setSpacing(0)
        self.sideBar.addWidget(self.topSelectionContainer)
        self.sideBar.addWidget(self.newSetBtn)
        self.sideBar.addWidget(self.saveBtn)
        self.sideBar.addWidget(self.cancelBtn)
        self.sideBar.addStretch()
        self.sideBar.addFooter() 
        self.horizontalLayout.addWidget(self.sideBar)
        self.horizontalLayout.addWidget(self.settingStack)
        self.settingStack.setContentsMargins(0,0,0,0)
   
    def _connectSignal(self):
        """ connects signals upon button clicks """
        self.requiredSetBtn.clicked.connect(self._activeRequiredSet)
        self.pluginBtn.clicked.connect(self._activatePlugin)
        self.selectSettings.currentTextChanged.connect(self._getProfile)
        self.newSetBtn.clicked.connect(self._addNew)
        self.saveBtn.clicked.connect(self.updateProfile)
        self.RequiredSetPage.deleteBtn.clicked.connect(self._deleteProfile)
  
    def _activeRequiredSet(self):
        """ switches current page from post transcription settings page to required settings page """
        self._setBtnDefault()
        self.newSetBtn.setText(Text.newProfileBtn)
        self.setState = SET_STATE.REQUIRED
        self.selectSettings.show()
        self.saveBtn.show()
        self.requiredSetBtn.setActiveStyle(Color.HIGHLIGHT)
        self.settingStack.setCurrentWidget(self.RequiredSetPage)
    
    def _activatePlugin(self):
        """ switches current page to plugin page """
        self._setBtnDefault()
        self.newSetBtn.setText(Text.newPluginBtn)
        self.setState = SET_STATE.PLUGIN
        self.selectSettings.hide()
        self.saveBtn.hide()
        self.pluginBtn.setActiveStyle(Color.HIGHLIGHT)
        self.settingStack.setCurrentWidget(self.PluginPage)
    
    def _setBtnDefault(self):
        """ private function that sets the default style of the buttons on the page """
        self.requiredSetBtn.setDefaultStyle()
        self.pluginBtn.setDefaultStyle()
    
    def _initStyle(self):
        """ initializes the style of the setting stack """
        self.settingStack.setObjectName(STYLE.settingStackID)
        self.settingStack.setStyleSheet(STYLE.settingStack)
    
    def _initDimension(self):
        """ initializes the dimensions of the buttons on the page """
        self.requiredSetBtn.setFixedWidth(Dimension.LBTNWIDTH)
        self.pluginBtn.setFixedWidth(Dimension.LBTNWIDTH)
   
    def _getProfile(self, profileName:str):
        """ sends the request to database to get profile data  """
        self.signals.get.emit(profileName)
        
    def _postNewProfile(self, profile: tuple):
        """ sends the request to database to post a new profile data """
        self.signals.post.emit(profile)
        
    def _deleteProfile(self):
        """ sends the delete signal to delete the profile"""
        profileName = self.selectSettings.currentText()
        ConfirmBox(Text.confirmDelete + profileName, 
                   lambda: self.signals.delete.emit(self.selectSettings.currentText()))
         
    def deleteProfileConfirmed(self, deleted: bool):
        """ if deleted, remove the current setting name from available setting"""
        if deleted:
            self.selectSettings.removeItem(self.selectSettings.currentIndex())
        
    def _addNew(self):
        """ opens a pop up window for user to create new setting profile """
        if self.setState == SET_STATE.REQUIRED:
            createNewSettingTab = CreateNewSetting(self.plugins)
            createNewSettingTab.signals.newSetting.connect(self._postNewProfile)
            createNewSettingTab.exec()
        elif self.setState == SET_STATE.PLUGIN:
            """ opens a pop up window to add plugin """
            pluginDialog = PluginDialog(self.signals)
            pluginDialog.exec()
        
    def loadProfile(self, profile:tuple):
        """ loads the profile data to be presented onto the table """
        try:
            self.logger.info(profile)
            key, data = profile 
            self.selectSettings.setCurrentText(key)
            self.RequiredSetPage.setValue(data)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("loading profile content", str(e)))
            
    def addProfile (self, profileName:str):
        """ adding a new profile option to the settings page 
        Arg:
            profileName(str): name to be added as profile name to the new profile entry
        """
        try:
            self.selectSettings.addItem(profileName)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("adding profile", str(e)))
    
        
    def updateProfile(self):
        """ updates the new profile setting """
        try:
            newSetting = self.RequiredSetPage.getValue()
            self.logger.info(newSetting)
            profileKey = self.selectSettings.currentText()
            self.signals.edit.emit((profileKey, newSetting))
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("updating profile", str(e)))

    
    
    def addPluginHandler(self, plugin:str):
        """ adds a new plugin to the plugin handler
        Args: plugin(str): name of the plugin to be added
        """
        self.RequiredSetPage.pluginForm.addPluginSuite(plugin)