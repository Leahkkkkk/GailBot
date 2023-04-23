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
from view.config.Style import STYLE_DATA

class BasicPage(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        STYLE_DATA.signal.changeColor.connect(self.changeColor)
        STYLE_DATA.signal.changeFont.connect(self.changeFont)
        self.iniLogo()
        
    def changeColor(self):
        self.updateLogo()
        
    def changeFont(self):
        pass 
    
    def iniLogo(self):
        self.logoContainer = QWidget()
        self.logoLayout = QHBoxLayout()
        self.logoContainer.setLayout(self.logoLayout)
        logo, pos = getLogo()
        self.logo = logo 
        self.logopos = pos
        self.logoLayout.addWidget(self.logo, alignment=pos)
        self.logoContainer.setContentsMargins(0,0,0,0)
    
    def updateLogo(self):
        self.logoLayout.removeWidget(self.logo)
        logo, pos = getLogo()
        self.logo = logo 
        self.logoLayout.addWidget(self.logo, alignment=pos)