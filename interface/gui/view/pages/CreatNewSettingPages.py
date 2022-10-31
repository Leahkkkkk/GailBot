import tomli
from asyncio.log import logger
from typing import Dict, List

from util.Logger import makeLogger
from view.widgets.Button import ColoredBtn
from view.widgets.Label import Label
from view.widgets.TabPage import TabPage
from view.widgets.MultipleCombo import ToggleCombo, UserForm
from view.widgets.InputBox import InputBox
from view.widgets.MsgBox import WarnBox
from view.components.RequiredSet import OutPutFormat
from view.widgets.TextForm import TextForm
from view.pages.PluginPage import PluginPage
from view.pages.PostSetPage import PostSetPage
from view.style.Background import initBackground
from view.style.styleValues import Color, FontSize,Dimension, FontFamily



from PyQt6.QtWidgets import (
    QComboBox, 
    QVBoxLayout)
from PyQt6.QtCore import QSize, Qt, pyqtSignal, QObject

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
        self._initConfig()
        self._initWidget()
        self._initLayout()
    
    def getData(self) -> str:
        """ return the user's input of profile name """
        return self.profileName.value()
        
    def _initWidget(self):
        """ initialize the widget """
        self.header = Label("Profile Name", 
            self.config["fontSizes"]["HEADER3"], 
            FontFamily.MAIN)
        self.profileName = InputBox(
            "", 
            False, 
            labelSize = self.config["fontSizes"]["HEADER3"])
        self.confirmBtn = ColoredBtn(
            "Start", 
            self.config["colors"]["GREEN"])
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
        
    def _initConfig(self):
        """ TODO: make loading tomli from the top level """
        with open("controller/interface.toml", mode="rb") as fp:
            self.config = tomli.load(fp)
    
class ChooseEngine(TabPage):
    def __init__(self, engines:List[str], *args, **kwargs) -> None:
        """ page with a combobox that allows user to choose setting engine 

        Args:
            engines (List[str]): a list of engine that user can choose from
        """
        super().__init__(*args, **kwargs)
        self._initConfig()
        self.engines = engines
        self._initWidget()
        self._initLayout()
    
    def getData(self) -> str:
        """ get the user's current selection of setting profile """
        return self.mainCombo.currentText()
        
    def _initWidget(self):
        """ initialize the widget """
        self.title = Label(
            "Select Speech-to-text Engine", 
            self.config["fontSizes"]["HEADER3"], 
            FontFamily.MAIN)
        self.mainCombo = QComboBox(self)
        self.mainCombo.setFixedSize(QSize(400,70))
        self.mainCombo.addItem("select speech engine")
        self.mainCombo.addItems(self.engines)
        self.mainCombo.currentIndexChanged.connect(self._nextPage)
        self.mainCombo.activated.connect(self._nextPage)
        
    def _initLayout(self):
        """ initialize the layout """
        self.verticallayout = QVBoxLayout()
        self.setLayout(self.verticallayout)
        self.verticallayout.addStretch()
        self.verticallayout.addWidget(
            self.title, 
            alignment=Qt.AlignmentFlag.AlignHCenter)
        self.verticallayout.addWidget(
            self.mainCombo,
            alignment=Qt.AlignmentFlag.AlignHCenter)
        self.verticallayout.addStretch()
 
    def _nextPage(self, idx=None):
        """ event handler to ge to next page """
        if idx != 0:
            self.signals.nextPage.emit()
    
    def _initConfig(self):
        with open("controller/interface.toml", mode="rb") as fp:
            self.config = tomli.load(fp)
         
class BasicSetting(TabPage):
    def __init__(self, *args, **kwargs) -> None:
        """ path with input fields for user to define basic setting
        """
        super().__init__(*args, **kwargs)
        self._initConfig()
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
            self.config["fontSizes"]["HEADER3"], 
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
            self.config["colors"]["GREEN"])
        self.confirmBtn.setFixedSize(Dimension.BGBUTTON)
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
    
    def _initConfig(self):
        with open("controller/interface.toml", mode="rb") as fp:
            self.config = tomli.load(fp)

