from typing import List, Dict, Tuple 
from view.config.Style import STYLE_DATA
from config_frontend import PROJECT_ROOT
from view.config.Text import ENGINE_SETTING_TEXT as TEXT
from view.Signals import DataSignal
from view.Request import Request
from view.util.ErrorMsg import ERR  
from view.components.PluginSuiteDetails import PluginSuiteDetails
import subprocess
from .MsgBox import WarnBox, ConfirmBox
from gbLogger import makeLogger
from .Table import BaseTable
from PyQt6.QtWidgets import (
    QTableWidgetItem, 
    QWidget, 
    QPushButton,
    QVBoxLayout,
)
class EngineTable(BaseTable):
    def __init__(self, signal: DataSignal ):
        super().__init__(TEXT.TABLE_HEADER)
        self.signal = signal
        self.resizeCol(TEXT.TABLE_DIMENSION)
    
    def addItems(self, items: List[Tuple[str, Dict[str, str]]]):
        pass 
    
    def addItem(self, engine_setting_name):
        self.logger.info(f"item {engine_setting_name} is received by table")
        try:
            newRowIdx = self.rowCount()
            self.insertRow(newRowIdx)
            tableItem = QTableWidgetItem(engine_setting_name)
            self.setItem(newRowIdx, 0, tableItem)
            self.addCellWidgets(engine_setting_name, tableItem, newRowIdx)
            self.resizeRowsToContents()  
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("uploading plugin suite", str(e)))
        
    def addCellWidgets(self, name: str, tableItem: QTableWidgetItem, row: int):
        cellWidget = QWidget()
        layout = QVBoxLayout()
        editBtn = QPushButton("Edit")
        deleteBtn = QPushButton("Delete")
        sourceBtn = QPushButton("View Source")
        cellWidget.setLayout(layout)
        layout.addWidget(editBtn)
        layout.addWidget(deleteBtn)
        layout.addWidget(sourceBtn)
        deleteBtn.clicked.connect(lambda: self.delete(name, tableItem))
        editBtn.clicked.connect(lambda: self.edit(name))
        sourceBtn.clicked.connect(lambda: self.signal.viewSourceRequest.emit(
            Request(data=name, succeed=self.displaySource)
        ))
        self.setCellWidget(row, len(self.headers) - 1, cellWidget)

    
    def edit(self, name): 
        pass # TODO: 
    
    
    def editSucceed(self):
        pass 
        