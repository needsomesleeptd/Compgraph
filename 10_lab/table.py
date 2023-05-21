import sys
import numpy as np

from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
import matplotlib
from matplotlib.artist import Artist


class Table(QtWidgets.QTableWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.adjust_table()
        self.saved_state = []
    def adjust_table(self):
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(
            ["x", "y"]
        )
        self.adjustSize()

    def push_node_back(self, xdata, ydata, color, precision=3):
        ix, iy = xdata, ydata
        rowPos = self.rowCount()
        colCount = self.columnCount()
        self.insertRow(rowPos)
        self.setItem(rowPos, 0, QtWidgets.QTableWidgetItem(str(round(ix, precision))))
        self.setItem(rowPos, 1, QtWidgets.QTableWidgetItem(str(round(iy, precision))))
        self.item(rowPos, 0).setBackground(color)
        self.item(rowPos, 1).setBackground(color)



    def update_to_canvas(self, graphs: list, color):
        for graph in graphs:
            for dot in graph:
                self.push_node_back(*dot,color)

    def highlight_rows(self, rows_indexes: list):
        for row_index in rows_indexes:
            for col_index in range(self.columnCount()):
                self.item(row_index, col_index).setSelected(True)

    def clearContents(self) -> None:
        super().clearContents()
        self.setRowCount(0)

    def add_to_table(self, graphs: list, color):
        self.update_to_canvas(graphs, color)

    def pop_node_from_table(self, index):
        self.model.removeRow(index)

    def add_graph_to_table(self, graph: list, color):
        for node in graph:
            self.push_node_back(node[0], node[1], color)
