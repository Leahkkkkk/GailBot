from typing import List, Dict, Tuple, Any
from view.config.Style import Dimension
from view.config.Text import PLUGIN_SUITE_TEXT
from view.style.WidgetStyleSheet import FILE_TABLE, SCROLL_BAR, TABLE_HEADER
from view.Signals import PluginSignals
from view.Request import Request
from view.util.ErrorMsg import ERR  
from view.components.PluginSuiteDetails import PluginSuiteDetails

from .MsgBox import WarnBox, ConfirmBox
from gbLogger import makeLogger
from PyQt6.QtWidgets import (
    QTableWidget, 
    QTableWidgetItem, 
    QWidget, 
    QHeaderView,
    QPushButton,
    QHeaderView, 
    QVBoxLayout,
    QAbstractItemView
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
        self.headers = PLUGIN_SUITE_TEXT.TABLE_HEADER
        self._initWidget()
        self._initStyle()
        self.resizeCol(PLUGIN_SUITE_TEXT.TABLE_DIMENSION)
    
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
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)  
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    
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
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def addPlugins(self, plugins: List[Tuple[str, Dict[str, str]]]):
        """ 
        add a list of plugins to the plugin suite table
        Args:
            plugins (List[Tuple[str, Dict[str, str]]]):  
            a list of tuple that stores the plugin suite information 
            the tuple contains the name of the plugin suite and a dictionary of the 
            plugin suite information
        """
        for plugin in plugins:
            self.addPluginSuite(plugin)
    
    def addPluginSuite(self, suiteInfo: Tuple[str, Dict[str, str]]):
        self.logger.info(suiteInfo)
        suiteName, metadata = suiteInfo
        try:
            newRowIdx = self.rowCount()
            self.insertRow(newRowIdx)
            suiteNameItem = QTableWidgetItem(str(suiteName))
            self.setItem(newRowIdx, 0, suiteNameItem)
            for col in range(len(self.headers)):
                if self.headers[col].lower() in metadata.keys():
                    newItem = QTableWidgetItem(str(metadata[self.headers[col].lower()]))
                    self.setItem(newRowIdx, col, newItem)
            self.addCellWidget(suiteName, suiteNameItem, newRowIdx)
            self.resizeRowsToContents()  
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("uploading plugin suite", str(e)))
    
    def deleteSuite(self, suiteName:str, tableItem: QTableWidgetItem):
        try:
            self.logger.info(f"trying to delete the plugin suite {suiteName}")
            succeed = lambda data: self.deleteSuiteSucceed(suiteName, tableItem)
            requestDelete = lambda : self.signal.deleteRequest.emit(
                Request(data=suiteName, succeed= succeed)
            )
            ConfirmBox(
                PLUGIN_SUITE_TEXT.CONFIRM_DELETE.format(suiteName),
                requestDelete)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("deleting plugin suite", str(e)))
   
    def deleteSuiteSucceed(self, name: str, tableItem: QTableWidgetItem):
        rowidx = self.indexFromItem(tableItem).row()
        self.removeRow(rowidx)
        self.signal.pluginDeleted.emit(name)
        
    def seeSuiteDetail(self, suiteName:str):
        self.signal.detailRequest.emit(
            Request(data = suiteName, succeed=self.displayPluginSuiteDetail))
        
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