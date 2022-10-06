'''
File: ToggleView.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 1:43:52 pm
Modified By:  Siara Small  & Vivian Li
-----
'''
from view.widgets import Button

from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt

class ToggleView(QtWidgets.QWidget):
    """ 
    A toggle view widget that show and hide content,
    the content is passed in as a widget 

    Args:
        label(str): 
        view(object): the content that will be toggled 
    """
    def __init__(self, label:str, view: object, *args, **kwargs):
        """initialize toggle view"""
        super().__init__(*args, **kwargs)
        self.layout = QtWidgets.QGridLayout()
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(False)
        
        self.setLayout(self.layout)
        self.Btn = Button.ToggleBtn()
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
        """set view for toggle class"""
        if self.hide:
            self.scroll.show()
            self.hide = False
        else:
            self.scroll.hide()
            self.hide = True


class OnOffView(ToggleView):
    """ A subclass of toggle button on which the text of the button is 
        "on" or "off"
    """
    def __init__(self, label: str, view: object, *args, **kwargs):
        super().__init__(label, view, *args, **kwargs)
        self.Btn = Button.ToggleBtn(("on", "off"))