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
        MainWindow.resize(1214, 816)
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
        self.Main_Vertical_Layout = QtWidgets.QVBoxLayout()
        self.Main_Vertical_Layout.setObjectName("Main_Vertical_Layout")
        self.draw_spectre = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.draw_spectre.setFont(font)
        self.draw_spectre.setObjectName("draw_spectre")
        self.Main_Vertical_Layout.addWidget(self.draw_spectre)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.Label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.Label.setFont(font)
        self.Label.setObjectName("Label")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.Label)
        self.sprectre_angle_val = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.sprectre_angle_val.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.sprectre_angle_val.setFont(font)
        self.sprectre_angle_val.setMinimum(1.0)
        self.sprectre_angle_val.setMaximum(360.0)
        self.sprectre_angle_val.setObjectName("sprectre_angle_val")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.sprectre_angle_val)
        self.Label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.Label_2.setFont(font)
        self.Label_2.setObjectName("Label_2")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.Label_2)
        self.spectre_line_len = QtWidgets.QDoubleSpinBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.spectre_line_len.setFont(font)
        self.spectre_line_len.setMinimum(1.0)
        self.spectre_line_len.setMaximum(1000.0)
        self.spectre_line_len.setObjectName("spectre_line_len")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.spectre_line_len)
        self.xcLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.xcLabel.setFont(font)
        self.xcLabel.setObjectName("xcLabel")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.xcLabel)
        self.Xc = QtWidgets.QDoubleSpinBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.Xc.setFont(font)
        self.Xc.setMinimum(-500.0)
        self.Xc.setMaximum(500.0)
        self.Xc.setObjectName("Xc")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.Xc)
        self.ycLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.ycLabel.setFont(font)
        self.ycLabel.setObjectName("ycLabel")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.ycLabel)
        self.Yc = QtWidgets.QDoubleSpinBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.Yc.setFont(font)
        self.Yc.setMinimum(-500.0)
        self.Yc.setMaximum(500.0)
        self.Yc.setObjectName("Yc")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.Yc)
        self.Main_Vertical_Layout.addLayout(self.formLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.choose_colors_button = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.choose_colors_button.setFont(font)
        self.choose_colors_button.setObjectName("choose_colors_button")
        self.verticalLayout.addWidget(self.choose_colors_button)
        self.choose_background_colors_button = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.choose_background_colors_button.setFont(font)
        self.choose_background_colors_button.setObjectName("choose_background_colors_button")
        self.verticalLayout.addWidget(self.choose_background_colors_button)
        self.clear_canvas = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.clear_canvas.setFont(font)
        self.clear_canvas.setObjectName("clear_canvas")
        self.verticalLayout.addWidget(self.clear_canvas)
        self.revert = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.revert.setFont(font)
        self.revert.setObjectName("revert")
        self.verticalLayout.addWidget(self.revert)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.Main_Vertical_Layout.addLayout(self.verticalLayout)
        self.draw_line_button = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.draw_line_button.setFont(font)
        self.draw_line_button.setObjectName("draw_line_button")
        self.Main_Vertical_Layout.addWidget(self.draw_line_button)
        self.standard = QtWidgets.QRadioButton(self.centralwidget)
        self.standard.setObjectName("standard")
        self.Main_Vertical_Layout.addWidget(self.standard)
        self.brez_float = QtWidgets.QRadioButton(self.centralwidget)
        self.brez_float.setChecked(True)
        self.brez_float.setObjectName("brez_float")
        self.Main_Vertical_Layout.addWidget(self.brez_float)
        self.brez_int = QtWidgets.QRadioButton(self.centralwidget)
        self.brez_int.setObjectName("brez_int")
        self.Main_Vertical_Layout.addWidget(self.brez_int)
        self.brez_smooth = QtWidgets.QRadioButton(self.centralwidget)
        self.brez_smooth.setObjectName("brez_smooth")
        self.Main_Vertical_Layout.addWidget(self.brez_smooth)
        self.CDA = QtWidgets.QRadioButton(self.centralwidget)
        self.CDA.setObjectName("CDA")
        self.Main_Vertical_Layout.addWidget(self.CDA)
        self.Vu = QtWidgets.QRadioButton(self.centralwidget)
        self.Vu.setObjectName("Vu")
        self.Main_Vertical_Layout.addWidget(self.Vu)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.xLineBeginLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.xLineBeginLabel.setFont(font)
        self.xLineBeginLabel.setObjectName("xLineBeginLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.xLineBeginLabel)
        self.X0 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.X0.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.X0.setFont(font)
        self.X0.setMinimum(-500.0)
        self.X0.setMaximum(500.0)
        self.X0.setObjectName("X0")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.X0)
        self.x0Label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.x0Label.setFont(font)
        self.x0Label.setObjectName("x0Label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.x0Label)
        self.Y0 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.Y0.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.Y0.setFont(font)
        self.Y0.setMinimum(-500.0)
        self.Y0.setMaximum(500.0)
        self.Y0.setObjectName("Y0")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.Y0)
        self.x1Label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.x1Label_2.setFont(font)
        self.x1Label_2.setObjectName("x1Label_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.x1Label_2)
        self.X1 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.X1.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.X1.setFont(font)
        self.X1.setMinimum(-500.0)
        self.X1.setMaximum(500.0)
        self.X1.setObjectName("X1")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.X1)
        self.y1Label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.y1Label.setFont(font)
        self.y1Label.setObjectName("y1Label")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.y1Label)
        self.Y1 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.Y1.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.Y1.setFont(font)
        self.Y1.setMinimum(-500.0)
        self.Y1.setMaximum(500.0)
        self.Y1.setObjectName("Y1")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.Y1)
        self.Main_Vertical_Layout.addLayout(self.formLayout)
        self.Main_Horixontal_layout.addLayout(self.Main_Vertical_Layout)
        self.verticalLayout_2.addLayout(self.Main_Horixontal_layout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1214, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
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
        self.menu.addAction(self.measurements_time)
        self.menu.addAction(self.measurements_steps)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.draw_spectre.setText(_translate("MainWindow", "Нарисовать спектр"))
        self.Label.setText(_translate("MainWindow", "Угол между отрезками в спектре"))
        self.Label_2.setText(_translate("MainWindow", "Длина отрезка"))
        self.xcLabel.setText(_translate("MainWindow", "Xc"))
        self.ycLabel.setText(_translate("MainWindow", "Yc"))
        self.choose_colors_button.setText(_translate("MainWindow", "Выбрать цвета линий"))
        self.choose_background_colors_button.setText(_translate("MainWindow", "Изменить цвет фона"))
        self.clear_canvas.setText(_translate("MainWindow", "Очистить канвас"))
        self.revert.setText(_translate("MainWindow", "Вернуть на состояние назад"))
        self.draw_line_button.setText(_translate("MainWindow", "Нарисовать Отрезок"))
        self.standard.setText(_translate("MainWindow", "Стандартный алгоритм"))
        self.brez_float.setText(_translate("MainWindow", "Алгоритм Брезенхема"))
        self.brez_int.setText(_translate("MainWindow", "Алгоритм Брезенхема с целыми числами"))
        self.brez_smooth.setText(_translate("MainWindow", "Алгоритм Брезенхема со сглаживанием"))
        self.CDA.setText(_translate("MainWindow", "Алгоритм ЦДА"))
        self.Vu.setText(_translate("MainWindow", "Алгоритм Ву"))
        self.xLineBeginLabel.setText(_translate("MainWindow", "X0"))
        self.x0Label.setText(_translate("MainWindow", "Y0"))
        self.x1Label_2.setText(_translate("MainWindow", "X1"))
        self.y1Label.setText(_translate("MainWindow", "Y1"))
        self.menu.setTitle(_translate("MainWindow", "Замеры"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.measurements_time.setText(_translate("MainWindow", "Время исполнения"))
        self.measurements_steps.setText(_translate("MainWindow", "Количество ступеней"))
from canvas import Canvas
