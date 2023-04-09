import sys
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtCore import Qt
import layout
from PyQt5.QtWidgets import QMessageBox
from methods_comparation import *

from controller import *


class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.cur_method = "canonic"
        self.ui = layout.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.canonic.pressed.connect(lambda: self.changeAlgotype("canonic"))
        self.ui.parametric.pressed.connect(lambda: self.changeAlgotype("parametric"))
        self.ui.standard.pressed.connect(lambda: self.changeAlgotype("standard"))
        self.ui.brez.pressed.connect(lambda: self.changeAlgotype("brez"))
        self.ui.mid_point.pressed.connect(lambda: self.changeAlgotype("midPoint"))

        self.ui.measurements_time.triggered.connect(lambda: plot_graphs_timing())
        self.ui.about_creator.triggered.connect(lambda: self.about_author_message())
        self.ui.about_programm.triggered.connect(lambda: self.about_program_message())

        self.ui.draw_ellipse_button.clicked.connect(self.processElllipse)
        self.ui.draw_circle_button.clicked.connect(self.processCircle)
        self.ui.draw_circle_spectre_button.clicked.connect(self.processSpectreCircle)
        self.ui.draw_ellipse_spectre_button.clicked.connect(self.processSpectreEllipse)

        self.ui.clear_canvas.clicked.connect(self.clear_calnvas)
        self.ui.choose_colors_button.clicked.connect(self.changeCanvasLineColor)
        self.ui.choose_background_colors_button.pressed.connect(self.ui.canvas.changeCanvasBackGroundColor)
        self.ui.revert.clicked.connect(self.ui.canvas.undo_action)

        self.show()

    def changeAlgotype(self, algo_type: str):
        self.cur_method = algo_type

    def processElllipse(self):
        A_ellipse = self.ui.A_ellipse.value()
        B_ellipse = self.ui.B_ellipse.value()
        x0 = self.ui.Xc.value()
        y0 = -self.ui.Yc.value()
        method = self.cur_method + "Ellipse"
        req = request([x0, y0], method, self.ui.canvas)
        req.setEllipseDim(A_ellipse, B_ellipse)
        handle_request(req)

    def processCircle(self):
        x0 = int(self.ui.Xc.value())
        y0 = -ceil(self.ui.Yc.value())
        R = ceil(self.ui.Radius.value())

        method = self.cur_method + "Circle"
        req = request([x0, y0], method, self.ui.canvas)
        req.setR(R)

        handle_request(req)

    def processSpectreCircle(self):
        x0 = ceil(self.ui.Xc.value())
        y0 = -ceil(self.ui.Yc.value())
        R = ceil(self.ui.Radius.value())

        spectre_step = self.ui.spectre_step.value()
        spectre_elem_count = self.ui.spectre_elem_count.value()
        method = self.cur_method + "Circle"
        req = request([x0, y0], method, self.ui.canvas)
        req.setR(R)
        req.setSpectreParams(spectre_step, spectre_elem_count)
        handle_request(req)

    def processSpectreEllipse(self):
        A_ellipse = self.ui.A_ellipse.value()
        B_ellipse = self.ui.B_ellipse.value()
        x0 = self.ui.Xc.value()
        y0 = -self.ui.Yc.value()

        spectre_step_A = self.ui.A_step.value()
        spectre_step_B = self.ui.B_step.value()
        spectre_step = [spectre_step_A, spectre_step_B]
        spectre_elem_count = self.ui.spectre_elem_count.value()

        method = self.cur_method + "Ellipse"
        req = request([x0, y0], method, self.ui.canvas)
        req.setEllipseDim(A_ellipse, B_ellipse)
        req.setSpectreParams(spectre_step, spectre_elem_count)
        handle_request(req)

    def clear_calnvas(self):
        self.ui.canvas.clearCanvas()

    def changeCanvasLineColor(self):
        button_color = QtWidgets.QColorDialog.getColor()
        if (button_color.isValid()):
            self.ui.canvas.changePenColor(button_color)

    def about_author_message(self):
        title = "Об авторе"
        text = "Данная работа была выполнена студентом Разиным Андреем группы ИУ7-44Б\n\n" \
               "Если бы он знал о command pattern его жизнь была бы проще"
        self.show_message(title, text)

    def about_program_message(self):
        title = "О программе"
        text = 'Данная программа позволяет нарисовать спектры окружностей и эллипсов различными алгоритмами:\n'\
                ''' 
                    Каноническое уравнение X^2+Y^2=R^2
                    Параметрическое уравнение X=Rcost, Y=Rsint
                    Алгоритм Брезенхема
                    Алгоритм средней точки
                    Библиотечная функция\n
                    '''\
            "И сравнить скорость построения фигур данными способами\n\n"\
               "Замечания по работе программы:\n" \
               "   1.Поле `Координаты центра фигуры` определеяет центр всех спектров для построения\n" \
               "   2.Параметр A задает размер горизонтальной полуоси эллипса,параметр B задает размеры вертикальной полуоси\n" \
               "   3.Поля со словом `шаг` задают значения последовательного смещения фигур в спектре "



        self.show_message(title, text)

    def show_message(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(title)
        msg.setInformativeText(message)
        msg.setWindowTitle(title)
        msg.exec_()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = UI()
    sys.exit(app.exec())
