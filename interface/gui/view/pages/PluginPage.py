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
from typing import Dict 
from view.config.Style import FontSize, Dimension, FontFamily
from view.config.Text import ProfilePageText as Text
from view.config.Text import ProfileSettingForm as Form
from util.Logger import makeLogger
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
        self.pluginDict : Dict[str, pluginCheckBox] = dict()
        self.logger = makeLogger("F")
        self._initWidget()
        self._initlayout()
        # self._initPlugins()
        
    def _initWidget(self):
        """ initializes widgets """
        self.logger.info("")
        self.header = Label.Label(
            Text.pluginHeader, FontSize.HEADER2, FontFamily.MAIN, 
            alignment= center)
        self.caption = Label.Label(
            Text.pluginCaption, FontSize.DESCRIPTION, FontFamily.MAIN)
        # self.placeholder = Label.Label(
        #     Text.pluginPlaceholder, FontSize.HEADER3, FontFamily.MAIN)

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
        # self.verticalLayout.addWidget(
        #     self.caption, 
        #     alignment = center)
        self.verticalLayout.setSpacing(Dimension.SMALL_SPACING)
        # self.verticalLayout.addWidget(
        #     self.scrollArea, 
        #     alignment=center)
        self.verticalLayout.addWidget(self.message, alignment=center)
        self.verticalLayout.addStretch()
        initSecondaryColorBackground(self.scrollArea)
        initSecondaryColorBackground(self.scrollContainer)

    def _initPlugins(self):
        """ initializes plugins to be shown on screen """
        try:
            self.logger.info("")
            for plugin in self.plugins:
                newPlugin = pluginCheckBox(plugin)
                self.pluginDict[plugin] = newPlugin
                self.scrollLayout.addWidget(
                    newPlugin, alignment=Qt.AlignmentFlag.AlignTop)
            self.scrollArea.setWidget(self.scrollContainer)
        except:
            WarnBox("An error occurred when loading the plugins")
    
    def addNewPlugin(self, plugin):
        """ adds new plugin as an option on the page
        Args: plugin: plugin to be added
        """
        self.logger.info("")
        newPlugin = pluginCheckBox(plugin)
        self.pluginDict[plugin] = newPlugin
        self.scrollLayout.addWidget(newPlugin)
        self.scrollArea.setWidget(self.scrollContainer)
    
    def setValue(self, appliedPlugins: set):
        """ sets the value of the given plugin
        Args: appliedPlugins:set: 
        """
        try: 
            self.logger.info("")
            for plugin, checkwidget in self.pluginDict.items():
                if plugin in appliedPlugins:
                    checkwidget.setCheck()
                else:
                    checkwidget.setUncheck()
        except:
            WarnBox("An error occurred when loading the plugins")
            
    
    def getValue(self) -> set:
        """ gets the value of the given plugin """
        try:
            self.logger.info("")
            appliedPlugins = set()
            for plugin, checkWidget in self.pluginDict.items():
                if checkWidget.isChecked():
                    appliedPlugins.add(plugin)
            return list(appliedPlugins)
        except:
            WarnBox("An error occurred when retrieving the plugins")
   
   
class pluginCheckBox(QWidget):
    """ class for a plugin checkbox """
    def __init__(self, plugin:str, *args, **kwargs) -> None:
        """ initializes the class """
        super().__init__( *args, **kwargs)
        self.logger = makeLogger("F")
        self.plugin  = plugin
        self.layout = QHBoxLayout()
        self.checkBox = QCheckBox()
        self.pluginLabel = Label.Label(plugin, FontSize.BODY)
        self.setLayout(self.layout)
        self.layout.addWidget(self.checkBox)
        self.layout.addWidget(self.pluginLabel)
        self.layout.setSpacing(20)
        self.layout.addStretch()

    def isChecked(self):
        """ determines if the given checkbox is currently checked """
        self.logger.info("")
        return self.checkBox.checkState() == Qt.CheckState.Checked 
    
    def setCheck(self):
        """ check the current checkbox """
        self.logger.info("")
        self.checkBox.setChecked(True)
    
    def setUncheck(self):
        """ uncheck the current checkbox """
        self.logger.info("")
        self.checkBox.setChecked(False)