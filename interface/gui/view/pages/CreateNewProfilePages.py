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

from view.config.Style import Color, FontSize, FontFamily, Dimension
from view.config.Text import CreateNewProfilePageText as Text 
from view.config.Text import EngineSettingForm as Form 
from util.Logger import makeLogger

from view.widgets.Form.DependentComboBox import DependentCombo
from view.widgets.ScrollArea import ScrollArea
from view.widgets.Button import ColoredBtn
from view.widgets.Label import Label
from view.widgets.TabPage import TabPage
from view.widgets.Form.TextInput import TextInput
from view.widgets.MsgBox import WarnBox
from view.widgets.Background import initSecondaryColorBackground
from view.components import OutputFormatForm
from view.pages.PluginPage import PluginPage
from view.pages.PostSettingPage import PostSettingPage


from PyQt6.QtWidgets import  QVBoxLayout
from PyQt6.QtCore import (
    Qt, 
    pyqtSignal, 
    QObject
)


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
        except:
            self.logger.error("An error occurred when reading the profile name")
            WarnBox("An error occurred when reading the profile name")
        
    def _initWidget(self):
        """ initializes the widgets """
        self.header = Label(Text.profileName, 
            FontSize.HEADER2, 
            FontFamily.MAIN)
        self.profileName = TextInput(
            "", 
            labelSize = FontSize.HEADER3,
            vertical=False)
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
        """ event handler for confirm button  """
        if self.profileName.value == "":
            WarnBox(Text.emptyNameMsg)
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
            FontSize.HEADER2, 
            FontFamily.MAIN)
        self.verticallayout.addWidget(
            self.header, 
            alignment=Qt.AlignmentFlag.AlignHCenter)
        self.mainForm = DependentCombo(Form.Engine, "Speech to Text Engine")
        self.scrollArea  = ScrollArea()
        self.scrollArea.setWidget(self.mainForm)
        initSecondaryColorBackground(self.scrollArea)
        self.verticallayout.addWidget(self.scrollArea)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setMaximumHeight(Dimension.LARGEDIALOGHEIGHT//4 * 3)
        self.confirmBtn = ColoredBtn(Text.cofirmBtn, Color.SECONDARY_BUTTON)
        self.confirmBtn.clicked.connect(self._confirmHandler)
        self.verticallayout.addWidget(self.confirmBtn, alignment=bottomRight)
        self.confirmBtn.clicked.connect(lambda: self.signals.close.emit())
    
    def _confirmHandler(self):
        """" handles if user should be able to go to the next page in popup """
        self.signals.nextPage.emit()
    
    def getData(self) -> Dict[str, dict]:
        """ gets current value of key in dictionary """
        try:
            return self.mainForm.getValue()
        except:
            WarnBox("an error occurred when getting the form data")

class OutPutFormatSetting(TabPage):
    """ class for the output of settings """
    def __init__(self, *args, **kwargs) -> None:
        """ initializes class """
        super().__init__(*args, **kwargs)
        self.mainForm = OutputFormatForm.OutPutFormat()
        self.scrollArea  = ScrollArea()
        self.scrollArea.setWidget(self.mainForm)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setFixedHeight(Dimension.LARGEDIALOGHEIGHT//4 * 3)
        initSecondaryColorBackground(self.scrollArea)
        self.verticallayout = QVBoxLayout()
        self.setLayout(self.verticallayout)
        self.header = Label(
            Text.outputSettingHeader, FontSize.HEADER2, FontFamily.MAIN)
        self.verticallayout.addWidget(
            self.header, alignment=hCenter|top)
        self.verticallayout.addWidget(self.scrollArea)
        self.confirmBtn = ColoredBtn(
            Text.cofirmBtn, 
            Color.SECONDARY_BUTTON)
        self.confirmBtn.clicked.connect(lambda: self.signals.nextPage.emit())
        self.verticallayout.addWidget(
            self.confirmBtn, 
            alignment=bottomRight)
        
    def getData(self):
        """ gets current value of data """
        try:
            return self.mainForm.getValue()
        except:
            WarnBox("an error occurred when getting the form data")
            

class PostTranscribeSetting(TabPage):
    """ class for the post-transcription settings tab """
    def __init__(self, *args, **kwargs) -> None:
        """ initializes tab """
        super().__init__(*args, **kwargs)
        self.logger = makeLogger("F")
        self.mainForm = PostSettingPage()
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
        try:
            self.logger.info(self.mainForm.getValue())
            return self.mainForm.getValue() 
        except:
            WarnBox("an error occurred when getting the form data")
                
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
  
        
        
    def getData(self):
        """ gets current value of data """
        try:
            return self.mainForm.getValue()
        except:
            WarnBox("an error occurred when getting the form data")
            
            
            

        
        
