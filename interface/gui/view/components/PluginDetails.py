from typing import TypedDict
from view.config import FontFamily, FontSize
from view.widgets import GraphDisplay, MarkdownDisplay, TextDisplay, Label
from PyQt6.QtWidgets import QDialog, QVBoxLayout
from PyQt6.QtCore import Qt

class PluginInfo(TypedDict):
    suite_name : str 
    metadata : dict 
    dependency_graph: dict
    documentation: dict
    
class PluginPopUp(QDialog):
    def __init__(self, pluginInfo: TypedDict) -> None:
        super().__init__()
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)
        self.name = Label(pluginInfo["suite_name"], FontSize.HEADER1, FontFamily.MAIN)
        self.metadata = TextDisplay(pluginInfo["metadata"])
        self.documentation = TextDisplay(pluginInfo["documentation"])
        self.graph = TextDisplay(pluginInfo["dependency_graph"])
        self._layout.addWidget(self.name, alignment=Qt.AlignmentFlag.AlignHCenter)
        self._layout.addWidget(self.metadata)
        self._layout.addWidget(self.documentation)
        self._layout.addWidget(self.graph)