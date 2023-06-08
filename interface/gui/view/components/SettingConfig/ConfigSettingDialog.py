'''
File: SettingConfigDialog.py
Project: GailBot GUI
File Created: 2022/10/
Author: Siara Small  & Vivian Li
-----
Last Modified:2023/04/21
Modified By:  Siara Small  & Vivian Li
-----
Description: abstract class for setting configuration tab
'''

from abc import ABC
from typing import Dict, Tuple
from gbLogger import makeLogger
from view.config.Text import ENGINE_TAB_TEXT as Text
from view.config.Style import STYLE_DATA
from view.widgets.TabPage import TabDialog
from view.widgets import  WarnBox
from view.util.ErrorMsg import ERR
from PyQt6.QtCore import QObject, pyqtSignal, QSize

class Signals(QObject):
    """ a signal object to send new setting data values """
    addEngine = pyqtSignal(tuple)
    editEngine = pyqtSignal(tuple)
    addProfile = pyqtSignal(tuple)
    editProfile = pyqtSignal(tuple)

class SettingConfigDialog(ABC):
    
    mainTab: TabDialog
   
    def __init__(self) -> None:
       self.logger = makeLogger() 
       self.mainTab.finishedBtn.clicked.connect(self._postSetting)
    
    def _postSetting(self):
        raise NotImplementedError("sub-class responsibility")
    
    def exec(self):
        """ 
        must be called to display the dialog
        """
        self.mainTab.exec()
