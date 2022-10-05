from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QGridLayout

""" 
a toggle button that display "on" and "off" text 
"""
class OnOffSelect(QWidget):
    def __init__(self, label:str, dependency=None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.label = label
        self.state = True
        self.dependency = dependency
        self._initWidget()
        self._initLayout()
        self._connectSignal()
        
    def _initWidget(self):
        self.label =  QLabel(self.label)
        self.onOffBtn = QPushButton("ON")
        self.onOffBtn.setMaximumSize(40, 100)
    
    def _initLayout(self):
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)
        self.layout.addWidget(self.label,0,0)
        self.layout.addWidget(self.onOffBtn,0,1) 
        if self.dependency:
            self.layout.addWidget(self.dependency,1,0,2,6)
        
    
    def _connectSignal(self):
        self.onOffBtn.clicked.connect(self._updateStatus)

    def _updateStatus(self):
        if self.state:
            self.state = False
            self.onOffBtn.setText("OFF")
            if self.dependency:
                self.dependency.hide()
        else:
            self.state = True 
            self.onOffBtn.setText("ON")
            if self.dependency:
                self.dependency.show()
    
    
    def value(self):
        return self.state