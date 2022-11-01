import tomli


from view.widgets import SideBar, SettingForm,  Label, Button
from view.style.Background import initBackground
from view.style.styleValues import FontFamily, FontSize
from view.Text.LinkText import Links
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QStackedWidget, QSpacerItem
from PyQt6.QtCore import QSize, Qt

bottom = Qt.AlignmentFlag.AlignBottom
class SystemSettingPage(QWidget):
    """ post-transcription settings page """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        initBackground(self)
        self._initConfig()
        self.data = self.config["system setting form"]
        self._initWidget()
        self._initLayout()
        self._initStyle()
        
    def _initWidget(self):
        """initialize widgets"""
        self.sidebar = SideBar.SideBar()
        header = "System Setting"
        caption = "These settings are applied for system setting"
        self.Mainstack = QStackedWidget()
        self.SysSet = SettingForm.SettingForm(header, self.data, caption)
        self.Mainstack.addWidget(self.SysSet)
        self.GuideLink = Label.Label(Links.guideLink, FontSize.LINK, link=True)
        self.cancelBtn = Button.BorderBtn(
            "Cancel", 
            self.config["colors"]["ORANGE"])
        self.saveBtn = Button.ColoredBtn(
            "Save and Exit", 
            self.config["colors"]["GREEN"])
        
        self.sidebar.addStretch()
        self.sidebar.addWidget(self.saveBtn)
        self.sidebar.addWidget(self.cancelBtn)
        self.sidebar.addStretch()
        self.sidebar.addWidget(self.GuideLink, alignment=bottom)
        
        
    def _initLayout(self):
        """ initialize layout"""

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0,0,0,0)
        self.horizontalLayout.setSpacing(0)
        
        self.setLayout(self.horizontalLayout)
        """ add widget to layout """
        self.horizontalLayout.addWidget(self.sidebar)
        self.horizontalLayout.addWidget(self.Mainstack)

    def _initStyle(self):
        self.Mainstack.setObjectName("sysForm")
        """ add this to an external stylesheet"""
        self.Mainstack.setStyleSheet("#sysForm {border: none; border-left:0.5px solid grey;}")
   
    def setValue(self, values:dict):
        self.SysSet.setValue(values)
    
    def getValue(self) -> dict:
        return self.SysSet.getValue()

        
    def _initConfig(self):
        with open("controller/interface.toml", mode="rb") as fp:
            self.config = tomli.load(fp)
    