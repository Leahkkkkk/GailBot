'''
File: SideBar.py
Project: GailBot GUI
File Created: Friday, 4th November 2022 1:01:27 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Friday, 4th November 2022 6:10:45 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: a side bar widget 
'''

from .Background import initSideBarBackground
from .Label import Label
from ..config.Style import STYLE_DATA
from ..config.Text import About, Links
from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout,
    QGridLayout
)
from PyQt6.QtCore import Qt

class SideBar(QWidget):
    """ implementation the sidebar of the settings page 
    
    public function:
    1. addWidget(self, widget: QWidget, alignment = None) -> None
    2. addStretch(self) -> None
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # initialize the top level grid layout 
        self.gridLayout  = QGridLayout()
        self.gridLayout.setRowMinimumHeight(0, 100)
        self.gridLayout.setRowMinimumHeight(2, 150)
        self.gridLayout.setRowStretch(1, 2)
        
        # initialize the top container 
        self.topContainer = QWidget()
        self.toplayout = QVBoxLayout()
        self.toplayout.setContentsMargins(0,0,0,0)
        self.toplayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.topContainer.setLayout(self.toplayout)
        self.gridLayout.addWidget(self.topContainer,0,0)

        # initialize the bottom container
        self.btmContainer = QWidget()
        self.btmlayout = QVBoxLayout()
        self.btmlayout.setContentsMargins(0,0,0,0)
        self.btmlayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.btmContainer.setLayout(self.btmlayout)
        self.gridLayout.addWidget(self.btmContainer,2,0)

        # initialize the middle container
        self.midContainer = QWidget()
        self.midlayout = QVBoxLayout()
        self.midlayout.setContentsMargins(0,0,0,0)
        self.midlayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.midContainer.setLayout(self.midlayout)
        self.gridLayout.addWidget(self.midContainer,1,0)
        self.setLayout(self.gridLayout )
        self.setFixedWidth(STYLE_DATA.Dimension.SIDEBAR)
        self.gridLayout.setContentsMargins(0,0,0,0)
        self.gridLayout.setSpacing(0)
        self.addFooter()
        self.midContainer.setStyleSheet( f"border-right:0.5px solid {STYLE_DATA.Color.OUTLINE};" )
        self.topContainer.setStyleSheet( f"border-right:0.5px solid {STYLE_DATA.Color.OUTLINE};" )
        self.btmContainer.setStyleSheet( f"border-right:0.5px solid {STYLE_DATA.Color.OUTLINE};" )
        STYLE_DATA.signal.changeColor.connect(self.colorChange)
        STYLE_DATA.signal.changeFont.connect(self.fontChange)
        initSideBarBackground(self)
        
    def colorChange(self):
        self.setObjectName("sidebar")
        self.midContainer.setStyleSheet(f"border-right:0.5px solid {STYLE_DATA.Color.OUTLINE};")
        self.topContainer.setStyleSheet(f"border-right:0.5px solid {STYLE_DATA.Color.OUTLINE};")
        self.btmContainer.setStyleSheet(f"border-right:0.5px solid {STYLE_DATA.Color.OUTLINE};")
        initSideBarBackground(self)
        
    def fontChange(self):
        self.GuideLink.fontChange(STYLE_DATA.FontSize.LINK) 
        self.versionLabel.fontChange(STYLE_DATA.FontSize.SMALL) 
        self.copyRightLabel.fontChange(STYLE_DATA.FontSize.SMALL) 

    def addTopWidget(self, widget) -> None:
        self.toplayout.addWidget(widget)
    
    def addMidWidget(self, widget) -> None:
        self.midlayout.addWidget(widget)
    
    def addBtmWidget(self, widget) -> None:
        self.btmlayout.addWidget(widget)

    def addFooter(self) -> None:
        self.GuideLink = Label(Links.guideLinkSideBar, STYLE_DATA.FontSize.LINK, link=True)
        self.versionLabel = Label(About.version, STYLE_DATA.FontSize.SMALL)
        self.versionName = Label(About.versionName, STYLE_DATA.FontSize.SMALL)
        self.copyRightLabel = Label(About.copyRight, STYLE_DATA.FontSize.SMALL)
        
        self.btmlayout.addStretch()
        self.btmlayout.addWidget(self.GuideLink, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.btmlayout.addWidget(self.versionLabel,alignment=Qt.AlignmentFlag.AlignHCenter)
        self.btmlayout.addWidget(self.versionName,alignment=Qt.AlignmentFlag.AlignHCenter)
        self.btmlayout.addWidget(self.copyRightLabel,alignment=Qt.AlignmentFlag.AlignHCenter)
        self.btmlayout.addStretch()

        
