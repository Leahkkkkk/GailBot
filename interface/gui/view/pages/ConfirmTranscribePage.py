"""
File: ConfirmTranscribePage.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 11:05:38 am
Modified By:  Siara Small  & Vivian Li
-----
Description: implementation of Confirm Transcription Page
"""
from view.config.Style import FileTableDimension, FontFamily, STYLE_DATA

from view.config.Text import ConfirmTranscribeText as Text
from view.config.Text import FileTableHeader
from view.config.InstructionText import INSTRUCTION
from gbLogger import makeLogger
from view.signal.signalObject import FileSignal, GBTranscribeSignal
from view.signal.Request import Request
from view.pages.BasicPage import BasicPage
from view.widgets import Label, ColoredBtn
from view.components.FileTable import SourceTable, TableWidget, DATA_FIELD
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt

center = Qt.AlignmentFlag.AlignHCenter
top = Qt.AlignmentFlag.AlignTop
right = Qt.AlignmentFlag.AlignRight


class ConfirmTranscribePage(BasicPage):
    """Confirm transcription page"""

    def __init__(self, *args, **kwargs) -> None:
        """initializes page"""
        self.pageInstruction = INSTRUCTION.CONFIRM_INS
        super().__init__(*args, **kwargs)
        self.signal = FileSignal
        self.logger = makeLogger("F")
        self._initWidget()
        self._initLayout()
        self._connectSignal()

    def _connectSignal(self):
        """connects signals upon button clicks"""
        self.confirmBtn.clicked.connect(self._sendTranscribeSignal)
        GBTranscribeSignal.sendToConfirm.connect(self.fileTable.resetFileDisplay)

    def _initWidget(self):
        """initializes widgets"""
        self.logger.info("")
        self.label = Label(
            Text.confirmLabel, STYLE_DATA.FontSize.HEADER2, FontFamily.MAIN
        )
        self.label.setAlignment(center)

        self.fileTable = SourceTable(
            FileTableHeader.confirmPage,
            self.signal,
            dataKeyToCol={
                DATA_FIELD.TYPE: 0,
                DATA_FIELD.NAME: 1,
                DATA_FIELD.PROFILE: 2,
            },
            appliedCellWidget={TableWidget.PROFILE_DETAIL},
        )

        self.fileTable.resizeCol(FileTableDimension.confirmPage)
        self.bottomButton = QWidget()
        self.confirmBtn = ColoredBtn(Text.confirm, STYLE_DATA.Color.SECONDARY_BUTTON)
        self.cancelBtn = ColoredBtn(Text.cancel, STYLE_DATA.Color.CANCEL_QUIT)

    def _initLayout(self):
        """initializes layout"""
        self.logger.info("")

        self.verticalLayout = QVBoxLayout()
        self.horizontalLayout = QHBoxLayout()
        self.bottomButton.setLayout(self.horizontalLayout)
        self.setLayout(self.verticalLayout)
        """ adds widgets to layout """
        self.verticalLayout.addWidget(self.logoContainer, alignment=self.logopos)
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.fileTable, alignment=center | top)
        self.horizontalLayout.addWidget(self.confirmBtn, alignment=right)
        self.horizontalLayout.addWidget(self.cancelBtn, alignment=center)
        self.bottomButton.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.addWidget(self.bottomButton, alignment=center)
        self.horizontalLayout.setSpacing(STYLE_DATA.Dimension.LARGE_SPACING)
        self.verticalLayout.addWidget(self.instructionBtn, self.instructionBtn.defaultPos)

    def _sendTranscribeSignal(self):
        """sends a signal with a set of file keys that will be transcribed"""
        files = self.fileTable.getAllFile()
        self.logger.info(files)
        GBTranscribeSignal.transcribe.emit(
            Request(data=files, succeed=self.transcribeComplete)
        )
        GBTranscribeSignal.sendToTranscribe.emit(files)

    def transcribeComplete(self, completeData):
        GBTranscribeSignal.sendToComplete.emit(completeData)
