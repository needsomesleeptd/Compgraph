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
