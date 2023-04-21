import subprocess
import os
from typing import List, Dict, Tuple 
from view.config.Style import STYLE_DATA
from view.util.ErrorMsg import ERR  
from .Label import Label
from .MsgBox import WarnBox, ConfirmBox
from view.Request import Request
from view.Signals import DataSignal
from view.components.SelectPathDialog import SaveSetting
from gbLogger import makeLogger
from PyQt6.QtWidgets import (
    QTableWidget, 
    QHeaderView, 
    QAbstractItemView,
    QTableWidgetItem, 
    QWidget, 
    QPushButton,
    QVBoxLayout,
)
from PyQt6.QtCore import (
    Qt
)

class BaseTable(QTableWidget):
    signal : DataSignal 
    dataKeyToCol : Dict[str, int] 
    def __init__(self, headers, *args, **kwargs):
        super().__init__(0, len(headers))
        self.logger = makeLogger("F")
        self.headers = headers 
        self._initWidget()
        self._initStyle()
        self.nameToTablePins: Dict[str, QTableWidgetItem] = dict()
        STYLE_DATA.signal.changeColor.connect(self.colorchange)

    def _initStyle(self) -> None:
        """ Initialize the table style """
        self.horizontalHeader().setFixedHeight(45)
        self.setObjectName("FileTable")
        self.setStyleSheet(f"#FileTable{STYLE_DATA.StyleSheet.FILE_TABLE}")
        for i in range(self.columnCount()):
            self.horizontalHeader().setSectionResizeMode(
                i, QHeaderView.ResizeMode.Fixed)
        self.setFixedWidth(STYLE_DATA.Dimension.DEFAULTTABWIDTH)
        self.setMinimumHeight(STYLE_DATA.Dimension.DEFAULTTABHEIGHT)
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

    def addCellWidgets(self, name: str, tableItem: QTableWidgetItem, row:int):
        cellWidget = QWidget()
        layout     = QVBoxLayout()
        editBtn    = QPushButton("Edit")
        deleteBtn  = QPushButton("Delete")
        sourceBtn  = QPushButton("View Source")
        detailBtn  = QPushButton("View Detail")
        cellWidget.setLayout(layout)
        
        layout.addWidget(editBtn)
        layout.addWidget(deleteBtn)
        layout.addWidget(sourceBtn)
        layout.addWidget(detailBtn)
        deleteBtn.clicked.connect(lambda: self.delete(name, tableItem))
        editBtn.clicked.connect(lambda: self.editSetting(name))
        sourceBtn.clicked.connect(lambda: self.viewSourceRequest(name))
        detailBtn.clicked.connect(lambda: self.viewDetailRequest(name))
        self.setCellWidget(row, len(self.headers) - 1, cellWidget)

    def addItems(self, items, **kwargs):
        for item in items:
            self.addItem(item, **kwargs)
    
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
        
    def displayDetail(self, data):
        pass 
    
    def viewDetailRequest(self, name):
        self.signal.getRequest.emit(
            Request(data=name, succeed=self.displayDetail))
    
    def displaySource(self, path:str): 
        """ TODO: open dialog """
        try:
            dialog = SaveSetting(origPath=path)
            dialog.exec()
            if dialog.copiedPath:
                pid = subprocess.check_call(["open", dialog.copiedPath]) 
        except Exception as e:
            self.logger.error(e, exc_info=e)
    
    def viewSourceRequest(self, name: str):
        self.signal.viewSourceRequest.emit(
            Request(data=name, succeed=self.displaySource))
    
    def addItem(self, setting: Tuple[str, Dict[str, str], str], **kwargs):
        self.logger.info(setting)
        name, data = setting
        try:
            newRowIdx = self.rowCount()
            self.insertRow(newRowIdx)
            # set the setting name
            nameItem = QTableWidgetItem(str(name))
            self.nameToTablePins[name] = nameItem 
            self.setItem(newRowIdx, 0, nameItem)
            
            for key, col in self.dataKeyToCol.items():
                if isinstance(data[key], list):
                    newItem = self.createListDisplay(data[key])
                    self.setCellWidget(newRowIdx, col, newItem)
                else:
                    newItem = QTableWidgetItem(str(data[key]))
                    self.setItem(newRowIdx, col, newItem)
            
            self.addCellWidgets(name, nameItem, newRowIdx, **kwargs)
            self.resizeRowsToContents()  
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("uploading  setting to table", str(e)))
            
    def editSucceed(self, setting):
        name, data = setting 
        rowIdx = self.indexFromItem(self.nameToTablePins[name]).row()
        try:
            for key, col in self.dataKeyToCol.items():
                self.removeCellWidget(rowIdx, col)
                if isinstance(data[key], list):
                    newItem = self.createListDisplay(data[key])
                    self.setCellWidget(rowIdx, col, newItem)
                else:
                    newItem = QTableWidgetItem(str(data[key]))
                    self.setItem(rowIdx, col, newItem)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("updating setting changes on table", str(e)))
        
    def sendEditRequest(self, data):
        self.signal.editRequest.emit(
            Request(data=data, succeed=self.editSucceed))
    
    def editSetting(self, name):
        self.signal.getRequest.emit(
            Request(data=name, succeed=self.openEditDialog)
        )
   
    def openEditDialog(self, data):
        pass
    
    def createListDisplay(self, items):
        listDisplay = QWidget()
        listLayout = QVBoxLayout()
        listDisplay.setLayout(listLayout)
        for item in items:
            newLabel = Label(item, STYLE_DATA.FontSize.BODY)
            listLayout.addWidget(newLabel)
        return listDisplay