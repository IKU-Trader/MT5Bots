# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 20:28:19 2022

@author: oIKUo
"""

import pyqtgraph
from pyqtgraph.Qt import QtWidgets
from pyqtgraph import mkQApp
from CandlePlotWidget import CandlePlotWidget
import FinanceDataReader as fdr

def timestampArray(df):
    array = []
    for i in range(len(df)):
        index = df.index[i]
        array.append(index.timestamp())
    return array
    
def createWindow(title, size=(640, 400)):
    window = QtWidgets.QMainWindow()
    window.setWindowTitle(title)
    window.resize(size[0], size[1])
    center_widget = QtWidgets.QWidget()
    window.setCentralWidget(center_widget)
    layout = QtWidgets.QVBoxLayout()
    center_widget.setLayout(layout)
    candle_plot = CandlePlotWidget()
    layout.addWidget(candle_plot)
    return window, candle_plot

def plot():
    mkQApp()
    window, candle_plot = createWindow('MarketChart')
    market = 'AAPL'
    df = fdr.DataReader(market, '2020')
    t = timestampArray(df)
    o = list(df['Open'])
    h = list(df['High'])
    l = list(df['Low'])
    c = list(df['Close'])    
    candle_plot.setTitle(market)
    candle_plot.draw([t, o, h, l, c])
    window.show()
    pyqtgraph.exec()
    
def test():
    import pyqtgraph.examples
    pyqtgraph.examples.run()
    
if __name__ == '__main__':
    #test()
    plot()