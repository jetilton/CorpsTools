# -*- coding: utf-8 -*-

#from utils import check_obj
#import pandas as pd
from merge_ts import merge_ts
from impute import test_impute
from plots import simple_plot, simple_boxplot 

class TimeSeriesObj(dict):
   
    
        
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)
            
            
#    def __init__(self, dictionary):
#        try:check_obj(dictionary, dict)
#        except TypeError:
#            raise TypeError('Dictionary not provided')
#        try: 
#            dictionary['daily']
#        except:
#            try: 
#                dictionary['hourly']
#            except:
#                try:
#                    dictionary['6hours']
#                except KeyError:
#                    raise KeyError('The provided dict does not have a standard interval')
#        for k, v in dictionary.items():
#            try: v['df']
#            except:
#                message = k + ' interval is missing a data frame'
#                raise KeyError(message)
#            try: check_obj(v['df'], pd.core.frame.DataFrame)
#            except TypeError:
#                message = str(k) +"['df'] is not a pandas data frame"
#                raise TypeError(message)
         
    
    def merge(self,new_ts):
        return merge_ts(self, new_ts)
    
    def plot(self, interval = 'all', bok = False, **kwargs):
        if interval == 'all':
            for interval, value in self.items():
                if bok: return simple_plot(value, bok, **kwargs)
                else: simple_plot(value, bok, **kwargs)
        else:
            if bok: return simple_plot(self[interval], bok, **kwargs)
            else: simple_plot(self[interval], bok, **kwargs)
    
    def boxplot(self, interval = 'all'):
        if interval == 'all':
            for interval, value in self.items():
                simple_boxplot(value)
        else: simple_boxplot(self[interval])
            
   
        
        
        