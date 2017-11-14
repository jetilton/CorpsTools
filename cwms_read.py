# -*- coding: utf-8 -*-
import requests
import json
import pandas as pd


def create_url(path,lookback):
    lb = '&backward=' + lookback + 'd'
    base_url = r'http://nww-wmlocal2.nww.usace.army.mil/common/web_service/webexec/getjson?'
    end_url = r'%22%5D'
    return '{}{}{}{}{}'.format(base_url, 'query=%5B%22', path, end_url, lb)
    
        
def cwms_read(url):
    r = requests.get(url)
    json_data = json.loads(r.text)
    ts_dict = {}


    for site,data in json_data.items():
        
        for path, vals in data['timeseries'].items():
            
            column_name = '_'.join(path.split('.')[:2])
            if '1Day' in path: interval = 'daily'
            elif '1Hour' in path: interval = 'hourly'
            elif '6Hours' in path: interval = '6hours'
            
            try:path_data = vals['values']
            except KeyError: 
                print('No data: ' + path)
                continue
                        
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
    return ts_dict









