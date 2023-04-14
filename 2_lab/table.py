import sys
import random
import numpy
import numpy as np

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import Qt
import matplotlib
from matplotlib.artist import Artist
from PyQt5 import QtGui
from PyQt5.QtGui import QMouseEvent

from copy import deepcopy

matplotlib.use('QT5Agg')


class Table(QtWidgets.QTableWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.setColumnCount(5)
        self.setRowCount(5)
        self.setVerticalHeaderLabels(
            ["x", "y"]
        )
        self.adjustSize()

    def add_dot(self, x, y):
        rowPos = self.rowCount()
        self.insertRow(rowPos)
        self.setItem(rowPos, 0, QtWidgets.QTableWidgetItem(str(round(x, 3))))
        self.setItem(rowPos, 1, QtWidgets.QTableWidgetItem(str(round(y, 3))))
        self.update()

    def update_to_canvas(self, polygons):
        self.clear()
        for polygon in polygons:
            for dot in polygon:
                self.add_dot(*dot)
