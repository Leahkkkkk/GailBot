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

from view.config.InstructionText import INSTRUCTION
from view.widgets.Button import InstructionBtn
from view.config.Text import PLUGIN_SUITE_TEXT as TEXT
from view.config.Style import STYLE_DATA
from view.widgets import ColoredBtn, WarnBox, UploadTable, Label, TextInput, initPrimaryColorBackground
from view.widgets import TextInput
from view.config.Style import Color, Dimension
from view.util.ErrorMsg import WARN, ERR
from gbLogger import makeLogger
from PyQt6.QtWidgets import (
    QDialog, 
    QVBoxLayout, 
    QHBoxLayout,
    QFileDialog,
    QWidget
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QObject

class Signal(QObject):
    addPlugin = pyqtSignal(str)
    
class UploadPlugin(QDialog):
    def __init__(self, *arg, **kwarg) -> None:
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
        self.signal = Signal()
        self.logger = makeLogger("F")
        
        self._initWidget()
        self._initLayout()
        self._connectSignal()
        initPrimaryColorBackground(self)
        
    def _initWidget(self):
        """ initializes the widget """
        self.header = Label(
            TEXT.HEADER,
            STYLE_DATA.FontSize.HEADER2, 
            STYLE_DATA.FontFamily.MAIN)
        self.uploadDir = ColoredBtn(
            TEXT.LOAD_DIR,
            STYLE_DATA.Color.PRIMARY_BUTTON)
        self.uploadUrl = ColoredBtn(
            TEXT.LOAD_URL, 
            STYLE_DATA.Color.PRIMARY_BUTTON
        )
        self.displayPlugins = UploadTable()
        self.addBtn = ColoredBtn(
            TEXT.REGISTER,
            STYLE_DATA.Color.SECONDARY_BUTTON
        )
        self.insBtn = InstructionBtn(INSTRUCTION.REGISTER_PLUGIN_SUITE_INS)
        
    def _initLayout(self):
        """ initalize the layout  """
        horizontalLayout = QHBoxLayout()
        horizontalLayout.addWidget(self.uploadDir)
        horizontalLayout.addWidget(self.uploadUrl)
        hContainer = QWidget()
        hContainer.setLayout(horizontalLayout)
        
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.verticalLayout.addWidget(self.header, 
                                      alignment=Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout.addWidget(self.displayPlugins,
                                      alignment=Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout.addWidget(hContainer, 
                                      alignment=Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout.addWidget(self.addBtn, 
                                      alignment=Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout.addWidget(self.insBtn,
                                      alignment=self.insBtn.defaultPos)
        
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
                self.displayPlugins.addItem(selectedFolder)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("uploading plugin", str(e)))

    def _addToPluginList(self, source):
        self.displayPlugins.addItem(source)
        
    def _addFromURL(self):
        self.uploadUrl = UploadURL()
        self.uploadUrl.sendurl.connect(self._addToPluginList)
        self.uploadUrl.exec()
    
    def _postPlugin(self):
        """ send the new plugins through the signal """
        plugins =self.displayPlugins.getValues() 
        if len(plugins) == 0:
            WarnBox(WARN.NO_PLUGIN)
        else:
            for plugin in plugins:
                self.signal.addPlugin.emit(plugin)
            self.close()
            
class UploadURL(QDialog):
    sendurl = pyqtSignal(str)
    def __init__(self) -> None:
        QObject.__init__(self)
        super().__init__()
        
        self._layout = QVBoxLayout()
        self.confirm = ColoredBtn(TEXT.UPLOAD, Color.PRIMARY_BUTTON)
        self.setLayout(self._layout)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.input = TextInput(TEXT.URL, vertical=True, width=400)
        
        self.caption = Label(TEXT.URL_INSTRUCTION, STYLE_DATA.FontSize.BTN, STYLE_DATA.FontFamily.MAIN)
        self._layout.addWidget(self.caption, alignment=Qt.AlignmentFlag.AlignHCenter)
        for source in TEXT.SOURCES:
            sourceText = Label(source, STYLE_DATA.FontSize.BTN, STYLE_DATA.FontFamily.MAIN)
            self._layout.addWidget(sourceText)
        self._layout.addWidget(self.input, alignment=Qt.AlignmentFlag.AlignHCenter)
        self._layout.addWidget(self.confirm, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.confirm.clicked.connect(self.upload)
        initPrimaryColorBackground(self)
    
    def getValue(self) -> str:
        return self.input.getValue()

    def upload(self):
        url = self.input.getValue()
        self.sendurl.emit(url)
        self.close()
   

    
        