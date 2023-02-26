
import sys
import numpy as np

from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
import matplotlib
from matplotlib.artist import Artist

matplotlib.use('QT5Agg')

import matplotlib.pylab as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

EPS = 1e-1

from math_canvas import are_eq_nodes

def find_node(node_x, node_y, list_of_nodes):
    for i in range(len(list_of_nodes)):
        if (abs(node_x - list_of_nodes[i][0]) < EPS and abs(node_y - list_of_nodes[i][1]) < EPS):
            return i
    return None

class Table(QtWidgets.QTableWidget):
    def __init__(self,parent):
        super().__init__(parent)
        self.adjust_table()


    def adjust_table(self):
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(
            ["x", "y"]
        )
        self.adjustSize()
        self.setSizeAdjustPolicy(self.AdjustToContents)
        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    def push_node_back(self,xdata,ydata,color):
        ix, iy = xdata, ydata
        rowPos = self.rowCount()
        colCount =self.columnCount()
        self.insertRow(rowPos)
        self.setItem(rowPos, 0, QtWidgets.QTableWidgetItem(str(ix)))
        self.setItem(rowPos, 1, QtWidgets.QTableWidgetItem(str(iy)))
        for i in range(colCount):
            color_table = QtGui.QColor()
            color_table.setRgbF(*color)
            self.item(rowPos, i).setBackground(color_table)
            self.resizeColumnToContents(i)

    def update_to_canvas(self,graphs:list,colors:list):
        rowPos = self.rowCount()
        dots_count = 0
        for graph in graphs:
            dots_count += len(graph)

        while (rowPos < dots_count):
            self.insertRow(rowPos)
            rowPos += 1


        while (rowPos > dots_count):
            self.removeRow(rowPos - 1)
            rowPos -= 1
        node_index = 0
        for i in range(len(graphs)):
            for j in range(len(graphs[i])):
                for col_index in range(self.columnCount()):
                    self.setItem(node_index, col_index, QtWidgets.QTableWidgetItem(str(graphs[i][j][col_index])))
                    color_table = QtGui.QColor()
                    color_table.setRgbF(*colors[i])
                    self.item(node_index, col_index).setBackground(color_table)
                node_index += 1

    def highlight_rows(self,rows_indexes:list):
        for row_index in rows_indexes:
            for col_index in range(self.columnCount()):
                self.item(row_index,col_index).setSelected(True)


    def create_from_canvas(self,graphs:list,colors:list):
        self.clear()
        self.setRowCount(0)
        self.update_to_canvas(graphs,colors)









    def pop_node_from_table(self,index):
        self.model.removeRow(index)


    def add_graph_to_table(self, graph:list,color):
        for node in graph:
            self.push_node_back(node[0],node[1],color)
