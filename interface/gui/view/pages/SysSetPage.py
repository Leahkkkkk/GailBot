"""
File: SystemSettingPage.py
Project: GailBot GUI
File Created: Friday, 4th November 2022 1:01:27 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Saturday, 5th November 2022 7:06:32 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: implement the system setting page
"""
import os
from dataclasses import dataclass
from typing import List
import toml
from view.config.Style import (
    STYLE_DATA,
)
from view.widgets import SettingForm, Label, Button
from view.widgets.Background import initBackground
from view.widgets.Form.ComBoInput import ComboBox
from view.components.SelectPath import SaveLogFile
from view.signal.signalObject import GlobalStyleSignal
from config_frontend.ConfigPath import WorkSpaceConfigPath, SettingDataPath
from view.config.Setting import SystemSetting, DefaultSetting
from view.config import StyleSource, StyleTable
from view.config.InstructionText import INSTRUCTION
from view.widgets.Button import InstructionBtn
from view.config.Text import SystemSetPageText as Text
from view.config.Text import SystemSettingForm as Form
from view.config.Text import LogDeleteTimeDict
from config_frontend import FRONTEND_CONFIG_ROOT as dirname
from view.util.FileManage import clearAllLog
from view.util.ErrorMsg import ERR
from gbLogger import makeLogger
from view.widgets import ConfirmBox, WarnBox
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QMessageBox, QVBoxLayout, QGridLayout
from PyQt6.QtCore import Qt, pyqtSignal, QObject, QSize


@dataclass 
class INPUT_COMBO:
    FONT_SIZE = "Font Size"
    COLOR_MODE = "Color Mode"
    LOG_AUTO_DELETE = "Log Auto Deletion Time"
    FONT_SELECTION = ["Medium", "Small", "Large"]
    COLOR_MODE_SELECTION = ["Light Mode", "Dark Mode"]
    LOGFILE_AUTO_DELETE_SELECTION = ["Daily", "Weekly", "Monthly", "Every 2 Months"]

@dataclass 
class BUTTON:
    RESTORE_DEFAULT = "Restore Defaults"
    CLEAR_LOG = "Clear Logs"
    SAVE_LOG = "Save Logs"
    CLEAR_CACHE = "Clear Cache"

class Signal(QObject):
    restart = pyqtSignal()
    clearCache = pyqtSignal()


bottom = Qt.AlignmentFlag.AlignBottom

ZIP_LOG_NAME = "gailbot_log_file"


