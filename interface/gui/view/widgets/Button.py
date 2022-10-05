from PyQt6.QtWidgets import QPushButton
from PyQt6 import QtCore
from view.style.style import FontSize

class ColoredBtn(QPushButton):
    def __init__(self,label:str, color:str, fontsize=FontSize.BTN, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # setting geometry of button
        self.setText(label)
        self.setStyleSheet(f"background-color:{color};"
                           f"color:#fff;"
                           f"border-radius:5;"
                           f"padding:1;"
                           f"font-size:{fontsize}")
        self.setMaximumSize(QtCore.QSize(100, 40))

    
class BorderBtn(QPushButton):
    def __init__(self,label:str, color:str,fontsize=FontSize.BTN, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # setting geometry of button
        self.setText(label)
        self.setStyleSheet(f"border: 2px solid {color};"
                           f"color:{color};"
                           f"border-radius:5;"
                           f"padding:1;"
                           f"font-size:{fontsize}")
        self.setMaximumSize(QtCore.QSize(100, 40))
