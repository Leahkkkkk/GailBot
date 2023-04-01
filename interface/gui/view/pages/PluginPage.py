'''
File: SettingPage.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Sunday, 6th November 2022 11:11:19 am
Modified By:  Siara Small  & Vivian Li
-----
Description: implementation of the plugin page
'''
from typing import Dict, List, Any
from view.config.Style import FontSize, Dimension, FontFamily, Color
from view.config.Text import ProfilePageText as Text
from view.config.Text import ProfileSettingForm as Form
from gbLogger import makeLogger
from view.widgets import Label, ColoredBtn
from view.widgets.PluginTable import PluginTable
from view.components.UploadPluginDialog import UploadPlugin
from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout)
from PyQt6.QtCore import Qt

center  = Qt.AlignmentFlag.AlignHCenter

class PluginPage(QWidget):
    """" class for the plugins page """
    def __init__(
        self,
        signal, 
        *args, 
        **kwargs) -> None:
        super().__init__( *args, **kwargs)
        """ initializes class """
        self.signal = signal
        self.logger = makeLogger("F")
        self._initWidget()
        self._initlayout()
       
    def _initWidget(self):
        """ initializes widgets """
        self.logger.info("")
        self.header = Label(
            Text.pluginHeader, FontSize.HEADER2, FontFamily.MAIN, 
            alignment= center)
        self.caption = Label(
            Text.pluginCaption, FontSize.DESCRIPTION, FontFamily.MAIN)
        self.pluginTable = PluginTable(self.signal)
        self.addBtn = ColoredBtn(Text.newPluginBtn, Color.SECONDARY_BUTTON)
        
    def _initlayout(self):
        """" initializes layout """
        self.logger.info("")
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.verticalLayout.addWidget(self.header)
        self.verticalLayout.setSpacing(Dimension.SMALL_SPACING)
        self.verticalLayout.addWidget(self.caption, alignment=center)
        self.verticalLayout.addSpacing(Dimension.SMALL_SPACING)
        self.verticalLayout.addWidget(self.pluginTable, alignment=center)
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(self.addBtn, alignment=center)

    def addPluginSuite(self):
        pluginDialog = UploadPlugin(self.signal)
        pluginDialog.exec()
    
    def addPluginSuiteConfirmed(self, pluginSuite):
        self.pluginTable.addPluginSuite(pluginSuite)
        