# -*- coding: utf-8 -*-
import pandas as pd
from rpy2.robjects import r



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
        
    df = pd.DataFrame()
    df['date'] = series.index
    s = [x for x in series.values]
    length = len(series)
    s = r.ts(s, frequency=frequency)
    decomposed = [x for x in r.stl(s, s_window, **kwargs).rx2('time.series')]
    df['observed'] = series.values
    df['trend'] = decomposed[length:2*length]
    df['seasonal'] = decomposed[0:length]
    df['residual'] = decomposed[2*length:3*length]
    return df
        
        


