# -*- coding: utf-8 -*-
import pandas as pd
import MetaTrader5 as mt5
from datetime import datetime, timedelta, timezone
import calendar
import pytz
from const import *


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
    
def timestamp2jst(utc_server):
    t = datetime.fromtimestamp(utc_server, TIMEZONE_TOKYO)
    if isSummerTime(t):
        dt = 3
    else:
        dt = 4
    t -= timedelta(hours=dt)
    return t

def isSummerTime(date_time):
    day0 = dayOfLastSunday(date_time.year, 3)
    tsummer0 = utcTime(date_time.year, 3, day0, 0, 0)
    day1 = dayOfLastSunday(date_time.year, 10)
    tsummer1 = utcTime(date_time.year, 10, day1, 0, 0)
    if date_time > tsummer0 and date_time < tsummer1:
        return True
    else:
        return False
    
def utcTime(year, month, day, hour, minute):
    local = datetime(year, month, day, hour, minute)
    return pytz.timezone('UTC').localize(local)    
    
    
def dayOfLastSunday(year, month):
    '''dow: Monday(0) - Sunday(6)'''
    dow = 6
    n = calendar.monthrange(year, month)[1]
    l = range(n - 6, n + 1)
    w = calendar.weekday(year, month, l[0])
    w_l = [i % 7 for i in range(w, w + 7)]
    return l[w_l.index(dow)]    
    
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
            jst = timestamp2jst(values[0])
            timeJst.append(jst)
            timestamp.append(jst.timestamp())
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
    test(5)