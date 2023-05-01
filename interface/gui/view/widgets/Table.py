import subprocess
from typing import List, Dict, Tuple 
from view.config.Style import STYLE_DATA
from view.util.ErrorMsg import ERR  
from .Label import Label
from .MsgBox import WarnBox, ConfirmBox
from view.Request import Request
from view.signal.interface import DataSignal
from view.widgets.Button import TableBtn
from view.widgets.ScrollArea import ScrollArea
from view.widgets.Background import initPrimaryColorBackground
from view.components.SelectPath import SaveSetting
from gbLogger import makeLogger
from PyQt6.QtWidgets import (
    QTableWidget, 
    QHeaderView, 
    QAbstractItemView,
    QTableWidgetItem, 
    QWidget, 
    QScrollArea,
    QVBoxLayout,
    QHBoxLayout
)
from PyQt6.QtCore import (
    Qt, QModelIndex
)
from PyQt6.QtGui import QFont
class BaseTable(QTableWidget):
    signal : DataSignal 
    dataKeyToCol : Dict[str, int] 
    tableWidth : int = STYLE_DATA.Dimension.DEFAULTTABWIDTH
    tableHeight :  int = STYLE_DATA.Dimension.DEFAULTTABHEIGHT
    nameAtFstColumn: bool = True
    def __init__(self, headers, *args, **kwargs):
        print("init table")
        super(BaseTable, self).__init__(0, len(headers))
        self.logger = makeLogger("F")
        self.headers = headers 
        self._initWidget()
        self._initStyle()
        self.nameToTablePins: Dict[str, QTableWidgetItem] = dict()
        self.actionWidgetCol = len(self.headers) - 1
        STYLE_DATA.signal.changeColor.connect(self.colorChange)
        STYLE_DATA.signal.changeFont.connect(self.fontChange)
        
    ###################### for configuring table style ######################
    def _initStyle(self) -> None:
        """ Initialize the table style """
        self.horizontalHeader().setFixedHeight(45)
        self.setObjectName("FileTable")
        self.setStyleSheet(f"#FileTable{STYLE_DATA.StyleSheet.FILE_TABLE}")
        for i in range(self.columnCount()):
            self.horizontalHeader().setSectionResizeMode(
                i, QHeaderView.ResizeMode.Fixed)
        self.setFixedWidth(self.tableWidth)
        self.setMinimumHeight(self.tableHeight)
        self.verticalScrollBar().setStyleSheet(STYLE_DATA.StyleSheet.SCROLL_BAR) 
        self.horizontalScrollBar().setStyleSheet(STYLE_DATA.StyleSheet.SCROLL_BAR)
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)  
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setTextElideMode(Qt.TextElideMode.ElideMiddle)
        font = QFont(STYLE_DATA.FontFamily.OTHER, STYLE_DATA.FontSize.TABLE_ROW)
        self.setFont(font)
        self.setTextElideMode(Qt.TextElideMode.ElideMiddle)
    
    def colorChange(self):
        self.setStyleSheet(f"#FileTable{STYLE_DATA.StyleSheet.FILE_TABLE}")
        self.verticalScrollBar().setStyleSheet(STYLE_DATA.StyleSheet.SCROLL_BAR) 
        self.horizontalScrollBar().setStyleSheet(STYLE_DATA.StyleSheet.SCROLL_BAR)
        self.horizontalHeader().setStyleSheet(STYLE_DATA.StyleSheet.TABLE_HEADER)
        
    def fontChange(self, font = None):
        font = QFont(STYLE_DATA.FontFamily.OTHER, STYLE_DATA.FontSize.TABLE_ROW)
        self.setFont(font)

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

    ################# for configuring table widget and  ################
    def addCellWidgets(self, name: str, row:int):
        cellWidget = QWidget()
        layout     = QHBoxLayout()
        cellWidget.setLayout(layout)
        layout.addWidget(self.getEditBtn(name))
        layout.addWidget(self.getRemoveBtn(name))
        layout.addWidget(self.getViewDetailBtn(name))
        self.setCellWidget(row, self.actionWidgetCol, cellWidget)
        

    def getRemoveBtn(self, name) -> QWidget:
        btn = TableBtn(icon=STYLE_DATA.Asset.tableRemove, instructions=" remove the source from the table")
        btn.clicked.connect(
            lambda:self.delete(name)
        )
        return btn
        
    def getEditBtn(self, name) -> QWidget:
        btn = TableBtn(icon=STYLE_DATA.Asset.tableEdit, instructions=" edit setting")
        btn.clicked.connect(
            lambda:self.editSetting(name)
        )
        return btn
        
    def getViewDetailBtn(self, name) -> QWidget:
        btn = TableBtn(icon=STYLE_DATA.Asset.tableDetail, instructions="view source detail")
        btn.clicked.connect(
            lambda:self.viewDetailRequest(name)
        )
        return btn

    def getViewSourceBtn(self, name) -> QWidget:
        btn = TableBtn(icon=STYLE_DATA.Asset.tableSource, instructions="view source raw file")
        btn.clicked.connect(
            lambda:self.viewSourceRequest(name)
        )
        return btn
    
    def getViewOutputBtn(self, name) -> QWidget:
        self.logger.info("ask for view output button")
        btn = TableBtn(icon=STYLE_DATA.Asset.tableOutput, instructions="view source output")
        btn.clicked.connect(
            lambda:self.viewOutputRequest(name)
        )
        return btn
    
        
    ########################### for configuring table action ###############
    def addItems(self, items, **kwargs):
        for item in items:
            self.addItem(item, **kwargs)

    def delete(self, name, withConfirm = True):
        try:
            self.logger.info(f"trying to delete the plugin suite {name}")
            succeed = lambda data: self.deleteSucceed(name)
            requestDelete = lambda : self.signal.deleteRequest.emit(
                Request(data=name, succeed= succeed)
            )
            if withConfirm:
                ConfirmBox(f"Confirming to delete {name}?", requestDelete)
            else:
                requestDelete()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("deleting plugin suite", str(e)))
    
    def deleteSucceed(self, name: str):
        rowidx = self.indexFromItem(self.nameToTablePins[name]).row()
        self.removeRow(rowidx)
        self.signal.deleteSucceed.emit(name)
        
    def displayDetail(self, data):
        raise NotImplementedError
    
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
    
    def viewOutputRequest(self, name:str) :
        self.signal.viewOutputRequest.emit(
            Request(data=name, succeed=self.viewPathFile))
    
    def viewPathFile(self, path:str):
        try:
            pid = subprocess.check_call(["open", path]) 
        except Exception as e:
            self.logger.error(e, exc_info=e)
            
    def addItem(self, setting: Tuple[str, Dict[str, str], str], **kwargs):
        self.logger.info(setting)
        name, data = setting
        try:
            newRowIdx = self.rowCount()
            self.insertRow(newRowIdx)
            # set the setting name
            nameItem = QTableWidgetItem(str(name)) \
                       if self.nameAtFstColumn else QTableWidgetItem()
            nameItem.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        
            self.setItem(newRowIdx, 0, nameItem)
            
            for key, col in self.dataKeyToCol.items():
                if isinstance(data[key], list):
                    newItem = self.createListDisplay(data[key], self.rowHeight(newRowIdx))
                    self.setCellWidget(newRowIdx, col, newItem)
                else:
                    newItem = QTableWidgetItem(str(data[key]))
                    newItem.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.setItem(newRowIdx, col, newItem)
            tablePin = self.item(newRowIdx, 0)
            self.nameToTablePins[name] = tablePin 
            self.addCellWidgets(name,  newRowIdx, **kwargs)
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
    
    def createListDisplay(self, items, height):
        listDisplay = QWidget()
        listLayout = QVBoxLayout()
        listDisplay.setLayout(listLayout)
        for item in items:
            newLabel = Label(item, STYLE_DATA.FontSize.BODY)
            listLayout.addWidget(newLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        listScroll = ScrollArea()
        listScroll.setWidget(listDisplay)
        listScroll.setWidgetResizable(True)
        listScroll.setFixedHeight(50)
        initPrimaryColorBackground(listDisplay)
        listScroll.setAutoFillBackground(True)
        listScroll.setStyleSheet(f"background-color: {STYLE_DATA.Color.MAIN_BACKGROUND}; border:none; margin: 0px;")
        listScroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        STYLE_DATA.signal.changeColor.connect(lambda: 
            listScroll.setStyleSheet(f"background-color: {STYLE_DATA.Color.MAIN_BACKGROUND}; border:none; margin: 0px;"))
        return listScroll