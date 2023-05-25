'''
File: FormWidget.py
Project: GailBot GUI
File Created: 2023/04/01
Author: Siara Small  & Vivian Li
-----
Last Modified:2023/05/23
Modified By:  Siara Small  & Vivian Li
-----
Description: base class for a form widget that is used to get the user's input 
'''

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
    
    