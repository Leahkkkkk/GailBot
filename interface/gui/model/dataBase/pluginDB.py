from typing import TypedDict, Tuple
from model.dummySettingData import dummySettingForms
from PyQt6.QtCore import QObject, pyqtSignal

KEYERROR = "Plugin key not found"

class pluginObject(TypedDict):
    Name:str 
    Path:str 

class Signals(QObject):
    send = pyqtSignal(object)
    pluginAdded = pyqtSignal(str)
    error = pyqtSignal(str)
    
class PluginModel:
    def __init__(self) -> None:
        self.data = dummySettingForms["Plugins"]
        self.signals = Signals()
    
    def post(self, plugin: Tuple[str, str]) -> None: 
        name, path = plugin 
        if name not in self.data:
            self.data[name] = path
            self.signals.pluginAdded.emit(name)
        else:
            self.signals.error.emit("plugin name has been taken ")
    
