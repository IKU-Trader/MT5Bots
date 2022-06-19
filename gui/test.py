# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 09:38:11 2022

@author: docs9
"""

import sys
from PyQt5 import QtWidgets
import numpy as np
import pyqtgraph as pg

'''
from PyQt5 import uic
class GraphWindow(QtWidgets.QWidget):   
    def __init__(self, *args, **kwargs):
        super(GraphWindow, self).__init__(*args, **kwargs)
        uic.loadUi('main_ui.ui', self)
'''

from main_gui import Ui_MainWindow
class GraphWindow(QtWidgets.QMainWindow, Ui_MainWindow):   
    def __init__(self):
        super(GraphWindow, self).__init__()
        self.setupUi(self)   
        self.pushButton.clicked.connect(self.plot)


    def plot(self):
        print('clicked')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myWin = GraphWindow()
    myWin.show()
    sys.exit(app.exec_())
