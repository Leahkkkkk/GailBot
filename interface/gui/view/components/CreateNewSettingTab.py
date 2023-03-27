'''
File: CreateNewSettingTab.py
Project: GailBot GUI
File Created: Sunday, 23rd October 2022 10:28:24 am
Author: Siara Small  & Vivian Li
-----
Last Modified: Monday, 24th October 2022 6:39:15 am
Modified By:  Siara Small  & Vivian Li
-----
Description: implementation of a pop up dialog that allow user to 
             create new transcription setting profile
'''

from typing import List 

from gbLogger import makeLogger
from view.config.Text import CreateNewProfileTabText as Text
from view.config.Style import Dimension
from view.pages.CreateNewProfilePages import (
    ProfileName,
    EngineSetting, 
    PluginSetting
)
from view.widgets.PopUpTab import Tab
from view.widgets.MsgBox import WarnBox
from view.util.ErrorMsg import ERR, WARN
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QDialog
)

from PyQt6.QtCore import QObject, pyqtSignal, QSize

class Signals(QObject):
    """ a signal object to send new setting data values """
    newSetting = pyqtSignal(object)
    
class CreateNewSetting(QDialog):
    def __init__(self, plugins : List[str], *agrs, **kwargs) -> None:
        """ a pop up dialog for user to create a new profile
            the tab implement below processes for creating a new profile:
            1. input for profile name
            2. a form to create speech engine setting 
            3. a form to select plugin setting 
             
        Constructor Args:
            plugins (List [str]): a list of string that stores the available 
                                  plugin
        
        """
        super().__init__(*agrs, **kwargs)
        self.logger = makeLogger("F")
        self.signals = Signals()
        self.addProfileName = ProfileName()
        self.engineSetting = EngineSetting()
        self.pluginSetting = PluginSetting(plugins)
        self.newSettingData = dict()
        self.setWindowTitle(Text.WindowTitle)
        
        mainTab = Tab(
            Text.WindowTitle,
            {
                Text.TabHeader1: self.addProfileName,
                Text.TabHeader2: self.engineSetting,
                Text.TabHeader3: self.pluginSetting
            },
            QSize(Dimension.LARGEDIALOGWIDTH, Dimension.LARGEDIALOGHEIGHT)
        )
        
        mainTab.changePageBtn.finishBtn.clicked.connect(self._postSetting)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(mainTab)
        self.logger.info("")
        
    def _postSetting(self):
        """ a function that send the new setting data through signal""" 
        setting = dict()
        profileName = self.addProfileName.getData()
        setting["engine_setting"] = self.engineSetting.getData()
        setting["plugin_setting"] = []
        try:
            self.logger.info(setting)
            self.signals.newSetting.emit((profileName, setting))
            self.close()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("creating new profile", str(e)))
            
        
        
        
