'''
File: PluginDialog.py
Project: GailBot GUI
File Created: Sunday, 30th October 2022 7:06:50 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Tuesday, 8th November 2022 4:01:32 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: implementation of the plugin dialog for user to upload new plugin
'''


import os 

from view.Signals import ProfileSignals
from view.widgets import Button, MsgBox
from util.Style import Color, Dimension
from util.Text import CreatNewProfileTabText as Text 

from PyQt6.QtWidgets import (
    QDialog, 
    QListWidget, 
    QVBoxLayout, 
    QFileDialog
)
from PyQt6.QtCore import Qt, QSize 

class PluginDialog(QDialog):
    def __init__(self, signal:ProfileSignals, *arg, **kwarg) -> None:
        """ a pop up dialog that allow  user to load new plugin
            once the user confirms adding the plugin, the widget will 
            send a signal to post the newly added plugin to the database

        Constructor Args:
            signal (ProfileSignals): a signal used to post plugin data to 
                                    database
        """
        super().__init__(*arg, **kwarg)
        self.setMinimumSize(
            QSize(Dimension.DEFAULTTABHEIGHT, Dimension.DEFAULTTABHEIGHT))
        self.plugins = dict()
        self.signal = signal
        self._initWidget()
        self._initLayout()
        self._connectSignal()
        
    def _initWidget(self):
        """ initializes the widget """
        self.uploadBtn = Button.ColoredBtn(
            "Load Plugins",
            Color.PRIMARY_BUTTON)
        self.displayPlugins = QListWidget()
        self.addBtn = Button.ColoredBtn(
            "Add Plugins",
            Color.SECONDARY_BUTTON
        )
        
    def _initLayout(self):
        """ initalize the layout  """
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.verticalLayout.addWidget(self.displayPlugins)
        self.verticalLayout.addWidget(self.uploadBtn, 
                                      alignment=Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.addBtn, 
                                      alignment=Qt.AlignmentFlag.AlignRight)

    def _connectSignal(self):
        """ connects the file signals upon button click """
        self.uploadBtn.clicked.connect(self._addPlugins)
        self.addBtn.clicked.connect(self._postPlugins)
        
    def _addPlugins(self):
        """ open a file dialog to let user load file """
        dialog = QFileDialog()
        dialog.setFileMode(dialog.FileMode.ExistingFiles)
        filter = Text.pluginFilter
        dialog.setNameFilter(filter)
        dialog.exec()
        files = dialog.selectedFiles()
        if files:
            for file in files:
                name = os.path.basename(file)
                self.plugins[name] = file
        self.displayPlugins.addItems(list(self.plugins))
             

    def _postPlugins(self):
        """ send the new plugins through the signal """
        if not self.plugins:
            MsgBox.WarnBox("No plugin is added")
        else:
            for key, plugin in self.plugins.items():
                self.signal.addPlugin.emit((key, plugin))
            self.close()