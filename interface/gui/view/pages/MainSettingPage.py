from view.pages import SettingPage, SystemSettingPage

from PyQt6.QtWidgets import QTabWidget
class MainSettingPage(QTabWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.SettingPage = SettingPage.SettingPage()