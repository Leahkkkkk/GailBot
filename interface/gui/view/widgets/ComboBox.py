from PyQt6.QtWidgets import QComboBox 
from PyQt6.QtCore import QSize

class ComboBox(QComboBox):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setStyleSheet("padding: 10px; font-size:14px")
        self.setContentsMargins(0,20,0,20)
        self.setFixedSize(QSize(170,50))