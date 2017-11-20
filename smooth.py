# -*- coding: utf-8 -*-
import pandas as pd
from rpy2.robjects import r
import rpy2.robjects.numpy2ri
rpy2.robjects.numpy2ri.activate()


def rmse(y, yhat):
    n = len(y)
    return (((y - yhat)**2).sum()*1/n)**0.5



def ses(y,yhat_prev, alpha, error = False):
    if error: yhat = yhat_prev + alpha * (y-yhat_prev)
    else:yhat = alpha*y +(1-alpha)*yhat_prev
    return yhat

def ses_series(series, alpha, error = False):
    yhat_list = [series[0]]
    for y in series:
        yhat_prev=yhat_list[-1]
        yhat_list.append(ses(y,yhat_prev,alpha, error))
    yhat = pd.Series(yhat_list)
    return yhat

def decompose(series, frequency, s_window, **kwargs):
        '''Use STL to decompose the time series into seasonal, trend, and
        residual components.'''
        
        
        
        
        
        index = series.index
        s = [x for x in series.values]
        length = len(series)
        s = r.ts(s, frequency=frequency)
        decomposed = [x for x in r.stl(s, s_window, **kwargs).rx2('time.series')]
        seasonal = decomposed[0:length]
        trend = decomposed[length:2*length]
        residual = decomposed[2*length:3*length]
        
        
        decomposed = r['stl'](series).rx2('time.series')
        decomposed = [ row for row in decomposed ]
        seasonal = decomposed[0:length]
        trend = decomposed[length:2*length]
        residual = decomposed[2*length:3*length]
        seasonal = TimeSeries(zip(timestamps, seasonal))
        trend = TimeSeries(zip(timestamps, trend))
        residual = TimeSeries(zip(timestamps, residual))
        return DataFrame(seasonal=seasonal, trend=trend, residual=residual)
    
    
    
u = [i for i in range(10)]  # set up another scatter plot, this one local
e = 5*[0.25,-0.25]
v = u[:]
for i in range(10): v[i] += e[i]
r.plot(u,v)
r.assign('remoteu',u)  # ship local u to R
r.assign('remotev',v)  # ship local v to R
r('plot(remoteu,remotev)')  # plot there




