# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime, timedelta, timezone
import calendar
import pytz
from MT5Bind import *
from TechnicalAnalysis import Indicator, Math
from utility import dic2Arrays, sliceDic

class DataBuffer:
    def __init__(self, param):
        self.param = param
        self.dic = None
        
    def slicedData(self, begin, end):
        return sliceDic(self.dic, begin, end)
    
    def minMax(self, begin, end):
        dic = self.slicedData(begin, end)
        high = dic[HIGH]
        low = dic[LOW]
        return (min(low), max(high))
    
    def data(self):
        return self.dic
    
    def size(self):
        if self.dic is None:
            return 0
        return len(self.dic[TIMESTAMP])
    
    def lastTime(self):
        if self.size() > 0:
            return self.dic[TIMEJST][-1]
        else:
            return None
        
    def deltaTime(self):
        if self.size() > 1:
            time = self.dic[TIMEJST]
            dt = time[1] - time[0]
            return dt
        else:
            return None
        
    def needSize(self):
        t1 = datetime.now(TIMEZONE_TOKYO)
        t0 = self.lastTime()
        n = (t1 - t0) / self.deltaTime()
        n = int(n + 0.5) +1
        return n
    
    def loadData(self, dic):
        atr_data, tr_data= Indicator.atr(dic[HIGH], dic[LOW], dic[CLOSE], self.param.atr_window)
        dic[ATR] = atr_data
        dic[TR] = tr_data
        self.dic = dic
        return   
    
    def deleteLastData(self, dic):
        keys, arrays = dic2Arrays(dic)
        out = {}
        for key, array in zip(keys, arrays):
            out[key] = array[:-1]
        return out
    
    def update(self, dic):
        self.dic = self.deleteLastData(self.dic)
        keys, arrays = dic2Arrays(self.dic)
        keys, newarrays = dic2Arrays(dic)        
        last_time = self.dic[TIMESTAMP][-1]
        indices = []
        for i  in range(len(dic[TIMESTAMP])):
            t = dic[TIMESTAMP][i]
            if t > last_time:
                indices.append(i)
                last_time = t
                for array, newarray in zip(arrays, newarrays):
                    array.append(newarray[i])
        n = len(self.dic[TIMESTAMP])
        m = len(indices)
        begin = n - m
        end = n -1
        self.updateAtr(self.dic, begin, end)
        return (begin, end)
            
    def updateAtr(self, dic, begin, end):
        n = len(dic[HIGH])
        sliced = sliceDic(dic, begin - self.param.atr_window, end)
        (atrdata, trdata) = Indicator.atr(sliced[HIGH], sliced[LOW], sliced[CLOSE], self.param.atr_window)
        atrarray = self.dic[ATR]
        trarray = self.dic[TR]
        index = -1
        for i in range(end , begin -1, -1):
            atrarray[i] = atrdata[index]
            trarray[i] = trdata[index]
            index -= 1

def save(dic, filepath):
    keys = dic.keys()
    data = []
    keys, arrays = DataBuffer.dic2Arrays(dic)
    n = len(arrays[0])
    for i in range(n):
        d = []
        for array in arrays:
            d.append(array[i])
        data.append(d)
    df = pd.DataFrame(data=data, columns=keys)
    df.to_csv(filepath, index=False)
    
def test():
    server = MT5Bind('DOWUSD')
    ohlc, ohlcv, dic =  server.download('M5', size=10)
    dic1, dic2 = DataBuffer.splitDic(dic, 9)
    print(dic1)
    print(dic2)
    dic2[HIGH] = [-1.0]
    
    buffer = DataBuffer()
    result1 = buffer.update(dic)    
    result2 = buffer.update(dic2)

    save(dic, './original.csv')
    save(result2, './buffered.csv')

if __name__ == '__main__':
    test()
    #save('US30Cash', 'D1')


        
