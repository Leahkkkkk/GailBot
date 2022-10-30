import os 

from view.Signals import ProfileSignals
from view.widgets import Button, MsgBox
from view.style.styleValues import Color, FontSize, Dimension
from view.style.Background import initBackground
from PyQt6.QtWidgets import QDialog, QListWidget, QVBoxLayout, QFileDialog
from PyQt6.QtCore import Qt


class PluginDialog(QDialog):
    def __init__(self, signal:ProfileSignals, *arg, **kwarg) -> None:
        super().__init__(*arg, **kwarg)
        self.setMinimumSize(300,300)
        self.setMaximumSize(500,500)
        self.plugins = dict()
        self.signal = signal
        self._initWidget()
        self._initLayout()
        self._connectSignal()
        initBackground(self, Color.BLUEWHITE)
        
    def _initWidget(self):
        self.uploadBtn = Button.ColoredBtn(
            "Load Plugins",
            Color.BLUEMEDIUM)
        self.displayPlugins = QListWidget()
        self.addBtn = Button.ColoredBtn(
            "Add Plugins",
            Color.GREEN
        )
        
    def _initLayout(self):
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.verticalLayout.addWidget(self.displayPlugins)
        self.verticalLayout.addWidget(self.uploadBtn, 
                                      alignment=Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.addBtn, 
                                      alignment=Qt.AlignmentFlag.AlignRight)
        self.uploadBtn.setFixedSize(Dimension.BGBUTTON)
        self.addBtn.setFixedSize(Dimension.BGBUTTON)
        
    
    def _connectSignal(self):
        self.uploadBtn.clicked.connect(self._addPlugins)
        self.addBtn.clicked.connect(self._postPlugins)

        
    def _addPlugins(self):
        dialog = QFileDialog()
        dialog.setFileMode(dialog.FileMode.ExistingFiles)
        filer = "json file (*.json *.py)"
        dialog.setNameFilter(filer)
        dialog.exec()
        files = dialog.selectedFiles()
        if files:
            for file in files:
                name = os.path.basename(file)
                self.plugins[name] = file
        self.displayPlugins.addItems(list(self.plugins))
             

    def _postPlugins(self):
        if not self.plugins:
            MsgBox.WarnBox("No plugin is added")
        else:
            for key, plugin in self.plugins.items():
                print(key, plugin)
                self.signal.addPlugin.emit((key, plugin))
            self.close()