# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\main.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1126, 615)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.Main_Horixontal_layout = QtWidgets.QHBoxLayout()
        self.Main_Horixontal_layout.setObjectName("Main_Horixontal_layout")
        self.canvas = Canvas(self.centralwidget)
        self.canvas.setMinimumSize(QtCore.QSize(800, 0))
        self.canvas.setObjectName("canvas")
        self.Main_Horixontal_layout.addWidget(self.canvas)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.table_points = Table(self.centralwidget)
        self.table_points.setMinimumSize(QtCore.QSize(200, 0))
        self.table_points.setLineWidth(2)
        self.table_points.setMidLineWidth(2)
        self.table_points.setObjectName("table_points")
        self.table_points.setColumnCount(2)
        self.table_points.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table_points.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_points.setHorizontalHeaderItem(1, item)
        self.table_points.horizontalHeader().setVisible(True)
        self.verticalLayout.addWidget(self.table_points)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.delay = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.delay.setObjectName("delay")
        self.verticalLayout.addWidget(self.delay)
        self.change_fill_color = QtWidgets.QPushButton(self.centralwidget)
        self.change_fill_color.setObjectName("change_fill_color")
        self.verticalLayout.addWidget(self.change_fill_color)
        self.change_bound_color = QtWidgets.QPushButton(self.centralwidget)
        self.change_bound_color.setObjectName("change_bound_color")
        self.verticalLayout.addWidget(self.change_bound_color)
        self.fill_line_by_line = QtWidgets.QPushButton(self.centralwidget)
        self.fill_line_by_line.setObjectName("fill_line_by_line")
        self.verticalLayout.addWidget(self.fill_line_by_line)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.panning = QtWidgets.QRadioButton(self.centralwidget)
        self.panning.setObjectName("panning")
        self.verticalLayout.addWidget(self.panning)
        self.dots_placement = QtWidgets.QRadioButton(self.centralwidget)
        self.dots_placement.setChecked(True)
        self.dots_placement.setObjectName("dots_placement")
        self.verticalLayout.addWidget(self.dots_placement)
        self.Main_Horixontal_layout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.Main_Horixontal_layout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1126, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.measurements_time = QtWidgets.QAction(MainWindow)
        self.measurements_time.setObjectName("measurements_time")
        self.measurements_steps = QtWidgets.QAction(MainWindow)
        self.measurements_steps.setObjectName("measurements_steps")
        self.about_programm = QtWidgets.QAction(MainWindow)
        self.about_programm.setObjectName("about_programm")
        self.about_creator = QtWidgets.QAction(MainWindow)
        self.about_creator.setObjectName("about_creator")
        self.menu.addAction(self.measurements_time)
        self.menu_2.addAction(self.about_programm)
        self.menu_2.addAction(self.about_creator)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.table_points.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "x"))
        item = self.table_points.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "y"))
        self.label_2.setText(_translate("MainWindow", "Задержка(миллисек):"))
        self.change_fill_color.setText(_translate("MainWindow", "Сменить цвет закраски"))
        self.change_bound_color.setText(_translate("MainWindow", "Сменить цвет прямых"))
        self.fill_line_by_line.setText(_translate("MainWindow", "Закрасить"))
        self.label.setText(_translate("MainWindow", "Выбор операции"))
        self.panning.setText(_translate("MainWindow", "Передвижение по холсту"))
        self.dots_placement.setText(_translate("MainWindow", "Расстановка точек"))
        self.menu.setTitle(_translate("MainWindow", "Замеры"))
        self.menu_2.setTitle(_translate("MainWindow", "О создателе..."))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.measurements_time.setText(_translate("MainWindow", "Время исполнения"))
        self.measurements_steps.setText(_translate("MainWindow", "Количество ступеней"))
        self.about_programm.setText(_translate("MainWindow", "Информация о программе"))
        self.about_creator.setText(_translate("MainWindow", "Информация об авторе"))
from canvas import Canvas
from table import Table
