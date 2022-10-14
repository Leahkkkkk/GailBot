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
from view.widgets import Button, Label
from view.style.styleValues import (
    Color,
    FontFamily,
    FontSize,
    Dimension,
    Geometry
) 

from PyQt6.QtWidgets import QHBoxLayout, QWidget, QScrollArea, QVBoxLayout, QGridLayout
from PyQt6.QtCore import Qt

class ToggleView(QWidget):
    """ 
    A toggle view widget that show and hide content,
    the content is passed in as a widget 

    Args:
        label(str): 
        view(object): the content that will be toggled 
        header(bool): if set to true, the width of the label will be wider
    """
    def __init__(self, label:str, view: object, header = False, color =Color.BLUELIGHT, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.labelStr = label
        self.view = view
        self.header = header
        self.color = color
        self._configHeader()
        self._configViewField()
        self._initLayout()
        self._connectSignal()
    
    
    def _configHeader(self):
        self.Btn = Button.ToggleBtn(text=self.labelStr)
        self.Btn.setStyleSheet("text-align:left;"
                               f"background-color: {self.color};"
                               "border:0.5px solid #000;"
                               "padding-left: 5px;"
                               f"font-size: {FontSize.BODY}")
        if self.header:
            self.Btn.setMinimumWidth(600)
       
    def _configViewField(self):
        self.scroll = QScrollArea()
        self.scroll.setMinimumWidth(400)
        self.scroll.setMaximumWidth(650)
        self.scroll.setMinimumHeight(100)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.view)
        self.setObjectName("viewWrapper")
        self.scroll.setObjectName("view")
        self.scroll.setStyleSheet(f"#viewWrapper, #view {{background-color:{Color.BLUEWHITE}}}")
        self.view.setObjectName("viewContainer")
        self.view.setStyleSheet(f"#viewContainer {{background-color:{Color.BLUEWHITE}}}")
        self.scroll.hide()
        self.hide = True
    
    
    def _initLayout(self):
        """ initialize the layout """
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.Btn, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.scroll)
    
    def _connectSignal(self):
        self.Btn.clicked.connect(self._toggleView)
        
    def _toggleView(self):
        """set view for toggle class"""
        if self.hide:
            self.scroll.show()
            self.hide = False
        else:
            self.scroll.hide()
            self.hide = True
    
    def resizeViewHeight(self,size: int):
        self.scroll.setMinimumHeight(size)


class OnOffView(ToggleView):
    """ A subclass of toggle button on which the text of the button is 
        "on" or "off"
    """
    def __init__(self, label: str, view: object, *args, **kwargs):
        super().__init__(label, view, *args, **kwargs)
        self.Btn = Button.ToggleBtn(("on", "off"))