from typing import List
from view.widgets.Form.MultiSelect import MultipleSelect
from view.widgets.ToggleView import ToggleView
from PyQt6.QtWidgets import QWidget , QHBoxLayout
from view.config.Style import Dimension

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
        self.pluginSuitesList = MultipleSelect("Select Plugin Suites", self.pluginSuites)
    
    def _initLayout(self):
        self._layout = QHBoxLayout()
        self.toggleView = ToggleView(
            "Plugin Suites Settings", self.pluginSuitesList, header=True)
        self.toggleView.setScrollHeight(Dimension.OUTPUT_FORM_HEIGHT)
        self.setLayout(self._layout)
        self._layout.addWidget(self.toggleView)
    
    def addPluginSuite(self, pluginSuite:str):
        """add a single plugin suite as available option

        Args:
            pluginSuite (str): the name of the single plugin suite
        """
        self.pluginSuitesList.addChoice(pluginSuite)
    
    def getValue(self):
        return self.pluginSuitesList.getValue()

    def setValue(self, values):
        return self.pluginSuitesList.setValue(values)
        
        
    