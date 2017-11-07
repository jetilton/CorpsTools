# -*- coding: utf-8 -*-
import numpy as np
import copy
import pandas as pd


def create_nan(series):
    nan_series_length = int(len(series)//(1/.2))
    nan_series = pd.Series(np.random.randint(1,len(series), size = nan_series_length -1))
    return nan_series
    
def test_impute(series, method = 'interp', max_missing = 25):
    s = copy.deepcopy(series)
    error_dict = {'missing_span':[],'rmse':[]}
    nan_series = create_nan(series)
    for i in range(1,max_missing):
        rmse_list = []
        for index in nan_series:
            start = index
            if start + i > len(s):
                continue
            else:
                end = start + i
            #create a set of nan values to make predictions
            s.iloc[start:end]=np.nan
            if method == 'interp':
                s = s.interpolate()
            elif method == 'mean':
                s.iloc[start:end]=s.mean()
            #grab the targets from original series to compare predictions
            targets = series[index:end]
            predictions = s[index:end]
            rmse = np.sqrt(((predictions - targets) ** 2).mean())
            rmse_list.append(rmse)
        #take the average of rmse over a particular span
        rmse = sum(rmse_list)/len(rmse_list)
        error_dict['missing_span'].append(i)
        error_dict['rmse'].append(rmse)
    return pd.DataFrame(error_dict).set_index('missing_span')


#series = c.ts['hourly']['df']['0']
#
#
#
#test_impute(series, method = 'mean').plot()
#
#
#
#
#i = 4
#
#index = nan_series[0]