class EngineSetting(TabPage):
    def __init__(self, data, *args, **kwargs) -> None:
        """ a page with form about enegine setting """
        super().__init__(*args, **kwargs)
        self._initConfig()
        self.verticallayout = QVBoxLayout()
        self.setLayout(self.verticallayout)
        self.header = Label(
            "Speech to text settings", 
            self.config["fontSizes"]["HEADER3"], 
            FontFamily.MAIN)
        self.verticallayout.addWidget(
            self.header, 
            alignment=Qt.AlignmentFlag.AlignHCenter)
        self.mainForm = ToggleCombo(data, showBasicSet=False)
        self.verticallayout.addWidget(self.mainForm)
        self.confirmBtn = ColoredBtn("confirm", self.config["colors"]["GREEN"])
        self.confirmBtn.clicked.connect(self._confirmHandler)
        self.confirmBtn.setFixedSize(Dimension.BGBUTTON)
        self.verticallayout.addWidget(self.confirmBtn, alignment=bottomRight)
    
    def _confirmHandler(self):
        self.signals.nextPage.emit()
        print (self.mainForm.getValue())
    
    def newForm(self,data):
        """ for initializing different setting form for different engines """
        self.verticallayout.removeWidget(self.mainForm)
        self.verticallayout.removeWidget(self.confirmBtn)
        self.mainForm.deleteLater()
        self.mainForm = ToggleCombo(data, showBasicSet=False)
        self.verticallayout.addWidget(self.mainForm)
        self.verticallayout.addWidget(self.confirmBtn, alignment=bottomRight)
        
    def getData(self) -> Dict[str, dict]:
        return self.mainForm.getValue()

    def _initConfig(self):
        with open("controller/interface.toml", mode="rb") as fp:
            self.config = tomli.load(fp)
    

class OutPutFormatSetting(TabPage):
    def __init__(self, data:dict, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._initConfig()
        self.mainForm = OutPutFormat(data)
        self.verticallayout = QVBoxLayout()
        self.setLayout(self.verticallayout)
        self.header = Label(
            "Output format settings", 
            self.config["fontSizes"]["HEADER2"], 
            FontFamily.MAIN)
        self.verticallayout.addWidget(
            self.header, 
            alignment=hcenter)
        self.verticallayout.addWidget(self.mainForm)
        self.confirmBtn = ColoredBtn(
            "confirm", 
            self.config["colors"]["GREEN"])
        self.confirmBtn.setFixedSize(Dimension.BGBUTTON)
        self.confirmBtn.clicked.connect(lambda: self.signals.nextPage.emit())
        self.verticallayout.addStretch()
        self.verticallayout.addWidget(
            self.confirmBtn, 
            alignment=bottomRight)
        
    def getData(self):
        return self.mainForm.getValue()

    def _initConfig(self):
        with open("controller/interface.toml", mode="rb") as fp:
            self.config = tomli.load(fp)
     

class PostTranscribeSetting(TabPage):
    def __init__(self, data:dict, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.mainForm = PostSetPage(data)
        self.confirmBtn = ColoredBtn("confirm", Color.GREEN)
        self.confirmBtn.clicked.connect(lambda: self.signals.nextPage.emit())
        self.confirmBtn.setFixedSize(Dimension.BGBUTTON)

        
        self.verticallayout = QVBoxLayout()
        self.setLayout(self.verticallayout)
        self.verticallayout.addWidget(self.mainForm)
        self.verticallayout.addWidget(
            self.confirmBtn, 
            alignment=Qt.AlignmentFlag.AlignRight)
        
    def getData(self):
        mylogger.info(self.mainForm.getValue())
        return self.mainForm.getValue() 

    def _initConfig(self):
        with open("controller/interface.toml", mode="rb") as fp:
            self.config = tomli.load(fp)
            
class PluginSetting(TabPage):
    def __init__(self, data, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.mainForm = PluginPage(data)
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

        
        
