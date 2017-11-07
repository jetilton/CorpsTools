# -*- coding: utf-8 -*-


"""
Created on Tue Oct 17 13:43:10 2017

@author: G0PDWJPT
"""
import requests
import json
import yaml
from cwms_read import cwms_read
from merge_ts import merge_ts
from TimeSeriesObj import TimeSeriesObj

class CWMSHydro:
    
    def __init__(self, lookback):
        self.ts = TimeSeriesObj()
        self.cat = {}
        self.lookback = str(lookback)
        self.base_url = r'http://nww-wmlocal2.nww.usace.army.mil/common/web_service/webexec/getjson?'
        self.end_url = r'%22%5D'
        
    def catalog(self):
        """
        This is a static list that will eventually get stale, should probably 
        do an option to pull directly from the web, it just takes a while
        """
        if not self.cat:
            with open("data/site_catalog.yml", 'r') as site_cat:
                try:
                   self.cat = yaml.load(site_cat)
                except yaml.YAMLError as exc:
                    print(exc)
        return self.cat
    
    def sites(self):
        return list(self.catalog().keys())
            
    def site_catalog(self, site):
        site = site.upper()
        cat_url = 'tscatalog=%5B%22'
        url = '{}{}{}{}'.format(self.base_url,cat_url,site,self.end_url)
        r = requests.get(url)
        return json.loads(r.text)
    
        
    def get_ts(self, path, merge = False):
        lb = '&backward=' + self.lookback + 'd'
        if type(path) == list:
            new_ts = TimeSeriesObj()
            for p in path:
                url = '{}{}{}{}{}'.format(self.base_url, 'query=%5B%22', p, self.end_url, lb)
                ts = cwms_read(url)
                new_ts = new_ts.merge(ts)
        else:
            url = '{}{}{}{}{}'.format(self.base_url, 'query=%5B%22', path, self.end_url, lb)
            new_ts = cwms_read(url)
        if merge:
            self.merge(new_ts) 
        else:return new_ts
            
    def merge(self, new_ts_dict):
        self.ts = merge_ts(self.ts, new_ts_dict)
        
    def plot(self, interval = 'all', bok = False):
        if bok: return self.ts.plot(interval, bok)
        else: self.ts.plot(interval, bok)
    
    def boxplot(self, interval = 'all'):
        self.ts.boxplot(interval)
            
    def meta(self, interval = 'all'):
        if interval == 'all':
            meta_dict = {}
            for k,v in self.ts.items():
                metadata = v.__dict__['metadata']
                meta_dict.update({k:metadata})
        else:
            meta_dict = self.ts[interval].__dict__['metadata']
        
        return meta_dict
                
         
        
        


        
        
        
        