import sys
from PyQt5 import QtWidgets, QtGui, QtCore, uic




class Canvas(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        #uic.loadUi('gui.ui', self)
        self.setFixedSize(self.size())
        self.show()
        self.points = QtGui.QPolygon()

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


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Canvas()
    sys.exit(app.exec())
