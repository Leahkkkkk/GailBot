'''
File: PostSetPage.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 11:08:27 am
Modified By:  Siara Small  & Vivian Li
-----
'''

from view.widgets import InputBox, Button, Label
from view.components import PostSet
from view.style.styleValues import FontFamily, FontSize

from PyQt6.QtWidgets import QWidget, QVBoxLayout,QScrollArea
from PyQt6.QtCore import Qt


class PostSetPage(QWidget):
    """ post-transcription settings page """
    def __init__(self, data, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.data = data
        self._initWidget()
        self._initLayout()
        
    def _initWidget(self):
        """initialize widgets"""
        self.header = Label.Label("Post Transcription Setting",
                                  FontSize.HEADER2,FontFamily.MAIN)
        self.caption = Label.Label("These settings are applied after the file is created.",
                                   FontSize.BODY)
        self.PostSet = PostSet.PostSet(self.data)
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setWidget( self.PostSet)
        self.scroll.setFixedWidth(600)
        self.PostSet.setFixedWidth(600)
        self.scroll.setMaximumHeight(600)
        self.scroll.setMinimumHeight(430)
        

       
    
    def _initLayout(self):
        """ initialize layout"""
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        """ add widget to layout """
        self.layout.addWidget(self.header, stretch= 1, alignment=Qt.AlignmentFlag.AlignHCenter
                                                    |Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(self.caption,alignment=Qt.AlignmentFlag.AlignLeft)
        self.caption.setContentsMargins(80,0,0,0)
        self.layout.addWidget(self.scroll,stretch = 7, alignment=Qt.AlignmentFlag.AlignHCenter
                                                    |Qt.AlignmentFlag.AlignTop)
        
       
    