class SystemSettingPage(QWidget):
    """class for the system settings page"""

    def __init__(self, *args, **kwargs) -> None:
        """initializes the page"""
        super().__init__(*args, **kwargs)
        self.data = Form
        self.signal = Signal()
        self.logger = makeLogger()
        self.formButtons: List[Button.BorderBtn] = []
        self.labels: List[Label] = []
        self._initWidget()
        self._initLayout()
        self._connectSignal()
        self.setValue(SystemSetting)
        STYLE_DATA.signal.changeColor.connect(self.colorChange)

    def _initWidget(self):
        """initializes widgets to be shown"""
        labelTexts = [INPUT_COMBO.FONT_SIZE, INPUT_COMBO.COLOR_MODE, 
                      INPUT_COMBO.LOG_AUTO_DELETE]
        self.labels = [Label(text, STYLE_DATA.FontSize.INSTRUCTION_CAPTION, 
                       STYLE_DATA.FontFamily.MAIN) for text in labelTexts]
        self.caption = Label(Text.caption, STYLE_DATA.FontSize.DESCRIPTION, STYLE_DATA.FontFamily.MAIN)
        self.header = Label(
            Text.header, STYLE_DATA.FontSize.HEADER2,STYLE_DATA.FontFamily.MAIN)
        self.fontSize = ComboBox()
        self.fontSize.addItems(INPUT_COMBO.FONT_SELECTION)
        self.colorMode = ComboBox()
        self.colorMode.addItems(INPUT_COMBO.COLOR_MODE_SELECTION)
        self.logDelete = ComboBox()
        self.logDelete.addItems(INPUT_COMBO.LOGFILE_AUTO_DELETE_SELECTION)
        self.comboInputs = [self.fontSize, self.colorMode, self.logDelete] 
        self.saveBtn = Button.ColoredBtn(Text.saveBtn, STYLE_DATA.Color.PRIMARY_BUTTON)
        self.instructionBtn = InstructionBtn(INSTRUCTION.SETTING_FORM_INS)

    def _connectSignal(self):
        """connect the signal to slots"""
        self.saveBtn.clicked.connect(self._confirmChangeSetting)
        STYLE_DATA.signal.changeColor.connect(self.colorChange)
        STYLE_DATA.signal.changeFont.connect(self.fontChange)

    def _initLayout(self):
        """initialize the form section"""
        self.mainLayout = QVBoxLayout()
        self.formLayout = QGridLayout()
        self.formContainer = QWidget()
        self.formContainer.setLayout(self.formLayout)
        self.formContainer.setFixedSize(QSize(STYLE_DATA.Dimension.FORMWIDTH, 
                                              STYLE_DATA.Dimension.FORMMINHEIGHT))
        initBackground(self.formContainer, STYLE_DATA.Color.LOW_CONTRAST)
        self.setLayout(self.mainLayout)
        for row, label in enumerate(self.labels):
            self.formLayout.addWidget(label,row, 0)
        for row, selections in enumerate(self.comboInputs):
            self.formLayout.addWidget(selections, row, 1)
        self.mainLayout.addWidget(self.header, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.mainLayout.addWidget(self.caption, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.mainLayout.addWidget(self.formContainer, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.mainLayout.addStretch()
        self.mainLayout.addWidget(self.saveBtn, alignment=Qt.AlignmentFlag.AlignHCenter)
        currRow = len(self.comboInputs)
        self._addFormButton(Text.restoreLabel, Text.restoreBtn, self._confirmRestore, currRow)
        self._addFormButton(Text.ClearLogLabel, Text.ClearLogBtn, self._clearLog, currRow + 1)
        self._addFormButton(Text.SaveLogLabel, Text.SaveLogBtn, self._saveLog, currRow + 2)
        self._addFormButton(Text.ClearCacheLabel, Text.ClearCacheBtn, self._clearCache,currRow + 3)
        
        self.mainLayout.addWidget(
            self.instructionBtn,
            alignment=Qt.AlignmentFlag.AlignAbsolute
            | Qt.AlignmentFlag.AlignBottom
            | Qt.AlignmentFlag.AlignRight,
        )

    def colorChange(self):
        self.saveBtn.colorChange(STYLE_DATA.Color.PRIMARY_BUTTON)
        for button in self.formButtons:
            button.addOtherStyle(
                f"background-color: {STYLE_DATA.Color.INPUT_BACKGROUND};"
            )
            button.colorChange(STYLE_DATA.Color.INPUT_TEXT)

    def fontChange(self):
        self.header.fontChange(STYLE_DATA.FontSize.HEADER2)
        for label in self.labels:
            label.fontChange(STYLE_DATA.FontSize.BODY)
        for btn in self.formButtons:
            btn.fontChange(STYLE_DATA.FontSize.BTN)

    def setValue(self, values: dict):
        """public function to set the system setting form value

        Args: values: a dictionary that stores the system setting value
        """
        self.fontSize.setCurrentText(values[INPUT_COMBO.FONT_SIZE])
        self.colorMode.setCurrentText(values[INPUT_COMBO.COLOR_MODE])
        self.logDelete.setCurrentText(values[INPUT_COMBO.LOG_AUTO_DELETE])

    def getValue(self) -> dict:
        """public function to get the system setting form value"""
        data = dict()
        data[INPUT_COMBO.FONT_SIZE] = self.fontSize.currentText()
        data[INPUT_COMBO.COLOR_MODE] = self.colorMode.currentText()
        data[INPUT_COMBO.LOG_AUTO_DELETE] = self.logDelete.currentText()
        return data

    def _confirmChangeSetting(self) -> None:
        """open a pop up box to confirm restarting the app and change the setting"""
        ConfirmBox(
            Text.confirmChange, self._changeSetting, QMessageBox.StandardButton.Ok
        )

    def _changeSetting(self) -> None:
        """rewrite the current setting file based on the user's choice"""
        setting = self.getValue()
        try:
            GlobalStyleSignal.changeColor.emit(setting[INPUT_COMBO.COLOR_MODE])
            GlobalStyleSignal.changeFont.emit(setting[INPUT_COMBO.FONT_SIZE])
            colorSource = StyleTable[setting[INPUT_COMBO.COLOR_MODE]]
            colorDes = StyleSource.CURRENT_COLOR
            fontSource = StyleTable[setting[INPUT_COMBO.FONT_SIZE]]
            fontDes = StyleSource.CURRENT_FONTSIZE
            logDeleteTime = LogDeleteTimeDict[setting[INPUT_COMBO.LOG_AUTO_DELETE]]
            f = open(
                f"{os.path.join(dirname, WorkSpaceConfigPath.logManagement)}", "w+"
            )
            toml.dump({"AUTO_DELETE_TIME": logDeleteTime}, f)
            f.close()
            self._copyTomlFile(colorSource, colorDes, dirname)
            self._copyTomlFile(fontSource, fontDes, dirname)
            f = open(f"{os.path.join(dirname, SettingDataPath.systemSetting)}", "w+")
            toml.dump(setting, f)
            f.close()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("changing system setting", str(e)))

    def _copyTomlFile(self, source, des, base):
        """private helper function for copying the toml file"""
        s = toml.load(os.path.join(base, source))
        with open(os.path.join(base, des), "w+") as f:
            toml.dump(s, f)

    def _clearLog(self):
        """open confirm box to confirm clearing the log file"""
        ConfirmBox(Text.confirmClear, clearAllLog)

    def _confirmRestore(self):
        """open confirm box to confirm restoring to the defaults"""
        ConfirmBox(
            "Confirm to restore to default setting",
            lambda: self.setValue(DefaultSetting),
        )

    def _saveLog(self):
        try:
            dialog = SaveLogFile()
            dialog.exec()
        except Exception as e:
            self.logger.error(e, exc_info=e)

    def _clearCache(self):
        try:
            ConfirmBox(Text.ConfirmClearCache, lambda: self.signal.clearCache.emit())
        except Exception as e:
            self.logger.error(e, exc_info=e)

    def _addFormButton(self, label, btnText, fun: callable, row):
        label = Label(label, STYLE_DATA.FontSize.INSTRUCTION_CAPTION, STYLE_DATA.FontFamily.MAIN)
        label.setFixedWidth(STYLE_DATA.Dimension.INPUTWIDTH)
        button = Button.BorderBtn(
            btnText,
            STYLE_DATA.Color.INPUT_TEXT,
            other=f"background-color: {STYLE_DATA.Color.INPUT_BACKGROUND}",
        )
        button.setFixedHeight(STYLE_DATA.Dimension.INPUTHEIGHT)
        button.setFixedWidth(130)
        button.clicked.connect(fun)
        self.formButtons.append(button)
        self.labels.append(label)
        self.formLayout.addWidget(label, row, 0)
        self.formLayout.addWidget(button, row, 1)
    
    def colorChange(self):
        initBackground(self.formContainer, STYLE_DATA.Color.LOW_CONTRAST)
        for button in self.formButtons:
            button.addOtherStyle(f"background-color: {STYLE_DATA.Color.INPUT_BACKGROUND}")
