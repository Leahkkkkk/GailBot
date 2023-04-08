from typing import Dict, List
import validators
import os
from view.config.Style import STYLE_DATA
from view.config.Text import FileUploadPageText as Text
from gbLogger import makeLogger
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QTableWidget,
    QTableWidgetItem,
    QPushButton)
from view.widgets.MsgBox import WarnBox
from PyQt6.QtCore import QSize
from view.util.ErrorMsg import WARN, ERR
class UploadTable(QTableWidget):
    """ a table widget to display a list of data 
    """
    def __init__(self) -> None:
        super().__init__(0,2)
        self.logger = makeLogger("F")
        self.keyToItem: Dict[str, str] = dict()
        self._initStyle()

    def isAudioFile(self, file_path):
        audio_extensions = {'.mp3', '.wav', '.flac', '.aac', '.m4a', '.wma', '.ogg', '.opus'}
        file_extension:str  = os.path.splitext(file_path)[1]
        return file_extension.lower() in audio_extensions 
    
    def _initStyle(self) -> None:
        self.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection)
        self.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers)
        self.horizontalHeader().hide()
        self.verticalHeader().hide()
        self.setStyleSheet(f"background-color:{STYLE_DATA.Color.MAIN_BACKGROUND};"
                                           f"color:{STYLE_DATA.Color.MAIN_TEXT}")
        self.setColumnWidth(0,STYLE_DATA.Dimension.SMALL_TABLE_WIDTH) 
        self.setFixedSize(QSize(STYLE_DATA.Dimension.SMALL_TABLE_WIDTH,
                                                STYLE_DATA.Dimension.SMALL_TABLE_HEIGHT)) 
        self.setColumnWidth(0, 325)
        self.setColumnWidth(1, 25)
    
    def addItem(self, item:str) -> bool:
        self.logger.info(f"{item} item added")
        if os.path.isdir(item):
            icon = Text.directoryLogo
        elif self.isAudioFile(item):
            icon = Text.audioLogo
        elif validators.url(item):
            icon = Text.urlLogo
        else:
            icon = " "
            
        try:
            row = self.rowCount()
            self.insertRow(row)
            self.keyToItem[row] = item
            filestr = item
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
    
    def deleteItem(self, key, item: QTableWidgetItem) -> bool:
        try:
            row = self.indexFromItem(item).row()
            self.removeRow(row)
            del self.keyToItem[key]
        except Exception as e:
            self.logger.error(e, exc_info=e)
        
        
    def getValues(self) -> List[str]:
        return list(self.keyToItem.values())
