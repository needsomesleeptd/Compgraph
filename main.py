import sys
from PyQt5 import QtWidgets, QtGui, QtCore


class Table(QtWidgets.QTableWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["x", "y"])



class Canvas(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.points = QtGui.QPolygon()
        canvas_layout = QtWidgets.QGridLayout()
        frame = QtWidgets.QFrame()
        frame.setStyleSheet("border: 4px solid rgb(0, 0, 0);")
        frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        canvas_layout.addWidget(frame)
        self.setLayout(canvas_layout)



    def mousePressEvent(self, e):
        self.points << e.pos()
        self.update()

    def paintEvent(self, ev):
        qp = QtGui.QPainter(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        pen = QtGui.QPen(QtCore.Qt.blue, 3)
        brush = QtGui.QBrush(QtCore.Qt.red)
        qp.setPen(pen)
        qp.setBrush(brush)
        qp.drawPoints(self.points)



class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QGridLayout()
        self.canvas = Canvas()
        self.label = QtWidgets.QLabel()

        self.table = Table()
        layout.addWidget(self.canvas,0,0)
        layout.addWidget(self.table, 0,1,int(self.height() / 2),9)
        container = QtWidgets.QWidget()



        container.setLayout(layout)
        container.resize(200, 100)
        self.setCentralWidget(container)

        self.update()
        self.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = UI()
    sys.exit(app.exec())
