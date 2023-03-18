import sys
from PyQt5 import QtWidgets, QtGui, QtCore,uic
from PyQt5.QtCore import Qt
import layout
from PyQt5.QtWidgets import QMessageBox
from drawing_algorithms import *




class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = layout.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.draw_line_button.pressed.connect(self.processCanvasLine)
        self.ui.Brez_algo_float_button.pressed.connect(self.processBrezAlgo)
        self.connectColorButton(self.ui.red_color_button)
        self.connectColorButton(self.ui.blue_color_button)
        self.connectColorButton(self.ui.green_color_button)


        self.show()

    def connectColorButton(self, button):
        button.pressed.connect((lambda: self.changeCanvasLineColor(button)))



    def processCanvasLine(self):
        x0 = self.ui.X0.value()
        y0 = self.ui.Y0.value()
        x1 = self.ui.X1.value()
        y1 = self.ui.Y1.value()
        self.ui.canvas.drawLine(x0, y0, x1, y1)

    def processBrezAlgo(self):
        x0 = int(self.ui.X0.value())
        y0 = int(self.ui.Y0.value())
        x1 = int(self.ui.X1.value())
        y1 = int(self.ui.Y1.value())
        points = bresenhamAlogorithmFloat(x0,y0,x1,y1)
        self.ui.canvas.drawLineByPoints(points)


    def changeCanvasLineColor(self, button):
        button_color = button.palette().window().color()
        self.ui.canvas.changePenColor(button_color)



    def about_author_message(self):
        title = "Об авторе"
        text = "Данная работа была выполнена студентом Разиным Андреем группы ИУ7-44Б\n\n" \
               "Если бы он знал о polygon его жизнь была бы проще"
        self.show_message(title,text)


    def about_program_message(self):
        title = "О программе"
        text = "Цель работы: Найти два подобных N-угольника, где N – максимально возможное."\
                "Многоугольники задаются на плоскости координатами вершин контуров. Вершины "\
                "в контуре перечисляются в порядке обхода против часовой стрелки. Считать, что "\
                "две величины равны с точностью до двух знаков после запятой."\
                "\n\n"\
                "Будем называть два многоугольника подобными, если существует взаимно"\
                         "однозначное отображение сторон этих двух фигур такое, что соответствующие "\
                         "стороны пропорциональны с коэффициентом пропорциональности k, а углы, "\
                         "образованные двумя соответствующими сторонами, равны."\
                "\n\n"\
                "Замечания по работе программы:\n"\
                "   1.Постановка точек на канвасе происходит при нажатии ПКМ\n"\
                "   2.Удаление точек на канвасе происходит при нажатии средней кнопки мыши(колесика)\n"\
                "   3.Для перемещения точки на канвасе необходимо дважды нажать на нее ЛКМ(расстояние от курсора до " \
               "точки должно быть <=0.1 единиц длины по канвасу), а затем дважды кликнуть нажатия на точку для ее " \
               "перемещения\n"\
                "   4.Возврат  состояний осуществляется <=5 раз\n" \
                "   5.Строка для ввода служит для ввода координат вершин многоугольников  в порядке их обхода и поддерживает формат ввода координат в скобках с пробелами\n"\
                "Пример:(0,1) (1,0) (1,1)"\
                "   Конечные и начальные координаты точек объеденятся автоматически\n"\
                "   6.В случае введения невалидных многоугольников поведелние программы не определено\n" \





        self.show_message(title, text)

    def show_message(self,title,message):
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