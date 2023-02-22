import sys
import numpy as np

from PyQt5 import QtCore, QtWidgets, uic
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


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('test_first.ui', self)
        # test data
        self.dots = []
        self.cur_nodes = []
        self.dots_fig_indexes = []
        self.cmap = np.random.rand(3)
        self.fig, self.ax1 = plt.subplots()
        self.ax1.grid()
        put_nodes_connection = self.fig.canvas.mpl_connect('button_press_event', self.put_node)
        modify_nodes_connection = self.fig.canvas.mpl_connect('pick_event', self.modify_node)
        self.plotWidget = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.plotWidget, self)
        lay = QtWidgets.QGridLayout(self.content_plot)
        self.table = QtWidgets.QTableWidget(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.table, 0, 1)
        lay.addWidget(self.plotWidget, 0, 0)
        lay.addWidget(self.toolbar, 0, 0, alignment=Qt.AlignBottom | Qt.AlignLeft)

    def put_node(self, event):
        if (event.inaxes == self.ax1 and event.button == 3):  # Right mouse key
            ix, iy = event.xdata, event.ydata
            if (find_node(ix,iy))
            self.cur_nodes.append([ix, iy])
            self.dots.append([ix, iy])
            if (len(self.cur_nodes) > 1):
                f = [self.cur_nodes[-1][0], self.cur_nodes[-2][0]]
                s = [self.cur_nodes[-1][1], self.cur_nodes[-2][1]]
                self.ax1.plot(f, s, marker='.', c=self.cmap, pickradius=5)
            else:
                self.cmap = np.random.rand(3)
                plt.plot(self.cur_nodes[0][0], self.cur_nodes[0][1], marker='.', c=self.cmap)
            if (abs(self.cur_nodes[0][0] - ix) < EPS and abs(self.cur_nodes[0][1] - iy)):
                f = [self.cur_nodes[0][0], self.cur_nodes[-1][0]]
                s = [self.cur_nodes[0][1], self.cur_nodes[-1][1]]
                self.ax1.plot(f, s, marker='.', c=self.cmap, picker=True, pickradius=5)
                self.dots.append(self.cur_nodes)
                self.cur_nodes = []



        self.fig.canvas.draw()

    def modify_node(self, event):
        line = event.artist
        x_d = line.get_xdata()
        y_d = line.get_ydata()
        ind = event.ind
        props = {'color':'red'}
        Artist.update(x_d[ind],props)
        x_d[ind] = event.artist
        self.fig.canvas.draw()

        '''for dot in self.dots:
            self.ax1.plot(dot[0], dot[1],'*',color = "red")'''

    '''def on_running(self, xdata, ydata):
        # Update data (with the new _and_ the old points)

        # We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()'''


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())