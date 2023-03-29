from PyQt6.QtWidgets import QDialog
from view.widgets import DisplayGraph, DisplayMarkdown

class PluginPopUp(QDialog):
    def __init__(self, pluginInfo) -> None:
        super().__init__()
        