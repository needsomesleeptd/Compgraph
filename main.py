import sys
from PyQt5 import QtWidgets, QtGui, QtCore,uic
from PyQt5.QtCore import Qt
import layaout
from PyQt5.QtWidgets import QMessageBox


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
        self.show()

    def show_message(self,title,message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(title)
        msg.setInformativeText(message)
        msg.setWindowTitle("Error")
        msg.exec_()

    def revert_state(self):
        state = self.ui.canvas.state_saver.pop_state() #cur_nodes graph colors
        if (state != None):
            print(state)
            self.ui.canvas.graphs = state[1]
            self.ui.canvas.cur_nodes = state[0]
            self.ui.canvas.colors = state[2]
            self.ui.canvas.redraw_everything()



        #Todo:add warnings + checks and popups
        #Todo:add removing and moving dots
        #Todo: test on bigger graphs
        #Todo:think about the same dot
        #Todo: add saving dots





if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = UI()
    sys.exit(app.exec())
