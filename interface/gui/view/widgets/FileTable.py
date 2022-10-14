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

from multiprocessing import parent_process
from view.style.styleValues import Color, FontSize, Dimension, FontFamily
from model.FileModel import FileModel
from view.widgets import TableWidgets

from PyQt6.QtWidgets import (
    QTableView, 
    QHeaderView,
    QAbstractItemView, 
  
)

from PyQt6.QtCore import QSize, Qt

class FileTable(QTableView):
    """ fie table widget """
    def __init__(
        self,   
        *args, 
        **kwargs) -> None:
        """initialize table model from QTableView"""
        super().__init__(*args, **kwargs)
        self.fullDetail = False 
        self.setMinimumSize(QSize(800, 200))
        self.setMaximumSize(QSize(800, 300))
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self._initStyle()
    
    def setFileModel(self, model:FileModel, setFun, createFun, deleteFun):
        self.model = model
        self.setModel(model)
        self.columnCount = model.columnCount(0) 
        self.addActionWidget(setFun, createFun, deleteFun)
        self.setTableLayout()
        self.setLineWidth(100)
    
    def setTableLayout(self):
        self.setColumnWidth(0,80)
        self.setColumnWidth(1,90)
        self.setColumnWidth(2,140)
        self.setColumnWidth(6,70)
        self.setColumnWidth(8,160)
        
    def addActionWidget(self,setFun, createFun, deleteFun, key=0):
        """ add acton buttons and checkbox to table cell """
        firstCellWidget = TableWidgets.selectAndCheck(self.fullDetail)
        lastCellWidget = TableWidgets.Actions(setFun, createFun, deleteFun,key)
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
        self.fullDetail = True
    
    def setTableLayout(self):
        self.setColumnWidth(0,60)
        self.setColumnWidth(1,130)
        self.setColumnWidth(2,300)
        self.setColumnWidth(3,100)
        self.setColumnWidth(4,150)
        self.setRowHeight(0,40)
  
    def addActionWidget(self, setFun, createFun, deleteFun, key=0):
        """ add acton buttons and checkbox to table cell """
        pass
    
    def addFirstAction(self, toggleFun):
        firstCellWidget = TableWidgets.ConfirmAction(toggleFun)
        idx = self.model.rowCount(0) - 1
        self.setIndexWidget(self.model.index(idx,0), firstCellWidget)
     
class progressTable(FileTable):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fullDetail = True

    def setTableLayout(self):
        self.setColumnWidth(0,80)
        self.setColumnWidth(1,80)
        self.setColumnWidth(2,400)
        self.setColumnWidth(3,220)
        self.setRowHeight(0,40)
    
    def addActionWidget(self, setFun, createFun, deleteFun, key=0):
        firstCellWidget = TableWidgets.selectAndCheck(self.fullDetail)
        idx = self.model.rowCount(0) - 1
        self.setIndexWidget(self.model.index(idx,0), firstCellWidget)
    
    
class successTable(FileTable):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fullDetail = True

    def setTableLayout(self):
        self.setColumnWidth(0,80)
        self.setColumnWidth(1,80)
        self.setColumnWidth(2,180)
        self.setColumnWidth(3,120)
        self.setColumnWidth(4,120)
        self.setColumnWidth(5,200)
        self.setRowHeight(0,40)
     
    def addActionWidget(self, setFun, createFun, deleteFun, key=0):
        """ add acton buttons and checkbox to table cell """
        firstCellWidget = TableWidgets.selectAndCheck(self.fullDetail)
        lastCellWidget = TableWidgets.PosTranscribeAction(setFun, createFun, deleteFun)
        idx = self.model.rowCount(0) - 1
        self.setIndexWidget(self.model.index(idx,0), firstCellWidget)
        self.setIndexWidget(self.model.index(idx,self.columnCount - 1), 
                            lastCellWidget)
        
    def addFirstAction(self, toggleFun):
        firstCellWidget = TableWidgets.ConfirmAction(toggleFun)
        idx = self.model.rowCount(0) - 1
        self.setIndexWidget(self.model.index(idx,0), firstCellWidget)
        


