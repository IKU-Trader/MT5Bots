# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 09:38:11 2022

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

from gui.multi_chart_design import Ui_MainWindow


SETTING_FILE = './settig.json'
MARKET1 = 'market1'
MARKET2 = 'market2'
MARKET3 = 'market3'
VERYSHORT = 'veryshort'
SHORT = 'short'
MIDDLE = 'middle'
LONG = 'long'

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
        
        self.comboBox_market1.addItems(GEM)
        self.comboBox_market2.addItems(GEM)
        self.comboBox_market3.addItems(GEM)
        
        self.comboBox_veryshort.addItems(TIMEFRAME.keys())
        self.comboBox_short.addItems(TIMEFRAME.keys())
        self.comboBox_middle.addItems(TIMEFRAME.keys())
        self.comboBox_long.addItems(TIMEFRAME.keys())
        
        self.plots = []
        p = []
        for i in range(4):
            candle_plot = CandlePlotWidget()
            self.verticalLayout_market1.addWidget(candle_plot)
            p.append(candle_plot)
        self.plots.append(p)
            
        p = []
        for i in range(4):
            candle_plot = CandlePlotWidget()
            self.verticalLayout_market2.addWidget(candle_plot)
            p.append(candle_plot)
        self.plots.append(p)
            
        p = []
        for i in range(4):
            candle_plot = CandlePlotWidget()
            self.verticalLayout_market3.addWidget(candle_plot)
            p.append(candle_plot)
        self.plots.append(p)
            
        self.pushButton_draw.clicked.connect(self.plot)
        
        self.loadSetting()


    def loadSetting(self):
        try:
            json_file = open(SETTING_FILE, 'r')
            dic = json.load(json_file)
            self.comboBox_market1.setCurrentIndex(dic[MARKET1])
            self.comboBox_market2.setCurrentIndex(dic[MARKET2])
            self.comboBox_market3.setCurrentIndex(dic[MARKET3])
            self.comboBox_veryshort.setCurrentIndex(dic[VERYSHORT])
            self.comboBox_short.setCurrentIndex(dic[SHORT]) 
            self.comboBox_middle.setCurrentIndex(dic[MIDDLE])
            self.comboBox_long.setCurrentIndex(dic[LONG])
        except:
            return None                
            
            

    def __del__(self):
        self.saveSettings()
        
    def saveSettings(self):
        dic = {}
        dic[MARKET1] = self.comboBox_market1.currentIndex()
        dic[MARKET2] = self.comboBox_market2.currentIndex()
        dic[MARKET3] = self.comboBox_market3.currentIndex()
        dic[VERYSHORT] = self.comboBox_veryshort.currentIndex()
        dic[SHORT] = self.comboBox_short.currentIndex()
        dic[MIDDLE] = self.comboBox_middle.currentIndex()
        dic[LONG] = self.comboBox_long.currentIndex()
        
        dump = json.dumps(dic)
        f = open(SETTING_FILE, 'w')
        f.write(dump + '\n')
        f.close()
        
        
    def plot(self):
        self.saveSettings()
        self.update()
        #アップデート時間設定
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(200)    
        
        
    def update(self):
        time_symbols = []
        time_symbols.append(self.comboBox_veryshort.currentText())
        time_symbols.append(self.comboBox_short.currentText())
        time_symbols.append(self.comboBox_middle.currentText())
        time_symbols.append(self.comboBox_long.currentText())
        #market1
        market_names = []
        market_names.append(self.comboBox_market1.currentText())
        market_names.append(self.comboBox_market2.currentText())
        market_names.append(self.comboBox_market3.currentText())
        
        
        plot = self.plots[0][0]
        if plot.buffer.size() == 0:
            size = 1000
        else:
            size = plot.buffer.needSize()
            
        for i, market_name in enumerate(market_names):
            for j, symbol in enumerate(time_symbols):
                self.plotChart(self.plots[i][j], market_name, symbol, size)
        
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
