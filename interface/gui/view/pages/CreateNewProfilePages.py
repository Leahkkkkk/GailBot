'''
File: CreateNewProfilePages.py
Project: GailBot GUI
File Created: Friday, 4th November 2022 1:01:27 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Saturday, 5th November 2022 7:22:34 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: implementation of pages for user to create new profile 
'''

from typing import Dict
from view.Signals import DataSignal
from view.Request import Request
from view.config.Text import CreateNewProfilePageText as Text 
from view.config.Text import EngineForm as Form 
from gbLogger import makeLogger


from view.util.ErrorMsg import ERR, WARN
from view.widgets.Button import ColoredBtn
from view.widgets.Label import Label
from view.widgets.TabPage import TabPage
from view.widgets.Table import BaseTable
from view.widgets.Form.TextInput import TextInput
from view.widgets.MsgBox import WarnBox
from view.widgets.ComboBox import ComboBox
from view.config.Text import EngineForm
from view.widgets import DependentCombo
from view.components import EngineSettingForm
from view.components import PluginForm
from PyQt6.QtWidgets import  QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import (
    Qt, 
    pyqtSignal, 
    QObject, 
    QSize
)

#### controlling style changes 
from view.config.Style import (
    FontFamily,
    STYLE_DATA)



######################

hCenter = Qt.AlignmentFlag.AlignHCenter
vCenter = Qt.AlignmentFlag.AlignVCenter
center = hCenter | vCenter
bottomRight = Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignBottom
top = Qt.AlignmentFlag.AlignTop

class settingSignals(QObject):
    engineSet = pyqtSignal()
    
class SettingName (TabPage):
    """ page with an input field to allow user add the profile name """
    def __init__(self, title = Text.profileName, *args, **kwargs) -> None:
        """" initializes page """
        super().__init__(*args, **kwargs)
        self.title = title
        self.logger = makeLogger("F")
        self._initWidget()
        self._initLayout()
    
    def getData(self) -> str:
        """ return the user's input of profile name """
        try:
            self.logger.info("")
            return self.profileName.value
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("reading profile name", str(e)))
        
    def _initWidget(self):
        """ initializes the widgets """
        self.header = Label(self.title, 
            STYLE_DATA.FontSize.HEADER2, 
            FontFamily.MAIN)
        self.profileName = TextInput(
            "", 
            labelSize = STYLE_DATA.FontSize.HEADER3,
            vertical=False)
        self.confirmBtn = ColoredBtn(
            "Start", 
            STYLE_DATA.Color.SECONDARY_BUTTON)
        self.confirmBtn.clicked.connect(self._confirmHandler)

    def _initLayout(self):
        """ initializes the layout """
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(
            self.header, 
            alignment=center)
        self.verticalLayout.addWidget(
            self.profileName,
            alignment = center)
        self.verticalLayout.addWidget(
            self.confirmBtn,
            alignment= center)
        self.verticalLayout.addStretch()
    
    def _confirmHandler(self):
        """ event handler for confirm button  """
        name = self.profileName.value
        if not name or len(name.replace(" ", "")) == 0 :
            WarnBox(WARN.EMPTY_PROFILE_NAME)
        else:
            self.signals.nextPage.emit()
            self.signals.goToNextPage.emit()
    
class EngineSetting(TabPage):
    """ class for engine setting form """
    def __init__(self,  *args, **kwargs) -> None:
        """ initializes page """
        super().__init__(*args, **kwargs)
        self.logger = makeLogger("F")
        self.verticallayout = QVBoxLayout()
        self.setLayout(self.verticallayout)
        self.header = Label(
            Text.engineSettingHeader, 
            STYLE_DATA.FontSize.HEADER2, 
            FontFamily.MAIN)
        self.verticallayout.addWidget(
            self.header, 
            alignment=Qt.AlignmentFlag.AlignHCenter)
        self.mainForm = EngineSettingForm.EngineSettingForm()
        self.verticallayout.addWidget(self.mainForm)
        self.verticallayout.addStretch()
        self.confirmBtn = ColoredBtn(Text.cofirmBtn, STYLE_DATA.Color.SECONDARY_BUTTON)
        self.confirmBtn.clicked.connect(lambda: self.signals.close.emit())
        self.verticallayout.addWidget(self.confirmBtn, alignment=bottomRight)
    
    def getData(self) -> Dict[str, str]:
        """ gets current value of key in dictionary """
        try:
            return self.mainForm.getValue()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("getting setting data", str(e)))

    def setData(self, data: Dict[str, str]):
        try:
            return self.mainForm.setValue(data)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("displaying setting data", str(e)))
