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


        self.ui.measurements_time.triggered.connect(lambda : plot_bars_timing())
        self.ui.measurements_steps.triggered.connect(lambda : plot_graph_steps())

        self.ui.draw_ellipse_button.clicked.connect(self.processElllipse)
        self.ui.draw_circle_button.clicked.connect(self.processCircle)
        self.ui.draw_circle_spectre_button.clicked.connect(self.processSpectreCircle)

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
        y0 = self.ui.Yc.value()
        method = self.cur_method + "Ellipse"
        req = request([x0, y0], method, self.ui.canvas)
        req.setEllipseDim(A_ellipse,B_ellipse)
        handle_request(req)

    def processCircle(self):
        x0 = int(self.ui.Xc.value())
        y0 = ceil(self.ui.Yc.value())
        R = ceil(self.ui.Radius.value())

        method = self.cur_method + "Circle"
        req = request([x0, y0], method, self.ui.canvas)
        req.setR(R)

        handle_request(req)

    def processSpectreCircle(self):
        x0 = int(self.ui.Xc.value())
        y0 = ceil(self.ui.Yc.value())
        R = ceil(self.ui.Radius.value())

        spectre_step = self.ui.spectre_step.value()
        spectre_elem_count = self.ui.spectre_elem_count.value()
        method = self.cur_method + "Circle"
        req = request([x0, y0], method, self.ui.canvas)
        req.setR(R)
        req.setSpectreParams(spectre_step,spectre_elem_count)
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
               "Если бы он знал о polygon его жизнь была бы проще"
        self.show_message(title, text)




    def about_program_message(self):
        title = "О программе"
        text = "Цель работы: Найти два подобных N-угольника, где N – максимально возможное." \
               "Многоугольники задаются на плоскости координатами вершин контуров. Вершины " \
               "в контуре перечисляются в порядке обхода против часовой стрелки. Считать, что " \
               "две величины равны с точностью до двух знаков после запятой." \
               "\n\n" \
               "Будем называть два многоугольника подобными, если существует взаимно" \
               "однозначное отображение сторон этих двух фигур такое, что соответствующие " \
               "стороны пропорциональны с коэффициентом пропорциональности k, а углы, " \
               "образованные двумя соответствующими сторонами, равны." \
               "\n\n" \
               "Замечания по работе программы:\n" \
               "   1.Постановка точек на канвасе происходит при нажатии ПКМ\n" \
               "   2.Удаление точек на канвасе происходит при нажатии средней кнопки мыши(колесика)\n" \
               "   3.Для перемещения точки на канвасе необходимо дважды нажать на нее ЛКМ(расстояние от курсора до " \
               "точки должно быть <=0.1 единиц длины по канвасу), а затем дважды кликнуть нажатия на точку для ее " \
               "перемещения\n" \
               "   4.Возврат  состояний осуществляется <=5 раз\n" \
               "   5.Строка для ввода служит для ввода координат вершин многоугольников  в порядке их обхода и поддерживает формат ввода координат в скобках с пробелами\n" \
               "Пример:(0,1) (1,0) (1,1)" \
               "   Конечные и начальные координаты точек объеденятся автоматически\n" \
               "   6.В случае введения невалидных многоугольников поведелние программы не определено\n"

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
