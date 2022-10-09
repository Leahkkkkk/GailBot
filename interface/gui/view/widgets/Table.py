'''
File: Table.py
Project: GailBot GUI
File Created: Sunday, 9th October 2022 12:26:08 pm
Author: Siara Small  & Vivian Li
-----
Last Modified: Sunday, 9th October 2022 12:26:16 pm
Modified By:  Siara Small  & Vivian Li
-----
'''

from PyQt6.QtWidgets import QTableView, QHeaderView

class Table (QTableView):
    """"""
    def __init__(self, *args, **kwargs) -> None:
        """initialize table model from QTableView"""
        super().__init__(*args, **kwargs)
    def setRowColor(self, rowIndex, color):
        for j in range(self.columnCount()):
            self.item(rowIndex, j).setBackground(color)

class TableHeader(QHeaderView):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.set