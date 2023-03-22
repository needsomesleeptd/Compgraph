import sys
from PyQt5 import QtWidgets, QtGui, QtCore,uic
from PyQt5.QtCore import Qt
import layout
from PyQt5.QtWidgets import QMessageBox
from drawing_algorithms import *

from controller import *



class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.cur_method = "brezFloat"
        self.ui = layout.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.draw_line_button.pressed.connect(self.processLine)
        self.ui.choose_background_colors_button.pressed.connect(self.changeCanvasBackGroundColor)

        self.ui.brez_int.pressed.connect(lambda :self.changeAlgotype("brezInt"))
        self.ui.brez_float.pressed.connect(lambda: self.changeAlgotype("brezFloat"))
        self.ui.brez_smooth.pressed.connect(lambda: self.changeAlgotype("brezSmooth"))
        self.ui.standard.pressed.connect(lambda : self.changeAlgotype("defaultAlgo"))

        self.ui.draw_spectre.clicked.connect(self.processSpectre)


        self.ui.choose_colors_button.clicked.connect(self.changeCanvasLineColor)

        self.show()



    def changeAlgotype(self,algo_type:str):
        self.cur_method = algo_type

    def processSpectre(self):
        min_angle = self.ui.sprectre_angle_val.value()
        lines_len  = self.ui.spectre_line_len.value()
        method = self.cur_method+"Spectre"
        req = request(None, method, self.ui.canvas)
        req.setMinAngle(min_angle)
        req.setSpectreLen(lines_len)
        handle_request(req)
    def processLine(self):
        x0 = self.ui.X0.value()
        y0 = self.ui.Y0.value()
        x1 = self.ui.X1.value()
        y1 = self.ui.Y1.value()
        req = request([x0,y0,x1,y1],self.cur_method,self.ui.canvas)
        handle_request(req)





    def changeCanvasBackGroundColor(self):
        background_color = QtWidgets.QColorDialog.getColor()
        if (background_color.isValid()):
            brush = QtGui.QBrush(background_color)
            self.ui.canvas.setBackgroundBrush(brush)
    def changeCanvasLineColor(self):
        button_color = QtWidgets.QColorDialog.getColor()
        if (button_color.isValid()):
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