# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import requests
import json
import pandas as pd


def create_url(path,lookback):
    lb = '&backward=' + str(lookback) + 'd'
    base_url = r'http://www.nwd-wc.usace.army.mil/dd/common/web_service/webexec/getjson?'
    end_url = r'%22%5D'
    return '{}{}{}{}{}'.format(base_url, 'query=%5B%22', path, end_url, lb)
    
def cwms_read(path, lookback):
    """
    Desc: A function to parse CWMS json data from webservice
        
    Params: path (str), example: 'TDDO.Temp-Water.Inst.1Hour.0.GOES-REV' 
            lookback: (int or str) example: 7
    Returns:A pandas dataframe with metadata stored in df.__dict__['metadata']
    """
    url = create_url(path, lookback)
    r = requests.get(url)
    json_data = json.loads(r.text)
   
    for site,data in json_data.items():
        lat = data['coordinates']['latitude']
        long = data['coordinates']['longitude']
        for path, vals in data['timeseries'].items():
            
            column_name = '_'.join(path.split('.')[:2])
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
            vals.update({'path':path, 'lat':lat,'long':long})
            metadata = {column_name:vals}
            
            df.__dict__['metadata'] = metadata
            
    return df

def merge(df1, df2):
    """
    Desc: A function to merge 2 pd df's that contain metadata, metadata is lost 
          if a dataframe is merged or copied.
        
    Params: df1, df2 (pandas.core.frame.DataFrame)
    Returns:A pandas dataframe with metadata stored in df.__dict__['metadata']
    """
    try:
        meta = df1.__dict__['metadata']
        meta2 = df2.__dict__['metadata']
        meta.update(meta2)
    except KeyError:
        meta = df2.__dict__['metadata']
    df = pd.concat([df1, df2], axis = 1)
    df.__dict__['metadata'] = meta
    return df
    


def get_cwms(paths, interval, lookback):
    """
    Desc: A function that requests multiple paths from the CWMS webservice. Paths
          must be the same time interval.
        
    Params: paths (str or list of str)
    
    Returns:A pandas dataframe with metadata stored in df.__dict__['metadata']
    """
    
    interval_dict = {
                    '1Hour':'1Hour',
                    'hour': '1Hour',
                    'hourly':'1Hour',
                    '1hour':'1Hour',
                    'daily':'1Day',
                    'day':'1Day',
                    'Daily':'1Day',
                    '1Day':'1Day',
                    }
    interval = interval_dict[interval]
    if type(paths)!= list: paths = [paths]
    if paths != [path for path in paths if interval in path]:
        raise ValueError('Not all paths are of the correct interval')
    
    df = pd.DataFrame()
    for path in paths:
        df = df.pipe(merge, df2 =cwms_read(path, 100))
    return df

def catalog():
    url = 'http://www.nwd-wc.usace.army.mil/dd/common/web_service/webexec/getjson?catalog=%5B%5D'
    r = requests.get(url)
    return json.loads(r.text)

def site_catalog(site):
    url = 'http://www.nwd-wc.usace.army.mil/dd/common/web_service/webexec/getjson?tscatalog=%5B%22SITE%22%5D'
    url = url.replace('SITE', site)
    r = requests.get(url)
    return json.loads(r.text)
