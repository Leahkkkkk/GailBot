from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import QSize
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