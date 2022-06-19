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
        super().__init__(name='Candle') #, axisItems=time_axis)
        self.max_display_bar_size = 100 
        
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
                
    def draw(self, tohlc:list, time_form='%y-%m-%d'):
        timestamp = tohlc[0]
        op = tohlc[1]
        hi = tohlc[2]
        lo = tohlc[3]
        cl = tohlc[4]   
        time_axis = TimeAxisItem(timestamp=timestamp, form=time_form, orientation='bottom')
        self.setAxisItems({'bottom': time_axis})
        n = len(timestamp)
        if n < 2:
            return
        width = 2.0 / 3.0
        candle = CandleObject()
        for i, ohlc in enumerate(zip(op, hi, lo, cl)):
            candle.draw(i, ohlc, width)
        candle.drawEnd()        
        self.addItem(candle)
        
        begin = n - self.max_display_bar_size + 1
        if begin < 0:
            begin = 0
        self.setXRange(begin, n)
        self.setYRange(np.min(np.array(lo)), np.max(np.array(hi)))
        self.customize()        
                
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
            
    def drawEnd(self):
        self.painter.end()
        
    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)
        
    def boundingRect(self):
        return QRectF(self.picture.boundingRect())
        