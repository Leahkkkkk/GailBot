from view.style.Background import initImgBackground
from view.widgets import Label, Button
from PyQt6.QtWidgets import (
    QWidget, 
    QHBoxLayout,
    QVBoxLayout
)
from PyQt6.QtCore import Qt



class SideBar(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.setFixedWidth(200)
        self.verticalLayout.setContentsMargins(0,0,0,0)
        initImgBackground(self,"settingBackground.png")
        

        
    def addWidget(self, widget: QWidget, alignment = None):
        center = Qt.AlignmentFlag.AlignHCenter
        if alignment:
            center = center | alignment
        self.verticalLayout.addWidget(widget, alignment = center)
        
    
    def addStretch(self):
        self.verticalLayout.addStretch()
        
        