# -*- coding: utf-8 -*-
import pandas as pd


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

