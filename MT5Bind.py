# -*- coding: utf-8 -*-
import pandas as pd
import MetaTrader5 as mt5
from datetime import datetime, timedelta, timezone
import calendar
import pytz
from Timeseries import Timeseries, OHLC, OHLCV


TIMEZONE_TOKYO = pytz.timezone('Asia/Tokyo')

MINUTE = 'MINUTE'
HOUR = 'HOUR'
DAY = 'DAY'

BROKER_XM = 'XM'
BROKER_GEMFOREX = "gemforex"

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
    
def dayOfLastSunday(year, month):
    '''dow: Monday(0) - Sunday(6)'''
    dow = 6
    n = calendar.monthrange(year, month)[1]
    l = range(n - 6, n + 1)
    w = calendar.weekday(year, month, l[0])
    w_l = [i % 7 for i in range(w, w + 7)]
    return l[w_l.index(dow)]

def nowUtc():
    now = datetime.now(pytz.timezone('UTC'))
    return now

def nowXm():
    now = nowUtc()
    zone = xmTimezone(now)
    return datetime.now(zone)

def nowJst():
    now = datetime.now(TIMEZONE_TOKYO)
    return now

def toJst(time):
    return time.astimezone(TIMEZONE_TOKYO)

def toXm(time):
    zone = xmTimezone(time)
    return time.astimezone(zone)

def utcTime(year, month, day, hour, minute):
    local = datetime(year, month, day, hour, minute)
    return pytz.timezone('UTC').localize(local)

def jstTime(year, month, day, hour, minute):
    local = datetime(year, month, day, hour, minute)
    return TIMEZONE_TOKYO.localize(local)

def xmTime(year, month, day, hour, minute):
    t0 = utcTime(year, month, day, hour, minute)
    timezone = xmTimezone(t0)
    t = datetime(year, month, day, hour, minute, tzinfo=timezone)
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
    
def xmTimezone(date_time):
    if isSummerTime(date_time):
        # summer time
        h = 3
    else:
        h = 2
    return timezone(timedelta(hours=h), name='XM')

def gemTimezone(date_time):
    if isSummerTime(date_time):
        # summer time
        h = 3
    else:
        h = 2
    return timezone(timedelta(hours=h), name='gemforex')

def xm2jst(time):
    zone = timezone(timedelta(hours=2), name='xm')
    t1 = time.astimezone(zone)
    if isSummerTime(t1):
        t = time + deltaHour(6)
    else:
        t = time + deltaHour(7)
    t2 = toJst(t)
    return t2

def gem2jst(time):
    zone = timezone(timedelta(hours=2), name='gemforex')
    t1 = time.astimezone(zone)
    if isSummerTime(t1):
        t = time + deltaHour(6)
    else:
        t = time + deltaHour(7)
    t2 = toJst(t)
    return t2

def jst2xm(time):
    if isSummerTime(time):
        t = time - deltaHour(6)
    else:
        t = time - deltaHour(7)
    return toXm(t)

def jst2gem(time):
    if isSummerTime(time):
        t = time - deltaHour(6)
    else:
        t = time - deltaHour(7)
    return toXm(t)    

def deltaDay(days):
    return timedelta(days=days)

def deltaHour(hours):
    return timedelta(hours=hours)

def deltaMinute(minutes):
    return timedelta(minutes=minutes)

def delta(timeframe, size):
    value, unit = timeframeTime(timeframe)
    if unit == MINUTE:
        return deltaMinute(value * size)
    elif unit == HOUR:
        return deltaHour(value * size)
    elif unit == DAY:
        return deltaDay(value * size)
    return None

def time2str(time):
    s = str(time.year) + '/' + str(time.month) + '/' + str(time.day)
    s += ' ' + str(time.hour) + ':' + str(time.minute) + ':' + str(time.second)
    return s
    
    
