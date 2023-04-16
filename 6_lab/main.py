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

        self.ui.place_dot.clicked.connect(self.place_dot_by_value)

        self.ui.revert.clicked.connect(self.revert_state)

        self.ui.about_creator.triggered.connect(self.about_author_message)
        self.ui.about_programm.triggered.connect(self.about_program_message)

        update_widget_by_Qcolor(self.ui.border_color_display, self.ui.canvas.pen.color())
        update_widget_by_Qcolor(self.ui.fill_color_display, self.ui.canvas.fill_color)

        self.show()

    def place_dot_by_value(self):
        x = self.ui.place_dot_x.value()
        y = self.ui.place_dot_y.value()
        self.ui.canvas.add_dot(QtCore.QPointF(x, y))

    def fill_by_seed(self):
        if (len(self.ui.canvas.cur_polygon) != 0):
            self.show_message("Многоугольник не завершен","В случае если многоугольник не будет замкнутым, возможно неверное закрашивание фигуры")
            return
        delay = self.ui.delay.value()
        self.ui.canvas.fill_seed(delay)

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

    def revert_state(self):
        if (self.ui.canvas.saved_state[0] != None):
            self.ui.canvas.image = self.ui.canvas.saved_state[0].copy()
            self.ui.canvas.polygons =  self.ui.canvas.saved_state[1].copy()
            self.ui.canvas.cur_polygon = self.ui.canvas.saved_state[2].copy()
            self.ui.canvas.seed_point = self.ui.canvas.saved_state[3].copy()
            self.ui.canvas.saved_state[0] = None
            self.ui.canvas.updatePixmap(is_reverting=True)
            self.ui.table_points.create_from_canvas(self.ui.canvas.polygons + [self.ui.canvas.cur_polygon])



    def about_program_message(self):
        title = "О программе"
        text = 'Данная программа позволяет заполнить многоугольники с помощью алгоритма закраски с затравкой' \
               ''' , а также сравнить скорость данного заполнения с растровым алгоритмом закраски с флагом
                   \n\n''' \
               "Замечания по работе программы:\n" \
               "   1. На колесико мыши ставится затравочная точка\n" \
               "   2. На левую кнопку мыши происходит построение самого многоугольника, замыкание происходит на правую кнопку мыши\n" \
               "   3. на колесико мыши есть возможность зума для детального рассмотра изображения"

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
