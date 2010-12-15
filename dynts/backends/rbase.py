from rpy2 import rinterface
from numpy import asarray, ndarray

import dynts
from dynts.utils import ascolumn
from dynts.utils.rutils import rpyobject, py2rdate, r2pydate, isoformat



class rts(dynts.TimeSeries,rpyobject):
    '''Base class for R-based timeseries objects'''
    
    @property
    def shape(self):
        try:
            s = tuple(self.rc('dim'))
        except:
            s = self.values().shape
        if len(s) == 1:
            s += 1,
        return s
    
    def __getitem__(self, i):
        '''This is not an efficient method'''
        return self.values()[i]
    
    def factory(self, date, data, raw = False):
        raise NotImplementedError
    
    def dateconvert(self, dte):
        return py2rdate(dte)
    
    def dateinverse(self, key):
        return r2pydate(key)
    
    def make(self, date, data, raw = False):
        if date is None:
            ts = None
        else:
            data = ascolumn(data)
            ts = self.factory(date, data, raw = raw)
        self._ts = ts
        
    def keys(self, desc = None):
        '''numpy asarray does not copy data'''
        res = asarray(self.rc('index'))
        if desc == True:
            return reversed(res)
        else:
            return res
        
    def values(self, desc = None):
        '''numpy asarray does not copy data'''
        if self._ts:
            res = asarray(self._ts)
            if desc == True:
                return reversed(res)
            else:
                return res
        else:
            return ndarray([0,0])
        
    def lag(self, k = 1, **kwargs):
        return self.rcts('lag',k)
    
    def delta(self, lag = 1, name = None, **kwargs):
        name = name or 'delta(%s,%s)' % (self.name,lag)
        return self.rcts('diff', lag = lag, name = name)
    
    def delta2(self, lag = 1, name = None, **kwargs):
        name = name or 'delta(%s,%s)' % (self.name,lag)
        return self.rcts('diff', lag = lag, differences = 2, name = name)
    
    def log(self, name = None, **kwargs):
        return self.rcts('log', name = name or 'log(%s)' % self.name)
    
    def logdelta(self, lag = 1, name = None, **kwargs):
        self.r('''logdelta <- function(df,lag){ diff(log(df),lag)}''')
        name = name or 'logdelta(%s,%s)' % (self.name,lag)
        return self.rcts('logdelta',lag, name = name)
    
    def stddev(self):
        raise self.rcts('sd')
    
    def isregular(self):
        return self.rc('is.regular')[0]
    
    def frequency(self):
        return self.rc('frequency')[0]
    
    def window(self, start, end):
        c = self.dateconvert
        return self.rcts('window', start = c(start), end = c(end))

    def rc(self, command, *args, **kwargs):
        return self.r[command](self._ts,*args,**kwargs)
    
    def rcts(self, command, *args, **kwargs):
        cls = self.__class__
        name = kwargs.pop('name','')
        date = kwargs.pop('date',None)
        data = kwargs.pop('data',None)
        kwargs.pop('bycolumn',None)
        ts  = cls(name=name,date=date,data=data)
        ts._ts = self.rc(command, *args, **kwargs)
        return ts
