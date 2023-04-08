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
from view.config.Style import STYLE_DATA,  FontFamily
from view.config.Text import ProfilePageText as Text
from view.config.Text import ProfileSettingForm as Form
from view.Signals import PluginSignals, GlobalStyleSignal
from view.Request import Request
from gbLogger import makeLogger
from view.widgets import Label, ColoredBtn
from view.widgets.PluginTable import PluginTable
from view.components.UploadPluginDialog import UploadPlugin
from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout,
    QHBoxLayout)
from PyQt6.QtCore import Qt

center  = Qt.AlignmentFlag.AlignHCenter

class PluginPage(QWidget):
    """" class for the plugins page """
    def __init__(
        self,
        signal: PluginSignals,
        *args, 
        **kwargs) -> None:
        super().__init__( *args, **kwargs)
        """ initializes class """
        self.signal = PluginSignals()
        self.logger = makeLogger("F")
        self._initWidget()
        self._initlayout()
        self._connectSignal()
       
    def _initWidget(self):
        """ initializes widgets """
        self.logger.info("")
        self.header = Label(
            Text.pluginHeader, STYLE_DATA.FontSize.HEADER2, FontFamily.MAIN, 
            alignment= center)
        self.caption = Label(
            Text.pluginCaption, STYLE_DATA.FontSize.DESCRIPTION, FontFamily.MAIN)
        self.pluginTable = PluginTable(self.signal)
        self.addBtn = ColoredBtn(Text.newPluginBtn, STYLE_DATA.Color.PRIMARY_BUTTON)
     
    def _initlayout(self):
        """" initializes layout """
        self.logger.info("")
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.verticalLayout.addWidget(self.header)
        self.verticalLayout.setSpacing(STYLE_DATA.Dimension.SMALL_SPACING)
        self.verticalLayout.addWidget(self.caption, alignment=center)
        self.verticalLayout.addSpacing(STYLE_DATA.Dimension.SMALL_SPACING)
        self.verticalLayout.addWidget(self.pluginTable, alignment=center)
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(self.addBtn, alignment=center)

    def _connectSignal(self):
        self.addBtn.clicked.connect(self.addPluginSuite)
        self.signal.addPlugin.connect(self.addRequestWrapper)
        GlobalStyleSignal.changeColor.connect(self.changeColor)
        
    def addRequestWrapper(self, suiteData):
        self.signal.addRequest.emit(
            Request(data = suiteData, succeed=self.addPluginSuiteConfirmed))
    
    def addPluginSuite(self):
        pluginDialog = UploadPlugin(self.signal)
        pluginDialog.exec()
    
    def addPluginSuiteConfirmed(self, pluginSuite):
        name, data = pluginSuite
        self.pluginTable.addPluginSuite(pluginSuite)
        self.signal.pluginAdded.emit(name)
    
    def changeColor(self, colormode):
        self.addBtn.colorChange(STYLE_DATA.Color.PRIMARY_BUTTON)
        