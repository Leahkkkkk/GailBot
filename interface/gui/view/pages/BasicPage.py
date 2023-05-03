'''
File: BasicPage.py
Project: GailBot GUI
File Created: 2022/10/
Author: Siara Small  & Vivian Li
-----
Last Modified:2023/04/18
Modified By:  Siara Small  & Vivian Li
-----
Description: The Base class for basic page, the hilab log is added to 
the top right of the page 
'''
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from view.widgets import getLogo
from view.widgets.Button import InstructionBtn
from view.config.Style import STYLE_DATA
from PyQt6.QtCore import Qt

class BasicPage(QWidget):
    pageInstruction = None 
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        STYLE_DATA.signal.changeColor.connect(self.changeColor)
        STYLE_DATA.signal.changeFont.connect(self.changeFont)
        self.instructionBtn = InstructionBtn(self.pageInstruction)
        self.iniLogo()
        self.logopos = Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight| Qt.AlignmentFlag.AlignAbsolute
        self.infopos = Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignAbsolute
        
    def _initLayout(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.instructionBtn, alignment=self.infopos)    
        self.mainLayout.addWidget(self.logoContainer, alignment=self.logopos) 
        self.setLayout(self.mainLayout)   
        
    def changeColor(self):
        self.updateLogo()
        
    def changeFont(self):
        pass 
    
    def iniLogo(self):
        self.logoContainer = QWidget()
        self.logoLayout = QHBoxLayout()
        self.logoContainer.setLayout(self.logoLayout)
        logo = getLogo()
        self.logo = logo 
        self.logoLayout.addWidget(self.logo)
        self.logoContainer.setContentsMargins(0,0,0,0)
    
    def updateLogo(self):
        self.logoLayout.removeWidget(self.logo)
        logo = getLogo()
        self.logo = logo 
        self.logoLayout.addWidget(self.logo, alignment=self.logopos)