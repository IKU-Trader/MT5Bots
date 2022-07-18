# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 10:37:24 2022

@author: docs9
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

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
from DataBuffer import *

from chart_design import Ui_MainWindow


SETTING_FILE = './settig.json'

MARKET = 'market'
QUICK = 'quick'
FAST = 'fast'
MID = 'mid'
SLOW = 'slow'

TIMEFORMAT = {'S1': '%H:%M',
               'S10': '%H:%M',
               'S30': '%H:%M',
               'M1': '%H:%M',
               'M5': '%H:%M',
               'M10': '%H:%M',
               'M15': '%H:%M',
               'M30': '%H:%M',
               'H1': '%H:%M',
               'H4': '%m-%d',
               'H8': '%m-%d',
               'D1': '%m-%d'}

INITIAL_DATA_SIZE = 50000

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
        self.pushButton_debug1.clicked.connect(self.debug1)
        self.pushButton_debug2.clicked.connect(self.debug2)
        self.time_format = None
        
        #self.loadSetting()


    def loadSetting(self):
        try:
            json_file = open(SETTING_FILE, 'r')
            dic = json.load(json_file)
            self.comboBox_market1.setCurrentIndex(dic[MARKET])
        except:
            return None                
            

    def __del__(self):
        self.saveSettings()
        
    def saveSettings(self):
        dic = {}
        dic[MARKET] = self.comboBox_market.currentIndex()
        dump = json.dumps(dic)
        f = open(SETTING_FILE, 'w')
        f.write(dump + '\n')
        f.close()
        
        
    def plot(self):
        market = self.comboBox_market.currentText()
        tf = self.comboBox_timeframe.currentText()
        self.resetChart(market, tf)
        self.plotChartMt5()
        
    def debug1(self):
        self.widget.removeLast()
        
    def debug2(self):
        self.widget.removeLast()
        dic = self.loadData('./add.csv')
        self.widget.update(dic)
        
    def plot1(self):
        #self.saveSettings()
        self.update()
        #アップデート時間設定
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(200)    
        
        
    def loadData(self, filepath):
        df = pd.read_csv(filepath)
        dic = {}
        keys = ['timejst', 'timestamp', 'open', 'high', 'low', 'close', 'volume']
        for key in keys:
            dic[key] = list(df[key])
        return dic
        
    def plotChart(self, plot, market_name, time_symbol, size):
        dic = self.loadData('./original.csv')
        plot.update(dic)
        
     
    def resetChart(self, market_name, time_symbol):
        self.market_name = market_name
        self.widget.setTitle(market_name + '-' + time_symbol)
        self.time_format = TIMEFORMAT[time_symbol]
        self.time_symbol = time_symbol
        self.widget.clearData()
        
        
    def plotChartMt5(self):
        if self.widget.dataSize() < 100:
            size = INITIAL_DATA_SIZE
        else:
            size = 10
        server = MT5Bind(self.market_name)
        ohlc, ohlcv, dic =  server.download(self.time_symbol, size=size)
        n = len(dic[TIMESTAMP])
        print('Download size:', n)
        d = DataBuffer.sliceDic(dic, n - 500, n - 1)
        self.widget.update(d, time_form=self.time_format)
            
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
