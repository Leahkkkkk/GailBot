from abc import ABC 
from PyQt6 import QtWidgets

class FormWidget():
    def __init__(self) -> None:
        self.value = None
        
    def initUI(self):
        pass 
    
    def connectSignal(self):
        pass
    
    def getValue(self):
        try:
          return self.value 
        except:
          pass 
    
    def updateValue(self, value):
        try:
          self.value = value 
        except:
          pass 
        
    def setValue(self, value):
        try:
            self.updateValue(self, value)
        except:
            pass 
    
    def enable(self):
        pass 
    
    def disable(self):
        pass
    
    