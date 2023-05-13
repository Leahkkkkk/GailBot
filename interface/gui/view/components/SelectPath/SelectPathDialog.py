'''
File: WorkSpaceDialog.py
Project: GailBot GUI
File Created: Tuesday, 22nd November 2022 2:09:54 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Tuesday, 29th November 2022 8:34:12 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: implement dialogues that ask users to choose file path 
             from their local machine, usage include saving log files
             saving plugin suites (currently unused)
'''
import os 
import datetime
from view.widgets.Label import Label
from view.widgets.Button import ColoredBtn
from view.util.io import zip_file, get_name, copy
from view.config.Style import STYLE_DATA
from view.config.Text import PATH_DIALOG as TEXT 
from gbLogger import makeLogger
from view.config import getWorkBasePath

from PyQt6.QtWidgets import QDialog, QFileDialog, QVBoxLayout
from PyQt6.QtCore import QSize, Qt
import userpaths
center = Qt.AlignmentFlag.AlignHCenter

class SelectPathDialog(QDialog):
    """base class for dialog that ask users to select file path
    """
    header : str       # dialog header 
    caption : str      # instruction text
    pathLabel : str    # a string that specifies what the path is used for 
    def __init__(self, *arg, **kwargs) -> None:
        super().__init__(*arg, **kwargs)
        self.userRoot = userpaths.get_desktop()
        self.logger = makeLogger()
        self._initWidget()
        self._initLayout()
        self._connectSignal()
        self._initStyle()
        
    def _initWidget(self):
        self.userRoot = userpaths.get_desktop()
        self.workDir = getWorkBasePath()
        self.header = Label(self.header, STYLE_DATA.FontSize.HEADER3, STYLE_DATA.FontFamily.MAIN)
        self.label = Label(self.caption, STYLE_DATA.FontSize.BODY, link=True)
        self.displayPath = Label(f"{self.pathLabel}: {self.userRoot}", 
            STYLE_DATA.FontSize.BODY, STYLE_DATA.FontFamily.MAIN, 
            others=f"border: 1px solid {STYLE_DATA.Color.MAIN_TEXT}; text-align:center;")
        self.confirm = ColoredBtn(TEXT.confirmBtn, STYLE_DATA.Color.SECONDARY_BUTTON)
        self.choose  = ColoredBtn(TEXT.changeDirBtn, STYLE_DATA.Color.PRIMARY_BUTTON)
   
    def _initLayout(self):
        """ initialize the layout """
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.verticalLayout.addWidget(self.header, alignment=center)
        self.verticalLayout.addWidget(self.label, alignment=center)
        self.verticalLayout.addWidget(self.displayPath)
        self.verticalLayout.addSpacing(STYLE_DATA.Dimension.MEDIUM_SPACING)
        self.verticalLayout.addWidget(self.choose, alignment=center)
        self.verticalLayout.addWidget(self.confirm, alignment=center)
    
    def _initStyle(self):
        """ initialize the style """
        self.setStyleSheet(f"background-color:{STYLE_DATA.Color.MAIN_BACKGROUND}")
        self.setFixedSize(QSize(STYLE_DATA.Dimension.PATH_DIALOG_WIDTH, 
                                STYLE_DATA.Dimension.PATH_DIALOG_HEIGHT))
    
    def _openDialog(self):
        """ open a file dialog that ask user to input the path """
        dialog = QFileDialog() 
        dialog.setDirectory(userpaths.get_profile())
        selectedFolder = dialog.getExistingDirectory()
        if selectedFolder:
            self.userRoot = selectedFolder
            self.displayPath.setText(
                f"{self.pathLabel}: {self.userRoot}")
        
    def _onConfirm(self):
        """ sub-class responsibility """
        pass
          
    def _connectSignal(self):
        self.choose.clicked.connect(self._openDialog)
        self.confirm.clicked.connect(self._onConfirm)
    
class SaveSetting(SelectPathDialog):
    """ implement a dialog that ask user to select a path to store the copy of 
        a setting data
    """
    def __init__(self, origPath, *args, **kwargs) -> None:
        self.header = TEXT.saveSettingHeader
        self.caption = TEXT.saveSettingcaption
        self.pathLabel = TEXT.selectPath 
        self.origPath = origPath
        self.copiedPath = None 
        super().__init__()
    
    def _onConfirm(self):
        try:
            self.copiedPath = copy(self.origPath, os.path.join(self.userRoot, os.path.basename(self.origPath)))
            self.close()
        except Exception as e: 
            self.logger.error(e, exc_info=e)

            
class SaveLogFile(SelectPathDialog):
    """ 
    open a dialog that ask user to select a space to store zipped log files 
    """
    def __init__(self, *arg, **kwargs) -> None:
        self.header = TEXT.saveLogPrompt
        linkFormat = "<a style='color:{0};' href='mailto: {1}'> {2} \n {1}</a>"
        self.caption =  linkFormat.format(STYLE_DATA.Color.MAIN_TEXT, TEXT.email, TEXT.sendZipMsg)
        self.pathLabel = TEXT.saveLogPath
        super().__init__(*arg, **kwargs)
        
    def _onConfirm(self):
        """ 
            On confirm, output the zipped log file to the directory selected 
            by user
        """
        try:
            logdir = getWorkBasePath()
            zip_file(logdir, os.path.join(self.userRoot, f"{TEXT.zipFileName}-{datetime.datetime.now()}.zip"), ".log")
            self.close()
        except Exception as e:
            self.logger.error(e, exc_info=e)
          
  