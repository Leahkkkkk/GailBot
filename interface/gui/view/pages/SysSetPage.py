'''
File: SystemSettingPage.py
Project: GailBot GUI
File Created: Friday, 4th November 2022 1:01:27 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Saturday, 5th November 2022 7:06:32 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: implement the system setting page
'''
import os
from typing import List
import toml
from view.config.Style import (
    STYLE_DATA,
)
from view.widgets import (
    SettingForm,
    Label,
    Button
)
from view.components.SaveLogDialog import SaveLogFile
from view.Signals import GlobalStyleSignal
from config_frontend.ConfigPath import WorkSpaceConfigPath, SettingDataPath
from view.config.Setting import SystemSetting, DefaultSetting
from view.config import StyleSource, StyleTable
from view.config.Text import SystemSetPageText as Text
from view.config.Text import SystemSettingForm as Form
from view.config.Text import LogDeleteTimeDict
from config_frontend import FRONTEND_CONFIG_ROOT as dirname
from view.util.FileManage import clearAllLog
from view.util.ErrorMsg import ERR
from gbLogger import makeLogger
from view.widgets import ConfirmBox, WarnBox
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QMessageBox,
    QVBoxLayout
    )
from PyQt6.QtCore import Qt, pyqtSignal, QObject

class Signal(QObject):
    restart    = pyqtSignal()
    clearCache = pyqtSignal()

bottom = Qt.AlignmentFlag.AlignBottom

ZIP_LOG_NAME = "gailbot_log_file"
class SystemSettingPage(QWidget):
    """ class for the system settings page """
    def __init__(self, *args, **kwargs) -> None:
        """ initializes the page """
        super().__init__(*args, **kwargs)
        self.data = Form
        self.signal = Signal()
        self.logger = makeLogger("F")
        self.formButtons: List[Button.BorderBtn] = []
        self.labels: List[Label] = []
        self._initWidget()
        self._initLayout()
        self._connectSignal()
        self._loadValue(SystemSetting)

    def _initWidget(self):
        """ initializes widgets to be shown """
        self.SysSetForm = SettingForm.SettingForm(Text.header, self.data, Text.caption)
        self.saveBtn = Button.ColoredBtn(Text.saveBtn, STYLE_DATA.Color.PRIMARY_BUTTON)
        
    def _connectSignal(self):
        """ connect the signal to slots """
        self.saveBtn.clicked.connect(self._confirmChangeSetting)
        STYLE_DATA.signal.changeColor.connect(self.colorChange)
        STYLE_DATA.signal.changeFont.connect(self.fontChange)
        
    def _initLayout(self):
        """ initialize the form section """
        self.formLayout = QVBoxLayout()
        self.setLayout(self.formLayout)
        self.formLayout.addWidget(self.SysSetForm,alignment=Qt.AlignmentFlag.AlignHCenter)
        self.formLayout.addStretch()
        self.formLayout.addWidget(self.saveBtn, alignment=Qt.AlignmentFlag.AlignHCenter)
        self._addFormButton(Text.restoreLabel, Text.restoreBtn, self._confirmRestore)
        self._addFormButton(Text.ClearLogLabel, Text.ClearLogBtn, self._clearLog)
        self._addFormButton(Text.SaveLogLabel, Text.SaveLogBtn, self._saveLog)
        self._addFormButton(Text.ClearCacheLabel, Text.ClearCacheBtn, self._clearCache)

    def colorChange(self, colormode = None):
        self.saveBtn.colorChange(STYLE_DATA.Color.PRIMARY_BUTTON)
        for button in self.formButtons:
            button.addOtherStyle( f"background-color: {STYLE_DATA.Color.INPUT_BACKGROUND};")
            button.colorChange(STYLE_DATA.Color.INPUT_TEXT)
    
    def fontChange(self, fontmode = None):
        for label in self.labels:
            label.fontChange(STYLE_DATA.FontSize.BODY)
        for btn in self.formButtons:
            btn.fontChange(STYLE_DATA.FontSize.BTN)
            
    def setValue(self, values:dict):
        """ public function to set the system setting form value

        Args: values: a dictionary that stores the system setting value
        """
        self.SysSetForm.setValue(values)

    def getValue(self) -> dict:
        """ public function to get the system setting form value"""
        return self.SysSetForm.getValue()

    def _confirmChangeSetting(self)->None:
        """ open a pop up box to confirm restarting the app and change the setting"""
        ConfirmBox(
            Text.confirmChange,
            self._changeSetting,
            QMessageBox.StandardButton.Ok)

    def _changeSetting(self)->None:
        """ rewrite the current setting file based on the user's choice"""
        setting = self.SysSetForm.getValue()
        try:
            GlobalStyleSignal.changeColor.emit(setting["Color Mode"])
            GlobalStyleSignal.changeFont.emit(setting["Font Size"])
            
            colorSource = StyleTable[setting["Color Mode"]]
            colorDes    = StyleSource.CURRENT_COLOR
            fontSource  = StyleTable[setting["Font Size"]]
            fontDes     = StyleSource.CURRENT_FONTSIZE
            logDeleteTime = LogDeleteTimeDict[setting["Log file auto deletion time"]]
            f = open (f"{os.path.join(dirname, WorkSpaceConfigPath.fileManageData)}", "w+")
            toml.dump({"AUTO_DELETE_TIME" : logDeleteTime}, f)
            f.close()
            self._copyTomlFile(colorSource, colorDes, dirname)
            self._copyTomlFile(fontSource, fontDes, dirname)
            f = open (f"{os.path.join(dirname, SettingDataPath.systemSetting)}", "w+")
            toml.dump(setting, f)
            f.close()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("changing system setting", str(e)))
       
        # self.signal.restart.emit()

    def _copyTomlFile(self, source, des, base):
        """ private helper function for copying the toml file """
        s = toml.load(os.path.join(base,source))
        with open(os.path.join(base, des), "w+") as f:
            toml.dump(s, f)

    def _clearLog(self):
        """ open confirm box to confirm clearing the log file """
        ConfirmBox(Text.confirmClear, clearAllLog)

    def _loadValue(self, setting):
        """ initialize the setting value """
        self.SysSetForm.setValue(setting)

    def _confirmRestore(self):
        """ open confirm box to confirm restoring to the defaults """
        ConfirmBox(
            "Confirm to restore to default setting",
            lambda: self._loadValue(DefaultSetting))

    def _saveLog(self):
        try:
            dialog = SaveLogFile()
            dialog.exec()
        except Exception as e:
            self.logger.error(e, exc_info=e)
    
    def _clearCache(self):
        try:
            ConfirmBox(Text.ConfirmClearCache, lambda : self.signal.clearCache.emit())
        except Exception as e:
            self.logger.error(e, exc_info=e)
            
    def _addFormButton(self, label, btnText, fun: callable):
        container = QWidget()
        layout = QHBoxLayout()
        label = Label(label, STYLE_DATA.FontSize.BODY)
        label.setFixedWidth(STYLE_DATA.Dimension.INPUTWIDTH)
        button = Button.BorderBtn(
            btnText,
            STYLE_DATA.Color.INPUT_TEXT,
            other = f"background-color: {STYLE_DATA.Color.INPUT_BACKGROUND}"
        )
        button.setFixedHeight(STYLE_DATA.Dimension.INPUTHEIGHT)
        button.setFixedWidth(130)
        container.setLayout(layout)
        layout.addWidget(label)
        layout.addSpacing(30)
        layout.addWidget(button)
        button.clicked.connect(fun)
        self.SysSetForm.addWidget(container)
        self.formButtons.append(button)
        self.labels.append(label)