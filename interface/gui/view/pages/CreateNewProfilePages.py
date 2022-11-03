import tomli
from typing import Dict

from util.Config import Color, FontSize
from util.Logger import makeLogger
from view.widgets.Button import ColoredBtn
from view.widgets.Label import Label
from view.widgets.TabPage import TabPage
from view.widgets.MultipleCombo import UserForm
from view.widgets.InputBox import InputBox
from view.widgets.MsgBox import WarnBox
from view.components import OutputFormatForm, SettingEngineForm
from view.pages.PluginPage import PluginPage
from view.pages.PostSetPage import PostSetPage
from view.style.styleValues import Dimension, FontFamily

from PyQt6.QtWidgets import  QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal, QObject

mylogger = makeLogger("Frontend")
hcenter = Qt.AlignmentFlag.AlignHCenter
vcenter = Qt.AlignmentFlag.AlignVCenter
center = hcenter | vcenter
bottomRight = Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignBottom

class settingSignals(QObject):
    engineSet = pyqtSignal()
    
class ProfileName (TabPage):
    """ page with an input field to allow user add the profile name """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._initWidget()
        self._initLayout()
    
    def getData(self) -> str:
        """ return the user's input of profile name """
        return self.profileName.value()
        
    def _initWidget(self):
        """ initialize the widget """
        self.header = Label("Profile Name", 
            FontSize.HEADER3, 
            FontFamily.MAIN)
        self.profileName = InputBox(
            "", 
            False, 
            labelSize = FontSize.HEADER3)
        self.confirmBtn = ColoredBtn(
            "Start", 
            Color.GREEN)
        self.confirmBtn.clicked.connect(self._confirmHandler)

    def _initLayout(self):
        """ initialize the layout """
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
            warn = WarnBox("The profile name cannot be empty")
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
        self.verticallayout.addWidget(
            self.header, 
            alignment=hcenter)
        self.verticallayout.addStretch()
        self.verticallayout.addWidget(
            self.mainWidget, 
            alignment=hcenter)
        self.confirmBtn = ColoredBtn(
            "confirm", 
            Color.GREEN)
        self.confirmBtn.clicked.connect(self._confirmHandler)
        self.verticallayout.addWidget(
            self.confirmBtn,
            alignment=bottomRight)
        self.verticallayout.addStretch()
    
    
    def _confirmHandler(self):
        """ confirm button handler """
        res = self.mainWidget.getValue()
        if res[0] == "" or res[1] == "":
            warn = WarnBox("Please enter user name and password")
        else:
            self.signals.nextPage.emit()
            self.signals.goToNextPage.emit()
    


class EngineSetting(TabPage):
    def __init__(self,  *args, **kwargs) -> None:
        """ a page with form about enegine setting """
        super().__init__(*args, **kwargs)

        self.verticallayout = QVBoxLayout()
        self.setLayout(self.verticallayout)
        self.header = Label(
            "Speech to text settings", 
            FontSize.HEADER3, 
            FontFamily.MAIN)
        self.verticallayout.addWidget(
            self.header, 
            alignment=Qt.AlignmentFlag.AlignHCenter)
        self.mainForm = SettingEngineForm.SettingEngineForm(showBasicSet=False)
        self.verticallayout.addWidget(self.mainForm)
        self.confirmBtn = ColoredBtn("confirm", Color.GREEN)
        self.confirmBtn.clicked.connect(self._confirmHandler)
        self.verticallayout.addWidget(self.confirmBtn, alignment=bottomRight)
    
    def _confirmHandler(self):
        self.signals.nextPage.emit()
        print (self.mainForm.getValue())
    
    def getData(self) -> Dict[str, dict]:
        return self.mainForm.getValue()

class OutPutFormatSetting(TabPage):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.mainForm = OutputFormatForm.OutPutFormat()
        self.verticallayout = QVBoxLayout()
        self.setLayout(self.verticallayout)
        self.header = Label(
            "Output format settings", 
            FontSize.HEADER2, 
            FontFamily.MAIN)
        self.verticallayout.addWidget(
            self.header, 
            alignment=hcenter)
        self.verticallayout.addWidget(self.mainForm)
        self.confirmBtn = ColoredBtn(
            "confirm", 
            Color.GREEN)
        self.confirmBtn.clicked.connect(lambda: self.signals.nextPage.emit())
        self.verticallayout.addStretch()
        self.verticallayout.addWidget(
            self.confirmBtn, 
            alignment=bottomRight)
        
    def getData(self):
        return self.mainForm.getValue()

     
class PostTranscribeSetting(TabPage):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.mainForm = PostSetPage()
        self.confirmBtn = ColoredBtn("confirm", Color.GREEN)
        self.confirmBtn.clicked.connect(lambda: self.signals.nextPage.emit())
        self.verticallayout = QVBoxLayout()
        self.setLayout(self.verticallayout)
        self.verticallayout.addWidget(self.mainForm)
        self.verticallayout.addWidget(
            self.confirmBtn, 
            alignment=Qt.AlignmentFlag.AlignRight)
        
    def getData(self):
        mylogger.info(self.mainForm.getValue())
        return self.mainForm.getValue() 
            
class PluginSetting(TabPage):
    def __init__(self, plugins, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.mainForm = PluginPage(plugins)
        self.confirmBtn = ColoredBtn("confirm", Color.GREEN)
        self.confirmBtn.clicked.connect(lambda: self.signals.close.emit())
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.verticalLayout.addWidget(self.mainForm)
        self.verticalLayout.addWidget(
            self.confirmBtn,
            alignment=Qt.AlignmentFlag.AlignRight)
        
    def getData(self):
        return self.mainForm.getValue()

        
        
