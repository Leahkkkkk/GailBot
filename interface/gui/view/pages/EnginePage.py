'''
File: EnginePage.py
Project: GailBot GUI
File Created: 2023/04/01
Author: Siara Small  & Vivian Li
-----
Last Modified:2023/05/18
Modified By:  Siara Small  & Vivian Li
-----
Description: implementation of engine setting page
'''
from view.config.Text import ENGINE_SETTING_TEXT as Text
from view.config.InstructionText import INSTRUCTION
from view.signal import EngineSignal
from view.Request import Request
from gbLogger import makeLogger
from view.components.SettingTables import EngineTable
from view.components.SettingConfig import CreateNewEngine
from PyQt6.QtCore import Qt
from .BaseSettingPage import BaseSettingPage

center  = Qt.AlignmentFlag.AlignHCenter

class EnginePage(BaseSettingPage):
    def __init__(
        self,
        *args, 
        **kwargs) -> None:
        """ initializes class """
        self.instruction = INSTRUCTION.ENGINE_TABLE_INS
        self.headerText = Text.HEADER
        self.START = Text.CAPTION
        self.addNewButtonText = Text.CREATE_NEW
        self.signal = EngineSignal 
        self.mainTable = EngineTable(self.signal)
        super().__init__( *args, **kwargs)
    
    def addItem(self):
        """
        called when user request to add a new engine 
        """
        engineDialog = CreateNewEngine()
        engineDialog.signals.addEngine.connect(self.sendAddRequest)
        engineDialog.exec()

    def addAvailableEngine(self, engines):
        """ 
        add the list of available engines to the frontend interface
        """
        self.mainTable.addItems(engines)
    
    