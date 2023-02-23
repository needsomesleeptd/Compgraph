import sys
from PyQt5 import QtWidgets, QtGui, QtCore,uic
from PyQt5.QtCore import Qt
import layaout

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
        self.ui.canvas.mouseClickSignal.connect(self.ui.table_nodes.push_node_back)
        self.ui.find_similar_polygons.clicked.connect(self.ui.canvas.find_similar_polygons)
        self.ui.input_line.iscompletedSignal.connect(self.ui.canvas.redraw_everything)
        self.ui.input_line.iscompletedSignal.connect(self.ui.table_nodes.add_graph_to_table)
        self.show()







if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = UI()
    sys.exit(app.exec())
