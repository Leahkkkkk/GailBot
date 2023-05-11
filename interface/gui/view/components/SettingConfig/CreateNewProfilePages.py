'''
File: CreateNewProfilePages.py
Project: GailBot GUI
File Created: Friday, 4th November 2022 1:01:27 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Saturday, 5th November 2022 7:22:34 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: implementation of pages for user to create new profile 
'''

from typing import Dict
from view.signal.interface import DataSignal
from view.Request import Request
from view.config.Text import CreateNewProfilePageText as Text 
from view.config.Text import ENGINE_FORM as Form 
from gbLogger import makeLogger


from view.util.ErrorMsg import ERR, WARN

from view.widgets.Label import Label
from view.widgets.TabPage import TabPage
from view.widgets.Form.TextInput import TextInput
from view.widgets.TextForm import TextForm
from view.widgets.MsgBox import WarnBox
from view.widgets.ComboBox import ComboBox

from .PluginForm import PluginForm
from ..SettingDetail import SettingDisplay
from PyQt6.QtWidgets import  QVBoxLayout, QStackedWidget
from PyQt6.QtCore import (
    Qt, 
    pyqtSignal, 
    QObject, 
)

#### controlling style changes 
from view.config.Style import (
    FontFamily,
    STYLE_DATA)

######################

hCenter = Qt.AlignmentFlag.AlignHCenter
vCenter = Qt.AlignmentFlag.AlignVCenter
center = hCenter | vCenter
bottomRight = Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignBottom
top = Qt.AlignmentFlag.AlignTop

class settingSignals(QObject):
    engineSet = pyqtSignal()
    
class SettingName (TabPage):
    """ page with an input field to allow user add the profile name """
    def __init__(self, title = Text.profileName, *args, **kwargs) -> None:
        """" initializes page """
        super().__init__(blockNext=True, *args, **kwargs)
        self.title = title
        self.logger = makeLogger()
        self._initWidget()
        self._initLayout()
    
    def getData(self) -> str:
        """ return the user's input of profile name """
        try:
            self.logger.info("")
            return self.profileName.value
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("reading profile name", str(e)))
        
    def _initWidget(self):
        """ initializes the widgets """
        self.header = Label(self.title, 
            STYLE_DATA.FontSize.HEADER2, 
            FontFamily.MAIN)
        self.profileName = TextInput(
            "", 
            labelSize = STYLE_DATA.FontSize.HEADER3,
            vertical=False)
        self.profileName.inputField.textChanged.connect(self._textChanged)
        self.profileName.inputField.setFixedWidth(STYLE_DATA.Dimension.INPUTWIDTH * 2)
        
    def _initLayout(self):
        """ initializes the layout """
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(
            self.header, 
            alignment=center)
        self.verticalLayout.addWidget(
            self.profileName,
            alignment = center)
        self.verticalLayout.addStretch()
    
    def _textChanged(self):
        """ event handler for confirm button  """
        name = self.profileName.value
        if name and len(name.replace(" ", "")) != 0 :
            self.signals.nextPage.emit()
            self.signals.goToNextPage.emit()
    
class SelectEngine(TabPage):
    """ class for engine setting form """
    def __init__(self, *args, **kwargs) -> None:
        """ initializes page """
        super().__init__(*args, **kwargs)
        self.logger = makeLogger()
        self._initWidget()
    
    def _initWidget(self):
        self.verticallayout = QVBoxLayout()
        self.setLayout(self.verticallayout)
        self.verticallayout.addStretch()
        # header area 
        self.header = Label(
            Text.engineSettingHeader, 
            STYLE_DATA.FontSize.HEADER2, 
            FontFamily.MAIN)
        
        self.verticallayout.addWidget(
            self.header, 
            alignment=Qt.AlignmentFlag.AlignHCenter)
        
        ## form stack
        self.selectEngine = ComboBox()
        self.selectEngine.addItems(["Google", "Whisper", "Watson"])
        self.selectEngine.setFixedWidth(STYLE_DATA.Dimension.INPUTWIDTH * 2)
        self.verticallayout.addWidget(
            self.selectEngine, 
            alignment=Qt.AlignmentFlag.AlignHCenter)
        self.verticallayout.addStretch()
        
    def getData(self) -> Dict[str, str]:
        """ gets current value of key in dictionary """
        try:
            return self.selectEngine.currentText().lower()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("getting setting data", str(e)))

    def setData(self, engine):
        try:
            self.selectEngine.setCurrentText(engine)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("displaying setting data", str(e)))

