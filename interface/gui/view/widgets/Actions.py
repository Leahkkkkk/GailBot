from view.widgets.Button import iconBtn
from view.style.styleValues import Dimension, Color

from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout

class Actions(QWidget):
    def __init__(self, *args, **kwagrs):
      super().__init__(*args, **kwagrs)
      self.setFixedSize(Dimension.ACTION)
      self.layout = QHBoxLayout(self)
      self.layout
      self.setLayout(self.layout)
      self.setBtn  = iconBtn("settings.png")
      self.deleteBtn = iconBtn("trash.png")
      self.saveBtn = iconBtn("disk.png")
      self.layout.addWidget(self.setBtn)
      self.layout.addWidget(self.deleteBtn)
      self.layout.addWidget(self.saveBtn)
      self.layout.setContentsMargins(0,0,0,0)