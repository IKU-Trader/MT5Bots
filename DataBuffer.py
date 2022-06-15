# -*- coding: utf-8 -*-
import pandas as pd
from MT5Bind import MT5Bind
from MT5Bind import nowJst, deltaMinute


class XMDataBuffer:
    def __init__(self, name_list, timeframe_list):
        self.name_list = name_list
    
    

    
    def update(self, timeframe):
        server = MT5Bind(self.stock)
        data = server.scrapeRange(timeframe, t0, t1)
  
        

            
            
def test():
    stock = 'US30Cash'
    timeframe = 'M1'



def save(stock, timeframe):
    server = MT5Bind(stock)
    dic = server.scrapeWithDic(timeframe)
    values = dic['data']
    d = []
    for value in values:
        d.append([value['time'], value['open'], value['high'], value['low'], value['close']])
    df = pd.DataFrame(data=d, columns=['Time', 'Open', 'High', 'Low', 'Close'])
    df.to_csv('./' + stock + '_' + timeframe + '.csv', index=False)
    
    
if __name__ == '__main__':
    test()
    #save('US30Cash', 'D1')


        
