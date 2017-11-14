# -*- coding: utf-8 -*-

#from utils import check_obj
#import pandas as pd
from merge_ts import merge_ts
from plots import simple_plot
from boxplot import simple_boxplot
import yaml
from cwms_read import cwms_read, create_url


class TimeSeriesObj(dict):
   
    def __init__(self, lookback):
        super().__init__() 
        
        self.__dict__['cat'] = {}
        self.__dict__['lookback'] = str(lookback)
    
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
    
    def catalog(self):
        """
        This is a static list that will eventually get stale, should probably 
        do an option to pull directly from the web, it just takes a while
        """
        if not self.__dict__['cat']:
            with open("data/site_catalog.yml", 'r') as site_cat:
                try:
                   self.__dict__['cat'] = yaml.load(site_cat)
                except yaml.YAMLError as exc:
                    print(exc)
        return self.__dict__['cat']

    def sites(self):
        return list(self.catalog().keys())
    
    def lookback(self):
        return self.__dict__['lookback']
    
    def get_ts(self, path, merge = False):
        new_ts = TimeSeriesObj(self.lookback)
        if type(path) == list:
            for p in path:
                url = create_url(p, self.lookback)
                ts = cwms_read(url)
                new_ts = new_ts.merge(ts)
        else:
            url = create_url(path, self.lookback)
            new_ts.merge(cwms_read(url))
        if merge:
            self.merge(new_ts) 
        else:return new_ts
    
    
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
            for interval in self.keys():
                meta = self.meta()
                simple_boxplot(tso = self, meta = meta, interval = interval)
        else:
            meta = self.meta()
            simple_boxplot(tso = self, meta = meta, interval = interval)
    
    def meta(self, interval = 'all'):
        if interval == 'all':
            meta_dict = {}
            for k,v in self.items():
                metadata = v.__dict__['metadata']
                meta_dict.update({k:metadata})
        else:
            meta_dict = self[interval].__dict__['metadata']
        
        return meta_dict
                
            
   
        
        
        