
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


def find_node(node_x, node_y, list_of_nodes):
    for i in range(len(list_of_nodes)):
        if (abs(node_x - list_of_nodes[i][0]) < EPS and abs(node_y - list_of_nodes[i][1]) < EPS):
            return i
    return None

class Table(QtWidgets.QTableWidget):
    def __init__(self,parent):
        super().__init__(parent)
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(
            ["x", "y"]
        )
        self.adjustSize()
        self.setSizeAdjustPolicy(self.AdjustToContents)
        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)



    def push_node_back(self,xdata,ydata):
        ix, iy = xdata, ydata
        rowPos = self.rowCount()
        self.insertRow(rowPos)
        self.setItem(rowPos, 0, QtWidgets.QTableWidgetItem(str(ix)))
        self.setItem(rowPos, 1, QtWidgets.QTableWidgetItem(str(iy)))
        self.resizeColumnToContents(0)
        self.resizeColumnToContents(1)

    def add_graph_to_table(self, graph:list):
        for node in graph:
            self.push_node_back(node[0],node[1])

