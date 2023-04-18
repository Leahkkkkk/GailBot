
from typing import List 

from gbLogger import makeLogger
from view.config.Text import CreateNewProfileTabText as Text
from view.config.Style import STYLE_DATA
from view.pages.CreateNewProfilePages import (
    SettingName,
    ChooseEngine, 
    PluginSetting
)
from view.widgets import Tab, WarnBox
from view.util.ErrorMsg import ERR
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QDialog
)

from PyQt6.QtCore import QObject, pyqtSignal, QSize

class Signals(QObject):
    """ a signal object to send new setting data values """
    addProfile = pyqtSignal(tuple)
    editProfile = pyqtSignal(tuple)

class CreateNewProfile(QDialog):
    def __init__(self, engines: List[str], plugins: List[str]) -> None:
        super().__init__()
        self.signals = Signals()
        self.logger = makeLogger("F")
        self.profileName   = SettingName()
        self.engineSetting = ChooseEngine(engines)
        self.pluginSetting = PluginSetting(plugins)
        self.newSettingData = dict()
        mainTab = Tab(
            Text.WindowTitle,
            {
                Text.TabHeader1: self.profileName,
                Text.TabHeader2: self.engineSetting,
                Text.TabHeader3: self.pluginSetting
            }
        )
        mainTab.changePageBtn.finishBtn.clicked.connect(self._postSetting)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(mainTab)
        self.logger.info("")
        
    def _postSetting(self):
        setting = dict()
        profileName = self.profileName.getData()
        setting["engine_setting_name"] = self.engineSetting.getData()
        setting["plugin_setting"] = self.pluginSetting.getData()
        try:
            self.logger.info(setting)
            self.signals.addProfile.emit((profileName, setting))
            self.close()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("creating new profile", str(e)))
            
            
class EditProfile(QDialog):
    def __init__(self, setting, engines, plugins, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        name, data = setting 
        self.profileName  = name 
        self.signals = Signals()
        self.logger = makeLogger("F")
        self.engineSetting = ChooseEngine(engines)
        self.pluginSetting = PluginSetting(plugins)
        self.newSettingData = dict()
        mainTab = Tab(
            self.profileName,
            {
                Text.TabHeader2: self.engineSetting,
                Text.TabHeader3: self.pluginSetting
            }
        )
        mainTab.changePageBtn.finishBtn.clicked.connect(self._postSetting)
        self.engineSetting.setData(data["engine_setting_name"])
        self.pluginSetting.setData(data["plugin_setting"])
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(mainTab)
        self.logger.info("")

    def _postSetting(self):
        data = dict()
        data["engine_setting_name"] = self.engineSetting.getData()
        data["plugin_setting"] = self.pluginSetting.getData()
        try:
            self.logger.info(data)
            self.signals.editProfile.emit((self.profileName, data))
            self.close()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("creating new engine setting", str(e)))