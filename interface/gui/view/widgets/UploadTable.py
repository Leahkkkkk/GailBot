from typing import Dict, List
import validators
import os
from view.config.Style import STYLE_DATA
from view.config.Text import FILEUPLOAD_PAGE as Text
from gbLogger import makeLogger
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QTableWidget,
    QTableWidgetItem,
    QPushButton)
from view.widgets.MsgBox import WarnBox
from PyQt6.QtCore import QSize, pyqtSignal
from view.util.ErrorMsg import WARN, ERR
class UploadTable(QTableWidget):
    """ a table widget to display a list of data 
    """
    DELETE_BTN_SIZE = STYLE_DATA.Dimension.SMALLICONBTN
    def __init__(self, zeroFileSignal:pyqtSignal = None) -> None:
        """ for displaying a list of source, support action to delete the soure
            from the list 

        Args:
            zeroFileSignal (pyqtSignal, optional): 
            signal will be emitted if there is no source . Defaults to None.
        """
        super().__init__(0,2)
        self.logger = makeLogger()
        self.keyToItem: Dict[str, str] = dict()
        self.zeroFileSignal = zeroFileSignal
        self._initStyle()
        

    def _isAudioFile(self, file_path) -> bool:
        """ 
        helper function to test if the file path is audio file 
        """
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
        self.setColumnWidth(0, self.width()- self.DELETE_BTN_SIZE - 2)
        self.setColumnWidth(1, self.DELETE_BTN_SIZE)
    
    def addItem(self, item:str) -> bool:
        """add an item to the display list 

        Args:
            item (str): a string that stands for the item source

        """
        self.logger.info(f"{item} item added")
        if os.path.isdir(item):
            icon = Text.DIR_LOGO
        elif self._isAudioFile(item):
            icon = Text.AUDIO_LOGO
        elif validators.url(item):
            icon = Text.URL_LOGO
        else:
            icon = " "
            
        try:
            row = self.rowCount()
            self.insertRow(row)
            self.keyToItem[row] = item
            filestr = item
            newFile = QTableWidgetItem(icon + filestr)
            self.setItem(row, 0, newFile)
            
            btn = QPushButton(Text.DELETE_LOGO)
            btn.setFixedSize(QSize(self.DELETE_BTN_SIZE, self.DELETE_BTN_SIZE))
            btn.setContentsMargins(1,5,1,5)
            self.setCellWidget(row, 1, btn)
            btn.clicked.connect(lambda: self.deleteItem(row, newFile))
            self.resizeRowsToContents()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("displaying uploaded item", str(e)))
    
    def deleteItem(self, key, item: QTableWidgetItem) -> bool:
        """ delete an Item from the file display list and 
            internal dictionary keyToItem which stores the items 
            on the table 

        Args:
            key (str): the key of the item
            item (QTableWidgetItem): the table widget that display the item 
        """
        try:
            row = self.indexFromItem(item).row()
            self.removeRow(row)
            del self.keyToItem[key]
            if not self.keyToItem and self.zeroFileSignal:
                self.zeroFileSignal.emit()
        except Exception as e:
            self.logger.error(e, exc_info=e)
        
        
    def getValues(self) -> List[str]:
        """return the list of sources stored on the table 
        """
        return list(self.keyToItem.values())
