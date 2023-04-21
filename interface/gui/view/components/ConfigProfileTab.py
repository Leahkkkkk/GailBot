'''
File: ConfigProfileTab.py
Project: GailBot GUI
File Created: 2022/10/
Author: Siara Small  & Vivian Li
-----
Last Modified:2023/04/18
Modified By:  Siara Small  & Vivian Li
-----
Description: implement tab widget for creating profile setting and 
             edit existing profile setting 
'''

from typing import List 
from gbLogger import makeLogger
from view.config.Text import CreateNewProfileTabText as Text
from view.widgets.TabPage import TabDialog
from view.config.Style import STYLE_DATA
from view.pages.CreateNewProfilePages import (
    SettingName,
    ChooseEngine, 
    PluginSetting
)
from view.widgets import WarnBox
from view.util.ErrorMsg import ERR
from PyQt6.QtCore import QObject, pyqtSignal, QSize

class Signals(QObject):
    """ a signal object to send new setting data values """
    addProfile = pyqtSignal(tuple)
    editProfile = pyqtSignal(tuple)

class CreateNewProfile():
    def __init__(self, engines: List[str], plugins: List[str], engineSettingSignal) -> None:
        self.signals = Signals()
        self.logger = makeLogger("F")
        self.profileName   = SettingName()
        self.engineSetting = ChooseEngine(engines, engineSettingSignal)
        self.pluginSetting = PluginSetting(plugins)
        self.newSettingData = dict()
        self.mainTab = TabDialog(
            Text.WindowTitle,
            {
                Text.TabHeader1: self.profileName,
                Text.TabHeader2: self.engineSetting,
                Text.TabHeader3: self.pluginSetting
            }
        )
        self.mainTab.finishedBtn.clicked.connect(self._postSetting)
        
    def exec(self):
        self.mainTab.exec()

    def _postSetting(self):
        setting = dict()
        profileName = self.profileName.getData()
        setting["engine_setting_name"] = self.engineSetting.getData()
        setting["plugin_setting"] = self.pluginSetting.getData()
        try:
            self.logger.info(setting)
            self.signals.addProfile.emit((profileName, setting))
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("creating new profile", str(e)))
            
class EditProfile():
    def __init__(self, setting, engines, plugins, engineSettingSignal, *args, **kwargs) -> None:
        name, data = setting 
        self.profileName  = name 
        self.signals = Signals()
        self.logger = makeLogger("F")
        self.engineSetting = ChooseEngine(engines, engineSettingSignal)
        self.pluginSetting = PluginSetting(plugins)
        self.pluginSetting.setData(data["plugin_setting"])
        self.engineSetting.setData(data["engine_setting_name"])
        self.newSettingData = dict()
        self.mainTab = TabDialog(
            self.profileName,
            { Text.TabHeader2: self.engineSetting,
              Text.TabHeader3: self.pluginSetting
            }
        )
        self.mainTab.finishedBtn.clicked.connect(self._postSetting)
    
    def exec(self):
        self.mainTab.exec()

    def _postSetting(self):
        data = dict()
        data["engine_setting_name"] = self.engineSetting.getData()
        data["plugin_setting"] = self.pluginSetting.getData()
        try:
            self.logger.info(data)
            self.signals.editProfile.emit((self.profileName, data))
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("creating new engine setting", str(e)))