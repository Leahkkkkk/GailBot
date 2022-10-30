import tomli

from view.widgets import Label,TextForm, SideBar, SettingForm
from view.style.Background import initBackground
from view.style.styleValues import FontFamily, FontSize
from model.dummySettingData import dummySystemSettingForm
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QStackedWidget
from PyQt6.QtCore import Qt


class SystemSettingPage(QWidget):
    """ post-transcription settings page """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.data = dummySystemSettingForm
        initBackground(self)
        self._initConfig()
        self._initWidget()
        self._initLayout()
        self._initStyle()
        
    def _initWidget(self):
        """initialize widgets"""
        self.sidebar = SideBar.SideBar()
        header = "System Setting"
        caption = "These settings are applied for system setting"
        self.Mainstack = QStackedWidget()
        self.SysSet = SettingForm.SettingForm(header, self.data, caption)
        self.Mainstack.addWidget(self.SysSet)
        
    def _initLayout(self):
        """ initialize layout"""

        self.horizontalLayout = QHBoxLayout()
        self.setLayout(self.horizontalLayout)
        """ add widget to layout """
        self.horizontalLayout.addWidget(self.sidebar)
        self.horizontalLayout.addWidget(self.Mainstack)

    def _initStyle(self):
        self.Mainstack.setObjectName("sysForm")
        """ add this to an external stylesheet"""
        self.Mainstack.setStyleSheet("#sysForm {border: none; border-left:0.5px solid grey;}")
   
    def setValue(self, values:dict):
        self.SysSet.setValue(values)
    
    def getValue(self) -> dict:
        return self.SysSet.getValue()

        
    def _initConfig(self):
        with open("controller/interface.toml", mode="rb") as fp:
            self.config = tomli.load(fp)
    