'''
File: TableWidgets.py
Project: GailBot GUI
File Created: Tuesday, 11th October 2022 4:06:08 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 13th October 2022 12:20:11 pm
Modified By:  Siara Small  & Vivian Li
-----
'''

from view.widgets.Button import iconBtn, ColoredBtn, dropDownButton, ToggleBtn
from view.widgets import InputBox, Label, ToggleView, Image
from view.components import PostSet, RequiredSet
from view.style.styleValues import (
    Dimension, Color, FontFamily, FontSize)
from view.style import Background
from model import SettingModel

from PyQt6.QtWidgets import (
    QWidget, 
    QCheckBox,
    QHBoxLayout,
    QVBoxLayout,
    QDialog,
    QGridLayout,
    QScrollArea)
from PyQt6.QtCore import QSize, Qt

""" TODO: add the functionalities of the trhee buttons"""
class Actions(QWidget):
    """ action widget with three buttons: delete, settings, save
    """
    def __init__(
                self,
                settingFun:callable = None, 
                createFun:callable = None,
                deleteFun:callable = None,
                fileKey:int = 0,
                *args, **kwagrs):
        super().__init__(*args, **kwagrs)
        self.setFixedSize(Dimension.ACTION)
        self.layout = QHBoxLayout(self)
        self.layout
        self.setLayout(self.layout)
        self.fileKey = fileKey
        self.setBtn  = iconBtn("settings.png")
        self.deleteBtn = iconBtn("trash.png")
        self.createBtn = iconBtn("disk.png")
        self.layout.addWidget(self.setBtn)
        self.layout.addWidget(self.deleteBtn)
        self.layout.addWidget(self.createBtn)
        self.layout.setContentsMargins(0,0,0,0)
        self.setBtn.clicked.connect(settingFun)
        self.deleteBtn.clicked.connect(lambda:deleteFun(fileKey))
        self.createBtn.clicked.connect(createFun)
    
""" TODO: 
1. try to make different pop up effect 
2. style of the icon - file directory 
"""
class selectAndCheck(QWidget):
    """

    Args:
       full(bool, defaults to False): 
            if true, shows the full file details with setting data 
    """
    def __init__(self, full=False, *args, **kwagrs):
        super().__init__(*args, **kwagrs)
        layout = QHBoxLayout(self)
        self.full = full
        self.setLayout(layout)
        layout.setContentsMargins(5,0,10,0)
        file = iconBtn("file.jpeg")
        file.setFixedWidth(25)
        checkBox = QCheckBox(self)
        layout.addWidget(file)
        layout.addWidget(checkBox)
        checkBox.setStyleSheet("margin-left: 10px")
        file.clicked.connect(self._showDetail)
        self.setFixedSize(Dimension.ACTION)
        
    
    def _showDetail(self):
        Dialog = FileDetailDialog(fullDetail=self.full)
        Dialog.exec()


class PosTranscribeAction(QWidget):
    """ widget for transcribe success table,
        inlude a change location button and a post  transcribe setting 
        button 

    Args:
        
    """
    def __init__(self, 
                  settingFun:callable = None, 
                  createFun:callable = None,
                  deleteFun:callable = None,
                  fileKey:int = 0,
                  *args, 
                  **kwagrs):
        super().__init__(*args, **kwagrs)
        self.layout = QVBoxLayout()
        self.changeLocationBtn = ColoredBtn("Change Location", 
                                            Color.BLUEMEDIUM, 
                                            FontSize.SMALL,
                                            borderRadius=0)
        self.postSettingBtn = ColoredBtn("Post Transcribe Setting", 
                                            Color.BLUEMEDIUM, 
                                            FontSize.SMALL,
                                            borderRadius=0)
        self.changeLocationBtn.setFixedSize(QSize(140,16))
        self.postSettingBtn.setFixedSize(QSize(140,16))
        self.layout.setSpacing(0.5)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.changeLocationBtn,
                              alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.postSettingBtn,
                              alignment=Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(self.layout)
        self.postSettingBtn.clicked.connect(settingFun)


class ConfirmAction(QWidget):
    def __init__(self, 
                  toggleFun:callable,
                  *args, 
                  **kwagrs):
        super().__init__(*args, **kwagrs)
    
        self.button = ToggleBtn(state = True)
        self.button.setFixedSize(QSize(18,18))
        self.button.setContentsMargins(40,-10,0,0)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.button)
        self.button.clicked.connect(toggleFun)
    

        
class FileDetailDialog(QDialog):
    """ 
        A pop up window that displays the file details
    """
    def __init__(
        self,  
        files=["file1", "file2", "file3", "file4", "file5", "file6"] , 
        transcriber="Dummy", 
        date="2022/10/10",
        fullDetail = False,
        *args, 
        **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setWindowTitle("File Datails")
        self.files = files 
        self.transcriberStr = transcriber
        self.dateStr = date
        if fullDetail:
            self.mainWidget = FullFileDetailWidget(self.files, 
                                         self.transcriberStr, 
                                         self.dateStr)
            self.setMinimumSize(Dimension.LARGEDIALOG)
        else:
            self.mainWidget = DirectoryDetails(self.files, 
                                            self.transcriberStr, 
                                            self.dateStr)
            self.setMaximumSize(Dimension.MEDIUMDIALOG)
            
        self.saveBtn = ColoredBtn("save",Color.BLUEDARK, FontSize.SMALL)
        self.saveBtn.setFixedSize(QSize(50,35))
        
        self.saveBtn.clicked.connect(self._closeWindow)
        self._initLayout()
        
    def _initLayout(self):
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.mainWidget)
        self.layout.addWidget(self.saveBtn, 
                              alignment=Qt.AlignmentFlag.AlignRight)
        Background.initBackground(self, Color.BLUEWHITE)
        
    def _closeWindow(self):
        print("close")
        self.close()
    

