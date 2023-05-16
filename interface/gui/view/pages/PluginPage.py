'''
File: SettingPage.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Sunday, 6th November 2022 11:11:19 am
Modified By:  Siara Small  & Vivian Li
-----
Description: implementation of the plugin page
'''
from typing import List

from view.config.Text import PLUGIN_PAGE as Text
from view.config.InstructionText import INSTRUCTION
from view.signal.interface import DataSignal
from view.signal import PluginSignal
from view.Request import Request
from view.components.SettingTables import PluginTable
from view.components.SettingConfig import UploadPlugin
from .BaseSettingPage import BaseSettingPage
from PyQt6.QtCore import Qt

center  = Qt.AlignmentFlag.AlignHCenter

class PluginPage(BaseSettingPage):
    """" class for the plugins page """
    def __init__(
        self,
        *args, 
        **kwargs) -> None:
        self.headerText = Text.HEADER
        self.START = Text.CAPTION
        self.addNewButtonText = Text.CREATE_NEW
        self.signal = PluginSignal
        self.mainTable = PluginTable(self.signal)
        self.instruction = INSTRUCTION.PLUGIN_TABLE_INS
        super().__init__(*args, **kwargs)
       
    def addItem(self):
        pluginDialog = UploadPlugin()
        pluginDialog.signal.addPlugin.connect(self.sendAddRequest)
        pluginDialog.exec()
        
    def sendAddRequest(self, suiteData):
        self.signal.postRequest.emit(
            Request(data = suiteData, succeed=self.addSucceed))
        
    def addSucceed(self, pluginSuite):
        name, data, isOfficial = pluginSuite
        self.mainTable.addItem(pluginSuite)
        self.signal.addSucceed.emit(name)
  