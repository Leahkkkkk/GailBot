from PyQt6.QtWidgets import QPushButton
from PyQt6 import QtCore

""" A toggle button that display "▶" and "▼" when being toggled """
""" TODO: use a button icon instead of unicode, 
          add style 
"""
class ToggleBtn(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setText("▶")
        # setting geometry of button
        self.setMaximumSize(QtCore.QSize(30, 30))
        # setting checkable to true
        self.setCheckable(True)
        # setting calling method by button
        self.clicked.connect(self._changeSymbol)
        # show all the widgets
        self.update()
        self.show()
    # method called by button
    def _changeSymbol(self):
        # if button is checked
        if self.isChecked():
            self.setText("▼")
        else:
            self.setText("▶")
    
  
  