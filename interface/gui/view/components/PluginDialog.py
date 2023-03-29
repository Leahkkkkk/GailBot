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
import validators

from view.Signals import ProfileSignals
from view.widgets import ColoredBtn, WarnBox
from view.widgets import TextInput
from view.config.Style import Color, Dimension
from view.config.Text import CreateNewProfileTabText as Text 
from view.util.io import get_name
from view.util.ErrorMsg import WARN, ERR
from gbLogger import makeLogger
from PyQt6.QtWidgets import (
    QDialog, 
    QListWidget, 
    QVBoxLayout, 
    QHBoxLayout,
    QFileDialog,
    QWidget
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QObject

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
        self.uploadDir = ColoredBtn(
            "Load from Directory",
            Color.PRIMARY_BUTTON)
        self.uploadUrl = ColoredBtn(
            "Load from URL", 
            Color.PRIMARY_BUTTON
        )
        self.displayPlugins = QListWidget()
        self.addBtn = ColoredBtn(
            "Register Plugin",
            Color.SECONDARY_BUTTON
        )
        
    def _initLayout(self):
        """ initalize the layout  """
        horizontalLayout = QHBoxLayout()
        horizontalLayout.addWidget(self.uploadDir)
        horizontalLayout.addWidget(self.uploadUrl)
        hContainer = QWidget()
        hContainer.setLayout(horizontalLayout)
        
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.verticalLayout.addWidget(self.displayPlugins)
        self.verticalLayout.addWidget(hContainer, 
                                      alignment=Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.addBtn, 
                                      alignment=Qt.AlignmentFlag.AlignCenter)

    def _connectSignal(self):
        """ connects the file signals upon button click """
        self.uploadDir.clicked.connect(self._addFromDir)
        self.addBtn.clicked.connect(self._postPlugin)
        self.uploadUrl.clicked.connect(self._addFromURL)
        
    def _addFromDir(self):
        """ open a file dialog to let user load file """
        try:
            dialog = QFileDialog()
            selectedFolder = dialog.getExistingDirectory()
            if selectedFolder:
                self.plugins.append(selectedFolder)
                self.displayPlugins.addItem(get_name(selectedFolder))
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("uploading plugin", str(e)))

    def _addToPluginList(self, source):
        self.plugins.append(source)
        self.displayPlugins.addItem(source)
        
    def _addFromURL(self):
        """ TODO: """
        self.uploadUrl = UploadURL()
        self.uploadUrl.sendurl.connect(self._addToPluginList)
        self.uploadUrl.exec()
    
    def _postPlugin(self):
        """ send the new plugins through the signal """
        if not self.plugins:
            WarnBox(WARN.NO_PLUGIN)
        else:
            for plugin in self.plugins:
                self.signal.addPlugin.emit(plugin)
            self.close()
            
class UploadURL(QDialog):
    sendurl = pyqtSignal(str)
    def __init__(self) -> None:
        QObject.__init__(self)
        super().__init__()
        
        self._layout = QVBoxLayout()
        self.input = TextInput("Plugin URL", vertical=True)
        self.confirm = ColoredBtn("Upload", Color.PRIMARY_BUTTON)
        self.setLayout(self._layout)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self._layout.addWidget(self.input)
        self._layout.addWidget(self.confirm)
        self.confirm.clicked.connect(self.upload)
    
    def getValue(self) -> str:
        return self.input.getValue()

    def upload(self):
        url = self.input.getValue()
        if validators.url(url):
            self.sendurl.emit(url)
            self.close()
        else:
            WarnBox(WARN.INVALID_PLUGIN_URL)
        

    
        