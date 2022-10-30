from PyQt6.QtWidgets import (
    QWidget, 
    QHBoxLayout,
    QVBoxLayout
)
from PyQt6.QtCore import Qt

from view.style.Background import initImgBackground

class SideBar(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        self.setFixedWidth(210)
        initImgBackground(self,"settingBackground.png")
        

        
    def addWidget(self, widget: QWidget):
        center = Qt.AlignmentFlag.AlignHCenter
        self.verticalLayout.addWidget(widget, alignment = center)
        
    
    def addStretch(self):
        self.verticalLayout.addStretch()
        
        