'''
File: ConfigEngineTab.py
Project: GailBot GUI
File Created: 2022/10/
Author: Siara Small  & Vivian Li
-----
Last Modified:2023/04/18
Modified By:  Siara Small  & Vivian Li
-----
Description: implement tab widget for creating Engine setting and 
              edit existing engine setting 
'''
from typing import List 

from gbLogger import makeLogger
from view.config.Text import CreateNewProfileTabText as Text
from view.config.Style import STYLE_DATA
from view.pages.CreateNewProfilePages import (
    SettingName,
    EngineSetting, 
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
    addEngine = pyqtSignal(tuple)
    editEngine = pyqtSignal(tuple)
    
class CreateNewEngine(QDialog):
    def __init__(self, *agrs, **kwargs) -> None:
        """ a pop up dialog for user to create a new profile
            the tab implement below processes for creating a new profile:
            1. input for profile name
            2. a form to create speech engine setting 
        """
        super().__init__(*agrs, **kwargs)
        self.logger = makeLogger("F")
        self.signals = Signals()
        self.EngineName = SettingName(title="Engine Setting Name")
        self.engineSetting = EngineSetting()
        self.setWindowTitle(Text.WindowTitle)
        
        mainTab = Tab(
            Text.WindowTitle,
            {
                Text.TabHeader1: self.EngineName,
                Text.TabHeader2: self.engineSetting,
            },
            QSize(STYLE_DATA.Dimension.LARGEDIALOGWIDTH, 
                  STYLE_DATA.Dimension.LARGEDIALOGHEIGHT)
        )
        
        mainTab.changePageBtn.finishBtn.clicked.connect(self._postSetting)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(mainTab)
        self.logger.info("")
        
    def _postSetting(self):
        """ a function that send the new setting data through signal""" 
        profileName = self.EngineName.getData()
        setting = self.engineSetting.getData()
        try:
            self.logger.info(setting)
            self.signals.addEngine.emit((profileName, setting))
            self.close()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("creating new engine setting", str(e)))
            
class EditEngine(QDialog):
    def __init__(self, setting, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        name, data = setting 
        self.logger = makeLogger("F")
        self.signals = Signals()
        self.engineSetting = EngineSetting()
        self.header = name 
        self.engineName = name
        mainTab = Tab(
            self.header,
            {self.header: self.engineSetting},
            QSize(STYLE_DATA.Dimension.LARGEDIALOGWIDTH, 
                  STYLE_DATA.Dimension.LARGEDIALOGHEIGHT)
        )
        ## set the data for the profile 
        self.engineSetting.setData(data)
        mainTab.changePageBtn.finishBtn.clicked.connect(self._postSetting)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(mainTab)
        self.logger.info("")
    
    def _postSetting(self):
        data = self.engineSetting.getData()
        try:
            self.logger.info(data)
            self.signals.editEngine.emit((self.engineName, data))
            self.close()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("creating new engine setting", str(e)))