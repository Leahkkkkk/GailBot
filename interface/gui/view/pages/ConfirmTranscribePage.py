'''
File: ConfirmTranscribePage.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 11:05:38 am
Modified By:  Siara Small  & Vivian Li
-----
'''
import tomli

from view.Signals import FileSignals
from view.style.styleValues import FontFamily, FontSize, Color
from view.style.Background import initImgBackground
from view.widgets import ( Label, 
                           Button, 
                           TableWidgets,
                           FileTable) 
from util.Logger import makeLogger

from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout,
    QHBoxLayout
)

from PyQt6 import QtCore
from PyQt6.QtCore import Qt 



class ConfirmTranscribePage(QWidget):
    """ Confirm transcription page """
    def __init__(self, signal:FileSignals, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.signal = signal
        self.logger = makeLogger("Frontend")
        self._initConfig()
        self._initWidget()
        self._initLayout()
        self._initStyle()
        self._connectSignal()
    
    def _connectSignal(self):
        self.confirmBtn.clicked.connect(self._sendTranscribeSignal)

    def _initWidget(self):
        """ initlialize widget """
        self.label = Label.Label("Confirm Files and Settings", 
                                 self.config["fontSizes"]["HEADER2"], 
                                 FontFamily.MAIN)
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        self.fileTable = FileTable.FileTable(
            FileTable.ConfirmHeader, 
            self.signal,
            {"setting"}, 
            {})
        
        self.fileTable.resizeCol(FileTable.ConfirmHeaderDimension)
        self.bottomButton = QWidget()
        self.confirmBtn = Button.ColoredBtn("Confirm", self.config["colors"]["GREEN"])
        self.cancelBtn = Button.ColoredBtn("Cancel", self.config["colors"]["ORANGE"])
        
    def _initLayout(self):
        """ initialize layout"""
        self.verticalLayout = QVBoxLayout()
        self.horizontalLayout = QHBoxLayout()
        self.bottomButton.setLayout(self.horizontalLayout)
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        self.verticalLayout.addWidget(self.label)
        self.label.setContentsMargins(0,20,0,50)
        self.verticalLayout.addWidget(self.fileTable,
                                      alignment = Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        
        self.horizontalLayout.addWidget(self.confirmBtn, 
                                      alignment = Qt.AlignmentFlag.AlignRight)
        
        self.horizontalLayout.addWidget(self.cancelBtn, 
                                      alignment = Qt.AlignmentFlag.AlignHCenter)
        
        self.bottomButton.setContentsMargins(0,0,0,0)
        self.verticalLayout.addStretch()
        
        self.verticalLayout.addWidget(self.bottomButton,
                                      alignment=Qt.AlignmentFlag.AlignHCenter)
    
    def _initStyle(self):
        initImgBackground(self,"backgroundConfirmPage.png")
        self.confirmBtn.setMinimumSize(QtCore.QSize(150,30))
        self.cancelBtn.setMinimumSize(QtCore.QSize(150,30))
  
    def _sendTranscribeSignal(self):
        """send a signal with a set of file keys that will be transcribed """
        self.logger.info("here")
        self.logger.info(self.fileTable.transferList)
        self.signal.transcribe.emit(self.fileTable.transferList)
        self.fileTable.transferState()

    def _initConfig(self):
        with open("controller/interface.toml", mode="rb") as fp:
            self.config = tomli.load(fp)
