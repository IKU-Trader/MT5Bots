# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 21:18:33 2022

@author: docs9
"""

import pandas as pd
from datetime import datetime, timedelta, timezone
import calendar
import pytz
from MT5Bind import *

from Timeframe import Timeframe
from DataBuffer import DataBuffer
from utility import dic2df, dic2Arrays, sliceTime, sliceDic
from Mt5DataServer import Mt5DataServer
from TechnicalAnalysis import Indicator, Math, AtrBreak, nans
from CandlePlot import CandlePlot, makeFig

from const import *

INITIAL_DATA_SIZE = 50000



class Params:
    def __init__(self):
        self.atr_window = 5
        self.atr_band_k = 0.7
        self.atr_break_input = OPEN
        
class TradeApp:
    
    def __init__(self, market, timeframe_symbol, params):
        self.params = params
        self.market = market
        self.timeframe = Timeframe(timeframe_symbol)
        self.buffer = DataBuffer(params)
        #self.loadInitialData()
        pass
    
    def loadInitialData(self, filepath, kind):
        self.stub = Mt5DataServer(self.market, self.timeframe)
        self.stub.loadFromCsv(filepath, kind)
        n = self.stub.length
        self.data_max = n
        self.current_index = int(n / 2)
        dic = self.stub.sliceData(0, self.current_index)
        self.buffer.loadData(dic)
        pass

    def fillNan(self, dic, keys):
        _, arrays = dic2Arrays(dic)
        n = len(arrays[0])
        for key in keys:
            dic[key] = nans(n)

    def update(self):
        i = self.current_index
        if i > self.data_max - 1:
            print('No data')
            return
        dic = self.stub.sliceData(i, i + 1)
        self.fillNan(dic, [TR, ATR])
        self.current_index = i + 1
        self.buffer.update(dic)

# -----

def dayRange(time, begin_hour, begin_minutes, end_hour, end_minutes):
    t0 = time[0]
    t1 = time[-1]
    print('Begin: ', t0, '  End: ', t1)
    out = []
    for y in range(t0.year, t1.year + 1):
        for m  in range(1, 13):
            for d in range(1, 31):
                try:
                    t0 = datetime(y, m, d, begin_hour, begin_minutes, tzinfo=TIMEZONE_TOKYO )
                    t1 = datetime(y, m, d, end_hour, end_minutes, tzinfo=TIMEZONE_TOKYO )
                    if end_hour < begin_hour:
                        t1 += timedelta(hours=24)
                    n, begin, end = sliceTime(time, t0, t1)
                    if n > 10:
                        out.append([begin, end])            
                except:
                    continue
    return out


def download():
    server = MT5Bind('DOWUSD')
    ohlc, ohlcv, dic = server.download('M5', size=INITIAL_DATA_SIZE)
    df = dic2df(dic)    
    df.to_csv('./data/dowusd_m5.csv', index=False)

def termStr(time):
    t0 = time[0]
    t1 = time[-1]
    form = '%Y-%m-%d %H:%M'
    s = t0.strftime(form) + ' - ' + t1.strftime(form)
    return s

def test():
    params = Params()
    app = TradeApp('DOWUSD', 'M5', params)
    #app.loadInitialData('./data/dowusd_m5.csv', 'mt5')
    app.loadInitialData('./data/OANDA_XAUUSD_m15.csv', 'tradingview')
    for i in range(app.data_max - app.current_index -1):
        app.update()
    
    dic = app.buffer.dic 
    time = dic[TIMEJST]
    print(time[0], '-', time[-1])
    
    indices = dayRange(time, 10, 0, 7, 0)
    print(len(indices))
    
    day_range1 = indices[-2]
    day_range2 = indices[-1]
    day_dic = sliceDic(dic, day_range2[0], day_range2[1])
    time = day_dic[TIMEJST]
    fig, ax = makeFig(1, 1, (12, 7))
    plot = CandlePlot(fig, ax, termStr(time))
    plot.drawCandle(time, day_dic, [OPEN, HIGH, LOW, CLOSE])


    br = AtrBreak(5, 0.5, HL2, CLOSE)
    (buy_signal, sell_signal) = br.calc(day_dic, is_multi_position=False)
    
    atr_ = day_dic[ATR]
    upper = day_dic[ATR_BAND_UPPER]
    lower = day_dic[ATR_BAND_LOWER]
    
    plot.drawLine(time, upper, color='pink')
    plot.drawLine(time, lower, color='lightgreen')
    plot.drawMarkers(time, lower, -2, buy_signal, 1, '^', 'blue', markersize=5)
    plot.drawMarkers(time, upper, 2, sell_signal, 1, 'v', 'red', markersize=5)
    
    pass
    
    
    

if __name__ == "__main__":
    #download()
    test()
    
    
    
    