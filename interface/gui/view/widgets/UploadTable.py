from typing import Dict
import os
from view.config.Style import Color, FontSize, Dimension, FontFamily
from view.config.Text import FileUploadPageText as Text
from gbLogger import makeLogger
from PyQt6.QtWidgets import (
    QWidget,
    QFileDialog, 
    QLineEdit,
    QHBoxLayout,
    QVBoxLayout,
    QAbstractItemView,
    QTableWidget,
    QTableWidgetItem,
    QPushButton)
from view.widgets.MsgBox import WarnBox
from PyQt6.QtCore import QSize, Qt
from view.util.ErrorMsg import WARN, ERR
from PyQt6.QtGui import QDragEnterEvent 


class UploadTable(QTableWidget):
    def __init__(self) -> None:
        super().__init__()
        self.logger = makeLogger("F")
        self.keyToItem: Dict[str, str] = dict()
    
    def _initStyle(self) -> None:
        self.insertColumn(0)
        self.insertColumn(1)
        self.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection)
        self.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers)
        self.horizontalHeader().hide()
        self.verticalHeader().hide()
        self.setStyleSheet(f"background-color:{Color.MAIN_BACKGROUND};"
                                           f"color:{Color.MAIN_TEXT}")
        self.setColumnWidth(0,Dimension.SMALL_TABLE_WIDTH) 
        self.setFixedSize(QSize(Dimension.SMALL_TABLE_WIDTH,
                                                Dimension.SMALL_TABLE_HEIGHT)) 
        self.setColumnWidth(0, 325)
        self.setColumnWidth(1, 25)
    
    def addItem(self, item:str) -> bool:
        icon = Text.directoryLogo if os.path.isdir(item) else Text.audioLogo
        try:
            row = self.rowCount()
            self.insertRow(row)
            self.keyToItem[row] = item
            filestr = os.path.join(os.path.basename(os.path.dirname(item)),os.path.basename(item))
            newFile = QTableWidgetItem(icon + filestr)
            self.setItem(row, 0, newFile)
            btn = QPushButton(Text.delete)
            btn.setFixedSize(QSize(20,20))
            btn.setContentsMargins(1,5,1,5)
            self.setCellWidget(row, 1, btn)
            btn.clicked.connect(lambda: self.deleteItem(row, newFile))
            self.resizeRowsToContents()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("displaying uploaded item", str(e)))
        raise NotImplementedError
    
    def deleteItem(self, key, item: QTableWidgetItem) -> bool:
        try:
            row = self.indexFromItem(item).row()
            self.removeRow(row)
            del self.keyToItem[key]
        except Exception as e:
            self.logger.error(e, exc_info=e)
