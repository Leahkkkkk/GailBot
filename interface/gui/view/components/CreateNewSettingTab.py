'''
File: CreateNewSettingTab.py
Project: GailBot GUI
File Created: Sunday, 23rd October 2022 10:28:24 am
Author: Siara Small  & Vivian Li
-----
Last Modified: Monday, 24th October 2022 6:39:15 am
Modified By:  Siara Small  & Vivian Li
-----
'''
from typing import List 

from util.Text import CreatNewProfileTabText as Text
from util.Style import Dimension
from view.pages.CreateNewProfilePages import (
    ProfileName,
    BasicSetting, 
    EngineSetting, 
    OutPutFormatSetting,
    PostTranscribeSetting,
    PluginSetting
)
from view.widgets.PopUpTab import Tab
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
        """ a pop up dialog to create a new setting

        Args:
            plugins (List [str]): a list of string that stores the available 
                                  plugin
        """
        super().__init__(*agrs, **kwargs)
        self.signals = Signals()
        self.profilename = ProfileName()
        self.BasicSetting = BasicSetting()
        self.EngineSetting = EngineSetting()
        self.OutPutFormSetting = OutPutFormatSetting()
        self.PostTranscribeSetting = PostTranscribeSetting()
        self.PluginSetting = PluginSetting(plugins)
        self.newSettingData = dict()
        self.setWindowTitle(Text.WindowTitle)
        
        mainTab = Tab(
            Text.WindowTitle,
            {
                Text.TabHeader1: self.profilename,
                Text.TabHeader2: self.BasicSetting,
                Text.TabHeader3: self.EngineSetting,
                Text.TabHeader4: self.OutPutFormSetting,
                Text.TabHeader5: self.PostTranscribeSetting,
                Text.TabHeader6: self.PluginSetting
            },
            QSize(Dimension.LARGEDIALOGWIDTH, Dimension.LARGEDIALOGHEIGHT)
        )
        
        mainTab.changePageBtn.finishBtn.clicked.connect(self.postSetting)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(mainTab)
        
    def postSetting(self):
        """ a function that send the new setting data through signal"""
        profileData = dict()
        requiredData = dict()
        profileName = self.profilename.getData()
        basicData = self.BasicSetting.getData()
        engineData = self.EngineSetting.getData()
        outputFormData = self.OutPutFormSetting.getData()
        postFormData = self.PostTranscribeSetting.getData()
        plugins = self.PluginSetting.getData()
        
        requiredData["User Info"] = basicData
        requiredData["Engine"] = engineData
        requiredData["Output Form Data"] = outputFormData
        profileData ["PostTranscribe"] = postFormData
        profileData ["RequiredSetting"] = requiredData
        profileData ["Plugins"] = plugins
        
        self.signals.newSetting.emit((profileName, profileData))
        self.close()
        
        
        