class MT5Bind:
    def __init__(self, stock, broker):
        self.stock = stock
        self.broker = broker
        if not mt5.initialize():
            print("initialize() failed")
            mt5.shutdown()
        #print('Version: ', mt5.version())
        pass
    def close(self):
        mt5.shutdown()
        pass
    
    def timestamp2jst(self, timestamp):
        t1 = datetime.utcfromtimestamp(timestamp)
        if self.broker == BROKER_GEMFOREX:
            t2 = gem2jst(t1)
        else:
            t2 = xm2jst(t1)
        return t2

    def getPrices(self, timeframe, begin_time, end_time):
        t0 = toXm(begin_time)
        t1 = toXm(end_time)
        if timeframeUnit(timeframe) == DAY:
            return self.getDay(timeframe, t0, t1)        
        elif timeframeUnit(timeframe) == HOUR:
            return self.getHour(timeframe, t0, t1)
        elif timeframeUnit(timeframe) == MINUTE:
            return self.getMinute(timeframe, t0, t1)

    def getTicks(self, time, size):
        t = toXm(time)
        ticks = mt5.copy_ticks_from(self.stock, t, size, mt5.COPY_TICKS_ALL) 
        data = []
        for tick in ticks:
            t = tick.time
            bid = tick.bid
            ask = tick.ask
            data.append([t, bid, ask])
        return data
    
    def getDay(self, timeframe, begin_time, end_time):
        begin = xmTime(begin_time.year, begin_time.month, begin_time.day, 0, 0)
        end = xmTime(end_time.year, end_time.month, end_time.day, 0, 0)
        data = mt5.copy_rates_range(self.stock, timeframeConstant(timeframe), begin, end) 
        return self.convert2Array(data)
    
    def cutUnderHour(self, time, offset):
        t = xmTime(time.year, time.month, time.day, time.hour, 0) + deltaHour(1)
        return t
    
    def getHour(self, timeframe, begin_time, end_time):
        begin = self.cutUnderHour(begin_time, 0)
        end = self.cutUnderHour(end_time, 1)
        data = mt5.copy_rates_range(self.stock, timeframeConstant(timeframe), begin, end) 
        return self.convert2Array(data)
    
    def convert2Array(self, data):
        out = []
        if data is None:
            return []
        for d in data:
            value = list(d)
            time = self.timestamp2jst(value[0])
            out.append([time] + value[1:7])
        return out
        
    def roundMinute(self, time, timeframe):
        dt = timeframeTime(timeframe)
        t = xmTime(time.year, time.month, time.day, time.hour, time.minute)
        t += deltaMinute(dt[0] - 1)
        minute = int(t.minute / dt[0]) * dt[0]
        t1 = xmTime(t.year, t.month, t.day, t.hour, minute)
        return t1

    def getMinute(self, timeframe, begin_time, end_time):
        begin = self.roundMinute(begin_time, timeframe)
        end = self.roundMinute(end_time, timeframe)
        tf = timeframeConstant(timeframe)
        data = mt5.copy_rates_range(self.stock, tf , begin, end) 
        return self.convert2Array(data)
     
    def download(self, timeframe, size=99999):
        d = mt5.copy_rates_from_pos(self.stock, timeframeConstant(timeframe) , 0, size) 
        data = self.convert2Array(d)
        return data
    
    def downloadWithTimeSeries(self, timeframe, size=99999):
        d = mt5.copy_rates_from_pos(self.stock, timeframeConstant(timeframe) , 0, size) 
        data = self.convert2Array(d)
        return self.toTimeSeries(data)
    
    def download2Dic(self, timeframe, size=99999):
        d = mt5.copy_rates_from_pos(self.stock, timeframeConstant(timeframe) , 0, size) 
        data = self.convert2Array(d)
        array = self.toDicArray(data)
        dic = {}
        dic['name'] = self.stock
        dic['timeframe'] = timeframe
        dic['length'] = len(data)
        dic['data'] = array
        return dic
    
    def jst2serverTime(self, jst):
        # タイムゾーンをUTCに設定する
        timezone = pytz.timezone("Etc/UTC")
        # create 'datetime' objects in UTC time zone to avoid the implementation of a local time zone offset
        if self.broker == BROKER_GEMFOREX:
            if isSummerTime(jst):
                delta = deltaHour(6)
            else:
                delta = deltaHour(7)         
        elif self.broker == BROKER_XM:
            if isSummerTime(jst):
                delta = deltaHour(6)
            else:
                delta = deltaHour(7)        
        t = datetime(jst.year, jst.month, jst.day, jst.hour, jst.minute, 0, tzinfo=timezone) - delta
        return t
    
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
    
    def toTimeSeries(self, data, data_type=OHLC):
        time = []
        values = []
        for v in data:
            time.append(v[0])
            if data_type == OHLCV:
                values.append(v[1:6])
            elif data_type == OHLC:
                values.append(v[1:5])
        return Timeseries(time, values, names=data_type)

    def toDicArray(self, data, data_type=OHLC):
        array = []
        for v in data:
            dic = {}
            dic['time'] = time2str(v[0])
            for i in range(len(data_type)):
                name = data_type[i]
                dic[name] = v[i + 1]
            array.append(dic)
        return array

    def toDi2(self, data, data_type=OHLC):
        time = []
        dic = {}
        for v in data:
            time.append(time2str(v[0]))
        dic['time'] = time
        for i in range(len(data_type)):
            values = []
            for v in data:
                values.append(v[i + 1])
            dic[data_type[i]] = values
        return dic
    
