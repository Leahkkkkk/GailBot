'''
File: RequiredSetPage.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 11:08:43 am
Modified By:  Siara Small  & Vivian Li
-----
'''

""" NOTE: currently replaced by Profile Setting Page """
from typing import Dict, List, Tuple
from view.config.Style import STYLE_DATA
from view.Signals import DataSignal
from view.Request import Request
from view.config.Text import ProfilePageText as Text
from gbLogger import makeLogger
from view.components import EngineSettingForm
from view.components.CreateNewSettingTab import CreateNewSetting
from view.components import PluginForm
from view.widgets import ColoredBtn, Label, ComboBox, WarnBox, ConfirmBox
from view.util.ErrorMsg import ERR  
from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout
)
from PyQt6.QtCore import Qt, QSize

center = Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter

class TranscriptionSetPage(QWidget):
    """ class for the required settings page """
    def __init__(self, *args, **kwargs) -> None:
        """ initializes the page """
        super().__init__(*args, **kwargs)
        self.logger = makeLogger("F")
        self.signal = DataSignal()
        self.plugins = []
        self._initWidget()
        self._initLayout()
        self._connectSignal()

    def setValue(self, data: Dict[str, Dict]):
        """ sets the value of data
        Args: data:dict: dictionary that is passed in to be updated
        """
        try:
            self.engineForm.setCurrentText(data["engine_setting"])
            self.pluginForm.setValue(data["plugin_setting"])
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("setting transcription setting data", str(e)))

            raise ValueError("Set Required Setting Data Error")
    
    def getValue(self) -> dict:
        """ gets the value of data """
        try:
            setting = dict()
            setting["engine_setting"] = self.engineForm.currentText()
            setting["plugin_setting"] = self.pluginForm.getValue()
            return setting 
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("getting transcription setting data", str(e)))
        
    def _initWidget(self):
        """ initializes the widgets on the page """
        # top page text 
        self.label = Label(
            Text.engineSettingHeader, STYLE_DATA.FontSize.HEADER2,  STYLE_DATA.FontFamily.MAIN )
        self.description = Label(
            Text.engineSettingCaption, STYLE_DATA.FontSize.DESCRIPTION,  STYLE_DATA.FontFamily.MAIN )
     
        self.selectSettings = ComboBox()
        self.selectSettings.setFixedSize(QSize(STYLE_DATA.Dimension.BTNWIDTH,  STYLE_DATA.Dimension.BTNHEIGHT))
        
        # main form area
        self.engineLabel = Label(Text.engineSetting, STYLE_DATA.FontSize.HEADER3)
        self.engineForm = ComboBox()
        
        self.pluginLabel= Label(Text.pluginSuiteSetting, STYLE_DATA.FontSize.HEADER3)
        self.pluginForm = PluginForm.PluginForm()
        
        # buttom button
        self.createBtn = ColoredBtn (Text.newProfileBtn,  STYLE_DATA.Color.PRIMARY_BUTTON)
        self.deleteBtn = ColoredBtn (Text.deleteBtn,  STYLE_DATA.Color.CANCEL_QUIT)
        self.editBtn = ColoredBtn (Text.saveBtn,  STYLE_DATA.Color.PRIMARY_BUTTON)
    
    def _initLayout(self):
        """ initializes the layout of the page """
        self.layout = QVBoxLayout()
        self.buttonContainer = QWidget()
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setSpacing( STYLE_DATA.Dimension.MEDIUM_SPACING)
        self.buttonContainer.setLayout(self.buttonLayout)
        self.buttonLayout.addWidget(self.createBtn)
        self.buttonLayout.addWidget(self.editBtn)
        self.buttonLayout.addWidget(self.deleteBtn)
        self.selectSettings.setFixedWidth( STYLE_DATA.Dimension.FORMWIDTH // 2)
        self.setLayout(self.layout)
        self.layout.addWidget(self.label, alignment=center)
        self.layout.addWidget(self.description, alignment=center)
        self.layout.addWidget(self.selectSettings, alignment=center)
        self.layout.addWidget(self.buttonContainer, alignment=center)
        self.layout.addWidget(self.engineLabel)
        self.layout.addWidget(self.engineForm)
        self.layout.addWidget(self.pluginLabel)
        self.layout.addWidget(self.pluginForm)
        self.layout.addStretch()
        self.layout.addWidget(self.buttonContainer, alignment=center)

    def _connectSignal(self):
        """ connects profileSignal upon button clicks """
        self.selectSettings.currentTextChanged.connect(self.getProfile)
        self.editBtn.clicked.connect(self.editProfile)
        self.deleteBtn.clicked.connect(self.deleteProfile)
        self.createBtn.clicked.connect(self.createProfile) 
        STYLE_DATA.signal.changeColor.connect(self.colorChange)
        STYLE_DATA.signal.changeFont.connect(self.fontChange)
    
    def colorChange(self, colormode = None):
        self.createBtn.colorChange(STYLE_DATA.Color.PRIMARY_BUTTON)
        self.editBtn.colorChange(STYLE_DATA.Color.PRIMARY_BUTTON)
        self.deleteBtn.colorChange(STYLE_DATA.Color.CANCEL_QUIT)
    
    def fontChange(self, fontmode = None):
        self.label.fontChange(STYLE_DATA.FontSize.HEADER2)
        self.description.fontChange(STYLE_DATA.FontSize.DESCRIPTION)
        self.pluginLabel.fontChange(STYLE_DATA.FontSize.HEADER3)
        self.engineLabel.fontChange(STYLE_DATA.FontSize.HEADER3)
    
    def addAvailableSetting(self, profileKeys: List[str]):
        """ add a list of profile keys """
        self.selectSettings.addItems(profileKeys)
    
    # function that will send request to get data
    def getProfile(self, profileName:str):
        """ sends the request to database to get profile data  """
        self.signal.getRequest.emit(
            Request(data = profileName, succeed = self.getSucceed))
    
    def editProfile(self):
        ConfirmBox(Text.confirmEdit, confirm=self.editProfileConfirmed)
    
    def editProfileConfirmed(self):
        """ updates the new profile setting """
        try:
            newSetting = self.getValue()
            self.logger.info(newSetting)
            profileKey = self.selectSettings.currentText()
            self.signal.editRequest.emit(
                Request(data = (profileKey, newSetting), succeed = self.editSucceed))
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("updating profile", str(e)))
       
    def deleteProfile(self):
        """ sends the delete signal to delete the profile"""
        profileName = self.selectSettings.currentText()
        ConfirmBox(Text.confirmDelete + profileName, 
        lambda: self.signal.deleteRequest.emit(
            Request(data = self.selectSettings.currentText(), succeed = self.deleteSucceed)))
    
    def createProfile(self):
        createNewSettingTab = CreateNewSetting(self.plugins)
        createNewSettingTab.signals.newSetting.connect(
            lambda profile: self.signal.postRequest.emit(
            Request(data = profile, succeed = self.createSucceed)))
        createNewSettingTab.exec()
    
    # continuation function when request succeeds
    def deleteSucceed(self, profielName: str):
        """ if deleted, remove the current setting name from available setting"""
        self.logger.info(f"delete profile {profielName} succeeds")
        try:
            self.signal.deleteSucceed.emit(profielName)
            self.selectSettings.removeItem(self.selectSettings.currentIndex())
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("deleting profile", str(e)))
    
    def createSucceed (self, profileName:str):
        """ adding a new profile option to the settings page 
        Arg:
            profileName(str): name to be added as profile name to the new profile entry
        """
        self.logger.info(f"create profile {profileName} succeeds")
        try:
            self.selectSettings.addItem(profileName)
            self.signal.addSucceed.emit(profileName)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("adding profile", str(e)))
    
    def editSucceed(self, profilename:str):
        self.logger.info("updating profile succeed")
    
    def getSucceed(self, profile: Tuple[str,Dict[str, Dict]]):
        """ loads the profile data to be presented onto the table """
        try:
            self.logger.info(profile)
            name, data = profile
            self.selectSettings.setCurrentText(name)
            self.setValue(data)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("loading profile content", str(e)))
    
    #### for adding plugin
    def addPluginSuite(self, suite: str):
        self.plugins.append(suite)
        self.pluginForm.addPluginSuite(suite)
    
    def deletePlugin(self, suite: str):
        self.plugins.remove(suite)
        self.pluginForm.deletePluginSuite(suite)