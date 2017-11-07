# -*- coding: utf-8 -*-
import requests
import json
import pandas as pd
from TimeSeriesObj import TimeSeriesObj

#def cwms_read(url):
#    r = requests.get(url)
#    json_data = json.loads(r.text)
#    ts_dict = {}
#    
#    for site,data in json_data.items():
#    
#        for path, vals in data['timeseries'].items():
#            
#            
#            if '1Day' in path: interval = 'daily'
#            elif '1Hour' in path: interval = 'hourly'
#            elif '6Hours' in path: interval = '6hours'
#            
#            try:path_data = vals['values']
#            except KeyError: 
#                print('No data: ' + path)
#                continue
#            try: column_name = str(max([int(x) for x in list(ts_dict[interval]['column_data'].keys())]) + 1)
#            except KeyError: column_name = '0'
#            
#            date = [val[0] for val in path_data]
#            values = [val[1] for val in path_data]
#            df= pd.DataFrame({'date': date, column_name: values})
#            df['date'] = pd.to_datetime(df['date'])
#            df.set_index('date', inplace = True)
#            vals.pop('values', None)
#            vals.update({'path':path})
#            data_dict = {column_name:vals}
#            try: 
#                new_df = pd.concat([ts_dict[interval]['df'], df], axis = 1)
#                ts_dict[interval]['df'] = new_df
#                ts_dict[interval]['column_data'].update(data_dict)
#                
#            except KeyError: 
#                ts_dict.update({interval:{'df':df}})
#                ts_dict[interval].update({'column_data':data_dict})
#            
#            
#            
#            
#    return TimeSeriesObj(ts_dict)
#


def cwms_read(url):
    r = requests.get(url)
    json_data = json.loads(r.text)
    ts_dict = {}


    for site,data in json_data.items():
        
        for path, vals in data['timeseries'].items():
            
            
            if '1Day' in path: interval = 'daily'
            elif '1Hour' in path: interval = 'hourly'
            elif '6Hours' in path: interval = '6hours'
            
            try:path_data = vals['values']
            except KeyError: 
                print('No data: ' + path)
                continue
            try: column_name = str(max([int(x) for x in list(ts_dict[interval]['column_data'].keys())]) + 1)
            except KeyError: column_name = '0'
            
            date = [val[0] for val in path_data]
            values = [val[1] for val in path_data]
            df= pd.DataFrame({'date': date, column_name: values})
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace = True)
            vals.pop('values', None)
            vals.update({'path':path})
            metadata = {column_name:vals}
            try: 
                main_metadata = ts_dict[interval].__dict__['metadata']
                new_df = pd.concat([ts_dict[interval], df], axis = 1)
                main_metadata.update(metadata)
                new_df.data_dict = main_metadata
                main_metadata = ts_dict[interval] = new_df
            except KeyError:
                df.metadata = metadata
                ts_dict.update({interval:df})
    return TimeSeriesObj(ts_dict)