"""
File: Button.py
Project: GailBot GUI
File Created: Wednesday, 5th October 2022 12:22:13 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Thursday, 6th October 2022 1:43:41 pm
Modified By:  Siara Small  & Vivian Li
-----
Description: implement reusable button widgets
"""
import os
from typing import List, Dict
from PyQt6.QtCore import QTimer
from view.config.Text import BTN_TEXT as Text
from config_frontend import PROJECT_ROOT
from view.util.ColorGenerator import colorScale
from .InstructionPop import Instruction
from .TextDisplay import TextDisplayDialog
from .Label import Label
from PyQt6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QDialog, QToolButton

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QCursor

#### controlling style changes
from view.config.Style import STYLE_DATA


class ColoredBtn(QPushButton):
    """a button widget with colored background and white button text

    Args:
        label (str): button text
        color (str): hex color in string
        fontSIze (str, optional): represented in string, unit is pixel
                                  Defaults to STYLE_DATA.FontSize.BTN.
    """

    def __init__(
        self,
        label: str,
        color: str,
        fontSIze: str = STYLE_DATA.FontSize.BTN,
        other: str = None,
        borderRadius: int = 5,
        *args,
        **kwargs,
    ):
        """"" defines and initialize classs for colored button """ ""
        super().__init__(*args, **kwargs)
        self.setText(label)
        self.origColor = color
        self.pressColor = colorScale(color, 0.7)
        self.borderRadius = borderRadius
        self.fontSIze = fontSIze
        self.other = other
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFixedSize(STYLE_DATA.Dimension.BTNWIDTH, STYLE_DATA.Dimension.BTNHEIGHT)
        self.defaultStyle = (
            f"border-radius:{self.borderRadius};"
            f"padding:1;"
            f"color:#fff;"
            f"font-size:{self.fontSIze};"
            f"{self.other};"
        )
        self.pressed.connect(self._pressStyle)
        self.released.connect(self._releaseStyle)
        self._releaseStyle()

    def _pressStyle(self):
        """sets the button color to be darker"""
        self.setStyleSheet(self.defaultStyle + f"background-color:{self.pressColor};")

    def _releaseStyle(self):
        """sets the button color to original color"""
        self.setStyleSheet(self.defaultStyle + f"background-color:{self.origColor};")

    def changeColor(self, color):
        self.origColor = color
        self.pressColor = colorScale(color, 0.7)
        self.defaultStyle = (
            f"border-radius:{self.borderRadius};"
            f"padding:1;"
            f"color:#fff;"
            f"font-size:{self.fontSIze};"
            f"{self.other};"
        )
        self._releaseStyle()

    def changeFont(self, fontsize):
        # set the updated palette to the label
        self.setStyleSheet(self.styleSheet() + f";font-size: {fontsize};")


class BorderBtn(QPushButton):
    """a button widget with colored border and text
        and white background

    Args:
        label (str): button text
        color (str): hex color in string
        fontSIze (str, optional): represented in string, unit is pixel
                                  Defaults to STYLE_DATA.FontSize.BTN
        borderRadius (int): button border
        other (str): other additional style
    """

    def __init__(
        self,
        label: str,
        color: str,
        fontSize: str = STYLE_DATA.FontSize.BTN,
        borderRadius: int = 5,
        other: str = None,
        width: int = STYLE_DATA.Dimension.BTNWIDTH,
        height: int = STYLE_DATA.Dimension.BTNHEIGHT,
        *args,
        **kwargs,
    ):
        """ "define and initialize class for border button"""
        super().__init__(*args, **kwargs)
        self.setText(label)
        self.color = color
        self.borderRadius = borderRadius
        self.fontSize = fontSize
        self.other = other
        self.setFixedSize(width, height)
        self.defaultStyle = (
            f"border: 1px solid {self.color};"
            f"color:{self.color};"
            f"border-radius:{self.borderRadius};"
            f"padding:1;"
            f"font-size:{self.fontSize};"
            f"{self.other};"
        )
        self.setDefaultStyle()
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def setDefaultStyle(self):
        """sets default style sheet"""
        self.setStyleSheet(self.defaultStyle)

    def setActiveStyle(self, color: str):
        """sets to current style sheet"""
        self.setStyleSheet(self.defaultStyle + f"background-color:{color};")

    def changeColor(self, color):
        self.color = color
        self.pressColor = colorScale(color, 0.7)
        self.defaultStyle = (
            f"border: 1px solid {self.color};"
            f"color:{self.color};"
            f"border-radius:{self.borderRadius};"
            f"padding:1;"
            f"font-size:{self.fontSize};"
            f"{self.other};"
        )
        self.setDefaultStyle()

    def addOtherStyle(self, style):
        self.other = style

    def applyOtherStyle(self):
        self.setDefaultStyle()

    def changeFont(self, fontsize=STYLE_DATA.FontSize.BTN):
        # set the updated palette to the label
        self.fontSize = fontsize
        self.defaultStyle = (
            f"border: 1px solid {self.color};"
            f"color:{self.color};"
            f"border-radius:{self.borderRadius};"
            f"padding:1;"
            f"font-size:{self.fontSize};"
            f"{self.other};"
        )
        self.setDefaultStyle()


