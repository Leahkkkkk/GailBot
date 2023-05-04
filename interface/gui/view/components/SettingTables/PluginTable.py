import os
from typing import List, Dict, Tuple
from view.config.Style import STYLE_DATA
from config_frontend import PROJECT_ROOT
from view.config.Text import PLUGIN_SUITE_TEXT
from view.signal.interface import DataSignal
from view.Request import Request
from view.util.ErrorMsg import ERR
from ..SettingDetail import PluginSuiteDetails
from view.widgets.MsgBox import WarnBox
from view.widgets.Table import BaseTable

from PyQt6.QtWidgets import (
    QTableWidgetItem,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtGui import QIcon


class PluginTable(BaseTable):
    def __init__(self, signal: DataSignal):
        super().__init__(PLUGIN_SUITE_TEXT.TABLE_HEADER)
        self.signal = signal
        self.dataKeyToCol = {"Author": 1, "Version": 2}
        self.resizeCol(PLUGIN_SUITE_TEXT.TABLE_DIMENSION)

    def addItem(self, suiteInfo: Tuple[str, Dict[str, str], str]):
        self.logger.info(suiteInfo)
        suiteName, metadata, isOfficial = suiteInfo
        super().addItem((suiteName, metadata), isOfficial=isOfficial)
        try:
            if isOfficial:
                self.nameToTablePins[suiteName].setIcon(
                    QIcon(os.path.join(PROJECT_ROOT, STYLE_DATA.Asset.pluginBadge))
                )
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.ERR_WHEN_DUETO.format("uploading plugin suite", str(e)))

    def addCellWidgets(self, suiteName: str, row: int, isOfficial: bool = False):
        cellWidget = QWidget()
        layout = QHBoxLayout()

        cellWidget.setLayout(layout)
        layout.addWidget(self.getViewSourceBtn(suiteName))
        layout.addWidget(self.getViewDetailBtn(suiteName))
        if not isOfficial:
            layout.addWidget(self.getRemoveBtn(suiteName))
        self.setCellWidget(row, self.actionWidgetCol, cellWidget)

    def viewDetailRequest(self, suiteName: str):
        self.signal.detailRequest.emit(
            Request(data=suiteName, succeed=self.displayPluginSuiteDetail)
        )

    def displayPluginSuiteDetail(self, suiteInfo) -> None:
        """
        open a frontend dialog to display suiteInfo
        """
        try:
            display = PluginSuiteDetails(suiteInfo)
            display.exec()
        except Exception as e:
            self.logger.error(e, exc_info=e)
            WarnBox(ERR.FAIL_TO.format("display plugin suite detail"))
