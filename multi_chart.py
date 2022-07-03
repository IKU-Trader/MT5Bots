# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 09:38:11 2022

@author: docs9
"""

import sys
from PyQt5 import QtWidgets
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QMainWindow, QSizePolicy
from CandlePlotWidget import CandlePlotWidget
import FinanceDataReader as fdr


from gui.multi_chart_design import Ui_MainWindow

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
        self.market1 = []
        for i in range(4):
            candle_plot = CandlePlotWidget()
            self.verticalLayout_market1.addWidget(candle_plot)
            self.market1.append(candle_plot)
            
        self.pushButton_draw.clicked.connect(self.plot)

    def plot(self):
        print('clicked')
        market = 'AAPL'
        df = fdr.DataReader(market, '2020')
        t = timestampArray(df)
        o = list(df['Open'])
        h = list(df['High'])
        l = list(df['Low'])
        c = list(df['Close'])    
        for plot in self.market1:      
            plot.setTitle(market)
            plot.draw([t, o, h, l, c])

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
