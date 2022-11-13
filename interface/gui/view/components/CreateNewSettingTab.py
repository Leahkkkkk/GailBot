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

from util.Logger import makeLogger
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
        """ a pop up dialog for user to create a new profile
            the tab implement below processes for creating a new profile:
            1. input for profile name
            2. a form of basic profile setting
            3. a form to create speech engine setting 
            4. a form to create output format setting 
            5. a form to create post transcription setting 
            6. a form to create plugin setting 
             
        Constructor Args:
            plugins (List [str]): a list of string that stores the available 
                                  plugin
        
        """
        super().__init__(*agrs, **kwargs)
        self.logger = makeLogger("F")
        self.signals = Signals()
        self.addProfileName = ProfileName()
        self.basicSetting = BasicSetting()
        self.engineSetting = EngineSetting()
        self.outPutFormSetting = OutPutFormatSetting()
        self.postTranscribeSetting = PostTranscribeSetting()
        self.pluginSetting = PluginSetting(plugins)
        self.newSettingData = dict()
        self.setWindowTitle(Text.WindowTitle)
        
        mainTab = Tab(
            Text.WindowTitle,
            {
                Text.TabHeader1: self.addProfileName,
                Text.TabHeader2: self.basicSetting,
                Text.TabHeader3: self.engineSetting,
                Text.TabHeader4: self.outPutFormSetting,
                Text.TabHeader5: self.postTranscribeSetting,
                Text.TabHeader6: self.pluginSetting
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
        profileData = dict()
        requiredData = dict()
        profileName = self.addProfileName.getData()
        basicData = self.basicSetting.getData()
        engineData = self.engineSetting.getData()
        outputFormData = self.outPutFormSetting.getData()
        postFormData = self.postTranscribeSetting.getData()
        plugins = self.pluginSetting.getData()
        
        requiredData["User Info"] = basicData
        requiredData["Engine"] = engineData
        requiredData["Output Form Data"] = outputFormData
        profileData ["PostTranscribe"] = postFormData
        profileData ["RequiredSetting"] = requiredData
        profileData ["Plugins"] = plugins
        
        self.signals.newSetting.emit((profileName, profileData))
        self.logger.info(profileData)
        self.close()
        
        
        
