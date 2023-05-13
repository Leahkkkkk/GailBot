from typing import List
from view.widgets import MultipleSelect
from PyQt6.QtWidgets import QWidget , QHBoxLayout
from view.config.Style import STYLE_DATA
from view.config.Text import PLUGIN_SUITE_TEXT

class PluginForm(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.pluginSuites  = []
        self._initWidget()
        self._initLayout()
    
    def addPluginSuites(self, pluginSuites: List[str]):
        """add a list of plugin suites as available plugin options

        Args:
            pluginSuites (List[str]): a list of plugin suite names
        """ 
        for suite in pluginSuites:
            self.addPluginSuite(suite)
    
    def _initWidget(self):
        self.pluginSuitesList = MultipleSelect(PLUGIN_SUITE_TEXT.SELECT_PLUGIN, self.pluginSuites)
    
    def _initLayout(self):
        self._layout = QHBoxLayout()
        self.setLayout(self._layout)
        self._layout.addWidget(self.pluginSuitesList)
    
    def addPluginSuite(self, pluginSuite:str):
        """add a single plugin suite as available option

        Args:
            pluginSuite (str): the name of the single plugin suite
        """
        self.pluginSuitesList.addChoice(pluginSuite)
    
    def deletePluginSuite(self, pluginSuite:str):
        """ delete a plugin suite from the front end interface

        Args:
            pluginSuite (str): the name of the plugin
        """ 
        self.pluginSuitesList.removeChoice(pluginSuite)
    
    def getValue(self):
        """return the list of plugin suite selected by the user

        Returns:
            List[stt]: the list of plugin suite name
        """
        return self.pluginSuitesList.getValue()

    def setValue(self, values):
        """set the all the plugin suite in values to be selected

        Args:
            values (Lis[str]): a list of plugin suite that are applied
        """
        return self.pluginSuitesList.setValue(values)
        
        
    