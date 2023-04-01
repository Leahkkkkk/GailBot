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
from typing import Dict, List
from view.config.Style import FontSize,FontFamily, Color, Dimension
from view.Signals import ProfileSignals
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

class RequiredSettingPage(QWidget):
    """ class for the required settings page """
    def __init__(self, signal: ProfileSignals, *args, **kwargs) -> None:
        """ initializes the page """
        super().__init__(*args, **kwargs)
        self.logger = makeLogger("F")
        self.signal = signal
        self.plugins = []
        self._initWidget()
        self._initLayout()

    def setValue(self, data: Dict[str, Dict]):
        """ sets the value of data
        Args: data:dict: dictionary that is passed in to be updated
        """
        try:
            self.engineForm.setValue(data["engine_setting"])
            self.pluginForm.setValue(data["plugin_setting"])
        except:
            raise ValueError("Set Required Setting Data Error")
    
    def getValue(self) -> dict:
        """ gets the value of data """
        try:
            setting = dict()
            setting["engine_setting"] = self.engineForm.getValue()
            setting["plugin_setting"] = self.pluginForm.getValue()
            return setting 
        except Exception as e:
            self.logger.error(e, exc_info=e)
            raise ValueError("Get Required Setting Data Error")
        
    def _initWidget(self):
        """ initializes the widgets on the page """
        # top page text 
        self.label = Label(
            Text.engineSettingHeader, FontSize.HEADER2, FontFamily.MAIN )
        self.description = Label(
            Text.engineSettingCaption,FontSize.DESCRIPTION, FontFamily.MAIN )
     
        self.selectSettings = ComboBox()
        self.selectSettings.setFixedSize(QSize(Dimension.BTNWIDTH, Dimension.BTNHEIGHT))
        
        # main form area
        self.engineForm = EngineSettingForm.EngineSettingForm()
        self.pluginForm = PluginForm.PluginForm()
        
        # buttom button
        self.createBtn = ColoredBtn (
            Text.newProfileBtn, Color.SECONDARY_BUTTON
        )
        self.deleteBtn = ColoredBtn (
            Text.deleteBtn, Color.CANCEL_QUIT
        )
        self.editBtn = ColoredBtn (
            Text.saveBtn, Color.PRIMARY_BUTTON
        )
    
    def _initLayout(self):
        """ initializes the layout of the page """
        self.layout = QVBoxLayout()
        self.buttonContainer = QWidget()
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setSpacing(Dimension.MEDIUM_SPACING)
        self.buttonContainer.setLayout(self.buttonLayout)
        self.buttonLayout.addWidget(self.createBtn)
        self.buttonLayout.addWidget(self.editBtn)
        self.buttonLayout.addWidget(self.deleteBtn)
        self.setLayout(self.layout)
        self.layout.addWidget(self.label, alignment=center)
        self.layout.addWidget(self.description, alignment=center)
        self.layout.addWidget(self.selectSettings, alignment=center)
        self.layout.addWidget(self.buttonContainer, alignment=center)
        self.layout.addWidget(self.engineForm, alignment=center)
        self.layout.addWidget(self.pluginForm, alignment=center)
        self.layout.addStretch()
        self.layout.addWidget(self.buttonContainer, alignment=center)

    def _connectSignal(self):
        """ connects profileSignal upon button clicks """
        self.selectSettings.currentTextChanged.connect(self.getProfile)
        self.editBtn.clicked.connect(self.updateProfile)
        self.deleteBtn.clicked.connect(self.deleteProfile)
        self.createBtn.clicked.connect(self.createProfileHandler) 
    
    def addAvailableSetting(self, profileKeys: List[str]):
        """ add a list of profile keys """
        self.selectSettings.addItems(profileKeys)
    
    def getProfile(self, profileName:str):
        """ sends the request to database to get profile data  """
        self.signal.get.emit(profileName)
    
    def updateProfile(self):
        """ updates the new profile setting """
        try:
            newSetting = self.getValue()
            self.logger.info(newSetting)
            profileKey = self.selectSettings.currentText()
            self.signal.edit.emit((profileKey, newSetting))
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("updating profile", str(e)))
       
    def deleteProfile(self):
        """ sends the delete signal to delete the profile"""
        profileName = self.selectSettings.currentText()
        ConfirmBox(Text.confirmDelete + profileName, 
                lambda: self.signal.delete.emit(self.selectSettings.currentText()))
    
    def deleteProfileConfirmed(self, deleted: bool):
        """ if deleted, remove the current setting name from available setting"""
        if deleted:
            self.selectSettings.removeItem(self.selectSettings.currentIndex())
    
    
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
    
    def createProfileHandler(self):
        createNewSettingTab = CreateNewSetting(self.plugins)
        createNewSettingTab.signals.newSetting.connect(
            lambda profile: self.signal.post.emit(profile))
        createNewSettingTab.exec()
    
    def addPluginSuite(self, suite: str):
        self.plugins.append(suite)
    
    def loadProfile(self, profile:tuple):
        """ loads the profile data to be presented onto the table """
        try:
            self.logger.info(profile)
            key, data = profile 
            self.selectSettings.setCurrentText(key)
            self.setValue(data)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("loading profile content", str(e)))
    