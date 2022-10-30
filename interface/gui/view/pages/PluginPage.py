from ctypes import alignment
from view.widgets import Label 
from view.style.styleValues import FontFamily, FontSize, Color
from view.style.Background import initBackground

from PyQt6.QtWidgets import (
    QWidget, 
    QCheckBox, 
    QVBoxLayout, 
    QHBoxLayout, 
    QScrollArea)
from PyQt6.QtCore import Qt

class PluginPage(QWidget):
    def __init__(
        self,
        plugins, 
        *args, 
        **kwargs) -> None:
        super().__init__( *args, **kwargs)
        self.plugins = plugins
        self.pluginDict = dict()
        self._initWidget()
        self._initlayout()
        self._initPlugins()
        
    def _initWidget(self):
        self.header = Label.Label(
            "Choose Plugins", 
            FontSize.HEADER2,
            FontFamily.MAIN, 
            alignment=Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignHCenter)
        self.caption = Label.Label(
            "These plugins are applied to transcription process",
            FontSize.DESCRIPTION, 
            FontFamily.MAIN)

    def _initlayout(self):
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.scrollContainer = QWidget()
        self.scrollLayout = QVBoxLayout()
        self.scrollContainer.setLayout(self.scrollLayout)
        self.scrollLayout.setSpacing(10)
        self.scroll = QScrollArea()
        self.scroll.setFixedWidth(650)
        self.scroll.setMinimumHeight(550)
        self.scroll.setMaximumHeight(700)
        self.scroll.setWidgetResizable(True)
        self.verticalLayout.addWidget(self.header)
        self.verticalLayout.addWidget(
            self.caption, 
            alignment = Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.addWidget(
            self.scroll, 
            alignment=Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout.addStretch()
        initBackground(self.scroll, Color.BLUEWHITE)
        initBackground(self.scrollContainer, Color.BLUEWHITE)

    def _initPlugins(self):
        for plugin in self.plugins:
            print(plugin)
            newPlugin = pluginCheckBox(plugin)
            self.pluginDict[plugin] = newPlugin
            self.scrollLayout.addWidget(
                newPlugin, alignment=Qt.AlignmentFlag.AlignTop)
        self.scroll.setWidget(self.scrollContainer)
    
    def addNewPlugin(self, plugin):
        newPlugin = pluginCheckBox(plugin)
        self.pluginDict[plugin] = newPlugin
        self.scrollLayout.addWidget(newPlugin)
        self.scroll.setWidget(self.scrollContainer)
    
    def setValue(self, appliedPlugins: set):
        for plugin, checkwidget in self.pluginDict.items():
            if plugin in appliedPlugins:
                checkwidget.setCheck()
            else:
                checkwidget.setUncheck()
    
    def getValue(self) -> set:
        appliedPlugins = set()
        for plugin, checkWidget in self.pluginDict.items():
            if checkWidget.isChecked():
                appliedPlugins.add(plugin)
        return appliedPlugins
                
        
class pluginCheckBox(QWidget):
    def __init__(self, plugin:str, *args, **kwargs) -> None:
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
        initBackground(self, Color.BLUEWHITE)
    
    def isChecked(self):
        return self.checkBox.checkState() == Qt.CheckState.Checked 
    
    def setCheck(self):
        self.checkBox.setChecked(True)
    
    def setUncheck(self):
        self.checkBox.setChecked(False)