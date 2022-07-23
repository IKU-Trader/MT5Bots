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
            count = 0
            for j in range(window):
                a = array[i - j]
                if np.isnan(a):
                    continue
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
    def atrBand(cls, atr, close, k):
        upper = Math.addArray(close, Math.multiply(atr, k))
        lower = Math.subtractArray(close, Math.multiply(atr, k))
        return (upper, lower)
    
    
    @classmethod 
    def hl2(cls, high, low):
        out = Math.addArray(high, low)
        out = Math.multiply(out, 0.5)
        return out

class Math:
    
    @classmethod
    def addArray(cls, array1: list, array2: list) ->list:
        out = []
        for a1, a2 in zip(array1, array2):
            if np.isnan(a1) or np.isnan(a2):
                out.append(np.nan)
            else:
                out.append(a1 + a2)
        return out
    
    @classmethod
    def subtractArray(cls, array1: list, array2: list) ->list:
        out = []
        for a1, a2 in zip(array1, array2):
            if np.isnan(a1) or np.isnan(a2):
                out.append(np.nan)
            else:
                out.append(a1 - a2)
        return out
        
    @classmethod
    def multiply(cls, array: list, value: float) ->list:
        out = []
        for a in array:
            if np.isnan(a) :
                out.append(np.nan)
            else:
                out.append(value * a)
        return out   
        
        
    @classmethod
    def greater(cls, ref:list, array:list) -> list:
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
    def greaterEqual(cls, ref: list, array:list) -> list:
        out = []
        for r, a in zip(ref, array):
            if np.isnan(r) or np.isnan(a):
                out.append(0)
            else:
                if r <= a:
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
                if r > a:
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
                if r >= a:
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
                        
class AtrBreak:    
    
    def __init__(self, atr_window:int, k:float, band_input:str, break_input:str):
        self.atr_window = atr_window
        self.band_input = band_input
        self.break_input = break_input
        self.k = k
        
    def calc(self, dic, is_multi_position=True):
        atr_ = dic[ATR]
        high = dic[HIGH]
        low = dic[LOW]
        close = dic[CLOSE]
        hl2 = Indicator.hl2(high, low)
        dic[HL2] = hl2
        inp = dic[self.band_input]
        upper, lower = Indicator.atrBand(atr_, inp, self.k)
        
        
        dic[ATR_BAND_UPPER] = upper
        dic[ATR_BAND_LOWER] = lower
        inp2 = dic[self.break_input]
        buy_signal = Math.greater(upper, inp2)
        sell_signal = Math.smaller(lower, inp2)
        if is_multi_position == False:
            Math.forceSinglePosition(buy_signal, sell_signal)
        return (buy_signal, sell_signal)
    
    