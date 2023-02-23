# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(759, 589)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.canvas = Canvas(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.canvas.sizePolicy().hasHeightForWidth())
        self.canvas.setSizePolicy(sizePolicy)
        self.canvas.setMinimumSize(QtCore.QSize(300, 100))
        self.canvas.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.canvas.setFrameShadow(QtWidgets.QFrame.Raised)
        self.canvas.setObjectName("canvas")
        self.horizontalLayout.addWidget(self.canvas)
        spacerItem = QtWidgets.QSpacerItem(64, 506, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.table_nodes = Table(self.centralwidget)
        self.table_nodes.setMinimumSize(QtCore.QSize(330, 200))
        self.table_nodes.setObjectName("table_nodes")
        self.gridLayout_2.addWidget(self.table_nodes, 0, 0, 1, 1)
        self.input_line = Input_line(self.centralwidget)
        self.input_line.setObjectName("input_line")
        self.gridLayout_2.addWidget(self.input_line, 1, 0, 1, 1)
        self.delete_nodes = QtWidgets.QPushButton(self.centralwidget)
        self.delete_nodes.setObjectName("delete_nodes")
        self.gridLayout_2.addWidget(self.delete_nodes, 2, 0, 1, 1)
        self.find_similar_polygons = QtWidgets.QPushButton(self.centralwidget)
        self.find_similar_polygons.setObjectName("find_similar_polygons")
        self.gridLayout_2.addWidget(self.find_similar_polygons, 3, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout_2)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 759, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.delete_nodes.setText(_translate("MainWindow", "Удалить все точки"))
        self.find_similar_polygons.setText(_translate("MainWindow", "Найти подобные n-угольники"))
from canvas import Canvas
from input_line import Input_line
from table_nodes import Table
