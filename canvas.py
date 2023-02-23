
import sys
import numpy as np

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import Qt
import matplotlib
from matplotlib.artist import Artist
from PyQt5 import QtGui
from PyQt5.QtGui import QMouseEvent
matplotlib.use('QT5Agg')

import matplotlib.pylab as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


from math_canvas import *


class Canvas(QtWidgets.QFrame):
    mouseClickSignal = QtCore.pyqtSignal(float,float)
    def __init__(self,parent):
        super().__init__(parent)
        self.dots = []
        self.cur_nodes = []
        self.cmap = np.random.rand(3)
        self.fig, self.ax1 = plt.subplots()
        self.ax1.grid()
        put_nodes_connection = self.fig.canvas.mpl_connect('button_press_event', self.put_node)
        modify_nodes_connection = self.fig.canvas.mpl_connect('pick_event', self.modify_node)
        self.plotWidget = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.plotWidget, parent)
        lay = QtWidgets.QGridLayout(self)
        lay.addWidget(self.plotWidget, 0, 0)
        lay.addWidget(self.toolbar, 0, 0, alignment=Qt.AlignBottom | Qt.AlignLeft)



    def put_node(self, event):
        if (not event.inaxes == self.ax1 or event.button != 3):  # Right mouse key
            return

        ix, iy = event.xdata, event.ydata
        print(ix,iy)
        if (len(self.cur_nodes) > 1 and are_eq_nodes([ix,iy],self.cur_nodes[0])): #end_of_loop
            xs = [self.cur_nodes[0][0], self.cur_nodes[-1][0]]
            ys = [self.cur_nodes[0][1], self.cur_nodes[-1][1]]
            self.ax1.plot(xs, ys, marker='.', c=self.cmap, picker=True, pickradius=5)
            self.dots.append(self.cur_nodes)
            self.cur_nodes = []
        else:
            if (find_node([ix,iy],self.cur_nodes) != None): #node_already_there
                return
            self.cur_nodes.append([ix, iy])
            if (len(self.cur_nodes) > 1):
                xs = [self.cur_nodes[-1][0], self.cur_nodes[-2][0]]
                ys = [self.cur_nodes[-1][1], self.cur_nodes[-2][1]]
                self.ax1.plot(xs, ys, marker='.', c=self.cmap,picker=True, pickradius=5)
            else:
                self.cmap = np.random.rand(3)
                plt.plot(self.cur_nodes[0][0], self.cur_nodes[0][1], marker='.', c=self.cmap)
            self.mouseClickSignal.emit(event.xdata, event.ydata)
        self.fig.canvas.draw()

    def modify_node(self, event):
        artist = event.artist
        x_d = artist.get_xdata()
        y_d = artist.get_ydata()
        ind = event.ind
        props = {"color" : "red"}
        Artist.update(artist,props)
        print(x_d, y_d, ind)
        self.plotWidget.draw()

