import sys
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtCore import Qt
import layout
from PyQt5.QtWidgets import QMessageBox


from PyQt5.QtCore import QPoint, QPointF


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
        self.ui.change_lines_color.clicked.connect(self.changeLineColor)
        self.ui.change_intersected_lines_color.clicked.connect(self.changeCutOffColor)

        self.ui.close_polygon.clicked.connect(self.closePolygon)
        self.ui.close_cutter.clicked.connect(self.closeCutter)

        self.ui.canvas.dotsPrintSignal.connect(self.ui.table_points.push_node_back)
        self.ui.canvas.clearSignal.connect(self.ui.table_points.clearContents)

        self.ui.clear_canvas_button.clicked.connect(self.ui.canvas.clearCanvasAndData)

        self.ui.add_polygon_dot.clicked.connect(self.createPolygonDotByValue)
        self.ui.add_cutter_dot.clicked.connect(self.createCutterDotByValue)

        self.ui.revert.clicked.connect(self.revert_state)

        self.ui.about_creator.triggered.connect(self.about_author_message)
        self.ui.about_programm.triggered.connect(self.about_program_message)

        update_widget_by_Qcolor(self.ui.change_rect_color, self.ui.canvas.pen.color())
        update_widget_by_Qcolor(self.ui.change_lines_color, self.ui.canvas.line_color)
        update_widget_by_Qcolor(self.ui.change_intersected_lines_color, self.ui.canvas.cut_off_color)

        self.show()






    def createCutterDotByValue(self):
        x = self.ui.Xdot.value()
        y = self.ui.Ydot.value()
        self.ui.canvas.add_dot_polygon(QPointF(x,y),self.ui.canvas.cutter,self.ui.canvas.pen.color())

    def createPolygonDotByValue(self):
        x = self.ui.XPolygonDot.value()
        y = self.ui.YPolygonDot.value()
        self.ui.canvas.add_dot_polygon(QPointF(x, y), self.ui.canvas.polygon, self.ui.canvas.line_color)

    def closeCutter(self):
        self.ui.canvas.close_cutter(self.ui.canvas.cutter)

    def closePolygon(self):
        self.ui.canvas.close_polygon(self.ui.canvas.polygon)

    def DisplayIntersections(self):
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
        self.show_message(title, text)

    def revert_state(self):
        if (len(self.ui.canvas.saved_state) > 0):
            popped_state = self.ui.canvas.saved_state.pop()
            #[self.cur_line.copy(), self.lines.copy(), self.cur_rect.copy()]
            self.ui.canvas.cur_line = popped_state[0].copy()
            self.ui.canvas.lines= popped_state[1].copy()
            self.ui.canvas.cutter = popped_state[2].copy()
            self.ui.canvas.is_cutter_closed = popped_state[-1]
            self.ui.table_points.clearContents()
            self.ui.table_points.add_to_table([self.ui.canvas.cutter], color = self.ui.canvas.pen.color())
            self.ui.table_points.add_to_table(self.ui.canvas.lines + [self.ui.canvas.cur_line],color = self.ui.canvas.line_color)
            self.ui.canvas.display_reverted_figures()
            if popped_state[-1]:#is_closed
                self.ui.canvas.close_cutter(skip_state=True)




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
