from PyQt6.QtWidgets import QComboBox, QWidget, QVBoxLayout
from PyQt6.QtGui import QStandardItemModel

class template(QWidget):
    def __init__(self, arg1:type, arg2:type, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.arg1 = arg1
        self.arg2 = arg2
        self._initWidget()
        self._initLayout()
        self._connectSignal()
        
        
    def _initWidget(self):
        pass 
    
    def _initLayout(self):
        pass 
    
    def _connectSignal(self):
        pass