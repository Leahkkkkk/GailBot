from view.widgets import Label,TextForm, Image, SideBar
from view.style.Background import initBackground
from view.style.styleValues import FontFamily, FontSize, Color
from PyQt6.QtWidgets import QWidget, QVBoxLayout,QScrollArea
from PyQt6.QtCore import Qt


class SettingForm(QWidget):
    def __init__(self, 
                 header:str, 
                 formData: dict, 
                 caption: str = None, 
                 *args, 
                 **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.headerText = header 
        self.formData = formData
        self.captionText = caption
        self._initWidget()
        self._initLayout()
        self.setObjectName("form")
        self.setStyleSheet("#form {border:0.5px solid grey;}")


    def _initWidget(self):
        self.header = Label.Label(
            self.headerText, FontSize.HEADER2,FontFamily.MAIN)
        if self.captionText:
            self.caption = Label.Label(
                self.captionText, FontSize.DESCRIPTION, FontFamily.MAIN)
        self.setForm = TextForm.TextForm(self.formData)
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setWidget(self.setForm)
        self.scroll.setFixedWidth(650)
        self.setForm.setFixedWidth(600)
        self.scroll.setMaximumHeight(750)
        self.scroll.setMinimumHeight(550)
        initBackground(self.scroll, color = Color.BLUEWHITE)
    
    def _initLayout(self):
        """ initialize layout"""
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)
        """ add widget to layout """
        self.verticalLayout.addWidget(
            self.header, 
            alignment=Qt.AlignmentFlag.AlignHCenter)
        if self.captionText:
            self.verticalLayout.addWidget(
                self.caption,
                alignment=Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(
            self.scroll,
            alignment=Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.verticalLayout.addStretch()
    
    def setValue(self, values:dict):
        self.setForm.updateValues(values)
    
    def getValue(self) -> dict:
        return self.setForm.getValue()