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

from view.style.styleValues import Color
from view.widgets import Actions
from model.FileModel import FileModel
from view.widgets.Button import ToggleBtn

from PyQt6.QtWidgets import (
    QTableView, 
    QHeaderView,
    QAbstractItemView, 
    QCheckBox,
    QWidget,
    QLabel,
    QHBoxLayout)
from PyQt6.QtCore import QSize

class FileTable(QTableView):
    """ fie table widget """
    def __init__(self, model:FileModel, *args, **kwargs) -> None:
        """initialize table model from QTableView"""
        super().__init__(*args, **kwargs)
        self.model = model
        self.setModel(model) 
        self.setMinimumSize(QSize(800, 200))
        self.setMaximumSize(QSize(800, 300))
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.setColumnWidth(0,90)
        self.setColumnWidth(1,90)
        self.addActionWidget()
    
    def rowCountChanged(self, oldCount, newCount):
        print("called")
        self._addActionWidget(oldCount)
    
    def addActionWidget(self):
        widgetContainer = QWidget()
        layout = QHBoxLayout(widgetContainer)
        layout.setContentsMargins(0,0,0,0)
        toggle = ToggleBtn(parent = widgetContainer)
        toggle.clicked.connect(self._toggle)
        toggle.setStyleSheet("border: none;"
                             "background-color:white;"
                             f"color:{Color.BLUEMEDIUM}")
        checkBox = QCheckBox(widgetContainer)
        layout.addWidget(toggle)
        layout.addWidget(checkBox)
        checkBox.setStyleSheet("margin-left: 10px")
        action = Actions.Actions()
        idx = self.model.rowCount(0) - 1
        self.setIndexWidget(self.model.index(idx,0), widgetContainer)
        self.setIndexWidget(self.model.index(idx,7), action)
    
    def _toggle(self):
        pass
     