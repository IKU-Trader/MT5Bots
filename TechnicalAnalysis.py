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

def sma(array, window):
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
            
def tr(high, low, close):
    n = len(close)
    out = nans(n)
    out[0] = high[0] - low[0]
    for i in range(1, n):
        r1 = np.abs(high[i] - low[i])
        r2 = np.abs(high[i] - close[i - 1])
        r3 = np.abs(close[i - 1] - low[i])
        out[i] = np.max([r1, r2, r3])
    return out
       
def atr(high, low, close, window):
    trdata = tr(high, low,close)
    out = sma(trdata, window)
    return (out, trdata)
    