class ToggleBtn(QPushButton):
    """A toggle button that display different label when being toggled

    Args:
        label(tuple(str), optional): the name of the icon image being displayed
        text: the text next to the icon on the toggle label
        sate: the initial state of the toggle bar, default to False
    """

    def __init__(
        self,
        label: tuple = (STYLE_DATA.Asset.rightImg, STYLE_DATA.Asset.downImg),
        text: str = "",
        state: bool = False,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.text = text
        self.setText(self.text)
        self.rightIcon = QIcon(os.path.join(PROJECT_ROOT, STYLE_DATA.Asset.rightImg))
        self.downIcon = QIcon(os.path.join(PROJECT_ROOT, STYLE_DATA.Asset.downImg))
        self.setCheckable(True)
        self.clicked.connect(self._changeSymbol)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.state = state
        self._changeSymbol()
        self.update()
        self.show()
        self.setStyleSheet(f";font-size:{STYLE_DATA.FontSize.HEADER4};")
        STYLE_DATA.signal.changeColor.connect(self.changeColor)
        STYLE_DATA.signal.changeFont.connect(self.changeFont)

    def _changeSymbol(self):
        """changes the button symbol"""
        if self.state:
            self.setIcon(self.downIcon)
        else:
            self.setIcon(self.rightIcon)
        self.state = not self.state

    def resetBtn(self):
        """reset teh button's state to initial state"""
        self.setIcon(self.rightIcon)
        self.state = True

    def changeColor(self, colormode=None):
        """change color"""
        self.rightIcon = QIcon(os.path.join(PROJECT_ROOT, STYLE_DATA.Asset.rightImg))
        self.downIcon = QIcon(os.path.join(PROJECT_ROOT, STYLE_DATA.Asset.downImg))
        self.state = not self.state
        self._changeSymbol()

    def changeFont(self, fontmode=None):
        self.setStyleSheet(
            self.styleSheet() + f";font-size: {STYLE_DATA.FontSize.HEADER4};"
        )


class IconBtn(QPushButton):
    """A button with icon
    icon (str): a string that indicate the icon file name
    label  (str, optional): the tex to be displayed on the icon
    """

    def __init__(self, icon: str, label: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        icon = QIcon(os.path.join(PROJECT_ROOT, icon))
        self.setIcon(icon)
        self.setObjectName(Text.ICON_BTN)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        if label:
            self.setText(label)

    def changeIcon(self, icon):
        icon = QIcon(os.path.join(PROJECT_ROOT, icon))
        self.setIcon(icon)


class TableBtn(QPushButton):
    def __init__(self, label=None, icon=None, iconname=None):
        super().__init__()
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        if label:
            self.setText(label)
        if icon:
            icon = QIcon(os.path.join(PROJECT_ROOT, icon))
            self.setIcon(icon)
        if iconname:
            icon = QIcon(
                os.path.join(PROJECT_ROOT, STYLE_DATA.ASSET_RAW_DICT[iconname])
            )
            self.setIcon(icon)
        self.iconname = iconname
        STYLE_DATA.signal.changeColor.connect(self.changeColor)

    def changeColor(self):
        if self.iconname:
            icon = QIcon(
                os.path.join(PROJECT_ROOT, STYLE_DATA.ASSET_RAW_DICT[self.iconname])
            )
            self.setIcon(icon)


class InstructionBtn(QToolButton):
    def __init__(self, instruction):
        super().__init__()
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.instruction = instruction
        icon = QIcon(os.path.join(PROJECT_ROOT, STYLE_DATA.Asset.info))
        self.setIcon(icon)
        self.setFixedSize(QSize(20, 20))
        self.clicked.connect(self.displayIns)
        self.setStyleSheet("border:none; background-color:none;")
        self.setIconSize(QSize(20, 20))
        self.setContentsMargins(0, 0, 0, 0)
        self.defaultPos = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignAbsolute 
        STYLE_DATA.signal.changeColor.connect(self.updateIcon)

    def displayIns(self):
        print("instruction button clicked")
        instruction = TextDisplayDialog(self.instruction)
        instruction.exec()

    def updateIcon(self):
        icon = QIcon(os.path.join(PROJECT_ROOT, STYLE_DATA.Asset.info))
        self.setIcon(icon)



class dropDownButton(QWidget):
    def __init__(
        self, label: str, textToFuns: Dict[str,callable],  *args, **kwargs
    ) -> None:
        """
            a dropdown button widget, when the button is clicked,
            there is a dropdown of a list of buttons

        Args:
            label (str): the text on the main button
            textToFuns: a mapping from button text to the function that will be 
                       called when the button is pressed
        """
        super().__init__(*args, **kwargs)
        self.buttonList = buttonList(textToFuns)
        self.btn = ColoredBtn(
            f"\u25B6 {label}",
            STYLE_DATA.Color.PRIMARY_BUTTON,
            STYLE_DATA.FontSize.SMALL,
            STYLE_DATA.StyleSheet.dropDownBtn,
        )
        self.label = label
        self.hideView = True
        self.setFixedWidth(130)
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.btn)
        self.layout.addWidget(self.buttonList)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.buttonList.hide()
        self.btn.clicked.connect(self._toggle)

    def _toggle(self):
        """change the state and the sign of the button"""
        if self.hideView == True:
            self.hideView = False
            self.buttonList.show()
            self.btn.setText(f"\u25BC {self.label}")
        else:
            self.hideView = True
            self.buttonList.hide()
            self.btn.setText(f"\u25B6 {self.label}")


""" NOTE: currently unused on the frontend interface  """


class buttonList(QWidget):
    def __init__(self, textToFuns: Dict[str, callable], *args, **kwargs) -> None:
        """a widget that implement a list of buttons

        Args:
           textToFuns: a mapping from button text to the function that will be 
                       called when the button is pressed
           
        """
        super().__init__(*args, **kwargs)
        self.btnList = []
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        for text, fun in textToFuns.items():
            newButton = ColoredBtn(
                text,
                STYLE_DATA.Color.PRIMARY_BUTTON,
                STYLE_DATA.FontSize.SMALL,
                STYLE_DATA.StyleSheet.buttonList,
            )
            newButton.clicked.connect(fun)
            self.layout.addWidget(newButton)