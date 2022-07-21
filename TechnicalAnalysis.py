# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 21:12:55 2022

@author: docs9
"""

import numpy as np
from const import *
from utility import *


def nans(length):
    out = []
    for i in range(length):
        out.append(np.nan)
    return out

class Indicator:
    @classmethod
    def sma(cls, array, window):
        n = len(array)
        out = nans(n)
        for i in range(window - 1, n):
            s = 0.0
            count = False
            for j in range(window):
                a = array[i - j]
                if np.isnan(a):
                    break
                else:
                    count += 1
                    s += a
            if count > 0:                
                out[i] = s / count
                return out            

    @classmethod            
    def tr(cls, high, low, close):
        n = len(close)
        out = nans(n)
        out[0] = high[0] - low[0]
        for i in range(1, n):
            r1 = np.abs(high[i] - low[i])
            r2 = np.abs(high[i] - close[i - 1])
            r3 = np.abs(close[i - 1] - low[i])
            out[i] = np.max([r1, r2, r3])
        return out
       
    @classmethod
    def atr(cls, high, low, close, window):
        trdata = cls.tr(high, low,close)
        out = cls.sma(trdata, window)
        return (out, trdata)
    
    @classmethod
    def atrBand(cls, atr, close, window, k):
        upper = np.array(close) + k * np.array(atr) 
        lower = np.array(close) - k * np.array(atr)
        return (list(upper), list(lower))


 
class Math:
    @classmethod
    def greater(cls, ref:list, array:list) -> list:
        out = []
        for r, a in zip(ref, array):
            if np.isnan(r) or np.isnan(a):
                out.append(0)
            else:
                if r > a:
                    out.append(1)
                else:
                    out.append(0)
        return out
    
    @classmethod
    def greaterEqual(cls, ref: list, array:list) -> list:
        out = []
        for r, a in zip(ref, array):
            if np.isnan(r) or np.isnan(a):
                out.append(0)
            else:
                if r >= a:
                    out.append(1)
                else:
                    out.append(0)
        return out

    @classmethod    
    def smaller(cls, ref: list, array:list) -> list:
        out = []
        for r, a in zip(ref, array):
            if np.isnan(r) or np.isnan(a):
                out.append(0)
            else:
                if r < a:
                    out.append(1)
                else:
                    out.append(0)
        return out
    
    @classmethod
    def smallerEqual(cls, ref: list, array: list) -> list:
        out = []
        for r, a in zip(ref, array):
            if np.isnan(r) or np.isnan(a):
                out.append(0)
            else:
                if r < a:
                    out.append(1)
                else:
                    out.append(0)
        return out
    
    @classmethod
    def forceSinglePosition(cls, buy: list, sell: list):
        n = len(buy)
        buy_state = None
        for i in range(n):
            b = buy[i]
            s = sell[i]
            if buy_state is None:
                if b > 0:
                    sell[i] = 0
                    buy_state = True
                elif s > 0:
                    buy_state = False
            else:
                if buy_state:
                    if s > 0:
                        buy[i] = 0
                        buy_state = False
                    elif b > 0:
                        buy[i] = 0
                else:
                    if b > 0:
                        sell[i] = 0
                        buy_state = True
                    elif s > 0:
                        sell[i] = 0
                        
class Signal:    
    @classmethod
    def atrBreak(cls, dic, param, is_multi_position=True):
        atr_ = dic[ATR]
        close = dic[CLOSE]
        upper, lower = Indicator.atrBand(atr_, close, param.atr_window, param.atr_band_k)
        dic[ATR_BAND_UPPER] = upper
        dic[ATR_BAND_LOWER] = lower
        buy_signal = Math.greater(upper, close)
        sell_signal = Math.smaller(lower, close)
        if is_multi_position == False:
            Math.forceSinglePosition(buy_signal, sell_signal)
        return (buy_signal, sell_signal)