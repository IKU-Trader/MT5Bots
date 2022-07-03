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
    def dicArrays(cls, dic):
        keys = dic.keys()
        arrays = []
        for key in keys:
            arrays.append(dic[key])
        return keys, arrays

    
    def arrays(self):
        return [   self.dic[TIMESTAMP],
                self.dic[TIMEJST],
                self.dic[OPEN],
                self.dic[HIGH],
                self.dic[LOW],
                self.dic[CLOSE],
                self.dic[VOLUME]]
        
    def update(self, dic):
        if self.dic is None:
            self.dic = dic
            return self.dic
        
        arrays = self.arrays()
        newarrays = [dic[TIMESTAMP],
                    dic[TIMEJST],
                    dic[OPEN],
                    dic[HIGH],
                    dic[LOW],
                    dic[CLOSE],
                    dic[VOLUME]]
        for i, t1 in enumerate(dic[TIMESTAMP]):
            n = len(self.dic[TIMESTAMP])
            for j  in range(n - 1, -1, -1):
                t0 = self.dic[TIMESTAMP][j]
                if t1 > t0:
                    for array, newarray in zip(arrays, newarrays):
                        array.insert(j + 1, newarray[i])
                    break
                elif t1 == t0:
                    for array, newarray in zip(arrays, newarrays):
                        del array[j]
                        array.insert(j, newarray[i])
                    break
        return self.dic
                
    
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


        
