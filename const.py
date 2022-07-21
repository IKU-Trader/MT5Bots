# -*- coding: utf-8 -*-
"""
Created on Sun Jan 16 09:49:46 2022

@author: docs9
"""

from datetime import datetime, timedelta, timezone
import calendar
import pytz
import MetaTrader5 as mt5

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

TIMEZONE_TOKYO = timezone(timedelta(hours=+9), 'Asia/Tokyo')

GEM_FX = ['USDJPY', 'AUDJPY', 'GBPJPY', 'EURJPY', 'EURUSD', 'GBPUSD', 'GBPAUD' ]
GEM_INDEX = ['DOWUSD', 'NASUSD', 'S&PUSD', 'JPXJPY', 'DAXEUR', 'HSXHKD']
GEM_COMODITY = ['WTIUSD', 'XAUUSD', 'XAGUSD']
GEM = GEM_INDEX + GEM_COMODITY + GEM_FX

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

ATR = 'atr'
TR = 'tr'
SMA = 'sma'
ATR_BAND_UPPER = 'atr_upper'
ATR_BAND_LOWER = 'atr_lower'