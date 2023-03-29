from typing import List, Dict, Tuple, Any
from view.config.Style import Dimension, Color
from view.style.WidgetStyleSheet import FILE_TABLE, SCROLL_BAR, TABLE_HEADER
from view.Signals import PluginSignals
from view.util.ErrorMsg import ERR  
from view.components.PluginDetails import PluginPopUp

from .MsgBox import WarnBox
from gbLogger import makeLogger
from PyQt6.QtWidgets import (
    QTableWidget, 
    QTableWidgetItem, 
    QWidget, 
    QHeaderView,
    QPushButton,
    QHeaderView, 
    QVBoxLayout
)

from PyQt6.QtCore import (
    QObject,
    Qt,
    QSize,
    pyqtSignal
)

class PluginTable(QTableWidget):
    def __init__(self, signal: PluginSignals):
        super().__init__(0, 4)
        self.logger = makeLogger("F")
        self.signal = signal
        self.plugins: Dict[str, Dict[str, str]] = dict()
        self.nameToTablepins: Dict[str, QTableWidgetItem] = dict()
        self.headers = ["Plugin Name", "Author", "Version", "Actions"]
        self._initWidget()
        self._initStyle()
        self.resizeCol([0.3, 0.2, 0.2, 0.3])
    
    def _initStyle(self) -> None:
        """ Initialize the table style """
        self.horizontalHeader().setFixedHeight(45)
        self.setObjectName("FileTable")
        self.setStyleSheet(f"#FileTable{FILE_TABLE}")
        for i in range(self.columnCount()):
            self.horizontalHeader().setSectionResizeMode(
                i, QHeaderView.ResizeMode.Fixed)
        self.setFixedWidth(Dimension.FORMWIDTH)
        self.setMinimumHeight(Dimension.FORMMINHEIGHT)
        self.verticalScrollBar().setStyleSheet(SCROLL_BAR) 
        self.horizontalScrollBar().setStyleSheet(SCROLL_BAR)
    
    def resizeCol(self, widths:List[float]) -> None:
        """ takes in a list of width and resize the width of the each 
            column to the width
        """
        try:
            widthSum = self.width()
            for i in range(len(widths)):
                self.setColumnWidth(i, int(widths[i] * widthSum))
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.FAIL_TO.format("resize plugin table column"))
    
    def _initWidget(self):
        for idx, header in enumerate(self.headers):
            headerItem = QTableWidgetItem(header)
            self.setHorizontalHeaderItem(idx, headerItem)
        self.verticalHeader().hide()
        self.horizontalHeader().setStyleSheet(TABLE_HEADER)

    def addPlugins(self, plugins: List[Dict]):
        for plugin in plugins:
            self.addPlugin(plugin)
    
    def addPlugin(self, suiteInfo: Tuple[str, Dict[str, str]]):
        self.logger.info(suiteInfo)
        suiteName, metadata = suiteInfo
        try:
            newRowIdx = self.rowCount()
            self.insertRow(newRowIdx)
            suiteNameItem = QTableWidgetItem(str(suiteName))
            self.setItem = (newRowIdx, 0, suiteNameItem)
            for col in range(len(self.headers)):
                if self.headers[col].lower() in metadata.keys():
                    newItem = QTableWidgetItem(str(metadata[self.headers[col]]))
                    self.setItem(newRowIdx, col, newItem)
            self.addCellWidget(suiteName, suiteNameItem, newRowIdx)
            self.resizeRowsToContents()  
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("uploading plugin suite", str(e)))
    
    def deleteSuite(self, suiteName:str, tableItem: QTableWidgetItem):
        try:
            self.signal.deletePlugin.emit(suiteName)
            rowidx = self.indexFromItem(tableItem).row()
            self.removeRow(rowidx)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("deleting plugin suite", str(e)))
   
    def seeSuiteDetail(self, suiteName:str):
        self.signal.requestPluginDetails.emit(suiteName)
        
    def displayPluginDetails(self, pluginInfo: Dict[str, Any]):
        infoDisplay = PluginPopUp(pluginInfo)
        infoDisplay.exec()
    
    def addCellWidget(self, suiteName: str, tableItem: QTableWidgetItem, row:int):
        cellWidget = QWidget()
        layout = QVBoxLayout()
        detailBtn = QPushButton("Details")
        deleteBtn = QPushButton("Delete")
        cellWidget.setLayout(layout)
        layout.addWidget(detailBtn)
        layout.addWidget(deleteBtn)
        deleteBtn.clicked.connect(lambda: self.deleteSuite(suiteName, tableItem))
        detailBtn.clicked.connect(lambda: self.seeSuiteDetail(suiteName))
        self.setCellWidget(row, len(self.headers) - 1, cellWidget)
