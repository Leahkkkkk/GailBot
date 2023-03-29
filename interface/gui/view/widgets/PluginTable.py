from typing import List, Dict
from PyQt6.QtWidgets import (
    QTableWidget, 
    QTableWidgetItem, 
    QWidget, 
    QHeaderView,
    QPushButton,
    QHeaderView
)

from PyQt6.QtCore import (
    QObject,
    Qt,
    QSize,
    pyqtSignal
)


class PluginTable(QTableWidget):
    def __init__(self):
        self.plugins: Dict[str, Dict[str, str]] = dict()
        self.nameToTablepins = Dict[str, QTableWidgetItem] = dict()
        self.headers = ["Plugin Name", "Author", "Version", "Plugin Details"]
        self._initWidget()
        
    def _initWidget(self):
        self.setHorizontalHeaderLabels(self.headers)
        self.verticalHeader().hide()
    
    def addPlugins(self, plugins: List[Dict]):
        raise NotImplementedError
    
    def addPlugin(self, pluginInfo: Dict[str, str]):
        raise NotImplementedError
    
    def deletePlugin(self, pluginName:str):
        raise NotImplementedError
   
    def seePluginDetails(self, pluginName:str):
        raise NotImplementedError
    