
from PyQt5 import QtWidgets, QtGui,QtCore
class Canvas(QtWidgets.QFrame):
    def __init__(self,qtwidget):
        super().__init__(qtwidget)
        self.points = QtGui.QPolygon()
        self.setStyleSheet("border: 4px solid rgb(0, 0, 0);")

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
