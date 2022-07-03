# -*- coding: utf-8 -*-
import pandas as pd
import MetaTrader5 as mt5
from datetime import datetime, timedelta, timezone

TIMEZONE_TOKYO = timezone(timedelta(hours=+9), 'Asia/Tokyo')

TIMEJST = 'timejst'
TIMESTAMP = 'timestamp'
OPEN = 'open'
HIGH = 'high'
LOW = 'low'
CLOSE = 'close'
VOLUME = 'volume'
    
MINUTE = 'MINUTE'
HOUR = 'HOUR'
DAY = 'DAY'


             # symbol : [(mt5 timeframe constants), number, unit]
TIMEFRAME = {'M1': [mt5.TIMEFRAME_M1,  1, MINUTE],
             'M5': [mt5.TIMEFRAME_M5,  5, MINUTE],
             'M10': [mt5.TIMEFRAME_M10, 10, MINUTE],
             'M15': [mt5.TIMEFRAME_M15, 15, MINUTE],
             'M30': [mt5.TIMEFRAME_M30, 30, MINUTE],
             'H1': [mt5.TIMEFRAME_H1  ,  1, HOUR],
             'H4': [mt5.TIMEFRAME_H4,    4, HOUR],
             'H8': [mt5.TIMEFRAME_H8,    8, HOUR],
             'D1': [mt5.TIMEFRAME_D1,    1, DAY]}

def timeframeUnit(symbol):
    try:
        a = TIMEFRAME[symbol]
        return a[2]
    except:
        return None
    
def timeframeTime(symbol):
    try:
        a = TIMEFRAME[symbol]
        return (a[1], a[2])
    except:
        return None
    
def timeframeConstant(symbol):
    try:
        a = TIMEFRAME[symbol]
        return a[0]
    except:
        return None
    
def timestamp2jst(utc):
    t = datetime.fromtimestamp(utc, TIMEZONE_TOKYO)
    return t


    
class MT5Bind:
    def __init__(self, market):
        self.market = market
        if not mt5.initialize():
            print("initialize() failed")
            mt5.shutdown()
        #print('Version: ', mt5.version())
        pass
    
    def close(self):
        mt5.shutdown()
        pass
    
    def convert(self, data):
        if data is None:
            return [], [], {}
        
        timeJst = []
        timestamp = []
        o = []
        h = []
        l = []
        c = []
        v = []
        ohlcv = []
        ohlc = []
        for d in data:
            values = list(d)
            timestamp.append(values[0])
            time = timestamp2jst(values[0])
            timeJst.append(time)
            o.append(values[1])
            h.append(values[2])
            l.append(values[3])
            c.append(values[4])
            v.append(values[7])
            ohlc.append([values[1], values[2], values[3], values[4]])
            ohlcv.append([values[1], values[2], values[3], values[4]])
            
        dic = {}
        dic[TIMEJST] = timeJst
        dic[TIMESTAMP] = timestamp
        dic[OPEN] = o
        dic[HIGH] = h
        dic[LOW] = l
        dic[CLOSE] = c
        dic[VOLUME] = v
        return ohlc, ohlcv, dic
     
    def download(self, timeframe, size=99999):
        d = mt5.copy_rates_from_pos(self.market, timeframeConstant(timeframe) , 0, size) 
        ohlc, ohlcv, dic = self.convert(d)
        return ohlc, ohlcv, dic

    def downloadRange(self, timeframe, begin_jst, end_jst):
        utc_from = self.jst2serverTime(begin_jst)
        utc_to = self.jst2serverTime(end_jst)
        d = mt5.copy_rates_range(self.stock, timeframeConstant(timeframe) , utc_from, utc_to) 
        data = self.convert2Array(d)
        return data
    
    def downloadTicks(self, timeframe, from_jst, size=100000):
        utc_from = self.jst2serverTime(from_jst)
        d = mt5.copy_ticks_from(self.stock, timeframeConstant(timeframe) , utc_from, size, mt5.COPY_TICKS_ALL) 
        data = self.convert2Array(d)
        return data
    




    
# -----
    



    
def test(size):
    server = MT5Bind('DOWUSD')
    ohlc, ohlcv, dic =  server.download('M5', size=size) 
    print(ohlc)
    print(dic[TIMEJST])

    
if __name__ == "__main__":
    test(50)