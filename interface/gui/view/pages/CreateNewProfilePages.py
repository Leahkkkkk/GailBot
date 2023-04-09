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

from view.config.Text import CreateNewProfilePageText as Text 
from view.config.Text import EngineForm as Form 
from gbLogger import makeLogger

from view.util.ErrorMsg import ERR, WARN
from view.widgets.Button import ColoredBtn
from view.widgets.Label import Label
from view.widgets.TabPage import TabPage
from view.widgets.Form.TextInput import TextInput
from view.widgets.MsgBox import WarnBox
from view.components import EngineSettingForm
from view.components import PluginForm
from PyQt6.QtWidgets import  QVBoxLayout
from PyQt6.QtCore import (
    Qt, 
    pyqtSignal, 
    QObject
)

#### controlling style changes 
from view.config.Style import (
    FontSize, 
    Color, 
    StyleSheet, 
    FontFamily,
    Asset, 
    ASSET_DICT, 
    STYLE_DICT,  
    FONT_DICT,
    COLOR_DICT)  
from view.Signals import GlobalStyleSignal

FONT_SIZE = FontSize
COLOR = Color
STYLESHEET = StyleSheet
ASSET = Asset

def colorchange(colormode):
    global COLOR 
    global STYLESHEET
    global ASSET
    COLOR = COLOR_DICT[colormode]
    STYLESHEET = STYLE_DICT[colormode]
    ASSET = ASSET_DICT[colormode]

def changeFont(fontsize):
    global FONT_SIZE
    FONT_SIZE = FONT_DICT[fontsize]

GlobalStyleSignal.changeColor.connect(colorchange)
GlobalStyleSignal.changeFont.connect(changeFont)
######################

hCenter = Qt.AlignmentFlag.AlignHCenter
vCenter = Qt.AlignmentFlag.AlignVCenter
center = hCenter | vCenter
bottomRight = Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignBottom
top = Qt.AlignmentFlag.AlignTop

class settingSignals(QObject):
    engineSet = pyqtSignal()
    
class ProfileName (TabPage):
    """ page with an input field to allow user add the profile name """
    def __init__(self, *args, **kwargs) -> None:
        """" initializes page """
        super().__init__(*args, **kwargs)
        self.logger = makeLogger("F")
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
        self.header = Label(Text.profileName, 
            FONT_SIZE.HEADER2, 
            FontFamily.MAIN)
        self.profileName = TextInput(
            "", 
            labelSize = FONT_SIZE.HEADER3,
            vertical=False)
        self.confirmBtn = ColoredBtn(
            "Start", 
            COLOR.SECONDARY_BUTTON)
        self.confirmBtn.clicked.connect(self._confirmHandler)

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
        self.verticalLayout.addWidget(
            self.confirmBtn,
            alignment= center)
        self.verticalLayout.addStretch()
    
    def _confirmHandler(self):
        """ event handler for confirm button  """
        if self.profileName.value == "":
            WarnBox(WARN.EMPTY_PROFILE_NAME)
        else:
            self.signals.nextPage.emit()
            self.signals.goToNextPage.emit()
    
class EngineSetting(TabPage):
    """ class for engine setting form """
    def __init__(self,  *args, **kwargs) -> None:
        """ initializes page """
        super().__init__(*args, **kwargs)
        self.logger = makeLogger("F")
        self.verticallayout = QVBoxLayout()
        self.setLayout(self.verticallayout)
        self.header = Label(
            Text.engineSettingHeader, 
            FONT_SIZE.HEADER2, 
            FontFamily.MAIN)
        self.verticallayout.addWidget(
            self.header, 
            alignment=Qt.AlignmentFlag.AlignHCenter)
        self.mainForm = EngineSettingForm.EngineSettingForm()
        self.verticallayout.addWidget(self.mainForm)
        self.verticallayout.addStretch()
        self.confirmBtn = ColoredBtn(Text.cofirmBtn, COLOR.SECONDARY_BUTTON)
        self.confirmBtn.clicked.connect(self._confirmHandler)
        self.verticallayout.addWidget(self.confirmBtn, alignment=bottomRight)
        # self.confirmBtn.clicked.connect(lambda: self.signals.close.emit())
    
    def _confirmHandler(self):
        """" handles if user should be able to go to the next page in popup """
        self.signals.nextPage.emit()
    
    def getData(self) -> Dict[str, dict]:
        """ gets current value of key in dictionary """
        try:
            return self.mainForm.getValue()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("getting setting data", str(e)))


class PluginSetting(TabPage):
    """ class for the plugin settings tab """
    def __init__(self, plugins, *args, **kwargs) -> None:
        """ initializes tab """
        super().__init__(*args, **kwargs)
        self.header = Label(
            Text.pluginSettingHeader, 
            FONT_SIZE.HEADER2, 
            FontFamily.MAIN)
        self.mainForm = PluginForm.PluginForm()
        self.mainForm.addPluginSuites(plugins)
        self.confirmBtn = ColoredBtn(Text.cofirmBtn, COLOR.SECONDARY_BUTTON)
        self.confirmBtn.clicked.connect(lambda: self.signals.close.emit())
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.verticalLayout.addWidget(self.header, alignment=center)
        self.verticalLayout.addWidget(self.mainForm)
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(
            self.confirmBtn,
            alignment=Qt.AlignmentFlag.AlignRight)
        self.logger = makeLogger("F")
  
    def getData(self):
        """ gets current value of data """
        try:
            return self.mainForm.getValue()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("getting plugin data", str(e)))
            
            
            

        
        
