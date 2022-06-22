# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 09:38:11 2022

@author: docs9
"""

import sys
from PyQt5 import QtWidgets
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QMainWindow
from CandlePlotWidget import CandlePlotWidget
import FinanceDataReader as fdr

'''
from PyQt5 import uic
class GraphWindow(QtWidgets.QWidget):   
    def __init__(self, *args, **kwargs):
        super(GraphWindow, self).__init__(*args, **kwargs)
        uic.loadUi('main_ui.ui', self)
'''

from gui_test1 import Ui_MainWindow


def timestampArray(df):
    array = []
    for i in range(len(df)):
        index = df.index[i]
        array.append(index.timestamp())
    return array

class Window(QtWidgets.QMainWindow, Ui_MainWindow):   
    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)
        
        scene = QGraphicsScene()
        self.graphicsView_LT.setScene(scene)
        self.candle_plot = CandlePlotWidget()
        proxy_widget = scene.addWidget(self.candle_plot)
        
        self.pushButton.clicked.connect(self.plot)


    def plot(self):
        print('clicked')
        market = 'AAPL'
        df = fdr.DataReader(market, '2020')
        t = timestampArray(df)
        o = list(df['Open'])
        h = list(df['High'])
        l = list(df['Low'])
        c = list(df['Close'])    
        self.candle_plot.setTitle(market)
        self.candle_plot.draw([t, o, h, l, c])
        
        


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
