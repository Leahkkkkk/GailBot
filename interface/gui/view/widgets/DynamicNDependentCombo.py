""" 
Takes in a dictionary that stores settings with depended logic 
between key setting and values 

Generate a dynamic list of combobox
"""

from PyQt6.QtWidgets import QComboBox, QWidget, QVBoxLayout, QLabel

class DynamicNDependentCombo(QWidget):
    def __init__(self, data:dict, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.data = data
        self._initWidget()
        self._initLayout()
        self._connectSignal()
        self._updateCombo(self.mainCombo.currentIndex())
        
    def _initWidget(self):
        self.mainCombo = QComboBox(self)
        self.combolist = None
        for key, value in self.data.items():
            self.mainCombo.addItem(key, value)
    
    def _initLayout(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.mainCombo)
         
    def _connectSignal(self):
        self.mainCombo.currentIndexChanged.connect(self._updateCombo)
    
    def _updateCombo(self, index):
        data = self.mainCombo.itemData(index)
        if self.combolist:
            self.combolist.deleteLater()
            
        self.combolist = ComboList(data)
        self.layout.addWidget(self.combolist)
        

class ComboList(QWidget):
    def __init__(self, data:dict, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.data = data
        self._initWidget()
        self._initLayout()
    
    def _initWidget(self):
        self.combolist = []
        self.labellist = []
        for key, items in self.data.items():
            newlabel = QLabel(key)
            self.labellist.append(newlabel)
            newCombo = QComboBox(self)
            newCombo.addItems(items)
            newCombo.setCurrentIndex(0)
            self.combolist.append(newCombo)

    def _initLayout(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        for i in range(len(self.combolist)):
            self.layout.addWidget(self.labellist[i]) 
            self.layout.addWidget(self.combolist[i])
            
