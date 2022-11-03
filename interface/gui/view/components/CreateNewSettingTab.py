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


from cProfile import run
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
    newSetting = pyqtSignal(object)
    

class CreateNewSetting(QDialog):
    def __init__(self, plugins, *agrs, **kwargs) -> None:
        super().__init__(*agrs, **kwargs)
        self.signals = Signals()
        self.profilename = ProfileName()
        self.BasicSetting = BasicSetting()
        self.EngineSetting = EngineSetting()
        self.OutPutFormSetting = OutPutFormatSetting()
        self.PostTranscribeSetting = PostTranscribeSetting()
        self.PluginSetting = PluginSetting(plugins)
        self.newSettingData = dict()
        self.setWindowTitle("Create New Profile")
        
        mainTab = Tab (
            "Create new setting", 
            {
                "ProfileName": self.profilename,
                "Basic Settings": self.BasicSetting,
                "Optional Settings": self.EngineSetting,
                "Output File Format Setting": self.OutPutFormSetting,
                "Post Transcribtion Settion": self.PostTranscribeSetting,
                "Plugin Setting" : self.PluginSetting
            },
            QSize(850,800)
        )
        
        mainTab.changePageBtn.finishBtn.clicked.connect(self.postSetting)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(mainTab)
        
    def postSetting(self):
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
        
        
        
        