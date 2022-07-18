# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 20:24:47 2022

@author: docs9
"""

import pandas as pd
import numpy as np

def df2dic(df: pd.DataFrame, is_numpy=True, time_key = 'time', convert_keys=None):
    columns = df.columns
    dic = {}
    for column in columns:
        d = None
        if column.lower() == time_key.lower():
            d = df[column].values
        else:
            d = df[column].values.tolist()
            d = [float(v) for v in d]
            if is_numpy:
                d = np.array(d)
        if convert_keys is None:
            key = column
        else:
            try:
                key = convert_keys[column]
            except Exception as e:
                key = column
        dic[key] = d
    return dic

def dic2df(dic):
    keys = list(dic.keys())
    values = list(dic.values())

    n = len(values)
    length = len(values[0])
    
    out = []
    for i in range(length):
        d = []
        for j in range(n):
            d.append(values[j][i])
        out.append(d)
    df = pd.DataFrame(data=out, columns = keys)
    return df

    
    