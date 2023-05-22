'''
File: Table.py
Project: GailBot GUI
File Created: 2023/04/01
Author: Siara Small  & Vivian Li
-----
Last Modified:2023/05/19
Modified By:  Siara Small  & Vivian Li
-----
Description: implementation of base class for Table widgets
'''
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
    QHBoxLayout,
)
from PyQt6.QtCore import Qt, QModelIndex
from PyQt6.QtGui import QFont


class BaseTable(QTableWidget):
    signal: DataSignal
    dataKeyToCol: Dict[str, int]
    tableWidth: int = STYLE_DATA.Dimension.DEFAULTTABWIDTH
    tableHeight: int = STYLE_DATA.Dimension.FORMMINHEIGHT
    nameAtFstColumn: bool = True

    def __init__(self, headers, *args, **kwargs):
        print("init table")
        super(BaseTable, self).__init__(0, len(headers))
        self.logger = makeLogger()
        self.headers = headers
        self._initWidget()
        self._initStyle()
        self.nameToTablePins: Dict[str, QTableWidgetItem] = dict()
        self.actionWidgetCol = len(self.headers) - 1
        STYLE_DATA.signal.changeColor.connect(self.changeColor)
        STYLE_DATA.signal.changeFont.connect(self.changeFont)

    ###################### for configuring table style ######################
    def _initStyle(self) -> None:
        """Initialize the table style"""
        self.horizontalHeader().setFixedHeight(45)
        self.setObjectName("FileTable")
        self.setStyleSheet(f"#FileTable{STYLE_DATA.StyleSheet.FILE_TABLE}")
        for i in range(self.columnCount()):
            self.horizontalHeader().setSectionResizeMode(
                i, QHeaderView.ResizeMode.Fixed
            )
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

    def changeColor(self):
        self.setStyleSheet(f"#FileTable{STYLE_DATA.StyleSheet.FILE_TABLE}")
        self.verticalScrollBar().setStyleSheet(STYLE_DATA.StyleSheet.SCROLL_BAR)
        self.horizontalScrollBar().setStyleSheet(STYLE_DATA.StyleSheet.SCROLL_BAR)
        self.horizontalHeader().setStyleSheet(STYLE_DATA.StyleSheet.TABLE_HEADER)
        for c in range(self.columnCount()):
            for r in range(self.rowCount()):
                if isinstance(self.cellWidget(r, c), ScrollArea):
                    self.logger.info(f"found list cell widget in {r}{c}")
                    self.cellWidget(r, c).setStyleSheet(STYLE_DATA.StyleSheet.TABLE_LIST)
   
    def changeFont(self, font=None):
        font = QFont(STYLE_DATA.FontFamily.OTHER, STYLE_DATA.FontSize.TABLE_ROW)
        self.setFont(font)

    def resizeCol(self, widths: List[float]) -> None:
        """takes in a list of width and resize the width of the each
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
        """ initialize the table widget """
        for idx, header in enumerate(self.headers):
            headerItem = QTableWidgetItem(header)
            self.setHorizontalHeaderItem(idx, headerItem)
        self.verticalHeader().hide()
        self.horizontalHeader().setStyleSheet(STYLE_DATA.StyleSheet.TABLE_HEADER)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    ################# for configuring table widget and  ################
    def addCellWidgets(self, name: str, row: int):
        """ add widget to the last table """
        cellWidget = QWidget()
        layout = QHBoxLayout()
        cellWidget.setLayout(layout)
        layout.addWidget(self.getEditBtn(name))
        layout.addWidget(self.getRemoveBtn(name))
        layout.addWidget(self.getViewDetailBtn(name))
        self.setCellWidget(row, self.actionWidgetCol, cellWidget)

    def getRemoveBtn(self, name) -> QWidget:
        """ 
        given the name that will identify the item on the table, 
        return a remove button that will delete the item both on the 
        front-end gui and back-end when clicked
        """
        btn = TableBtn(iconname="tableRemove")
        btn.clicked.connect(lambda: self.delete(name))
        return btn

    def getEditBtn(self, name) -> QWidget:
        """ 
        given the name that identify the item on the table, 
        return a button that will allow user to edit the item 
        when clicked
        """
        btn = TableBtn(iconname="tableEdit")
        btn.clicked.connect(lambda: self.editItem(name))
        return btn

    def getViewDetailBtn(self, name) -> QWidget:
        """ 
        given the name that identify the item on the table
        return a button that allow user to view the detail data 
        of the item when clicked
        """
        btn = TableBtn(iconname="tableDetail")
        btn.clicked.connect(lambda: self.viewDetailRequest(name))
        return btn

    def getViewSourceBtn(self, name) -> QWidget:
        """ 
        given the name that identify the item on the table, 
        return a button that will allow user to view the source file 
        of the item when clicked
        """
        btn = TableBtn(iconname="tableSource")
        btn.clicked.connect(lambda: self.viewSourceRequest(name))
        return btn

    def getViewOutputBtn(self, name) -> QWidget:
        """ 
        given the name that identify the item on the table, 
        return a button that will allow user to view the output file 
        of the item when clicked
        """
        self.logger.info("ask for view output button")
        btn = TableBtn(iconname="tableOutput")
        btn.clicked.connect(lambda: self.viewOutputRequest(name))
        return btn

    ########################### for configuring table action ###############
    def addItems(self, items, **kwargs):
        """ 
        add a list of items to the table
        """
        for item in items:
            self.addItem(item, **kwargs)

    def delete(self, name, withConfirm=True):
        """ 
        send the request to delete the item identified by name
        
        Args:
            name: the name of the item to be deleted
            withConfirm: if true, open up a confirmation pop-up 
                         before sending the deletion request
        """
        try:
            self.logger.info(f"trying to delete the plugin suite {name}")
            succeed = lambda data: self.deleteSucceed(name)
            requestDelete = lambda: self.signal.deleteRequest.emit(
                Request(data=name, succeed=succeed)
            )
            if withConfirm:
                ConfirmBox(f"Confirming to delete {name}?", requestDelete)
            else:
                requestDelete()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("deleting plugin suite", str(e)))

    def deleteSucceed(self, name: str):
        """ 
        delete the item identified by name from the table 
        """
        rowidx = self.indexFromItem(self.nameToTablePins[name]).row()
        self.removeRow(rowidx)
        self.signal.deleteSucceed.emit(name)

    def viewDetailRequest(self, name):
        """ 
        send a request to the backend to ask detail data of item identified 
        by name
        """
        self.signal.getRequest.emit(Request(data=name, succeed=self.displayDetail))

    def displayDetail(self, data):
        """ 
        display the data , sub-class responsibility
        """
        raise NotImplementedError

    def viewSourceRequest(self, name: str):
        """ 
        send a request to get the path to the source file
        """
        self.signal.viewSourceRequest.emit(
            Request(data=name, succeed=self.viewPathFile)
        )

    def displaySource(self, path: str):
        """ 
        given the path, copy the path to the destination directory 
        selected by the user
        """
        try:
            dialog = SaveSetting(origPath=path)
            dialog.exec()
            if dialog.copiedPath:
                pid = subprocess.check_call(["open", dialog.copiedPath])
        except Exception as e:
            self.logger.error(e, exc_info=e)

    def viewPathFile(self, path: str):
        """ 
        given the path, open the path in the user's machine 
        success continuation for view source request
        """
        try:
            pid = subprocess.check_call(["open", path])
        except Exception as e:
            self.logger.error(e, exc_info=e)

    def viewOutputRequest(self, name: str):
        """
        send a request to get the path to the output file, 
        """
        self.signal.viewOutputRequest.emit(
            Request(data=name, succeed=self.viewPathFile)
        )


    def addItem(self, item: Tuple[str, Dict[str, str], str], **kwargs):
        """ 
        add item to the table
        """
        self.logger.info(item)
        name, data = item
        try:
            newRowIdx = self.rowCount()
            self.insertRow(newRowIdx)
            # set the item name
            nameItem = (
                QTableWidgetItem(str(name))
                if self.nameAtFstColumn
                else QTableWidgetItem()
            )
            nameItem.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.setItem(newRowIdx, 0, nameItem)

            for key, col in self.dataKeyToCol.items():
                if isinstance(data[key], list):
                    newItem = self.createListDisplay(data[key])
                    self.setCellWidget(newRowIdx, col, newItem)
                else:
                    newItem = QTableWidgetItem(str(data[key]))
                    newItem.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.setItem(newRowIdx, col, newItem)
            tablePin = self.item(newRowIdx, 0)
            self.nameToTablePins[name] = tablePin
            self.addCellWidgets(name, newRowIdx, **kwargs)
            self.resizeRowsToContents()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("uploading  item to table", str(e)))

    def editSucceed(self, item):
        """ 
        edit the item on the table
        success continuation for edit request
        """
        name, data = item
        rowIdx = self.indexFromItem(self.nameToTablePins[name]).row()
        try:
            for key, col in self.dataKeyToCol.items():
                self.removeCellWidget(rowIdx, col)
                if isinstance(data[key], list):
                    newItem = self.createListDisplay(data[key])
                    newItem.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.setCellWidget(rowIdx, col, newItem)
                else:
                    newItem = QTableWidgetItem(str(data[key]))
                    newItem.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.setItem(rowIdx, col, newItem)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(
                ERR.ERR_WHEN_DUETO.format("updating item changes on table", str(e))
            )

    def sendEditRequest(self, data):
        """ 
        send a request to edit the item 
        """
        self.signal.editRequest.emit(Request(data=data, succeed=self.editSucceed))

    def editItem(self, name):
        """ 
        send a get request to get the current data, and open the edit dialogue 
        that allow user to edit the item 
        """
        self.signal.getRequest.emit(Request(data=name, succeed=self.openEditDialog))

    def openEditDialog(self, data):
        """ 
        open edit dialog that display the current data of the item
        sub-class responsibility 
        """
        pass

    def createListDisplay(self, items):
        """ 
        given the items in a list, return a widget that display the 
        item in a list
        """
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
        listScroll.setStyleSheet(STYLE_DATA.StyleSheet.TABLE_LIST)
        listScroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff) 
        return listScroll
