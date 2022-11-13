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

from util.Style import FontSize, Dimension, FontFamily
from util.Text import ProfilePageText as Text
from util.Text import ProfileSettingForm as Form
from view.widgets import Label 
from view.widgets.Background import initSecondaryColorBackground

from PyQt6.QtWidgets import (
    QWidget, 
    QCheckBox, 
    QVBoxLayout, 
    QHBoxLayout, 
    QScrollArea)
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
        self.pluginDict = dict()
        self._initWidget()
        self._initlayout()
        self._initPlugins()
        
    def _initWidget(self):
        """ initializes widgets """
        self.header = Label.Label(
            Text.pluginHeader, FontSize.HEADER2, FontFamily.MAIN, 
            alignment= center)
        self.caption = Label.Label(
            Text.pluginCaption, FontSize.DESCRIPTION, FontFamily.MAIN)

    def _initlayout(self):
        """" initializes layout """
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.scrollContainer = QWidget()
        self.scrollLayout = QVBoxLayout()
        self.scrollContainer.setLayout(self.scrollLayout)
        self.scrollLayout.setSpacing(10)
        self.scroll = QScrollArea()
        self.scroll.setFixedWidth(Dimension.FORMWIDTH)
        self.scroll.setMinimumHeight(Dimension.FORMMINHEIGHT)
        self.scroll.setMaximumHeight(Dimension.FORMMAXHEIGHT)
        self.scroll.setWidgetResizable(True)
        self.verticalLayout.addWidget(self.header)
        self.verticalLayout.addWidget(
            self.caption, 
            alignment = center)
        self.verticalLayout.setSpacing(Dimension.SMALL_SPACING)
        self.verticalLayout.addWidget(
            self.scroll, 
            alignment=center)
        self.verticalLayout.addStretch()
        initSecondaryColorBackground(self.scroll)
        initSecondaryColorBackground(self.scrollContainer)

    def _initPlugins(self):
        """ initializes plugins to be shown on screen """
        for plugin in self.plugins:
            newPlugin = pluginCheckBox(plugin)
            self.pluginDict[plugin] = newPlugin
            self.scrollLayout.addWidget(
                newPlugin, alignment=Qt.AlignmentFlag.AlignTop)
        self.scroll.setWidget(self.scrollContainer)
    
    def addNewPlugin(self, plugin):
        """ adds new plugin as an option on the page
        Args: plugin: plugin to be added
        """
        newPlugin = pluginCheckBox(plugin)
        self.pluginDict[plugin] = newPlugin
        self.scrollLayout.addWidget(newPlugin)
        self.scroll.setWidget(self.scrollContainer)
    
    def setValue(self, appliedPlugins: set):
        """ sets the value of the given plugin
        Args: appliedPlugins:set: 
        """
        for plugin, checkwidget in self.pluginDict.items():
            if plugin in appliedPlugins:
                checkwidget.setCheck()
            else:
                checkwidget.setUncheck()
    
    def getValue(self) -> set:
        """ gets the value of the given plugin """
        appliedPlugins = set()
        for plugin, checkWidget in self.pluginDict.items():
            if checkWidget.isChecked():
                appliedPlugins.add(plugin)
        return appliedPlugins
   
   
                
class pluginCheckBox(QWidget):
    """ class for a plugin checkbox """
    def __init__(self, plugin:str, *args, **kwargs) -> None:
        """ initializes the class """
        super().__init__( *args, **kwargs)
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
        return self.checkBox.checkState() == Qt.CheckState.Checked 
    
    def setCheck(self):
        """ check the current checkbox """
        self.checkBox.setChecked(True)
    
    def setUncheck(self):
        """ uncheck the current checkbox """
        self.checkBox.setChecked(False)