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
        self.ui.fill_line_by_line.clicked.connect(self.DisplayIntersections)

        self.ui.change_rect_color.clicked.connect(self.changeRectLineColor)
        self.ui.change_lines_color.clicked.connect(self.changeLineColor)
        self.ui.change_intersected_lines_color.clicked.connect(self.changeCutOffColor)


        self.ui.canvas.displayRectCoordsSignal.connect(self.updateRectCoords)

        self.ui.canvas.dotsPrintSignal.connect(self.ui.table_points.push_node_back)
        self.ui.canvas.clearSignal.connect(self.ui.table_points.clearContents)

        self.ui.clear_canvas_button.clicked.connect(self.ui.canvas.clearCanvasAndData)

        self.ui.create_line.clicked.connect(self.createLineByValue)
        self.ui.create_rect.clicked.connect(self.createRectByValue)

        self.ui.revert.clicked.connect(self.revert_state)

        self.ui.about_creator.triggered.connect(self.about_author_message)
        self.ui.about_programm.triggered.connect(self.about_program_message)

        update_widget_by_Qcolor(self.ui.change_rect_color, self.ui.canvas.pen.color())
        update_widget_by_Qcolor(self.ui.change_lines_color, self.ui.canvas.line_color)
        update_widget_by_Qcolor(self.ui.change_intersected_lines_color, self.ui.canvas.cut_off_color)

        self.show()

    def updateRectCoords(self,xl,yu,xr,yd):
        self.ui.XRightRect.setValue(xr)
        self.ui.XLeftRect.setValue(xl)
        self.ui.YUpRect.setValue(yu)
        self.ui.YDownRect.setValue(yd)



    def createLineByValue(self):
        x1 = self.ui.X1Line.value()
        x2 = self.ui.X2Line.value()
        y1 = self.ui.Y1Line.value()
        y2 = self.ui.Y2Line.value()
        temp = None
        if (len(self.ui.canvas.cur_line) != 0):
            temp = self.ui.canvas.cur_line[0]
            self.ui.canvas.cur_line = []
        self.ui.canvas.add_dot_line(QPointF(x1, y1))
        self.ui.canvas.add_dot_line(QPointF(x2, y2))
        if (temp != None):
            self.ui.canvas.cur_line = [temp]

    def createRectByValue(self):
        xl = self.ui.XLeftRect.value()
        xr = self.ui.XRightRect.value()
        yd = self.ui.YDownRect.value()
        yu = self.ui.YUpRect.value()
        if len(self.ui.canvas.cur_polygon) != 0:
            self.ui.canvas.clear_cur_rect()
        self.ui.canvas.add_dot_polygon(QPointF(xl, yu))
        self.ui.canvas.add_dot_polygon(QPointF(xr, yd), skip_state=True)

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
        if (self.ui.canvas.saved_state[0] != None):
            #[self.cur_line.copy(), self.lines.copy(), self.cur_rect.copy()]
            self.ui.canvas.cur_line = self.ui.canvas.saved_state[0]
            self.ui.canvas.lines= self.ui.canvas.saved_state[1].copy()
            self.ui.canvas.cur_polygon = self.ui.canvas.saved_state[2].copy()
            self.ui.table_points.create_from_canvas(self.ui.canvas.lines + [self.ui.canvas.cur_line])
            is_intersected = self.ui.canvas.saved_state[3]
            self.ui.canvas.display_reverted_figures()



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
