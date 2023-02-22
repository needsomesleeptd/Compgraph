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




class UI(layaout.Ui_MainWindow,QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()







if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = UI()
    sys.exit(app.exec())
