'''
File: SideBar.py
Project: GailBot GUI
File Created: Friday, 4th November 2022 1:01:27 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Friday, 4th November 2022 6:10:45 pm
Modified By:  Siara Small  & Vivian Li
-----
'''

from view.style.Background import initImgBackground
from util.Config import Asset, Dimension
from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout
)
from PyQt6.QtCore import Qt



class SideBar(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.setFixedWidth(Dimension.SIDEBAR)
        self.verticalLayout.setContentsMargins(0,0,0,0)
        initImgBackground(self, Asset.sidebarColor)

        
    def addWidget(self, widget: QWidget, alignment = None):
        center = Qt.AlignmentFlag.AlignHCenter
        if alignment:
            center = center | alignment
        self.verticalLayout.addWidget(widget, alignment = center)
        
    
    def addStretch(self):
        self.verticalLayout.addStretch()
        
        