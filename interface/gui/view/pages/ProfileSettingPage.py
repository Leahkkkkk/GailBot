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


from typing import List

from util.Style import Color, Dimension
from util.Text import ProfilePageText as Text, About
from util.Style import FontSize as FS 
from util.Style import StyleSheet as SS 
from util.Text import ProfileSettingForm as Form 
from util.Text import Links
from util.Logger import makeLogger

from view.Signals import ProfileSignals
from view.pages import (
    RequiredSettingPage, 
    PostSettingPage, 
    PluginPage
)
from view.widgets import (
    Button, 
    Label, 
    ComboBox, 
    SideBar
)
from view.widgets.MsgBox import WarnBox
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

class ProfileSettingPage(QWidget):
    """ class for settings page """
    def __init__(
        self, 
        profilekeys:List[str],
        signals:ProfileSignals,
        *args, 
        **kwargs) -> None:
        """ initializes class """
        super().__init__(*args, **kwargs)
    
        self.signals = signals
        self.profilekeys = profilekeys
        self.plugins = list(Form.Plugins)
        self.logger = makeLogger("F")
        self._initWidget()
        self._initLayout()
        self._connectSignal()
        self._initStyle()
        self._initDimension()
    
    def _initWidget(self):
        """ initializes widgets"""
        self.sideBar = SideBar.SideBar()
        self.selectSettings = ComboBox.ComboBox()
        self.selectSettings.addItems(self.profilekeys)
        self.cancelBtn = Button.ColoredBtn(
            Text.cancelBtn, Color.CANCEL_QUIT)
        self.saveBtn = Button.ColoredBtn(
            Text.saveBtn, Color.SECONDARY_BUTTON)
        self.newProfileBtn = Button.ColoredBtn(
            Text.newProfileBtn,Color.PRIMARY_BUTTON)
        self.requiredSetBtn = Button.BorderBtn(
            Text.reuquiredSetBtn, Color.GREYDARK, FS.BTN, 0, SS.onlyTopBorder)
        # self.postSetBtn = Button.BorderBtn(
        #     Text.postSetBtn,Color.GREYDARK, FS.BTN, 0,SS.noSideBorder)
        self.GuideLink = Label.Label(Links.guideLinkSideBar, FS.LINK, link=True)
        self.newPluginBtn = Button.ColoredBtn(
            Text.newPluginBtn, Color.PRIMARY_BUTTON)
        self.pluginBtn = Button.BorderBtn(
            Text.pluginSetBtn, Color.GREYDARK, FS.BTN, 0, SS.onlyBottomBorder)
        self.versionLabel = Label.Label(About.version, FS.SMALL)
        self.copyRightLabel = Label.Label(About.copyRight, FS.SMALL)
        self.settingStack = QStackedWidget(self)
        self.RequiredSetPage = RequiredSettingPage.RequiredSettingPage()
        # self.PostSetPage = PostSettingPage.PostSettingPage()   
        self.PluginPage = PluginPage.PluginPage()
        self.selectSettings.setCurrentIndex(0)     
        self.placeHolder = QWidget()
        self.settingStack.addWidget(self.placeHolder)
        self.settingStack.addWidget(self.RequiredSetPage)
        # self.settingStack.addWidget(self.PostSetPage)
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
        # self.sidebarTopLayout.addWidget(self.postSetBtn)
        self.sidebarTopLayout.addWidget(self.pluginBtn)
        self.sidebarTopLayout.setSpacing(0)
        self.sideBar.addWidget(self.topSelectionContainer)
        # self.sideBar.addWidget(self.newPluginBtn)  NOTE: currently unused
        self.sideBar.addWidget(self.newProfileBtn)
        self.sideBar.addWidget(self.saveBtn)
        self.sideBar.addWidget(self.cancelBtn)
        self.sideBar.addStretch()
        self.sideBar.addWidget(self.GuideLink, alignment=bottom)
        self.sideBar.addWidget(self.versionLabel, alignment=bottom)
        self.sideBar.addWidget(self.copyRightLabel, alignment=bottom)
        self.horizontalLayout.addWidget(self.sideBar)
        self.horizontalLayout.addWidget(self.settingStack)
        self.settingStack.setContentsMargins(0,0,0,0)
   
    def _connectSignal(self):
        """ connects signals upon button clicks """
        # self.postSetBtn.clicked.connect(self._activatePostSet)
        self.requiredSetBtn.clicked.connect(self._activeRequiredSet)
        self.pluginBtn.clicked.connect(self._activatePlugin)
        self.selectSettings.currentTextChanged.connect(self._getProfile)
        self.newProfileBtn.clicked.connect(self.createNewSetting)
        self.saveBtn.clicked.connect(self.updateProfile)
        self.newPluginBtn.clicked.connect(self.addPluginRequest)
    
    # def _activatePostSet(self):
        """ switches current page from required settings page to post transcription settings page """
        # self._setBtnDefault()
        # self.postSetBtn.setActiveStyle(Color.HIGHLIGHT)
        # self.settingStack.setCurrentWidget(self.PostSetPage)
    
    def _activeRequiredSet(self):
        """ switches current page from post transcription settings page to required settings page """
        self._setBtnDefault()
        self.requiredSetBtn.setActiveStyle(Color.HIGHLIGHT)
        self.settingStack.setCurrentWidget(self.RequiredSetPage)
    
    def _activatePlugin(self):
        """ switches current page to plugin page """
        self._setBtnDefault()
        self.pluginBtn.setActiveStyle(Color.HIGHLIGHT)
        self.settingStack.setCurrentWidget(self.PluginPage)
    
    def _setBtnDefault(self):
        """ private function that sets the default style of the buttons on the page """
        # self.postSetBtn.setDefaultStyle()
        self.requiredSetBtn.setDefaultStyle()
        self.pluginBtn.setDefaultStyle()
    
    def _initStyle(self):
        """ initializes the style of the setting stack """
        self.settingStack.setObjectName(SS.settingStackID)
        self.settingStack.setStyleSheet(SS.settingStack)
    
    def _initDimension(self):
        """ initializes the dimensions of the buttons on the page """
        self.requiredSetBtn.setFixedWidth(Dimension.LBTNWIDTH)
        # self.postSetBtn.setFixedWidth(Dimension.LBTNWIDTH)
        self.pluginBtn.setFixedWidth(Dimension.LBTNWIDTH)
   
    def _getProfile(self, profileName:str):
        """ sends the request to database to get profile data  """
        self.signals.get.emit(profileName)
        
    def _postNewProfile(self, profile: tuple):
        """ sends the request to database to post a new profile data """
        self.signals.post.emit(profile)
    
    def createNewSetting(self):
        """ opens a pop up window for user to create new setting profile """
        createNewSettingTab = CreateNewSetting(self.plugins)
        createNewSettingTab.signals.newSetting.connect(self._postNewProfile)
        createNewSettingTab.exec()
        
    def loadProfile(self, profile:tuple):
        """ loads the profile data to be presented onto the table """
        try:
            self.logger.info(profile)
            key, data = profile 
            self.selectSettings.setCurrentText(key)
            # self.PostSetPage.setValue(data["PostTranscribe"])
            self.RequiredSetPage.setValue(data["engine_setting"])
            # self.PluginPage.setValue(data["Plugins"])
        except:
            WarnBox("An error occurred when loading the profile")
            
    def addProfile (self, profileName:str):
        """ adding a new profile option to the settings page 
        Arg:
            profileName(str): name to be added as profile name to the new profile entry
        """
        try:
            self.selectSettings.addItem(profileName)
        except: 
            WarnBox("An error occurred when adding the profile")
    
    def addPluginRequest(self):
        """ opens a pop up window to add plugin """
        pluginDialog = PluginDialog(self.signals)
        pluginDialog.exec()
    
    def addPluginHandler(self, plugin:str):
        """ adds a new plugin to the plugin handler
        Args: plugin(str): name of the plugin to be added
        """
        self.plugins.add(plugin)
        self.PluginPage.addNewPlugin(plugin)
        
    def updateProfile(self):
        """ updates the new profile setting """
        try:
            newSetting = dict()
            newSetting["engine_setting"] = self.RequiredSetPage.getValue()
            newSetting["plugin_setting"] = self.PluginPage.getValue()
            self.logger.info(newSetting)
            profileKey = self.selectSettings.currentText()
            self.signals.edit.emit((profileKey, newSetting))
        except:
            WarnBox("An error occurred when updating the profile")
