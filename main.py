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
        '''layout = QtWidgets.QGridLayout()
        self.canvas = Canvas()
        self.table = Table()
        self.create_button = QtWidgets.QPushButton()
        self.input_line = QtWidgets.QLineEdit(self)
        #self.input_line.setFixedWidth(100)
        self.create_button.clicked.connect(self.table.update)
        self.input_line.returnPressed.connect(self.get_text)
        layout.addWidget(self.canvas,0,0,2,1)
        layout.addWidget(self.table, 0,1,2,2,alignment=Qt.AlignLeft)
        layout.addWidget(self.input_line, 0, 1,alignment=Qt.AlignBottom | Qt.AlignLeft)
        layout.addWidget(self.create_button,1,1)
        container = QtWidgets.QWidget()
        container.setLayout(layout)
        container.resize(200, 100)
        self.setCentralWidget(container)

        self.update()
        self.show()'''

    '''def get_text(self):
        print(self.input_line.text())'''






if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = UI()
    sys.exit(app.exec())
