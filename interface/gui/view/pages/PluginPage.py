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
from typing import Dict, List
from view.config.Style import FontSize, Dimension, FontFamily
from view.config.Text import ProfilePageText as Text
from view.config.Text import ProfileSettingForm as Form
from gbLogger import makeLogger
from view.widgets import Label, ScrollArea
from view.widgets.MsgBox import WarnBox
from view.widgets.Background import initSecondaryColorBackground

from PyQt6.QtWidgets import (
    QWidget, 
    QCheckBox, 
    QVBoxLayout, 
    QHBoxLayout)
from PyQt6.QtCore import Qt

center  = Qt.AlignmentFlag.AlignHCenter
defaultPlugin = list (Form.Plugins)

class PluginPage(QWidget):
    """" class for the plugins page """
    def __init__(
        self,
        plugins = defaultPlugin,
        *args, 
        **kwargs) -> None:
        super().__init__( *args, **kwargs)
        """ initializes class """
        self.plugins = plugins
        self.logger = makeLogger("F")
        self._initWidget()
        self._initlayout()
       
    def displayPlugin(self, plugins: Dict[str, List[str]]):
        raise NotImplementedError    
      
    def getValue(self):
        return [] 
        
    def _initWidget(self):
        """ initializes widgets """
        self.logger.info("")
        self.header = Label.Label(
            Text.pluginHeader, FontSize.HEADER2, FontFamily.MAIN, 
            alignment= center)
        self.caption = Label.Label(
            Text.pluginCaption, FontSize.DESCRIPTION, FontFamily.MAIN)
        self.message = Label.Label(
            Text.tempMessage, FontSize.DESCRIPTION, FontFamily.MAIN)

    def _initlayout(self):
        """" initializes layout """
        self.logger.info("")
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.scrollContainer = QWidget()
        self.scrollLayout = QVBoxLayout()
        self.scrollContainer.setLayout(self.scrollLayout)
        self.scrollLayout.setSpacing(10)
        self.scrollArea = ScrollArea.ScrollArea()
        self.scrollArea.setFixedWidth(Dimension.FORMWIDTH)
        self.scrollArea.setMinimumHeight(Dimension.FORMMINHEIGHT)
        self.scrollArea.setMaximumHeight(Dimension.FORMMAXHEIGHT)
        self.scrollArea.setWidgetResizable(True)
        self.verticalLayout.addWidget(self.header)
        self.verticalLayout.setSpacing(Dimension.SMALL_SPACING)
        self.verticalLayout.addWidget(self.message, alignment=center)
        self.verticalLayout.addStretch()
        initSecondaryColorBackground(self.scrollArea)
        initSecondaryColorBackground(self.scrollContainer)