class EngineForm(TabPage):
    def __init__(self,*args, **kwargs) -> None:
        super().__init__(blockNext=False, *args, **kwargs)
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)
        self.mainStack = QStackedWidget()
        
        self.currentForm = None 
        self.formDict = {
            "google" : TextForm(Form.google),
            "watson" : TextForm(Form.watson),
            "whisper": TextForm(Form.whisper)
        }
        
        self.header = Label("Speech to Text Engine Setting", STYLE_DATA.FontSize.HEADER4, STYLE_DATA.FontFamily.MAIN)
        self._layout.addWidget(self.header, alignment=center)
        self._layout.addWidget(self.mainStack)
        for form in self.formDict.values():
            self.mainStack.addWidget(form)
    
    def setForm(self, engine):
        self.currentForm = self.formDict[engine.lower()]
        self.mainStack.setCurrentWidget(self.currentForm)
    
    def getData(self):
        return self.mainStack.currentWidget().getValue()

    def setData(self, settingData):
        self.currentForm = self.formDict[settingData["engine"].lower()]
        self.mainStack.setCurrentWidget(self.currentForm)
        self.currentForm.setValues(settingData)

class PluginSetting(TabPage):
    """ class for the plugin settings tab """
    def __init__(self, plugins, *args, **kwargs) -> None:
        """ initializes tab """
        super().__init__(*args, **kwargs)
        self.header = Label(
            Text.pluginSettingHeader, 
            STYLE_DATA.FontSize.HEADER2, 
            FontFamily.MAIN)
        self.mainForm = PluginForm()
        self.mainForm.addPluginSuites(plugins)
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.verticalLayout.addWidget(self.header, alignment=center)
        self.verticalLayout.addWidget(self.mainForm)
        self.verticalLayout.addStretch()
        self.logger = makeLogger()
    
    def getData(self):
        """ gets current value of data """
        try:
            return self.mainForm.getValue()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("getting plugin data", str(e)))
    
    def setData(self, data):
        try:
            self.mainForm.setValue(data)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("displaying plugin data", str(e)))
            
class ChooseEngine(TabPage):
    def __init__(self, engineSettings, engineSignal: DataSignal, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.logger = makeLogger()
        self.verticallayout = QVBoxLayout()
        self.setLayout(self.verticallayout)
        self.header = Label(
            Text.engineSettingHeader,
            STYLE_DATA.FontSize.HEADER2,
            FontFamily.MAIN
        )     
        self.engineSignal = engineSignal 
        self.selectEngines = ComboBox()
        self.selectEngines.setFixedWidth(STYLE_DATA.Dimension.WIN_MIN_WIDTH//2)
        self.engineDisplay = SettingDisplay()
        self.selectEngines.addItems(engineSettings)
        self.verticallayout.addWidget(self.header, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.verticallayout.addWidget(self.selectEngines, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.verticallayout.addWidget(self.engineDisplay)
        self.verticallayout.addStretch()
        self.selectEngines.currentTextChanged.connect(self.requestSetting)
        self.requestSetting(self.selectEngines.currentText())
    

    def getData(self) -> str:
        try:
            return self.selectEngines.currentText()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("reading engine setting name", str(e)))
    
    def setData(self, data):
        try:
            self.selectEngines.setCurrentText(data)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("displaying engine setting", str(e)))

    def displayData(self, data):
        try:
            name, setting = data 
            self.engineDisplay.setData(setting)
        except Exception as e:
            self.logger.error(e, exc_info=e)
    
    def requestSetting(self, name:str):
        self.engineSignal.getRequest.emit(
            Request(data=name, succeed=self.displayData)
        ) 
  