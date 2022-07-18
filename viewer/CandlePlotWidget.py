# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 21:57:52 2022

@author: docs9
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 20:28:19 2022

@author: oIKUo
"""

import numpy as np
from datetime import datetime 

import pyqtgraph
from pyqtgraph.Qt import QtCore, QtWidgets
from pyqtgraph import PlotWidget, GraphicsObject, mkPen, mkBrush, mkQApp, AxisItem, LabelItem
from pyqtgraph.Qt.QtWidgets import QGraphicsRectItem
from pyqtgraph.Qt.QtCore import QPointF, QRectF
from PyQt5.QtGui import QPicture, QPainter
from DataBuffer import *

class TimeAxisItem(AxisItem):
    def __init__(self, timestamp=None, form='%H:%M', *args, **kwargs):
        self.timestamp = timestamp        
        self.form = form
        super(TimeAxisItem, self).__init__(*args, **kwargs)
 
    def tickStrings(self, values, scale, spacing):
        labels = []
        n = len(self.timestamp)
        for value in values:
            i = int(value)
            if i < 0 or i > n - 1:
                l = ''
            else:
                v = self.timestamp[i]
                l = datetime.fromtimestamp(v).strftime(self.form)
            labels.append(l)
        return labels
    
class CandlePlotWidget(PlotWidget):
    def __init__(self):
        super().__init__(name='Candle')
        self.max_display_bar_size = 40
        self.candle_objects = []
        self.clearData()
        
    def dataSize(self):
        return self.buffer.size()
        
    def customize(self):
        xaxis = self.getAxis('bottom')
        xaxis.setTickSpacing(major=20, minor=10)
        xaxis.setPen(mkPen(color='#000000'))
        xaxis.setGrid(32)
        yaxis = self.getAxis('left')
        #yaxis.setTickSpacing(major=20, minor=10)
        yaxis.setPen(mkPen(color='#000000'))
        yaxis.setGrid(32)
        self.setBackground((220, 220, 210))
                
    def clearData(self):
        self.buffer = DataBuffer()
        self.last_candle = None
        if len(self.candle_objects) > 0:
            for item in self.candle_objects:
                self.removeItem(item)
        self.candle_objects = []
        self.display_range = None
        
    def update(self, tohlc:dict, time_form='%m-%d'):
        begin, end = self.buffer.update(tohlc)
        timestamp = self.buffer.dic[TIMESTAMP] 
        time_axis = TimeAxisItem(timestamp=timestamp, form=time_form, orientation='bottom')
        self.setAxisItems({'bottom': time_axis})
        n = len(timestamp)
        if n < 2:
            return
        width = 2.0 / 3.0
        
        op = self.buffer.dic[OPEN]
        hi = self.buffer.dic[HIGH]
        lo = self.buffer.dic[LOW]
        cl = self.buffer.dic[CLOSE]
        for i in range(begin, end + 1):
            candle = CandleObject()
            ohlc = [op[i], hi[i], lo[i], cl[i]]
            candle.draw(i, ohlc, width)     
            self.addItem(candle)
            self.candle_objects.append(candle)
    
        begin = n - self.max_display_bar_size + 1
        if begin < 0:
            begin = 0
        vmin, vmax = self.buffer.minMax(begin, n - 1)
        margin = (vmax - vmin) * 0.1
        xrange = (begin, n)
        yrange = (vmin - margin, vmax + margin)
        self.setXRange(xrange[0], xrange[1])
        self.setYRange(yrange[0], yrange[1])
        self.display_range = (xrange, yrange)
        self.customize()
        
    def removeLast(self):
        n = len(self.candle_objects)
        if n > 0:
            item = self.candle_objects.pop()
            self.removeItem(item)
            self.buffer.dic = DataBuffer.deleteLast(self.buffer.dic)
                
class CandleObject(GraphicsObject):
    def __init__(self):
        super().__init__()
        self.picture = QPicture()
        self.painter = QPainter(self.picture)
        
    def draw(self, i, ohlc, width):
        op, hi, lo, cl = ohlc
        if cl > op:
            color_body = (120, 200, 225)
            color_line = (20, 100, 255)
        else:
            color_body = (225, 180, 180)
            color_line = (255, 60, 60)
        self.painter.setPen(mkPen(color_line))
        self.painter.drawLine(QPointF(i, lo), QPointF(i, hi))
        self.painter.setBrush(mkBrush(color_body))
        self.painter.drawRect(QRectF(i - width / 2, op, width, cl - op))
        self.painter.end()
        
       
        
    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)
        
    def boundingRect(self):
        return QRectF(self.picture.boundingRect())
        