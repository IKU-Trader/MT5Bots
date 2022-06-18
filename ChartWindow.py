# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 20:28:19 2022

@author: oIKUo
"""

import numpy as np
import datetime
from datetime import datetime
import pyqtgraph
from pyqtgraph.Qt import QtCore, QtWidgets
from pyqtgraph import PlotWidget, GraphicsObject, mkPen, mkBrush, mkQApp, AxisItem, LabelItem
from pyqtgraph.Qt.QtWidgets import QGraphicsRectItem
from pyqtgraph.Qt.QtCore import QPointF, QRectF
from PyQt5.QtGui import QPicture, QPainter
import FinanceDataReader as fdr


def timestampArray(df):
    array = []
    for i in range(len(df)):
        index = df.index[i]
        array.append(index.timestamp())
    return array
    
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
    
class ChartWindow():
    def __init__(self, title, size=(640, 400)):
        self.window = QtWidgets.QMainWindow()
        self.window.setWindowTitle(title)
        self.window.resize(size[0], size[1])
        center_widget = QtWidgets.QWidget()
        self.window.setCentralWidget(center_widget)
        self.layout = QtWidgets.QVBoxLayout()
        center_widget.setLayout(self.layout)
        self.candlePlot = CandlePlot()
        self.layout.addWidget(self.candlePlot)

    def show(self, title, df):
        self.candlePlot.setTitle(title)
        self.candlePlot.draw(df)
        xaxis = self.candlePlot.getAxis('bottom')
        xaxis.setTickSpacing(major=20, minor=10)
        xaxis.setPen(mkPen(color='#000000'))
        xaxis.setGrid(32)
        yaxis = self.candlePlot.getAxis('left')
        #yaxis.setTickSpacing(major=20, minor=10)
        yaxis.setPen(mkPen(color='#000000'))
        yaxis.setGrid(32)
        self.window.show()

class CandlePlot(PlotWidget):
    def __init__(self):
        super().__init__(name='Candle') #, axisItems=time_axis)
         
    def draw(self, df):
        timestamp = timestampArray(df)
        time_axis = TimeAxisItem(timestamp=timestamp, form='%m-%d %H:%M', orientation='bottom')
        self.setAxisItems({'bottom': time_axis})
        op = list(df['Open'].values)
        hi = list(df['High'].values)
        lo = list(df['Low'].values)
        cl = list(df['Close'].values)        
        n = len(timestamp)
        if n < 2:
            return
        width = 2.0 / 3.0
        candle = CandleObject()
        for i, ohlc in enumerate(zip(op, hi, lo, cl)):
            candle.draw(i, ohlc, width)
        candle.drawEnd()        
        self.addItem(candle)
        self.setXRange(0, n) #timestamp[0], timestamp[-1])
        self.setYRange(np.min(np.array(lo)), np.max(np.array(hi)))
        self.setBackground((220, 220, 210))     
                
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
        self.painter.setBrush(mkBrush(color_body))
        self.painter.drawRect(QRectF(i - width / 2, op, width, cl - op))
        self.painter.setPen(mkPen(color_line))
        if cl > op:
            self.painter.drawLine(QPointF(i, cl), QPointF(i, hi))
            self.painter.drawLine(QPointF(i, op), QPointF(i, lo))
        else:
            self.painter.drawLine(QPointF(i, cl), QPointF(i, lo))
            self.painter.drawLine(QPointF(i, op), QPointF(i, hi))
            
    def drawEnd(self):
        self.painter.end()
        
    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)
        
    def boundingRect(self):
        return QRectF(self.picture.boundingRect())
        
def plot():
    app = mkQApp()
    window = ChartWindow('MarketChart')
    df = fdr.DataReader("AAPL", "2022")
    window.show('AAPL', df[:100])
    pyqtgraph.exec()    
    
    
if __name__ == '__main__':
    plot()