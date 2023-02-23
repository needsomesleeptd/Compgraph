
import sys
import numpy as np

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import Qt


def is_float(string:str):
    string = string.replace(".","",1)
    string = string.replace("-", "", 1)
    if (string.isnumeric()):
        return True
    else:
        return False



class Input_line(QtWidgets.QLineEdit):
    iscompletedSignal = QtCore.pyqtSignal(list)
    def __init__(self,parent):
        super().__init__(parent)
        self.returnPressed.connect(self.get_nodes)


    def get_nodes(self): # valid : (%d,%d) ($d,%d)
        text = self.text()
        print(text)
        nodes_float = []
        nodes_str = text.split(' ')
        if (len(nodes_str) < 3):
            return None
        else:
            for node_str in nodes_str:
                if (node_str.count('(') != 1 and node_str.count(')') != 1):
                    return None
                if (node_str.count(',') != 1):
                    return None
                coords = node_str.split(',')
                x_str = coords[0][1:]
                y_str = coords[1][:len(coords[1]) - 1]
                if is_float(x_str) and is_float(y_str):
                    nodes_float.append([float(x_str),float(y_str)])

        self.iscompletedSignal.emit(nodes_float)


                        
                        
                        




