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

from view.widgets.Background import initSideBarBackground
from config.Style import Dimension

from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout
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
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.setFixedWidth(Dimension.SIDEBAR)
        self.verticalLayout.setContentsMargins(0,0,0,0)
        initSideBarBackground(self)
        
    def addWidget(self, widget: QWidget, alignment = None) -> None:
        """ adds a widget to the sidebar
        Args: widget(QWidget): widget to add
              alignment: alignment of the added widget
        """
        center = Qt.AlignmentFlag.AlignHCenter
        if alignment:
            center = center | alignment
        self.verticalLayout.addWidget(widget, alignment = center)
        
    def addStretch(self) -> None:
        """ adds a stretch to the sidebar """
        self.verticalLayout.addStretch()
        
        