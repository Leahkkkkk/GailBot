'''
File: FileUploadPage.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 11:08:37 am
Modified By:  Siara Small  & Vivian Li
-----
'''

from xml.etree.ElementTree import TreeBuilder
from view.widgets import Label, Button, FileTable
from view.style.styleValues import (
    FontFamily, 
    FontSize, 
    Color, 
    Dimension,
)

from view.style import Background

from PyQt6.QtWidgets import (
    QWidget, 
    QPushButton, 
    QVBoxLayout,
    QTableView, 
    QVBoxLayout,

)
from PyQt6.QtCore import Qt, QSize, QAbstractTableModel


class dropDownWidget(QWidget):
    def __init__(self, label:str, view:QWidget, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.view = view 
        self.btn = Button.ColoredBtn(label, 
                                     Color.BLUEMEDIUM,
                                     FontSize.SMALL, 
                                     "margin-top:0px;border-radius:0px;padding:5px")
        self.hideView = True 
        self.setFixedWidth(130)
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.btn)
        self.layout.addWidget(self.view)
        self.view.hide()
        self.btn.clicked.connect(self._toggle)

    
    def _toggle(self):
        if self.hideView == True:
            self.hideView = False
            self.view.show()
        else:
            self.hideView = True 
            self.view.hide()

class buttonList(QWidget):
    def __init__(self, labels: list,  *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.layout  = QVBoxLayout(self)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        for label in labels:
            newButton = Button.ColoredBtn(label,
                                          Color.BLUEMEDIUM, 
                                          FontSize.SMALL,
                                          "margin-top:0px;border-radius:0px;border:1px solid #fff; padding:3px 0px")
            self.layout.addWidget(newButton)
            
            
class FileUploadPage(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        """ file upload page """
        super().__init__(*args, **kwargs)
        self._initWidget()
        self._initLayout()
        self._initStyle()
        
    def _initWidget(self):
        """ initialzie widget """
        self.label = Label.Label("File to Transcribe", 
                                 FontSize.HEADER2, 
                                 FontFamily.MAIN)
        self.gotoMainBtn = Button.BorderBtn("back to main", 
                                            Color.BLUEMEDIUM, 
                                            FontSize.BODY)
        self.uploadFileBtn = Button.ColoredBtn("Add File", 
                                               Color.BLUEMEDIUM, 
                                               FontSize.SMALL)
        self.transcribeBtn = Button.ColoredBtn("Transcribe", 
                                               Color.GREYMEDIUM1, 
                                               FontSize.BTN)
        self.uploadFileBtn.setFixedSize(Dimension.MEDIUMBUTTON)
        self.transcribeBtn.setFixedSize(Dimension.BGBUTTON)
        self.profiles = buttonList(["Default Settings",
                                   "Coffee Setting", 
                                   "Create New Profile"])
        self.settingProfile = dropDownWidget("Settings Profile", 
                                             self.profiles)
        self.fileTable = FileTable.FileTable()
        
        
    def _initLayout(self):
        """ initialize layout """
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        self.verticalLayout.addWidget(self.gotoMainBtn)
        self.verticalLayout.addWidget(self.label, 
                                      alignment = Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout.addWidget(self.settingProfile,
                                      alignment=Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTop)
        self.verticalLayout.addWidget(self.fileTable,
                                      alignment = Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout.addWidget(self.uploadFileBtn,
                                      alignment = Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout.addWidget(self.transcribeBtn,
                                      alignment = Qt.AlignmentFlag.AlignHCenter)
    

        
    def _initStyle(self):
        """ initialize the style """
        Background.initBackground(self)
        
   