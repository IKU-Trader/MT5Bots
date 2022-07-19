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
from utility import dic2df
from Mt5DataServer import Mt5DataServer

INITIAL_DATA_SIZE = 50000

class TradeApp:
    
    def __init__(self, market, timeframe_symbol):
        self.market = market
        self.timeframe = Timeframe(timeframe_symbol)
        self.buffer = DataBuffer()
        self.loadInitialData()
        pass
    
    
    def loadInitialData(self):
        self.stub = Mt5DataServer(self.market, self.timeframe)
        self.stub.loadFromCsv('./data/dowusd_m5.csv')
        n = self.stub.length
        self.current_index = int(n / 2)
        dic = self.stub.sliceData(0, self.current_index)
        self.buffer.loadData(dic)
        pass
    
    
    
    
# -----
def download():
    server = MT5Bind('DOWUSD')
    ohlc, ohlcv, dic = server.download('M5', size=INITIAL_DATA_SIZE)
    df = dic2df(dic)    
    df.to_csv('./data/dowusd_m5.csv', index=False)

def test():
    app = TradeApp('DOWUSD', 'M5')
    

if __name__ == "__main__":
    #download()
    test()
    
    
    
    