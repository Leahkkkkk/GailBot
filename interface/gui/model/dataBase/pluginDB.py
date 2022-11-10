from typing import TypedDict, Tuple

from PyQt6.QtCore import QObject, pyqtSignal


class pluginObject(TypedDict):
    Name:str 
    Path:str 

class Signals(QObject):
    send = pyqtSignal(object)
    pluginAdded = pyqtSignal(str)
    error = pyqtSignal(str)


class PluginModel:
    def __init__(self) -> None:
        self.data = dict()
        self.signals = Signals()
    
    def post(self, plugin: Tuple[str, str]) -> None: 
        """ add a new pugin to the data base

        Args:
            plugin (Tuple[str, str]): a tuple with the plugin name  and 
                                      the path to the plugin source
        """     
        name, path = plugin 
        if name not in self.data:
            self.data[name] = path
            self.signals.pluginAdded.emit(name)
        else:
            self.signals.error.emit("plugin name has been taken ")
    
