import sys
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtCore import Qt
import layout
from PyQt5.QtWidgets import QMessageBox

from algo_time_comparation import plot_bars_timing


def Qcolor_to_stylesheet(color):
    return '* { background-color: ' + color.name() + ' }'


def update_widget_by_Qcolor(widget, color):
    widget.setStyleSheet(Qcolor_to_stylesheet(color))


class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = layout.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.panning.clicked.connect(self.changetoPanMode)
        self.ui.dots_placement.clicked.connect(self.changetoPlaceMode)
        self.ui.fill_line_by_line.clicked.connect(self.fill_by_seed)
        self.ui.change_fill_color.clicked.connect(self.changeColorFill)
        self.ui.change_bound_color.clicked.connect(self.changeColorBound)

        self.ui.measurements_time.triggered.connect(self.show_timings)

        self.ui.canvas.dotsPrintSignal.connect(self.ui.table_points.push_node_back)
        self.ui.canvas.clearSignal.connect(self.ui.table_points.clearContents)

        self.ui.clear_canvas_button.clicked.connect(self.ui.canvas.clearCanvas)

        update_widget_by_Qcolor(self.ui.border_color_display, self.ui.canvas.pen.color())
        update_widget_by_Qcolor(self.ui.fill_color_display, self.ui.canvas.fill_color)

        self.show()

    def fill_by_seed(self):
        delay = self.ui.delay.value()
        self.ui.canvas.fill_line_by_line(delay)

    def changeColorBound(self):
        border_color = QtWidgets.QColorDialog.getColor()
        if (border_color.isValid()):
            self.ui.canvas.changePenColor(border_color)
            update_widget_by_Qcolor(self.ui.border_color_display, border_color)

    def changeColorFill(self):
        fill_color = QtWidgets.QColorDialog.getColor()
        if (fill_color.isValid()):
            self.ui.canvas.changeFillColor(fill_color)
            update_widget_by_Qcolor(self.ui.fill_color_display, fill_color)

    def changetoPanMode(self):
        self.ui.canvas.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.ui.canvas.pan_mode = True

    def changetoPlaceMode(self):
        self.ui.canvas.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        self.ui.canvas.pan_mode = False

    def clear_calnvas(self):
        self.ui.canvas.clearCanvas()

    def changeCanvasLineColor(self):
        button_color = QtWidgets.QColorDialog.getColor()
        if (button_color.isValid()):
            self.ui.canvas.changePenColor(button_color)

    def show_timings(self, count=10):
        copied_params = self.ui.canvas.get_params()
        plot_bars_timing(*copied_params)

    def about_author_message(self):
        title = "Об авторе"
        text = "Данная работа была выполнена студентом Разиным Андреем группы ИУ7-44Б\n\n" \
               "Если бы он знал о command pattern его жизнь была бы проще"
        self.show_message(title, text)

    def about_program_message(self):
        title = "О программе"
        text = 'Данная программа позволяет нарисовать спектры окружностей и эллипсов различными алгоритмами:\n' \
               ''' 
                   Каноническое уравнение X^2+Y^2=R^2
                   Параметрическое уравнение X=Rcost, Y=Rsint
                   Алгоритм Брезенхема
                   Алгоритм средней точки
                   Библиотечная функция\n
                   ''' \
               "И сравнить скорость построения фигур данными способами\n\n" \
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