class PluginSetting(TabPage):
    """ class for the plugin settings tab """
    def __init__(self, plugins, *args, **kwargs) -> None:
        """ initializes tab """
        super().__init__(*args, **kwargs)
        self.header = Label(
            Text.pluginSettingHeader, 
            STYLE_DATA.FontSize.HEADER2, 
            FontFamily.MAIN)
        self.mainForm = PluginForm.PluginForm()
        self.mainForm.addPluginSuites(plugins)
        self.confirmBtn = ColoredBtn(Text.cofirmBtn, STYLE_DATA.Color.SECONDARY_BUTTON)
        self.confirmBtn.clicked.connect(lambda: self.signals.close.emit())
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.verticalLayout.addWidget(self.header, alignment=center)
        self.verticalLayout.addWidget(self.mainForm)
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(
            self.confirmBtn,
            alignment=Qt.AlignmentFlag.AlignRight)
        self.logger = makeLogger("F")
  
    def getData(self):
        """ gets current value of data """
        try:
            return self.mainForm.getValue()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("getting plugin data", str(e)))
    
    def setData(self, data):
        try:
            self.mainForm.setValue(data)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("displaying plugin data", str(e)))
class ChooseEngine(TabPage):
    def __init__(self, engineSettings, engineSignal: DataSignal, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.logger = makeLogger("F")
        self.verticallayout = QVBoxLayout()
        self.setLayout(self.verticallayout)
        self.header = Label(
            Text.engineSettingHeader,
            STYLE_DATA.FontSize.HEADER2,
            FontFamily.MAIN
        )     
        self.engineSignal = engineSignal 
        self.selectEngines = ComboBox()
        self.selectEngines.setFixedWidth(STYLE_DATA.Dimension.WIN_MIN_WIDTH//2)
        self.engineDisplay = SettingDisplay()
        self.selectEngines.addItems(engineSettings)
        self.verticallayout.addWidget(self.header, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.verticallayout.addWidget(self.selectEngines, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.verticallayout.addWidget(self.engineDisplay)
        self.verticallayout.addStretch()
        self.confirmBtn = ColoredBtn(Text.cofirmBtn, STYLE_DATA.Color.SECONDARY_BUTTON)
        self.confirmBtn.clicked.connect(self._confirmHandler)
        self.verticallayout.addWidget(self.confirmBtn, alignment=bottomRight)
        self.selectEngines.currentTextChanged.connect(self.requestSetting)
        self.requestSetting(self.selectEngines.currentText())
    
    def _confirmHandler(self):
        self.signals.nextPage.emit()

    def getData(self) -> str:
        try:
            return self.selectEngines.currentText()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("reading engine setting name", str(e)))
    
    def setData(self, data):
        try:
            self.selectEngines.setCurrentText(data)
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("displaying engine setting", str(e)))

    def displayData(self, data):
        try:
            name, setting = data 
            self.engineDisplay.setData(setting)
        except Exception as e:
            self.logger.error(e, exc_info=e)
    
    def requestSetting(self, name:str):
        self.engineSignal.getRequest.emit(
            Request(data=name, succeed=self.displayData)
        ) 
    
    
    
class SettingDisplay(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._layout = QVBoxLayout()
        self.currentTableWidget = None 
        self.setLayout(self._layout)
        self.mainLabel = Label("Engine Setting Details", STYLE_DATA.FontSize.HEADER3, FontFamily.MAIN)
        self._layout.addSpacing(20)
        self._layout.setSpacing(STYLE_DATA.Dimension.MEDIUM_SPACING)
        self._layout.addWidget(self.mainLabel, alignment=Qt.AlignmentFlag.AlignCenter)
    
    def setData(self, data: Dict[str, str]):
        if self.currentTableWidget:
            self._layout.removeWidget(self.currentTableWidget)
        newTable = BaseTable(["Setting Options", "Value"])
        newTable.setFixedSize(QSize(STYLE_DATA.Dimension.WIN_MIN_WIDTH//2, 
                                    STYLE_DATA.Dimension.SMALL_TABLE_HEIGHT))
        newTable.resizeCol([0.5, 0.5])
        for row, (key, value) in enumerate(data.items()):
            newTable.insertRow(row)
            key = key.replace("_", " ").upper()
            newTable.setItem(row, 0, QTableWidgetItem(key))
            newTable.setItem(row, 1, QTableWidgetItem(str(value)))
        self._layout.addWidget(newTable,alignment=Qt.AlignmentFlag.AlignHCenter)
        self.currentTableWidget = newTable
       