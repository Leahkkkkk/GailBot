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
from view.widgets.Button import ToggleBtn, iconBtn, ColoredBtn
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

from PyQt6.QtCore import QSize, Qt


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

class selectAndCheck(QWidget):
    def __init__(self, *args, **kwagrs):
        super().__init__(*args, **kwagrs)
        layout = QHBoxLayout(self)
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)
        directory = iconBtn("directory.png")
        directory.setStyleSheet("background-color:white;")
        directory.setFixedSize(QSize(25,25))
        checkBox = QCheckBox(self)
        layout.addWidget(directory)
        layout.addWidget(checkBox)
        checkBox.setStyleSheet("margin-left: 10px")
        directory.clicked.connect(self._showDetail)
        self.setFixedSize(Dimension.ACTION)
    
    def _showDetail(self):
        Dialog = FileDetaial()
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
        firstCellWidget = selectAndCheck()
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
        
        

class FileDetaial(QDialog):
    def __init__(
        self, 
        files=["file1", "file2", "file3", "file4", "file5", "file6"] , 
        transcriber="Dummy", 
        date="2022/10/10",
        *args, 
        **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setWindowTitle("File Datails")
        self.setMinimumSize(Dimension.MEDIUMDIALOG)
        self.files = files 
        self.transcriberStr = transcriber
        self.dateStr = date
        self._initWidget()
        self._initLayout()

    def _initWidget(self):
        self.transcriber = InputBox.InputBox("Transcribed by: ", True, FontSize.SMALL)
        self.transcriber.setText(self.transcriberStr)
        self.transcribeDate = InputBox.InputBox("Transcribed on: ", True, FontSize.SMALL)
        self.transcribeDate.setText(self.dateStr)
        self.transcribeDate.disableEdit()
       
        self.inDirLabel = Label.Label("In this directory", FontSize.BODY, 
                                          FontFamily.MAIN)
        self.inDirLabel.setMinimumWidth(200)
        self.aboutDirLabel = Label.Label("About this directory", FontSize.BODY, 
                                          FontFamily.MAIN)
        self.fileList = DirectoryView(self.files)
        self.saveBtn = ColoredBtn("save",Color.BLUEDARK, FontSize.SMALL)
        self.saveBtn.setFixedSize(QSize(50,35))
        self.saveBtn.clicked.connect(self._close)
        
    def _initLayout(self):
        self.gridlayout = QGridLayout(self)
        self.setLayout(self.gridlayout)
        self.gridlayout.addWidget(self.inDirLabel, 0, 0, 2, 2, 
                                  alignment=Qt.AlignmentFlag.AlignTop)
        self.gridlayout.addWidget(self.fileList, 1, 0,2,2)
        self.gridlayout.addWidget(self.aboutDirLabel, 0, 2, 1, 2,
                                  alignment=Qt.AlignmentFlag.AlignTop)
        self.gridlayout.addWidget(self.transcriber, 1, 2)
        self.gridlayout.addWidget(self.transcribeDate, 1, 3)
        self.gridlayout.addWidget(self.saveBtn, 2,3, 
                                  alignment=Qt.AlignmentFlag.AlignRight)
        Background.initBackground(self, Color.BLUEWHITE)
        
    
    def _close(self):
        self.close()
    
    


class DirectoryView(QWidget):
    def __init__(self,files: list, *args, **kwargs) -> None:
        super().__init__( *args, **kwargs)
        self.layout = QGridLayout()
        count = 0
        for file in files:
            label = Label.Label(file,FontSize.SMALL, color=Color.GREYDARK)
            self.layout.addWidget(label, count//2, count%2, 
                                  alignment=Qt.AlignmentFlag.AlignTop)
            count += 1
        self.setLayout(self.layout)
        self.setMinimumSize(QSize(200, 140))
        