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
from view.config.Style import Color, Dimension
from view.config.Text import CreateNewProfileTabText as Text 
from view.util.io import get_name
from gbLogger import makeLogger
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
        self.plugins = list()
        self.signal = signal
        self.logger = makeLogger("F")
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
        self.uploadBtn.clicked.connect(self._addPlugin)
        self.addBtn.clicked.connect(self._postPlugin)
        
    def _addPlugin(self):
        """ open a file dialog to let user load file """
        try:
            dialog = QFileDialog()
            selectedFolder = dialog.getExistingDirectory()
            if selectedFolder:
                self.plugins.append(selectedFolder)
                self.displayPlugins.addItem(get_name(selectedFolder))
        except Exception as e:
            self.logger.error(e, exc_info=e)

    def _postPlugin(self):
        """ send the new plugins through the signal """
        if not self.plugins:
            MsgBox.WarnBox("No plugin is added")
        else:
            for plugin in self.plugins:
                self.signal.addPlugin.emit(plugin)
            self.close()