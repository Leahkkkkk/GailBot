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


from view.pages.CreatNewSettingPages import (
    ProfileName,
    ChooseEngine,
    BasicSetting, 
    EngineSetting, 
    OutPutFormatSetting,
    PostTranscribeSetting
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
    def __init__(self, 
                 engineKey:list, 
                 engineFormData:dict, 
                 outputFormData:dict,
                 postTranscribeFormData:dict,
                 *agrs, 
                 **kwargs) -> None:
        super().__init__(*agrs, **kwargs)
        self.engineForm = engineFormData
        print(engineFormData)
        self.signals = Signals()
        self.profilename = ProfileName()
        self.ChooseEngine = ChooseEngine(engineKey)
        self.BasicSetting = BasicSetting()
        self.EngineSetting = EngineSetting(self.engineForm[engineKey[0]])
        self.OutPutFormSetting = OutPutFormatSetting(outputFormData)
        self.PostTranscribeSetting = PostTranscribeSetting(postTranscribeFormData)
        self.newSettingData = dict()
        
        self.setWindowTitle("Create New Profile")
        
        mainTab = Tab (
            "Create new setting", 
            {
                "ProfileName": self.profilename,
                "Speech to text engine": self.ChooseEngine,
                "Basic Settings": self.BasicSetting,
                "Optional Settings": self.EngineSetting,
                "Output File Format Setting": self.OutPutFormSetting,
                "Post Transcribtion Settion": self.PostTranscribeSetting
            },
            QSize(800,800)
        )
        
        self.ChooseEngine.mainCombo.currentTextChanged.connect(self._changeEngineSetting)
        self.ChooseEngine.signals.nextPage.emit()
        mainTab.changePageBtn.finishBtn.clicked.connect(self.postSetting)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(mainTab)

    def _changeEngineSetting(self, engine:str):
        if engine in self.engineForm:
            self.EngineSetting.newForm(self.engineForm[engine])
        
    def postSetting(self):
        settingData = dict()
        
        profileName = self.profilename.getData()
        basicData = self.BasicSetting.getData()
        engine = self.ChooseEngine.getData()
        engineData = self.EngineSetting.getData()
        outputFormData = self.OutPutFormSetting.getData()
        postFormData = self.PostTranscribeSetting.getData()
        
        settingData["engine"] = {engine:engineData}
        settingData["Post Transcribe"] = postFormData
        settingData["Output Form Data"] = outputFormData
        settingData["User Info"] = basicData
        
        self.signals.newSetting.emit({profileName: settingData})
        self.close()
        
        
        
        