'''
File: FileTable.py
Project: GailBot GUI
File Created: Sunday, 9th October 2022 6:56:46 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Sunday, 9th October 2022 6:57:12 pm
Modified By:  Siara Small  & Vivian Li
-----
'''

from view.style.styleValues import Color, FontSize, Dimension, FontFamily
from model.FileModel import FileModel
from view.widgets.Button import ToggleBtn, iconBtn
from view.widgets import InputBox, Label
from view.style import Background

from PyQt6.QtWidgets import (
    QTableView, 
    QHeaderView,
    QDialog,
    QAbstractItemView, 
    QCheckBox,
    QWidget,
    QHBoxLayout,
    QGridLayout)
from PyQt6.QtCore import QSize


class Actions(QWidget):
    def __init__(self, *args, **kwagrs):
        super().__init__(*args, **kwagrs)
        self.setFixedSize(Dimension.ACTION)
        self.layout = QHBoxLayout(self)
        self.layout
        self.setLayout(self.layout)
        self.setBtn  = iconBtn("settings.png")
        self.deleteBtn = iconBtn("trash.png")
        self.saveBtn = iconBtn("disk.png")
        self.layout.addWidget(self.setBtn)
        self.layout.addWidget(self.deleteBtn)
        self.layout.addWidget(self.saveBtn)
        self.layout.setContentsMargins(0,0,0,0)

class checkAndToggle(QWidget):
    def __init__(self, *args, **kwagrs):
        super().__init__(*args, **kwagrs)
        layout = QHBoxLayout(self)
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)
        toggle = ToggleBtn(parent=self)
        toggle.setStyleSheet("border: none;"
                             "background-color:white;"
                             f"color:{Color.BLUEMEDIUM}")
        checkBox = QCheckBox(self)
        layout.addWidget(toggle)
        layout.addWidget(checkBox)
        checkBox.setStyleSheet("margin-left: 10px")
        toggle.clicked.connect(self._toggle)
    
    def _toggle(self):
        Dialog = FileDetail()
        Dialog.exec()
        
class FileTable(QTableView):
    """ fie table widget """
    def __init__(self, *args, **kwargs) -> None:
        """initialize table model from QTableView"""
        super().__init__(*args, **kwargs)
        self.setMinimumSize(QSize(800, 200))
        self.setMaximumSize(QSize(800, 300))
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self._initStyle()
    
    def setFileModel(self, model:FileModel):
        self.model = model
        self.setModel(model)
        self.columnCount = model.columnCount(0) 
        self.addActionWidget()
        self.setTableLayout()
    
    def setTableLayout(self):
        self.setColumnWidth(0,80)
        self.setColumnWidth(1,90)
        self.setColumnWidth(2,140)
        self.setColumnWidth(6,70)
        self.setColumnWidth(8,160)
        
    def addActionWidget(self):
        """ add acton buttons and checkbox to table cell """
        firstCellWidget = checkAndToggle()
        lastCellWidget = Actions()
        idx = self.model.rowCount(0) - 1
        self.setIndexWidget(self.model.index(idx,0), firstCellWidget)
        self.setIndexWidget(self.model.index(idx,self.columnCount - 1), 
                            lastCellWidget)
    
    def _toggle(self):
        pass
    
    def _initStyle(self):
        self.horizontalHeader().setStyleSheet(f"font-size:{FontSize.BODY};"
                                               "font-weight:600")

class confirmTable(FileTable):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    
    def setTableLayout(self):
        self.setColumnWidth(0,80)
        self.setColumnWidth(1,120)
        self.setColumnWidth(2,280)
        self.setColumnWidth(3,130)
        self.setColumnWidth(4,180)


class progressTable(FileTable):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    
    def setTableLayout(self):
        self.setColumnWidth(0,80)
        self.setColumnWidth(1,80)
        self.setColumnWidth(2,450)
        self.setColumnWidth(3,170)

class successTable(FileTable):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    
    def setTableLayout(self):
        self.setColumnWidth(0,80)
        self.setColumnWidth(1,80)
        self.setColumnWidth(2,210)
        self.setColumnWidth(3,120)
        self.setColumnWidth(4,150)
        self.setColumnWidth(5,150)
        
        

class FileDetail(QDialog):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setWindowTitle("File Datails")
        self.setFixedSize(Dimension.MEDIUMDIALOG)
        self._initWidget()
        self._initLayout()

    def _initWidget(self):
        self.transcriber = InputBox.InputBox("Transcribed by: ")
        self.transcribeDate = InputBox.InputBox("Transcribed on: ")
        self.inDirLabel = Label.Label("In this directory", FontSize.SMALL, 
                                          FontFamily.OTHER)
        self.aboutDirLabel = Label.Label("About this directory", FontSize.SMALL, 
                                          FontFamily.OTHER)
        
    def _initLayout(self):
        self.gridlayout = QGridLayout(self)
        self.setLayout(self.gridlayout)
        self.gridlayout.addWidget(self.inDirLabel, 0, 0, 2, 2)
        self.gridlayout.addWidget(self.aboutDirLabel, 0, 2, 1, 2)
        self.gridlayout.addWidget(self.transcriber, 1, 2)
        self.gridlayout.addWidget(self.transcribeDate, 1, 3)
        Background.initBackground(self)
        
        
            