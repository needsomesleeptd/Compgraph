import sys
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtCore import Qt
import layout
from PyQt5.QtWidgets import QMessageBox



class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.cur_method = "canonic"
        self.ui = layout.Ui_MainWindow()
        self.ui.setupUi(self)



        self.show()


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
