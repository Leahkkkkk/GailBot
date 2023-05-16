'''
File: InstructionPop.py
Project: GailBot GUI
File Created: 2022/10/
Author: Siara Small  & Vivian Li
-----
Last Modified:2023/04/30
Modified By:  Siara Small  & Vivian Li
-----
Description:  implement the instruction pop up that display the instruction
'''
import os
import logging


from ..config.Style import STYLE_DATA, FontSource
from .Label import Label
from view.widgets.Background import initPrimaryColorBackground
from PyQt6.QtWidgets import QLabel, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt 
from config_frontend import PROJECT_ROOT

class Instruction(QWidget):
    def __init__(
        self, text:str) -> None:
        super().__init__()
        label = Label(
            text, STYLE_DATA.FontSize.INSTRUCTION_CAPTION)
        label.setContentsMargins(20,20,20,20)
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.addWidget(
            label, alignment=Qt.AlignmentFlag.AlignHCenter)
        initPrimaryColorBackground(self)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint)
        self.setStyleSheet("{border-radius: 40px; border: 2px solid black}")