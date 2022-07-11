# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 10:37:24 2022

@author: docs9
"""


import sys
import numpy as np
import time
import threading
import json
import pyqtgraph as pg
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QMainWindow, QSizePolicy
from pyqtgraph.Qt import QtCore, QtWidgets
from CandlePlotWidget import CandlePlotWidget
#import FinanceDataReader as fdr
from MT5Bind import *

from gui.chart_design import Ui_MainWindow


SETTING_FILE = './settig.json'

QUICK = 'quick'
FAST = 'fast'
MID = 'mid'
SLOW = 'slow'



def timestampArray(df):
    array = []
    for i in range(len(df)):
        index = df.index[i]
        array.append(index.timestamp())
    return array

class ChartWindow(QtWidgets.QMainWindow, Ui_MainWindow):   
    def __init__(self):
        super(ChartWindow, self).__init__()
        self.setupUi(self)
        self.comboBox_market.addItems(GEM)        
        self.comboBox_timeframe.addItems(TIMEFRAME.keys())
        self.widget = CandlePlotWidget()
        self.verticalLayout.addWidget(self.widget)
        self.pushButton_draw.clicked.connect(self.plot)
        
        #self.loadSetting()


    def loadSetting(self):
        try:
            json_file = open(SETTING_FILE, 'r')
            dic = json.load(json_file)
            self.comboBox_market1.setCurrentIndex(dic[MARKET1])
        except:
            return None                
            

    def __del__(self):
        self.saveSettings()
        
    def saveSettings(self):
        dic = {}
        dic[MARKET1] = self.comboBox_market1.currentIndex()
        dump = json.dumps(dic)
        f = open(SETTING_FILE, 'w')
        f.write(dump + '\n')
        f.close()
        
        
    def plot(self):
        market = self.comboBox_market.currentText()
        tf = self.comboBox_timeframe.currentText()
        self.plotChart(self.widget, market, tf, 80 )
        
    def plot1(self):
        #self.saveSettings()
        self.update()
        #アップデート時間設定
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(200)    
        
        

        
    def plotChart(self, plot, market_name, time_symbol, size):
        server = MT5Bind(market_name)
        ohlc, ohlcv, dic =  server.download(time_symbol, size=size)
        plot.setTitle(market_name + '-' + time_symbol)
        plot.update(dic, time_form='%H:%M')
            
    def plot_fdr(self):
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
    window = ChartWindow()
    window.show()
    sys.exit(app.exec_())
