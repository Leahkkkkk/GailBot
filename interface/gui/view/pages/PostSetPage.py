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

from view.widgets import InputBox, Button, ToggleView

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout


class PostSetPage(QWidget):
    """ post-transcription settings page """
    def __init__(self,data, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.data = data
        self.generallist = dict()
        self.onandOfflist = dict()
        self.microBoundlist = dict()
        self.laghter = True
        self._initWidget()
        self._initLayout()
        
    def _initWidget(self):
        """initialize widgets"""
        self.header = QLabel("Post Transcription Setting")
        self.label0 = QLabel("General Setting")
        for item in self.data["General"]:
            newInput = InputBox.InputBox(item)
            self.generallist[item] = newInput
        self.label1 = QLabel("Laughter Settings")
        self.laughtherSetting = QWidget()
        laughterSectionLayout = QVBoxLayout()
        self.laughtherSetting.setLayout(laughterSectionLayout)
        self.laughterProbability= InputBox.InputBox("Laughter Probability - Lower Bound")
        self.laughterLength = InputBox.InputBox("Laughter Length")
        laughterSectionLayout.addWidget(self.laughterProbability)
        laughterSectionLayout.addWidget(self.laughterLength)
        self.LaughterToggle = Button.onOffButton("Laughter Detection Mode",
                                                self.laughtherSetting)
        self.label2 = QLabel("MicroPause Bound")
        for item in self.data["MicroPause Bound"]:
            newInput = InputBox.InputBox(item)
            self.microBoundlist[item]= newInput
            
        self.label3 = QLabel("Transcription Module")
        for item in self.data["Transcription Model"]:
            newOnandOff = Button.onOffButton(item)
            self.onandOfflist[item] = newOnandOff
    
    
    def _initLayout(self):
        """ initialize layout"""
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        """ add widget to layout """
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.label0)
        for item in self.generallist.values():
            self.layout.addWidget(item)


    