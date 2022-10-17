import sys

from FileTab.MainTab import ChooseFileTab
from FileTable.TableWidgets import FileTabel

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication
from PyQt6.QtCore import QSize

class Table(QWidget):
    def __init__(self):
        super().__init__()
        headers =["Select All", 
                  "Type", 
                  "Name", 
                  "Profile", 
                  "Status", 
                  "Date", 
                  "Size", 
                  "Actions"]
        data = {
                   "1": {
                        "Type": ".wav",
                        "Name": "hello.wav",
                        "Profile": "Coffee Study",
                        "Status": "Not Transcribed",
                        "Date": "10/13/2020",
                        "Size": "85mb",
                        "Output": "Desktop",
                    },
                 }
       
        self.Table =FileTabel(headers, data, parent=self)
        self.Table.resizeCol([70,70,150,150,150,80,80,200])
        self.button = QPushButton("add file")
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.layout.addWidget(self.Table)
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.Table.getFile)
        
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     example = Table()
#     example.resize(QSize(800, 500))
#     example.show()
#     sys.exit(app.exec())