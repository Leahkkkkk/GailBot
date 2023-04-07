from typing import TypedDict
from view.config import FontFamily, FontSize, Dimension
from view.widgets import GraphDisplay, MarkdownDisplay, TextDisplay, Label, ScrollArea
from view.widgets.Background import initPrimaryColorBackground
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

class PluginInfo(TypedDict):
    suite_name : str 
    metadata : dict 
    dependency_graph: dict
    documentation: dict
    
class PluginSuiteDetails(QDialog):
    def __init__(self, pluginInfo: TypedDict) -> None:
        super().__init__()
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)
        self.maincontainer = QWidget()
        self._containerLayout = QVBoxLayout()
        self.maincontainer.setLayout(self._containerLayout)
        self._scroll = ScrollArea()
        self._scroll.setWidget(self.maincontainer)
        self._scroll.setWidgetResizable(True)
        self.name = Label(pluginInfo["suite_name"], FontSize.HEADER1, FontFamily.MAIN)
        self.metadata = TextDisplay(pluginInfo["metadata"])
        self.documentation = MarkdownDisplay(pluginInfo["documentation"])
        self.graph = GraphDisplay(pluginInfo["dependency_graph"])
        self._containerLayout.addWidget(self.name, alignment=Qt.AlignmentFlag.AlignHCenter)
        self._containerLayout.addWidget(self.metadata)
        self._containerLayout.addWidget(self.graph)
        self._containerLayout.addWidget(self.documentation)
        self.setMinimumWidth(Dimension.WIN_MIN_WIDTH)
        self.setMaximumWidth(Dimension.WINMAXWIDTH)
        self._scroll.setMinimumWidth(Dimension.WIN_MIN_WIDTH - Dimension.MEDIUM_SPACING)
        self._scroll.setMaximumWidth(Dimension.WINMAXWIDTH - Dimension.MEDIUM_SPACING)
        self.setMaximumHeight(900)
        self.setMinimumHeight(750)
        self._scroll.setMaximumHeight(900)
        self._scroll.ensureWidgetVisible(self.maincontainer)
        self._layout.addWidget(self._scroll, alignment=Qt.AlignmentFlag.AlignHCenter)
        initPrimaryColorBackground(self)