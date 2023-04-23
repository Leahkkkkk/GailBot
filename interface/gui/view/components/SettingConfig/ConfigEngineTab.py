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
from typing import Dict, Tuple
from gbLogger import makeLogger
from view.config.Text import ENGINE_TAB_TEXT as Text
from view.config.Style import STYLE_DATA
from .CreateNewProfilePages import (
    SettingName,
    SelectEngine, 
    EngineForm)
from view.widgets.TabPage import TabDialog
from view.widgets import  WarnBox
from view.util.ErrorMsg import ERR

from PyQt6.QtCore import QObject, pyqtSignal, QSize

class Signals(QObject):
    """ a signal object to send new setting data values """
    addEngine = pyqtSignal(tuple)
    editEngine = pyqtSignal(tuple)
    
class CreateNewEngine:
    def __init__(self) -> None:
        """ a pop up dialog for user to create a new engine setting
            include pages:
            1. self.engineName: input for engine name
            2. self.selectEngine: select the speech to text engine
            3. self.engineForm: a form to create speech to text engine setting 
        """
        self.logger = makeLogger("F")
        self.signals = Signals()
        self.engineName = SettingName(title="Engine Setting Name")
        self.selectEngine = SelectEngine()
        self.engineForm = EngineForm()
        self.mainTab = TabDialog(
            Text.CREATE_TITTLE,
            {
                Text.NAME_TAB: self.engineName,
                Text.SELECT_ENGINE: self.selectEngine,
                Text.ENGINE_SETTING: self.engineForm
            },
            QSize(STYLE_DATA.Dimension.LARGEDIALOGWIDTH, 
                  STYLE_DATA.Dimension.LARGEDIALOGHEIGHT)
        )
        self.mainTab.finishedBtn.clicked.connect(self._postSetting)
        self.selectEngine.selectEngine.currentTextChanged.connect(
            self.engineForm.setForm)

    def exec(self):
        """ 
        must be called to display the dialog
        """
        self.mainTab.exec()
        
    def _postSetting(self):
        """ 
        send the new setting data through signal
        """ 
        setting = dict()
        profileName = self.engineName.getData()
        setting["engine"]  = self.selectEngine.getData()
        setting.update(self.engineForm.getData())
        try:
            self.logger.info(setting)
            self.signals.addEngine.emit((profileName, setting))
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("creating new engine setting", str(e)))
            
class EditEngine():
    def __init__(self, setting: Tuple[str, Dict]) -> None:
        """ a pop up dialog for user to edit engine setting  
            include pages:
            1. self.selectEngine: select the speech to text engine
            2. self.engineForm: a form to create speech to text engine setting 
        """
        name, data = setting 
        self.logger = makeLogger("F")
        self.signals = Signals()
        self.logger.info(name)
        self.logger.info(data)
        self.selectEngine = SelectEngine()
        self.engineForm = EngineForm()
        self.header = name 
        self.engineName = name
        self.mainTab = TabDialog(
            self.header,
            {"Select STT Engine" : self.selectEngine,
             "STT Engine Setting": self.engineForm},
            QSize(STYLE_DATA.Dimension.LARGEDIALOGWIDTH, 
                  STYLE_DATA.Dimension.LARGEDIALOGHEIGHT)
        )
        
        ## set the data for the profile 
        self.selectEngine.setData(data["engine"].title())
        self.engineForm.setData(data)
        self.mainTab.finishedBtn.clicked.connect(self._postSetting)
        self.selectEngine.selectEngine.currentTextChanged.connect(
            self.engineForm.setForm)
    
    def exec(self):
        """ 
        must be called to display the dialog
        """
        self.mainTab.exec()

    def _postSetting(self):
        """ 
        send the new setting data through signal
        """ 
        data = dict()
        data["engine"] = self.selectEngine.getData()
        data.update(self.engineForm.getData())
        try:
            self.logger.info(data)
            self.signals.editEngine.emit((self.engineName, data))
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("creating new engine setting", str(e)))