# -----
    
def test0():
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()
    print('Version:', mt5.version())    

    t1 = nowXm() 
    t0 = t1 - deltaMinute(5)
    values = mt5.copy_rates_range("US30Cash", mt5.TIMEFRAME_M1, t0, t1)
    for value in values:
        t = pd.to_datetime(value[0], unit='s')
        pytime = t.to_pydatetime()
        print(t, pytime, toXm(pytime), value)

    mt5.shutdown()
    pass


def test():
    # connect to MetaTrader 5
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()
    print('Version:', mt5.version())
    
    
    #dji = mt5.copy_rates_range('US30Cash', mt5.TIMEFRAME_M30, Now() - DeltaDay(2), Now())
    #print(dji)
 
    # request 1000 ticks from EURAUD
    euraud_ticks = mt5.copy_ticks_from("US30Cash", datetime(2020,4,17,23), 1000, mt5.COPY_TICKS_ALL)
    # request ticks from AUDUSD within 2019.04.01 13:00 - 2019.04.02 13:00
    audusd_ticks = mt5.copy_ticks_range("AUDUSD", datetime(2020,1,27,13), datetime(2020,1,28,13), mt5.COPY_TICKS_ALL)
 
    # get bars from different symbols in a number of ways
    eurusd_rates = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_M1, datetime(2020,1,28,13), 1000)
    eurgbp_rates = mt5.copy_rates_from_pos("EURGBP", mt5.TIMEFRAME_M1, 0, 1000)
    eurcad_rates = mt5.copy_rates_range("EURCAD", mt5.TIMEFRAME_M1, datetime(2020,1,27,13), datetime(2020,1,28,13))
    #print(eurusd_rates)
    # shut down connection to MetaTrader 5
    mt5.shutdown()
    return

def test1():
    server = MT5Bind('US30Cash')
    t1 = nowXm()
    t0 = t1 - deltaDay(1)
    data = server.getPrices('M1',t0, t1)
    server.close()  
    print('T0=', t0, xm2jst(t0))
    print('T1=', t1, xm2jst(t1))
    for d in data:
        print(d)
    print('n=', len(data))
  
    
    
def test2(stock, timeframe):
    server = MT5Bind(stock)
    data = server.download(timeframe, size=100)
    server.close()  
    print(stock)
    for d in data:
        print(d)
    print('n=', len(data))
    
def test3():
    server = MT5Bind('US30Cash')
    t0 = jstTime(2020, 1, 12, 12, 31)
    t1 = server.roundMinute(t0, 'M30')
    print(t0, t1)
    t2 = server.roundMinute(t0, 'M5')
    print(t0, t2)
    
def test4():
    
    now = nowUtc()
    jst = toJst(now)
    xm = toXm(now)
    print('JST', jst)
    print('XM', nowXm())
    print('JST2', toJst(now))
    
    jst = jstTime(2020, 4, 8, 22, 13)
    print('XM2', toXm(jst))
    
    
def test5(size):
    server = MT5Bind('DOWUSD', BROKER_GEMFOREX)
    d =  server.download('M5', size=size) 
    print(d)
    
def test6():
    server = MT5Bind('US30Cash')
    jst = nowJst() - deltaHour(1)
    d =  server.downloadTicks('M5', jst, size=100) 
    print(d)
    
if __name__ == "__main__":
    test5(50)