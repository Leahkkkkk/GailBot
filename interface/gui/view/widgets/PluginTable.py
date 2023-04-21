import os
from typing import List, Dict, Tuple 
from view.config.Style import STYLE_DATA
from config_frontend import PROJECT_ROOT
from view.config.Text import PLUGIN_SUITE_TEXT
from view.Signals import DataSignal, GlobalStyleSignal
from view.Request import Request
from view.util.ErrorMsg import ERR  
from view.components.SettingDetail import PluginSuiteDetails
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

class PluginTable(BaseTable):
    def __init__(self, signal: DataSignal):
        super().__init__(PLUGIN_SUITE_TEXT.TABLE_HEADER)
        self.signal = signal
        self.dataKeyToCol = {"author": 1, "version": 2}
        self.resizeCol(PLUGIN_SUITE_TEXT.TABLE_DIMENSION)
    
    def addItem(self, suiteInfo: Tuple[str, Dict[str, str], str]):
        self.logger.info(suiteInfo)
        suiteName, metadata, isOfficial = suiteInfo
        super().addItem((suiteName, metadata), isOfficial = isOfficial)
        try:
            if isOfficial:
                self.nameToTablePins[suiteName].setIcon(QIcon(os.path.join(PROJECT_ROOT, STYLE_DATA.Asset.pluginBadge)))
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("uploading plugin suite", str(e)))
        
    def addCellWidgets(self, suiteName: str, tableItem: QTableWidgetItem, row:int, isOfficial: bool = False):
        cellWidget = QWidget()
        layout = QVBoxLayout()
        detailBtn = QPushButton("Details")
        sourceBtn = QPushButton("View Source")
        cellWidget.setLayout(layout)
        layout.addWidget(detailBtn)
        layout.addWidget(sourceBtn)
        detailBtn.clicked.connect(lambda: self.viewDetail(suiteName))
        sourceBtn.clicked.connect(lambda: self.signal.viewSourceRequest.emit(
            Request(data=suiteName, succeed=self.displaySource)
        ))
        if not isOfficial:
            deleteBtn = QPushButton("Delete")
            layout.addWidget(deleteBtn)
            deleteBtn.clicked.connect(lambda: self.delete(suiteName, tableItem))
        self.setCellWidget(row, len(self.headers) - 1, cellWidget)

    def viewDetail(self, suiteName:str):
        self.signal.detailRequest.emit(
            Request(data = suiteName, succeed=self.displayPluginSuiteDetail))

    def displayPluginSuiteDetail(self, suiteInfo) -> None :
        """ 
        open a frontend dialog to display suiteInfo 
        """
        try:
            display = PluginSuiteDetails(suiteInfo)
            display.exec()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.FAIL_TO.format("display plugin suite detail"))
    
