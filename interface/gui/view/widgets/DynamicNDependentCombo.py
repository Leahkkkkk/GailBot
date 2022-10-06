'''
File: DynamicNDependentCombo.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 1:44:39 pm
Modified By:  Siara Small  & Vivian Li
-----
'''


from PyQt6.QtWidgets import (
    QComboBox, 
    QWidget, 
    QVBoxLayout, 
    QLabel
)

class DynamicNDependentCombo(QWidget):
    """ Generate a dynamic list of combobox
    
    Args:
        data (dict): a dictionary that stores settings with depended logic 
                     between key setting and values 
    
    """
    def __init__(self, data:dict, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.data = data
        self._initWidget()
        self._initLayout()
        self._connectSignal()
        self._updateCombo(self.mainCombo.currentIndex())
        
    def _initWidget(self):
        """ initialize the widget """
        self.mainCombo = QComboBox(self)
        self.combolist = None
        for key, value in self.data.items():
            self.mainCombo.addItem(key, value)
    
    def _initLayout(self):
        """ initialize the layout """
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.mainCombo)
         
    def _connectSignal(self):
        """ connect the signal  """
        self.mainCombo.currentIndexChanged.connect(self._updateCombo)
    
    def _updateCombo(self, index):
        """ function to update the combobox """
        data = self.mainCombo.itemData(index)
        if self.combolist:
            self.combolist.deleteLater()
            
        self.combolist = ComboList(data)
        self.layout.addWidget(self.combolist)
        

class ComboList(QWidget):
    """ generalise a list of combobox
    
    Args:
        data(dict): a dixtionary that stores combobox data
                    the key is a string stores the label
                    the valu is a list of string that stores combobox items
    
    """
    def __init__(self, data:dict, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.data = data
        self._initWidget()
        self._initLayout()
    
    def _initWidget(self):
        """ initialize the widget """
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
        """ initialize layout """
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        for i in range(len(self.combolist)):
            self.layout.addWidget(self.labellist[i]) 
            self.layout.addWidget(self.combolist[i])
            
