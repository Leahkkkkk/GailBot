import os
from typing import List, Dict, Tuple 
from view.config.Style import STYLE_DATA
from config_frontend import PROJECT_ROOT
from view.config.Text import ProfilePageText as Text
from view.Signals import DataSignal, GlobalStyleSignal
from view.Request import Request
from view.util.ErrorMsg import ERR  
from view.components.PluginSuiteDetails import PluginSuiteDetails
import subprocess
from .MsgBox import WarnBox, ConfirmBox
from .Table import BaseTable
from PyQt6.QtWidgets import (
    QTableWidgetItem, 
    QWidget, 
    QPushButton,
    QVBoxLayout,
)

from PyQt6.QtCore import (
    Qt
)
from PyQt6.QtGui import QIcon

class ProfileTable(BaseTable):
    def __init__(self, signal: DataSignal):
        super().__init__(Text.tableHeader)
        self.signal = signal
        self.resizeCol(Text.tableDimension)
    
    def addItem(self, profile: Tuple[str, Dict[str, str], str]):
        self.logger.info(profile)
        name, data = profile
        try:
            newRowIdx = self.rowCount()
            self.insertRow(newRowIdx)
            suiteNameItem = QTableWidgetItem(str(name))
        
            self.setItem(newRowIdx, 0, suiteNameItem)
            
            for col in range(len(self.headers)):
                if self.headers[col].lower() in data.keys():
                    newItem = QTableWidgetItem(str(data[self.headers[col].lower()]))
                    self.setItem(newRowIdx, col, newItem)
            self.addCellWidgets(name, suiteNameItem, newRowIdx)
            self.resizeRowsToContents()  
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("uploading plugin suite", str(e)))
        
    def addCellWidgets(self, name: str, tableItem: QTableWidgetItem, row:int):
        cellWidget = QWidget()
        layout = QVBoxLayout()
        deleteBtn = QPushButton("Delete")
        editBtn = QPushButton("Edit")
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

    def edit(self, name:str):
        pass 
    
    
