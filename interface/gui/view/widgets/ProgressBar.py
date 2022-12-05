'''
File: ProgressBar.py
Project: GailBot GUI
File Created: Sunday, 4th December 2022 12:55:30 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Sunday, 4th December 2022 1:02:53 pm
Modified By:  Siara Small  & Vivian Li
-----
'''

from util.Style import Dimension, Color

from PyQt6.QtWidgets import QSlider

DEFAULT_MAXIMUM = 100

class ProgressBar (QSlider):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimumWidth(Dimension.PROGRESSBARWIDTH)
        self.initStyle()
        self.setMaximum(100)
    
    def initStyle(self):
        self.setStyleSheet("QSlider::groove:horizontal {"
                            "border: 1px solid #bbb;"
                            f"background: {Color.PRIMARY_BUTTON};"
                            "height: 10px; border-radius: 4px;"
                            "}"
                            "QSlider::add-page:horizontal {"
                            f"background: {Color.GREYEXTRALIGHT};"
                            "border: 1px solid #777;"
                            "height: 10px; border-radius: 4px;"
                            "}"
                            "QSlider::handle:horizontal {"
                            "background: qlineargradient(x1:0, y1:0, x2:1, y2:1,stop:0 #eee, stop:1 #ccc);"
                            "border: 1px solid #777;width: 13px; margin-top: -2px; margin-bottom: -2px; border-radius: 4px;"
                            "}")
        self.setEnabled(False)
    
    def updateValue(self, value: int):
        if value >= self.maximum() // 1.5:
            self.setMaximum(int (value + 10))
        self.setValue(value)
    
    def resetRange(self):
        self.setMaximum(DEFAULT_MAXIMUM)