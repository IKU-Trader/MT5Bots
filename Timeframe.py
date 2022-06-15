
from datetime import datetime, timedelta

SECOND = 'SECOND'
MINUTE = 'MINUTE'
HOUR = 'HOUR'
DAY = 'DAY'
             # symbol : [(number, value, unit]
TIMEFRAME = {'S1':  [1,  1, SECOND],
             'S10': [2, 10, SECOND],
             'S30': [3, 30, SECOND],
             'M1':  [4,  1, MINUTE],
             'M5':  [5,  5, MINUTE],
             'M10': [6, 10, MINUTE],
             'M15': [7, 15, MINUTE],
             'M30': [8, 30, MINUTE],
             'H1':  [9,  1, HOUR],
             'H4':  [10, 4, HOUR],
             'H8':  [11, 8, HOUR],
             'D1':  [12, 1, DAY]}

class Timeframe:
    def __init__(self, symbol):
        self.symbol = symbol.upper()
        self.values = TIMEFRAME[self.symbol]

    @property
    def constant(self):
        return self.values[0]

    @property
    def value(self):
        return self.values[1]

    @property
    def unit(self):
        return self.values[2]


        
    @property
    def isDay(self):
        if self.unit == DAY:
            return True
        else:
            return False

    @property
    def isHour(self):
        if self.unit == HOUR:
            return True
        else:
            return False

    @property
    def isMinute(self):
        if self.unit == MINUTE:
            return True
        else:
            return False
        
    @property
    def isSecond(self):
        if self.unit == SECOND:
            return True
        else:
            return False

    def deltaTime(self, multiply=1.0):
        if self.unit == SECOND:
            return timedelta(seconds=multiply * self.value)
        elif self.unit == MINUTE:
            return timedelta(seconds=multiply * self.value * 60)
        elif self.unit == HOUR:
            return timedelta(minutes=multiply * self.value * 60)
        elif self.unit == DAY:
            return timedelta(hours=multiply * self.value * 24)

    def roundTime(self, time):
        if self.unit == SECOND:
            t = datetime(time.year, time.month, time.day, time.hour, time.minute)
            while t < time:
                t += timedelta(seconds= self.value)
            return t
        
        elif self.unit == MINUTE:
            t = datetime(time.year, time.month, time.day, time.hour)
            while t < time:
                t += timedelta(minutes=self.value)
            return t

        elif self.unit == HOUR:
            t = datetime(time.year, time.month, time.day)
            while t < time:
                t += timedelta(hours=self.value)
            return t
        
        elif self.unit == DAY:
            t = datetime(time.year, time.month, 1)
            while t < time:
                t += timedelta(days=self.value)
            return t

    @property
    def symbols(self):
        return list(TIMEFRAME.keys())

    @classmethod
    def timeframes(cls):
        symbols = list(TIMEFRAME.keys())
        l = []
        for symbol in symbols:
            l.append(Timeframe(symbol))
        return l

    @classmethod
    def load(cls, timeframe_constant):
        symbols = list(TIMEFRAME.keys())
        for symbol in symbols:
            v = TIMEFRAME[symbol]
            if v[0] == timeframe_constant:
                return Timeframe(symbol)
        return None
    
# -----
        
def test1():
    tf = Timeframe('S10')
    t1 = datetime(2020, 10, 27, 23, 59, 59, 100)
    t2= tf.roundTime(t1)
    print(t1, t2)
    
    t3 = datetime(2020, 10, 28, 0,  0,  0, 0)
    t4= tf.roundTime(t3)
    print(t3, t4)
    
    t5 = datetime(2020, 10, 28, 0, 0, 10, 10)
    t6= tf.roundTime(t5)
    print(t5, t6) 
    return

def test2():
    tf = Timeframe('M5')
    t1 = datetime(2020, 10, 27, 23, 57, 59, 100)
    t2= tf.roundTime(t1)
    print(t1, t2)
    
    t3 = datetime(2020, 10, 28, 0,  0,  0, 0)
    t4= tf.roundTime(t3)
    print(t3, t4)
    
    t5 = datetime(2020, 10, 28, 0, 0, 10, 10)
    t6= tf.roundTime(t5)
    print(t5, t6) 
    return

def test3():
    tf = Timeframe('H4')
    t1 = datetime(2020, 10, 27, 3, 54, 59, 100)
    t2= tf.roundTime(t1)
    print(t1, t2)
    
    t3 = datetime(2020, 10, 27, 4,  0,  0, 0)
    t4= tf.roundTime(t3)
    print(t3, t4)
    
    t5 = datetime(2020, 10, 27, 4, 0, 10, 10)
    t6= tf.roundTime(t5)
    print(t5, t6) 
    return

if __name__ == '__main__':
    test3()