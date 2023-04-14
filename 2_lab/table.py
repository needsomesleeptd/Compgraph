
import sys
import numpy as np

from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
import matplotlib
from matplotlib.artist import Artist




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
        #self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        #self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.str
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)



    def push_node_back(self,xdata,ydata):
        ix, iy = xdata, ydata
        rowPos = self.rowCount()
        colCount =self.columnCount()
        self.insertRow(rowPos)
        print(ix,iy)
        self.setItem(rowPos, 0, QtWidgets.QTableWidgetItem(str(round(ix,3))))
        self.setItem(rowPos, 1, QtWidgets.QTableWidgetItem(str(round(iy,3))))


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
                    self.setItem(node_index, col_index, QtWidgets.QTableWidgetItem(str(round(graphs[i][j][col_index],3))))
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
        self.adjust_table()









    def pop_node_from_table(self,index):
        self.model.removeRow(index)


    def add_graph_to_table(self, graph:list,color):
        for node in graph:
            self.push_node_back(node[0],node[1],color)
