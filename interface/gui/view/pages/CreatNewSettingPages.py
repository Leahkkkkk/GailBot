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
from view.style.Background import initBackground
from view.style.styleValues import Color, FontSize,Dimension


from PyQt6.QtWidgets import (
    QComboBox, QVBoxLayout, QWidget)
from PyQt6.QtCore import QSize, Qt, pyqtSignal, QObject

mylogger = makeLogger("Frontend")

class settingSignals(QObject):
    engineSet = pyqtSignal()
    

class ProfileName (TabPage):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.verticallayout = QVBoxLayout()
        self.setLayout(self.verticallayout)
        self.profileName = InputBox("Profile Name",False, labelSize=FontSize.HEADER2)
        self.confirmBtn = ColoredBtn("Start", Color.GREEN)
        self.verticallayout.addStretch()
        self.verticallayout.addWidget(self.profileName,alignment=Qt.AlignmentFlag.AlignHCenter)
        self.verticallayout.addWidget(self.confirmBtn,alignment=Qt.AlignmentFlag.AlignHCenter)
        self.verticallayout.addStretch()
        self.confirmBtn.clicked.connect(self._confirm)
        self.confirmBtn.setFixedSize(Dimension.BGBUTTON)
    
    def _confirm(self):
        if self.profileName.value() == "":
            warn = WarnBox("The profile name cannot be empty")
        else:
            self.signals.nextPage.emit()
            self.signals.goToNextPage.emit()
        
    def getData(self):
        return self.profileName.value()
    
    
class ChooseEngine(TabPage):
    def __init__(self, engines:List[str], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.verticallayout = QVBoxLayout()
        self.setLayout(self.verticallayout)
        self.title = Label("Select Speech-to-text Engine", FontSize.HEADER2)
        self.mainCombo = QComboBox(self)
        self.mainCombo.setFixedSize(QSize(400,70))
        self.mainCombo.addItems(engines)
        self.verticallayout.addStretch()
        self.verticallayout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.verticallayout.addWidget(self.mainCombo,alignment=Qt.AlignmentFlag.AlignHCenter)
        self.verticallayout.addStretch()
        self.signals.nextPage.emit()
        self.mainCombo.currentIndexChanged.connect(self._nextPage)
        self.mainCombo.activated.connect(self._nextPage)
        
    def _nextPage(self, idx=None):
        self.signals.nextPage.emit()
    
    def getData(self) -> str:
        return self.mainCombo.currentText()
         

class BasicSetting(TabPage):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.mainWidget = UserForm()
        self.verticallayout = QVBoxLayout()
        self.setLayout(self.verticallayout)
        self.verticallayout.addWidget(self.mainWidget, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.confirmBtn = ColoredBtn("confirm", Color.GREEN,Qt.AlignmentFlag.AlignRight)
        self.confirmBtn.clicked.connect(self._confirm)
        self.verticallayout.addWidget(self.confirmBtn)
        self.verticallayout.addStretch()
    
    def _confirm(self):
        res = self.mainWidget.getValue()
        if res[0] == "" or res[1] == "":
            warn = WarnBox("Please enter user name and password")
        else:
            self.signals.nextPage.emit()
            self.signals.goToNextPage.emit()
            
    def getData(self) -> Dict[str, str]:
        info = self.mainWidget.getValue()
        return {"username": info[0], "password":info[1]}

class EngineSetting(TabPage):
    def __init__(self, data, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.verticallayout = QVBoxLayout()
        self.setLayout(self.verticallayout)
        self.mainForm = ToggleCombo(data, showBasicSet=False)
        self.verticallayout.addWidget(self.mainForm)
        self.confirmBtn = ColoredBtn("confirm", Color.GREEN)
        self.confirmBtn.clicked.connect(self._confirm)
        self.verticallayout.addWidget(self.confirmBtn)
    
    def _confirm(self):
        self.signals.nextPage.emit()
        print (self.mainForm.getValue())
        
    
    def getData(self) -> Dict[str, dict]:
        print (self.mainForm.getValue())
        return self.mainForm.getValue()
    

class OutPutFormatSetting(TabPage):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.mainForm = OutPutFormat(self)
        self.verticallayout = QVBoxLayout()
        self.setLayout(self.verticallayout)
        self.verticallayout.addWidget(self.mainForm)
        self.confirmBtn = ColoredBtn("confirm", Color.GREEN)
        self.confirmBtn.clicked.connect(self._confirm)
        self.verticallayout.addWidget(self.confirmBtn)
    
    def _confirm(self):
        self.signals.nextPage.emit()

    def getData(self):
        return self.mainForm.getValue()
     

class PostTranscribeSetting(TabPage):
    def __init__(self, data:dict, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.mainForm = TextForm(data)
        self.verticallayout = QVBoxLayout()
        self.setLayout(self.verticallayout)
        self.verticallayout.addWidget(self.mainForm)
        self.signals.nextPage.emit()
        self.confirmBtn = ColoredBtn("confirm", Color.GREEN)
        self.confirmBtn.clicked.connect(self._confirm)
        self.verticallayout.addWidget(self.confirmBtn)
    def _confirm(self):
        self.signals.close.emit()
       
    def getData(self):
        mylogger.info(self.mainForm.getValue())
        return self.mainForm.getValue() 
     