import sys
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtCore import Qt
import layout
from PyQt5.QtWidgets import QMessageBox


from PyQt5.QtCore import QPoint, QPointF


def show_warning_message(title, message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText(title)
    msg.setInformativeText(message)
    msg.setWindowTitle('Warning')
    msg.exec_()

def show_info_message(title, message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(title)
    msg.setInformativeText(message)
    msg.setWindowTitle('Info')
    msg.exec_()


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
        self.ui.cut.clicked.connect(self.DisplayIntersections)

        self.ui.change_rect_color.clicked.connect(self.changeRectLineColor)





        self.ui.revert.clicked.connect(self.revert_state)

        self.ui.about_creator.triggered.connect(self.about_author_message)
        self.ui.about_programm.triggered.connect(self.about_program_message)

        update_widget_by_Qcolor(self.ui.change_rect_color, self.ui.canvas.pen.color())

        self.ui.XSlider.valueChanged.connect(self.DisplayIntersections)
        self.ui.YSlider.valueChanged.connect(self.DisplayIntersections)
        self.ui.ZSlider.valueChanged.connect(self.DisplayIntersections)

        self.show()







    def get_angles(self):
        return [self.ui.XSlider.value(),self.ui.YSlider.value(),self.ui.ZSlider.value()]



    def DisplayIntersections(self):
        self.clear_calnvas()
        self.ui.canvas.angles = self.get_angles()
        self.ui.canvas.scale = self.ui.ScaleSlider.value()
        self.ui.canvas.DisplayIntersections()

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
        self.ui.canvas.clearCanvasAndData()

    def changeRectLineColor(self):
        button_color = QtWidgets.QColorDialog.getColor()
        if (button_color.isValid()):
            self.ui.canvas.changePenColor(button_color)
            update_widget_by_Qcolor(self.ui.change_rect_color, self.ui.canvas.pen.color())

    def changeLineColor(self):
        button_color = QtWidgets.QColorDialog.getColor()
        if (button_color.isValid()):
            self.ui.canvas.changeLineColor(button_color)
            update_widget_by_Qcolor(self.ui.change_lines_color, self.ui.canvas.line_color)

    def changeCutOffColor(self):
        button_color = QtWidgets.QColorDialog.getColor()
        if (button_color.isValid()):
            self.ui.canvas.changeCutOffColor(button_color)
            update_widget_by_Qcolor(self.ui.change_intersected_lines_color, self.ui.canvas.cut_off_color)


    def about_author_message(self):
        title = "Об авторе"
        text = "Данная работа была выполнена студентом Разиным Андреем группы ИУ7-44Б\n\n" \
               "Если бы он знал о command pattern его жизнь была бы проще"
        show_info_message(title, text)

    def revert_state(self):
        if (len(self.ui.canvas.saved_state) > 0):
            popped_state = self.ui.canvas.saved_state.pop()
            #[self.cur_line.copy(), self.lines.copy(), self.cur_rect.copy()]
            self.ui.canvas.polygon= popped_state[0].copy()
            self.ui.canvas.cutter = popped_state[1].copy()
            self.ui.table_points.clearContents()
            self.ui.table_points.add_to_table([self.ui.canvas.cutter], color = self.ui.canvas.pen.color())
            self.ui.table_points.add_to_table([self.ui.canvas.polygon],color = self.ui.canvas.line_color)
            self.ui.canvas.display_reverted_figures()
            self.ui.canvas.is_cutter_closed = popped_state[-2]
            self.ui.canvas.is_polygon_closed = popped_state[-1]
            if self.ui.canvas.is_cutter_closed:
                self.ui.canvas.close_cutter(skip_state=True)
            if self.ui.canvas.is_polygon_closed:
                self.ui.canvas.close_polygon(skip_state=True)

            self.update()






    def about_program_message(self):
        title = "О программе"
        text = 'Данная программа позволяет построить выпуклый отсекатель и многоугольник и выделить отсекаемые прямые\n' \
               "Замечания по работе программы:\n" \
               "   1. На правую кнопку мыши ставятся точки многоугольника\n" \
               "   2.  На правую кнопку мыши ставятся точки отсекателя\n" \
               "   3. на колесико мыши есть возможность зума для детального рассмотра изображения"

        show_info_message(title, text)




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = UI()
    sys.exit(app.exec())
