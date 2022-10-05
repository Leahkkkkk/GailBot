from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from view.widgets import ToggleBtn

""" 
A toggle view widget that show and hide content,
the content is passed in as a widget 

param:
    @label: 
    @view: the content that will be toggled 
"""
class ToggleView(QtWidgets.QWidget):
    def __init__(self, label:str, view: object, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QtWidgets.QGridLayout()
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(False)
        
        self.setLayout(self.layout)
        self.Btn = ToggleBtn.ToggleBtn()
        self.label = QtWidgets.QLabel(label)
        self.label.setAlignment( Qt.AlignmentFlag.AlignLeft)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.label, 1, 1)
        self.layout.addWidget(self.Btn, 1, 0)
        self.view = view
        self.scroll.setWidget(self.view)
        self.layout.addWidget(self.scroll, 2, 0, 2,8)
        self.scroll.hide()
        self.hide = True
        self.Btn.clicked.connect(self._toggleView)
  
    def _toggleView(self):
        if self.hide:
            self.scroll.show()
            self.hide = False
        else:
            self.scroll.hide()
            self.hide = True