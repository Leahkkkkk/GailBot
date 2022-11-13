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

from util.Style import Color, FontSize, FontFamily
from util.Text import CreateNewProfilePageText as Text 
from util.Logger import makeLogger

from view.widgets.Button import ColoredBtn
from view.widgets.Label import Label
from view.widgets.TabPage import TabPage
from view.widgets.MultipleCombo import UserForm
from view.widgets.InputBox import InputBox
from view.widgets.MsgBox import WarnBox
from view.components import OutputFormatForm, SpeechEngineForm
from view.pages.PluginPage import PluginPage
from view.pages.PostSetPage import PostSetPage
from view.widgets.Background import initPrimaryColorBackground

from PyQt6.QtWidgets import  QVBoxLayout
from PyQt6.QtCore import (
    Qt, 
    pyqtSignal, 
    QObject
)


hcenter = Qt.AlignmentFlag.AlignHCenter
vcenter = Qt.AlignmentFlag.AlignVCenter
center = hcenter | vcenter
bottomRight = Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignBottom

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
        return self.profileName.value()
        
    def _initWidget(self):
        """ initializes the widgets """
        self.header = Label(Text.profileName, 
            FontSize.HEADER3, 
            FontFamily.MAIN)
        self.profileName = InputBox(
            "", 
            False, 
            labelSize = FontSize.HEADER3)
        self.confirmBtn = ColoredBtn(
            "Start", 
            Color.SECONDARY_BUTTON)
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
        """ event hander for confirm button  """
        if self.profileName.value() == "":
            warn = WarnBox(Text.emptyNameMsg)
        else:
            self.signals.goToNextPage.emit()
        
          
class BasicSetting(TabPage):
    def __init__(self, *args, **kwargs) -> None:
        """ path with input fields for user to define basic setting
        """
        super().__init__(*args, **kwargs)
        self._initWidget()
        self._initLayout()
        
    def getData(self) -> Dict[str, str]:
        """ return a dictionary that stores the basic setting values

        Returns:
            Dict[str, str]: a dictionary that stores the basic setting values
        """
        info = self.mainWidget.getValue()
        return {"username": info[0], "password":info[1]}
    
    def _initWidget(self):
        """ initialize the widget """
        self.mainWidget = UserForm()
        self.header = Label(
            "Basic settings", 
            FontSize.HEADER3, 
            FontFamily.MAIN)
    
    def _initLayout(self):
        """ initialize the layout """
        self.verticallayout = QVBoxLayout()
        self.setLayout(self.verticallayout)
        self.verticallayout.addStretch()
        self.verticallayout.addWidget(self.header, alignment=hcenter)
        self.verticallayout.addWidget(self.mainWidget, alignment=hcenter)
        self.confirmBtn = ColoredBtn(
            Text.cofirmBtn, 
            Color.SECONDARY_BUTTON)
        self.confirmBtn.clicked.connect(self._confirmHandler)
        self.verticallayout.addWidget(
            self.confirmBtn,
            alignment=bottomRight)
        self.verticallayout.addStretch()
    
    
    def _confirmHandler(self):
        """ confirm button handler """
        res = self.mainWidget.getValue()
        if res[0] == "" or res[1] == "":
            warn = WarnBox(Text.emptyUserMsg)
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
            FontSize.HEADER3, 
            FontFamily.MAIN)
        self.verticallayout.addWidget(
            self.header, 
            alignment=Qt.AlignmentFlag.AlignHCenter)
        self.mainForm = SpeechEngineForm.SpeechEngineForm(showBasicSet=False)
        self.verticallayout.addWidget(self.mainForm)
        self.confirmBtn = ColoredBtn(Text.cofirmBtn, Color.SECONDARY_BUTTON)
        self.confirmBtn.clicked.connect(self._confirmHandler)
        self.verticallayout.addWidget(self.confirmBtn, alignment=bottomRight)
    
    def _confirmHandler(self):
        """" handles if user should be able to go to the next page in popup """
        self.signals.nextPage.emit()
        print (self.mainForm.getValue())
    
    def getData(self) -> Dict[str, dict]:
        """ gets current value of key in dictionary """
        return self.mainForm.getValue()

class OutPutFormatSetting(TabPage):
    """ class for the output of settings """
    def __init__(self, *args, **kwargs) -> None:
        """ initializes class """
        super().__init__(*args, **kwargs)
        self.mainForm = OutputFormatForm.OutPutFormat()
        self.verticallayout = QVBoxLayout()
        self.setLayout(self.verticallayout)
        self.header = Label(
            Text.outputSettingHeader, 
            FontSize.HEADER2, 
            FontFamily.MAIN)
        self.verticallayout.addWidget(
            self.header, 
            alignment=hcenter)
        self.verticallayout.addWidget(self.mainForm)
        self.confirmBtn = ColoredBtn(
            Text.cofirmBtn, 
            Color.SECONDARY_BUTTON)
        self.confirmBtn.clicked.connect(lambda: self.signals.nextPage.emit())
        self.verticallayout.addStretch()
        self.verticallayout.addWidget(
            self.confirmBtn, 
            alignment=bottomRight)
        
    def getData(self):
        """ gets current value of data """
        return self.mainForm.getValue()

     
class PostTranscribeSetting(TabPage):
    """ class for the post-transcription settings tab """
    def __init__(self, *args, **kwargs) -> None:
        """ initializes tab """
        super().__init__(*args, **kwargs)
        self.logger = makeLogger("F")
        self.mainForm = PostSetPage()
        self.confirmBtn = ColoredBtn(Text.cofirmBtn, Color.SECONDARY_BUTTON)
        self.confirmBtn.clicked.connect(lambda: self.signals.nextPage.emit())
        self.verticallayout = QVBoxLayout()
        self.setLayout(self.verticallayout)
        self.verticallayout.addWidget(self.mainForm)
        self.verticallayout.addWidget(
            self.confirmBtn, 
            alignment=Qt.AlignmentFlag.AlignRight)
        
    def getData(self):
        """ gets current value of data """
        self.logger.info(self.mainForm.getValue())
        return self.mainForm.getValue() 
            
class PluginSetting(TabPage):
    """ class for the plugin settings tab """
    def __init__(self, plugins, *args, **kwargs) -> None:
        """ initializes tab """
        super().__init__(*args, **kwargs)
        self.mainForm = PluginPage(plugins)
        self.confirmBtn = ColoredBtn(Text.cofirmBtn, Color.SECONDARY_BUTTON)
        self.confirmBtn.clicked.connect(lambda: self.signals.close.emit())
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.verticalLayout.addWidget(self.mainForm)
        self.verticalLayout.addWidget(
            self.confirmBtn,
            alignment=Qt.AlignmentFlag.AlignRight)
        initPrimaryColorBackground(self.mainForm.scrollContainer)
        
    def getData(self):
        """ gets current value of data """
        return self.mainForm.getValue()

        
        
