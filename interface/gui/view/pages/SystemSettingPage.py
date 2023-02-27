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
import shutil 
import toml
from util.Style import Color, StyleSheet, FontSize,Dimension
from view.widgets import (
    SideBar, 
    SettingForm, 
    Label, 
    Button
)
from view.components.WorkSpaceDialog import ChangeWorkSpace

from config.ConfigPath import BackEndDataPath, SettingDataPath
from util.Setting import SystemSetting, DefaultSetting
from util.StyleSource import StyleSource, StyleTable
from util.Text import SystemSetPageText as Text 
from util.Text import SystemSettingForm as Form
from util.Text import About, Links, LogDeleteTimeDict
from util.Path import getProjectRoot
from util.FileManage import clearAllLog
from util.GailBotData import getWorkBasePath
from view.widgets import MsgBox

from PyQt6.QtWidgets import (
    QWidget, 
    QHBoxLayout,
    QStackedWidget,
    QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal, QObject

dirname = getProjectRoot()
class Signal(QObject):
    restart = pyqtSignal()

bottom = Qt.AlignmentFlag.AlignBottom
class SystemSettingPage(QWidget):
    """ class for the system settings page """
    def __init__(self, *args, **kwargs) -> None:
        """ initializes the page """
        super().__init__(*args, **kwargs)
        self.data = Form
        self.signal = Signal()
        self._initWidget()
        self._initLayout()
        self._initStyle()
        self._connectSignal()
        self._loadValue(SystemSetting)
        
    def _initWidget(self):
        """ initializes widgets to be shown """
        self.sideBar = SideBar.SideBar()
        self.Mainstack = QStackedWidget()
        self.SysSetForm = SettingForm.SettingForm(
            Text.header, self.data, Text.caption)
        self.deleteLog = Button.BorderBtn(
            "Clear", 
            Color.INPUT_TEXT, 
            other= f"background-color: {Color.INPUT_BACKGROUND}")
        self.deleteLog.setFixedWidth(100)
        self.deleteLog.setFixedHeight(Dimension.INPUTHEIGHT)
        self.deleteLogLabel = Label.Label(Text.clearLog, FontSize.BODY)

        self.changeDir = Button.BorderBtn(
            "Change", 
            Color.INPUT_TEXT, 
            other= f"background-color: {Color.INPUT_BACKGROUND}")
        self.changeDir.setFixedWidth(100)
        self.changeDir.setFixedHeight(Dimension.INPUTHEIGHT)
        self.changeDirLabel = Label.Label(
            Text.changeWorkSpace, FontSize.BODY)
        directory = getWorkBasePath()
        self.directoryDisplay = Label.Label(
            f"    Current work space: {directory}/GailBot",
            FontSize.SMALL, 
            Color.PRIMARY_INTENSE
        )
        
        self.restoreBtnContainer = QWidget()
        self.restoreBtnLayout = QHBoxLayout()
        self.restoreBtnContainer.setLayout(self.restoreBtnLayout)
        self.restoreBtn = Button.BorderBtn(
            "Restore Defaults", 
            Color.INPUT_TEXT, 
            other= f"background-color: {Color.INPUT_BACKGROUND}")
        self.restoreBtn.setFixedHeight(Dimension.INPUTHEIGHT)
        self.restoreBtnLayout.addWidget(
            self.restoreBtn, alignment=Qt.AlignmentFlag.AlignRight)
       
        self.Mainstack.addWidget(self.SysSetForm)
        self.GuideLink = Label.Label(Links.guideLinkSideBar, FontSize.LINK, link=True)
        self.cancelBtn = Button.ColoredBtn(
            Text.cancelBtn, Color.CANCEL_QUIT)
        self.saveBtn = Button.ColoredBtn(
            Text.saveBtn, Color.SECONDARY_BUTTON)
        self.versionLabel = Label.Label(About.version, FontSize.SMALL)
        self.copyRightLabel = Label.Label(About.copyRight, FontSize.SMALL)
        self.deleteContainer = QWidget()
        self.deleteLayout = QHBoxLayout()
        self.changeDirContainer = QWidget()
        self.changeDirLayout = QHBoxLayout()
    
    def _connectSignal(self):
        """ connect the signal to slots """
        self.deleteLog.clicked.connect(self._clearLog)
        self.saveBtn.clicked.connect(self._confirmChangeSetting)
        self.changeDir.clicked.connect(self._changeDirHandler)
        self.restoreBtn.clicked.connect(self._confirmRestore)
        
    
    def _changeDirHandler(self):
        dialog = ChangeWorkSpace()
        dialog.exec()
        directory = getWorkBasePath()
        self.directoryDisplay.setText(
            f"    Current work space: {directory}/GailBot"
        )
    
    def _initLayout(self):
        """ initializes the layout of the page """
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0,0,0,0)
        self.horizontalLayout.setSpacing(0)
        
        self.setLayout(self.horizontalLayout)
        """ add widgets to horizontal layout """
        self.horizontalLayout.addWidget(self.sideBar)
        self.horizontalLayout.addWidget(self.Mainstack)
        self.sideBar.addStretch()
        self.sideBar.addWidget(self.saveBtn)
        self.sideBar.addWidget(self.cancelBtn)
        self.sideBar.addStretch()
        self.sideBar.addWidget(self.GuideLink, alignment=bottom)
        self.sideBar.addWidget(self.versionLabel, alignment=bottom)
        self.sideBar.addWidget(self.copyRightLabel, alignment=bottom)
    
        self.deleteContainer.setLayout(self.deleteLayout)
        self.deleteLayout.addWidget(self.deleteLogLabel)
        self.deleteLayout.addSpacing(55)
        self.deleteLayout.addWidget(self.deleteLog)
        self.SysSetForm.addWidget(self.deleteContainer)
    
        self.changeDirContainer.setLayout(self.changeDirLayout)
        self.changeDirLayout.addWidget(self.changeDirLabel)
        self.changeDirLayout.addWidget(self.changeDir)
        
        self.SysSetForm.addWidget(self.changeDirContainer)
        self.SysSetForm.addWidget(self.directoryDisplay)
        self.restoreBtn.setContentsMargins(10,50,10,20)
        self.SysSetForm.addWidget(self.restoreBtnContainer)
        
    def _initStyle(self):
        self.Mainstack.setObjectName(StyleSheet.sysSettingStackID)
        """ add this to an external stylesheet"""
        self.Mainstack.setStyleSheet(StyleSheet.sysSettingStack)
   
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
        MsgBox.ConfirmBox(
            Text.confirmChange, 
            self._changeSetting, 
            QMessageBox.StandardButton.Reset)
        
        
    def _changeSetting(self)->None:
        """ rewrite the current setting file based on the user's choice"""
        setting = self.SysSetForm.getValue()
        try:
            colorSource = StyleTable[setting["Color Mode"]]
            colorDes    = StyleSource.CURRENT_COLOR
            fontSource  = StyleTable[setting["Font Size"]]
            fontDes     = StyleSource.CURRENT_FONTSIZE
            logDeleteTime = LogDeleteTimeDict[setting["Log file auto deletion time"]]
            f = open (f"{os.path.join(dirname, BackEndDataPath.fileManageData)}", "w+")
            toml.dump({"AUTO_DELETE_TIME" : logDeleteTime}, f)
            f.close()
            self._copyTomlFile(colorSource, colorDes, dirname)
            self._copyTomlFile(fontSource, fontDes, dirname) 
            
            f = open (f"{os.path.join(dirname, SettingDataPath.systemSetting)}", "w+")
            toml.dump(setting, f)
            f.close()
        except shutil.SameFileError:
            MsgBox.WarnBox("No setting is changed")
        except KeyError:
            MsgBox.WarnBox("Error loading File")
        except:
            MsgBox.WarnBox(Text.changeError)
        self.signal.restart.emit() 
               
    def _copyTomlFile(self, source, des, base):
        """ private helper function for copying the toml file """
        s = toml.load(os.path.join(base,source))
        with open(os.path.join(base, des), "w+") as f:
            toml.dump(s, f)

    def _clearLog(self):
        """ open confirm box to confirm clearing the log file """
        MsgBox.ConfirmBox(Text.confirmClear, clearAllLog)
    
    def _loadValue(self, setting):
        """ initialize the setting value """
        self.SysSetForm.setValue(setting)
    
    def _confirmRestore(self):
        """ open confirm box to confirm restoring to the defaults """
        MsgBox.ConfirmBox(
            "Confirm to restore to default setting", 
            lambda: self._loadValue(DefaultSetting))