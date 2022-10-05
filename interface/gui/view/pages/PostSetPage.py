from PyQt6.QtWidgets import *
from view.widgets import InputBox, OnOffSelect


""" class for post-transcription settings page """
class PostSetPage(QWidget):
    """ initialize class"""
    def __init__(self,data, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.data = data
        self.generallist = dict()
        self.onandOfflist = dict()
        self.microBoundlist = dict()
        self.laghter = True
        self._initWidget()
        self._initLayout()
    """initialize widgets"""
    def _initWidget(self):
        self.header = QLabel("Post Transcription Setting")
        self.label0 = QLabel("General Setting")
        for item in self.data["General"]:
            newInput = InputBox.InputBox(item)
            self.generallist[item] = newInput
        self.label1 = QLabel("Laughter Settings")
        self.l_settings = QWidget()
        l_layout = QVBoxLayout()
        self.l_settings.setLayout(l_layout)
        self.l_probability= InputBox.InputBox("Laughter Probability - Lower Bound")
        self.l_length = InputBox.InputBox("Laughter Length")
        l_layout.addWidget(self.l_probability)
        l_layout.addWidget(self.l_length)
        self.l_toggle = OnOffSelect.OnOffSelect("Laughter Detection Mode", self.l_settings)
        self.label2 = QLabel("MicroPause Bound")
        for item in self.data["MicroPause Bound"]:
            newInput = InputBox.InputBox(item)
            self.microBoundlist[item]= newInput
            
        self.label3 = QLabel("Transcription Module")
        for item in self.data["Transcription Model"]:
            newOnandOff = OnOffSelect.OnOffSelect(item)
            self.onandOfflist[item] = newOnandOff
    """ initialize layout"""
    def _initLayout(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        """ add widget to layout """
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.label0)
        for item in self.generallist.values():
            self.layout.addWidget(item)


    