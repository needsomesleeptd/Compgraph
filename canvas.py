
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
from state_saver import StateSaver

from math_canvas import *

from copy import deepcopy,copy

class Canvas(QtWidgets.QFrame):
    mouseClickSignal = QtCore.pyqtSignal(float,float)
    displayMessageSignal = QtCore.pyqtSignal(str, str)
    getDotsSignal = QtCore.pyqtSignal(list)

    def __init__(self,parent):
        super().__init__(parent)
        self.graphs = []
        self.cur_nodes = []
        self.cmap = np.random.rand(3)
        self.drawn_lines = []
        self.node_to_remove = None
        self.fig, self.ax1 = plt.subplots()
        self.adjust_graph()
        self.state_saver = StateSaver()
        self.colors = []
        put_nodes_connection = self.fig.canvas.mpl_connect('button_press_event', self.put_node)
        highlight_nodes_connection = self.fig.canvas.mpl_connect('pick_event', self.highlight_node)
        modify_nodes_connection = self.fig.canvas.mpl_connect('button_press_event', self.modify_node)
        delete_nodes_connection = self.fig.canvas.mpl_connect('button_press_event', self.delete_node)

        self.plotWidget = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.plotWidget, parent)
        lay = QtWidgets.QGridLayout(self)
        lay.addWidget(self.plotWidget, 0, 0)
        lay.addWidget(self.toolbar, 0, 0, alignment=Qt.AlignBottom | Qt.AlignLeft)


    def adjust_graph(self):
        self.ax1.grid()
        self.ax1.set(xlabel='X-Axis', ylabel='Y-Axis',
                     xlim=(0, 12), ylim=(0, 12),
                     title='Полученные многоугольники')
        self.ax1.autoscale(enable=True, axis="x", tight=True)
        self.ax1.autoscale(enable=True, axis="y", tight=True)
    def put_node(self, event):
        if (not event.inaxes == self.ax1):  # Right mouse key
            return

        ix, iy = event.xdata, event.ydata
        if (event.button == 3):

            if (len(self.cur_nodes) > 1 and are_eq_nodes([ix,iy],self.cur_nodes[0])): #end_of_loop
                xs = [self.cur_nodes[0][0], self.cur_nodes[-1][0]]
                ys = [self.cur_nodes[0][1], self.cur_nodes[-1][1]]
                self.ax1.plot(xs, ys, marker='.', c=self.cmap, picker=True, pickradius=2)
                self.graphs.append(self.cur_nodes)
                self.cur_nodes = []
            else:
                if (find_node([ix,iy],self.cur_nodes) != None): #node_already_there
                    return
                self.cur_nodes.append([ix, iy])
                if (len(self.cur_nodes) > 1):
                    xs = [self.cur_nodes[-1][0], self.cur_nodes[-2][0]]
                    ys = [self.cur_nodes[-1][1], self.cur_nodes[-2][1]]
                    self.ax1.plot(xs, ys, marker='.', c=self.cmap,picker=True, pickradius=2)
                else:
                    self.cmap = np.random.rand(3)
                    self.colors.append(self.cmap)
                    plt.plot(self.cur_nodes[0][0], self.cur_nodes[0][1], marker='.', c=self.cmap)
                self.mouseClickSignal.emit(event.xdata, event.ydata)

            self.state_saver.push_state([copy(self.cur_nodes), deepcopy(self.graphs), copy(self.colors)])
            print("state:",self.cur_nodes, self.graphs, self.colors)
            self.fig.canvas.draw()



    def delete_node(self,event):
        ix, iy = event.xdata, event.ydata
        if (event.button == 2):
            graph_index, node_index = find_graph_node([ix, iy], self.graphs)
            if (graph_index != None):
                del self.graphs[graph_index]
                del self.colors[graph_index]
                self.state_saver.push_state([self.cur_nodes, self.graphs, self.colors])
                self.redraw_everything()

    def modify_node(self,event):
        if (event.inaxes == self.ax1 and event.button == 1 and event.dblclick):
            ix, iy = event.xdata, event.ydata
            graph_index, node_index = find_graph_node([ix, iy], self.graphs)
            if (self.node_to_remove != None):
                self.graphs[self.node_to_remove[0]][self.node_to_remove[1]] = [ix, iy]
                self.node_to_remove = None
                self.state_saver.push_state([self.cur_nodes, self.graphs, self.colors])
                self.redraw_everything()

            elif (graph_index != None):
                if (self.node_to_remove == None):
                    self.node_to_remove = [graph_index,node_index]







    def add_graph(self, polygon):
        self.graphs.append(polygon)
        self.cmap = np.random.rand(3)
        self.colors.append(self.cmap)
        self.ax1.plot(polygon[0][0], polygon[0][1], marker='.', c=self.cmap, picker=True, pickradius=2)
        for i in range(len(polygon)):
            xs = [polygon[i][0], polygon[(i + 1) % len(polygon)][0]]
            ys = [polygon[i][1], polygon[(i + 1) % len(polygon)][1]]
            self.ax1.plot(xs, ys, marker='.', c=self.cmap, picker=True, pickradius=2)
        self.getDotsSignal.emit(self.graphs)
        self.state_saver.push_state([self.cur_nodes, self.graphs, self.colors])
        self.fig.canvas.draw()

    def redraw_everything(self,new_dots = None):
        print(new_dots)
        self.ax1.clear()
        if(new_dots != None):
            self.graphs.append(new_dots)
        for index,polygon in enumerate(self.graphs):
            self.ax1.plot(polygon[0][0], polygon[0][1], marker='.', c=self.colors[index], picker=True, pickradius=2)
            for i in  range(len(polygon)):
                xs = [polygon[i][0], polygon[(i+1) % len(polygon)][0]]
                ys = [polygon[i][1], polygon[(i + 1)  % len(polygon) ][1]]
                self.ax1.plot(xs, ys, marker='.', c=self.colors[index],picker=True, pickradius=2)
        if (len(self.cur_nodes) > 0):
            self.ax1.plot(self.cur_nodes[0][0], self.cur_nodes[0][1], marker='.', c=self.cmap, picker=True, pickradius=2)
            for dot_index in  range(len(self.cur_nodes) - 1):
                    xs = [self.cur_nodes[dot_index][0], self.cur_nodes[dot_index + 1][0]]
                    ys = [self.cur_nodes[dot_index][1], self.cur_nodes[dot_index + 1][1]]
                    self.ax1.plot(xs, ys, marker='.', c=self.cmap, picker=True, pickradius=2)

        self.adjust_graph()
        self.fig.canvas.draw()
        self.getDotsSignal.emit(self.graphs)





    def find_similar_polygons(self):
        graphs_params = find_similar_graphs_with_max_nodes(self.graphs) #loop_1 loop_2 nodes_count
        if (graphs_params == None):
            print("Not found")
            self.displayMessageSignal.emit("Результат поиска подобных многоугольников", "Подобных многоугольников не найдено")
        else:
            graph_len = graphs_params[2] #to compensate for reverse node
            start_dot_first = get_dot_index(self.graphs,graphs_params[0])
            start_dot_second = get_dot_index(self.graphs, graphs_params[1])
            print(start_dot_first,start_dot_second)
            for i in range(len(self.ax1.lines)):
                print(self.ax1.lines[i].get_xdata(),self.ax1.lines[i].get_ydata())
            for line_index in range(start_dot_first,start_dot_first + graph_len):
                self.ax1.lines[line_index].set_linestyle('-.')
                self.ax1.lines[line_index].set_color('red')

            for line_index in range(start_dot_second,start_dot_second + graph_len):
                self.ax1.lines[line_index].set_linestyle('-.')
                self.ax1.lines[line_index].set_color('red')


            message = "Подобные n-угольники найдены, максимальное n - {}, их линия преобразована в штриховую".format(graphs_params[2])
            self.displayMessageSignal.emit("Результат поиска подобных многоугольников", message)
            self.state_saver.push_state([self.cur_nodes, self.graphs, self.colors])
            self.fig.canvas.draw()



    def highlight_node(self, event):
        artist = event.artist
        x_d = artist.get_xdata()
        y_d = artist.get_ydata()
        ind = event.ind
        props = {"color" : "red"}
        Artist.update(artist,props)
        print(x_d, y_d, ind)
        self.state_saver.push_state([self.cur_nodes, self.graphs, self.colors])
        self.plotWidget.draw()

    def clear_canvas(self,event):
        self.cur_nodes.clear()
        self.graphs.clear()
        self.colors.clear()
        self.state_saver.push_state([self.cur_nodes, self.graphs, self.colors])
        self.redraw_everything()

