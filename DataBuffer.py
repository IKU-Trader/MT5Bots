# -*- coding: utf-8 -*-

import pandas as pd
from MT5Bind import *

class DataBuffer:
    def __init__(self):
        self.dic = None
        
    @classmethod
    def splitDic(cls, dic, i):
        keys = dic.keys()
        arrays = []
        for key in keys:
            arrays.append(dic[key])
        split1 = {}
        split2 = {}
        for key, array in zip(keys, arrays):
            split1[key] = array[:i]
            split2[key] = array[i:]
        return (split1, split2)
    
    @classmethod
    def sliceDic(cls, dic, begin, end):
        keys = dic.keys()
        arrays = []
        for key in keys:
            arrays.append(dic[key])
        out = {}
        for key, array in zip(keys, arrays):
            out[key] = array[begin: end + 1]
        return out
        
    @classmethod
    def dicArrays(cls, dic):
        keys = dic.keys()
        arrays = []
        for key in keys:
            arrays.append(dic[key])
        return keys, arrays

    def slicedData(self, begin, end):
        return self.sliceDic(self.dic, begin, end)
    
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
    
    def update(self, dic):
        if self.dic is None:
            self.dic = dic
            return self.dic
        keys, arrays = self.dicArrays(self.dic)
        keys, newarrays = self.dicArrays(dic)
        indices = []
        for i, t1 in enumerate(dic[TIMESTAMP]):
            n = len(self.dic[TIMESTAMP])
            for j  in range(n - 1, -1, -1):
                t0 = self.dic[TIMESTAMP][j]
                if t1 > t0:
                    for array, newarray in zip(arrays, newarrays):
                        array.insert(j + 1, newarray[i])
                        indices.append(i)
                    break
                #elif t1 == t0:
                #    for array, newarray in zip(arrays, newarrays):
                #        del array[j]
                #        array.insert(j, newarray[i])
                #    break
        
        dic = {}
        for key, array in zip(keys, newarrays):
            a = []
            for i in indices:
                a.append(array[i])
            dic[key] = a
        return dic
                   
def save(dic, filepath):
    keys = dic.keys()
    data = []
    keys, arrays = DataBuffer.dicArrays(dic)
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


        
