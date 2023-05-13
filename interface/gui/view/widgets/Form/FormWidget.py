from abc import ABC 
class FormWidget():
    def __init__(self) -> None:
        self.value = None
    
        
    def initUI(self):
        raise NotImplementedError

    def connectSignal(self):
        raise NotImplementedError
    
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
        raise NotImplementedError 
    
    def disable(self):
        raise NotImplementedError
    
    