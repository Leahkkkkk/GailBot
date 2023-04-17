import subprocess
from typing import List, Dict, Tuple 
from view.config.Style import STYLE_DATA
from view.util.ErrorMsg import ERR  
from .MsgBox import WarnBox, ConfirmBox
from view.Request import Request
from view.Signals import DataSignal
from gbLogger import makeLogger
from PyQt6.QtWidgets import (
    QTableWidget, 
    QTableWidgetItem, 
    QHeaderView,
    QHeaderView, 
    QAbstractItemView,
)

from PyQt6.QtCore import (
    Qt
)

class BaseTable(QTableWidget):
    signal : DataSignal = None 
    def __init__(self, headers, *args, **kwargs):
        super().__init__(0, len(headers))
        self.logger = makeLogger("F")
        self.headers = headers 
        self._initWidget()
        self._initStyle()
        self.nameToTablepins: Dict[str, QTableWidgetItem] = dict()
        STYLE_DATA.signal.changeColor.connect(self.colorchange)

    def _initStyle(self) -> None:
        """ Initialize the table style """
        self.horizontalHeader().setFixedHeight(45)
        self.setObjectName("FileTable")
        self.setStyleSheet(f"#FileTable{STYLE_DATA.StyleSheet.FILE_TABLE}")
        for i in range(self.columnCount()):
            self.horizontalHeader().setSectionResizeMode(
                i, QHeaderView.ResizeMode.Fixed)
        self.setFixedWidth(STYLE_DATA.Dimension.FORMWIDTH)
        self.setMinimumHeight(STYLE_DATA.Dimension.FORMMINHEIGHT)
        self.verticalScrollBar().setStyleSheet(STYLE_DATA.StyleSheet.SCROLL_BAR) 
        self.horizontalScrollBar().setStyleSheet(STYLE_DATA.StyleSheet.SCROLL_BAR)
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)  
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setTextElideMode(Qt.TextElideMode.ElideMiddle)
    
    def colorchange(self):
        self.setStyleSheet(f"#FileTable{STYLE_DATA.StyleSheet.FILE_TABLE}")
        self.verticalScrollBar().setStyleSheet(STYLE_DATA.StyleSheet.SCROLL_BAR) 
        self.horizontalScrollBar().setStyleSheet(STYLE_DATA.StyleSheet.SCROLL_BAR)
        self.horizontalHeader().setStyleSheet(STYLE_DATA.StyleSheet.TABLE_HEADER)
        
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
        self.horizontalHeader().setStyleSheet(STYLE_DATA.StyleSheet.TABLE_HEADER)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def addCellWidgets(self):
        pass 
    
    def addItems(self, items):
        for item in items:
            self.addItem(item)
    
    def addItem(self, item):
        pass  
   
    def delete(self, name, tableItem):
        try:
            self.logger.info(f"trying to delete the plugin suite {name}")
            succeed = lambda data: self.deleteSucceed(name, tableItem)
            requestDelete = lambda : self.signal.deleteRequest.emit(
                Request(data=name, succeed= succeed)
            )
            ConfirmBox(f"Confirming to delete {name}?", requestDelete)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("deleting plugin suite", str(e)))
    
    def deleteSucceed(self, name: str, tableItem: QTableWidgetItem):
        rowidx = self.indexFromItem(tableItem).row()
        self.removeRow(rowidx)
        self.signal.deleteSucceed.emit(name)
    
    def displaySource(self, path:str): 
        pid = subprocess.check_call(["open", path]) 
    
    
    