""" TODO: add functionality to change the transcriber data  """
class DirectoryDetails(QWidget):
    """ 
        A widget that display the file directory details, transcriber and 
        transcribeDate
    """
    def __init__(
        self, 
        files=["file1", "file2", "file3", "file4", "file5", "file6"] , 
        transcriber="Dummy", 
        date="2022/10/10",
        *args, 
        **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setMinimumSize(Dimension.MEDIUMDIALOG)
        self.files = files 
        self.transcriberStr = transcriber
        self.dateStr = date
        self._initWidget()
        self._initLayout()

    def _initWidget(self):
        self.transcriber = InputBox.InputBox("Transcribed by: ", True, FontSize.SMALL)
        self.transcriber.setText(self.transcriberStr)
        self.transcribeDate =Label.Label(f"Transcribed on: \n {self.dateStr}", True, FontSize.SMALL)
        self.inDirLabel = Label.Label("In this directory", FontSize.BODY, 
                                          FontFamily.MAIN)
        self.inDirLabel.setMinimumWidth(200)
        self.aboutDirLabel = Label.Label("About this directory", FontSize.BODY, 
                                          FontFamily.MAIN)
        self.fileLsitScroll = QScrollArea()
        self.fileList = DirectoryView(self.files)
        self.fileLsitScroll.setWidget(self.fileList)

    def _initLayout(self):
        Background.initBackground(self, Color.BLUEWHITE)
        self.leftVLayout  = QVBoxLayout()
        self.rightVLayout = QVBoxLayout()
        self.mainLayout = QHBoxLayout()
        self.leftContainer = QWidget()
        self.rightContainer = QWidget()
        self.leftContainer.setLayout(self.leftVLayout)
        self.rightContainer.setLayout(self.rightVLayout)
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.leftContainer)
        self.mainLayout.addWidget(self.rightContainer)
        self.leftVLayout.addWidget(self.inDirLabel)
        self.leftVLayout.addWidget(self.fileLsitScroll)
        self.leftVLayout.addStretch()
        self.leftVLayout.setSpacing(20)
        self.rightVLayout.addWidget(self.aboutDirLabel)
        self.rightVLayout.addWidget(self.transcriber)
        self.rightVLayout.addWidget(self.transcribeDate)
        self.rightVLayout.addStretch()
        self.rightVLayout.setSpacing(20)
        
        
        

""" TODO:1. add function to accept setting data, 
         2. disable all editing for setting data 
"""
class FullFileDetailWidget(QWidget):
    """ A widget that will show the details in the directory 

        Args:
            files (list, optional): list of filenames
            transcriber (str, optional): the transcriber name
            date (str, optional): transcription time 
    """
    def __init__(
        self, 
        files=["file1", "file2", "file3", "file4", "file5", "file6"] , 
        transcriber="Dummy", 
        date="2022/10/10",
        *args, 
        **kwargs) -> None:
        
        super().__init__(*args, **kwargs)
        self.setMaximumSize(Dimension.LARGEDIALOG)
        self.files = files 
        self.transcriberStr = transcriber
        self.dateStr = date
        self._initWidget()
        self._initLayout()
    
    def _initWidget(self):
        self.briefDetail = DirectoryDetails(self.files, 
                                            self.transcriberStr, 
                                            self.dateStr)
        setData = SettingModel.SettingModel().data
        self.settingHeader = Label.Label("settings applied", FontSize.BODY, FontFamily.MAIN)
        self.requiredSetWidget = RequiredSet.RequiredSet(setData["Coffee Study"]["engine"])
        self.requiredSetting = ToggleView.ToggleView("Required Setting", 
                                                     self.requiredSetWidget,
                                                     header=True, 
                                                     headercolor="#fff", 
                                                     viewcolor="#fff")
        self.postSetWidget = PostSet.PostSet(setData["Coffee Study"]["Post Transcribe"])
        self.postSetting = ToggleView.ToggleView("Post Transcribe Setting", 
                                                 self.postSetWidget,
                                                 header=True,
                                                 headercolor="#fff", 
                                                 viewcolor="#fff")
        
    def _initLayout(self):
        self.briefDetail.setMaximumSize(Dimension.MEDIUMDIALOG)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.briefDetail)
        self.layout.addWidget(self.settingHeader)
        self.layout.addWidget(self.requiredSetting,alignment=Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(self.postSetting, alignment=Qt.AlignmentFlag.AlignTop)
        self.layout.setSpacing(0)
        self.layout.addStretch()
        self.requiredSetting.setContentsMargins(0,0,0,0)
        self.postSetting.setContentsMargins(0,0,0,0)
        Background.initBackground(self, Color.BLUEWHITE)
            
    
class DirectoryView(QWidget):
    """ a widget to display a list of file  """
    def __init__(self, files: list, *args, **kwargs) -> None:
        super().__init__( *args, **kwargs)
        self.layout = QVBoxLayout()
        for file in files:
            fileIcon  = FileDisplay(file)
            self.layout.addWidget(fileIcon, alignment=Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.layout)
        self.setMinimumSize(QSize(200, 140))
        self.layout.setSpacing(5)
        

""" TODO: make the file detail clickable  """
class FileDisplay(QWidget):
    """ a widget to display a single filename with the file icon """
    def __init__(self,filename: str, *args, **kwargs) -> None:
        super().__init__( *args, **kwargs)
        self.layout = QHBoxLayout(self)
        self.icon = Image.Image("file.jpeg", size=20)
        self.label = Label.Label(filename, 
                                 FontSize.SMALL, 
                                 color=Color.GREYDARK)
        self.layout.addWidget(self.icon)
        self.layout.addWidget(self.label)