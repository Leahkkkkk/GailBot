from typing import List 

from view.widgets.Button import ColoredBtn
from view.widgets.Label import Label
from view.widgets.TabPage import TabPage
from view.widgets.MultipleCombo import ToggleCombo, UserForm
from view.widgets.InputBox import InputBox
from view.components.RequiredSet import OutPutFormat
from view.components.PostSet import PostSet
from view.style.Background import initBackground
from view.style.styleValues import Color, FontSize


from PyQt6.QtWidgets import (
    QComboBox, QVBoxLayout, QWidget)
from PyQt6.QtCore import QSize, Qt

class ProfileName (TabPage):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.verticallayout = QVBoxLayout()
        self.setLayout(self.verticallayout)
        self.profileName = InputBox("Profile Name")
        self.confirmBtn = ColoredBtn("confirm", Color.GREEN)
        self.verticallayout.addWidget(self.profileName,alignment=Qt.AlignmentFlag.AlignTop)
        self.verticallayout.addWidget(self.confirmBtn,alignment=Qt.AlignmentFlag.AlignTop)
        self.verticallayout.addStretch()
        self.confirmBtn.clicked.connect(self._confirm)
    
    def _confirm(self):
        self.signals.nextPage.emit()
        
    def _getProfileName(self):
        pass
    
    
class ChooseEngine(TabPage):
    def __init__(self, engines:List[str], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.verticallayout = QVBoxLayout()
        self.setLayout(self.verticallayout)
        self.title = Label("Select Speech-to-text Engine", FontSize.HEADER3)
        self.mainCombo = QComboBox(self)
        self.mainCombo.addItems(engines)
        self.verticallayout.addWidget(self.title)
        self.verticallayout.addWidget(self.mainCombo)
        self.verticallayout.addStretch()
        self.mainCombo.currentTextChanged.connect(self._changeEngine)
        self.signals.nextPage.emit()
        self.mainCombo.currentIndexChanged.connect(lambda: self.signals.nextPage.emit())
    def _changeEngine(self):
        pass 

class BasicSetting(TabPage):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.mainWidget = UserForm()
        self.verticallayout = QVBoxLayout()
        self.setLayout(self.verticallayout)
        self.verticallayout.addWidget(self.mainWidget)
        self.confirmBtn = ColoredBtn("confirm", Color.GREEN)
        self.confirmBtn.clicked.connect(self._confirm)
        self.verticallayout.addWidget(self.confirmBtn)
        self.verticallayout.addStretch()
    
    def _confirm(self):
        self.signals.nextPage.emit()

class EngineSetting(TabPage):
    def __init__(self, data, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.verticallayout = QVBoxLayout()
        self.setLayout(self.verticallayout)
        self.mainForm = ToggleCombo(data)
        self.verticallayout.addWidget(self.mainForm)
        self.confirmBtn = ColoredBtn("confirm", Color.GREEN)
        self.confirmBtn.clicked.connect(self._confirm)
        self.verticallayout.addWidget(self.confirmBtn)
    
    def _confirm(self):
        self.signals.nextPage.emit()
    
    def _getData(self):
        pass
    

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

    def _getData(self):
        pass
     

class PostTranscribeSetting(TabPage):
    def __init__(self, data:dict, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.mainForm = PostSet(data)
        self.verticallayout = QVBoxLayout()
        self.setLayout(self.verticallayout)
        self.verticallayout.addWidget(self.mainForm)
        self.signals.nextPage.emit()
        self.confirmBtn = ColoredBtn("confirm", Color.GREEN)
        self.confirmBtn.clicked.connect(self._confirm)
        self.verticallayout.addWidget(self.confirmBtn)
    def _confirm(self):
        self.signals.close.emit()
    

    def _getData(self):
        pass 
     