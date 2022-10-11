import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('QScrollArea Test')
        self.setGeometry(400, 400, 400, 800)

        formLayout = QFormLayout()
        groupBox = QGroupBox()

        for n in range(100):
            label1 = QLabel('Slime_%2d' % n)
            label2 = QLabel()
            label2.setPixmap(QPixmap('s1.png'))
            formLayout.addRow(label1, label2)

        groupBox.setLayout(formLayout)

        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)

        layout = QVBoxLayout(self)
        layout.addWidget(scroll)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())