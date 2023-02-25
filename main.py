import sys
from PyQt5 import QtWidgets, QtGui, QtCore,uic
from PyQt5.QtCore import Qt
import layaout
from PyQt5.QtWidgets import QMessageBox

from copy import deepcopy,copy


'''class Table(QtWidgets.QTableWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(2)
        self.setRowCount(0)
        self.setHorizontalHeaderLabels(["x", "y"])
        self.setMaximumHeight(500)
        #self.sizePolicy(QtWidgets.QSizePolicy.setHorizontalPolicy())
        self.resizeColumnsToContents()

    def update(self,rows):
        for i in range(len(rows)):
            self.tableWidget.setItem(i, 0, rows[i][0])
            self.tableWidget.setItem(i, 1, rows[i][1])

'''




class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui =layaout.Ui_MainWindow()
        self.ui.setupUi(self)
         #canvas
        self.ui.canvas.mouseClickSignal.connect(self.ui.table_nodes.push_node_back)
        self.ui.find_similar_polygons.clicked.connect(self.ui.canvas.find_similar_polygons)
        self.ui.delete_nodes.clicked.connect(self.ui.canvas.clear_canvas)
        self.ui.input_line.iscompletedSignal.connect(self.ui.canvas.add_graph)
        #input_line
        #self.ui.input_line.iscompletedSignal.connect(self.ui.table_nodes.add_graph_to_table)

        self.ui.canvas.getDotsSignal.connect(self.ui.table_nodes.create_from_canvas)
        self.ui.canvas.displayMessageSignal.connect(self.show_message)
        self.ui.input_line.isNotValidCompletedSignal.connect(self.show_message)
        self.ui.revert_state_button.clicked.connect(self.revert_state)
        self.ui.about_author.triggered.connect(self.about_author_message)
        self.ui.about_program.triggered.connect(self.about_program_message)
        self.show()


    def about_author_message(self):
        title = "Об авторе"
        text = "Данная работа была выполнена студентом Разиным Андреем группы ИУ7-34Б\n\n" \
               "Если бы он знал о polygon его жизнь была бы проще"
        self.show_message(title,text)


    def about_program_message(self):
        title = "О программе"
        text = "Цель работы: Найти два подобных N-угольника, где N – максимально возможное."\
                "Многоугольники задаются на плоскости координатами вершин контуров. Вершины"\
                "в контуре перечисляются в порядке обхода против часовой стрелки. Считать, что"\
                "две величины равны с точностью до двух знаков после запятой."\
                "\n\n"\
                "Будем называть два многоугольника подобными, если существует взаимно"\
                         "однозначное отображение сторон этих двух фигур такое, что соответствующие"\
                         "стороны пропорциональны с коэффициентом пропорциональности k, а углы,"\
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
                "   6.В случае введения невалидных многоугольников поведелние программы не определено\n"




        self.show_message(title, text)

    def show_message(self,title,message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        #msg.setText(title)
        msg.setInformativeText(message)
        msg.setWindowTitle(title)
        msg.exec_()

    def revert_state(self):
        state = self.ui.canvas.state_saver.pop_state() #cur_nodes graph colors
        if (state != None):
            print("using state",state)
            self.ui.canvas.cur_nodes = copy(state[0])
            self.ui.canvas.graphs = deepcopy(state[1])
            self.ui.canvas.colors = copy(state[2])
            self.ui.canvas.redraw_everything()
            self.ui.table_nodes.add_graph_to_table(self.ui.canvas.cur_nodes)








if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = UI()
    sys.exit(app.exec())
