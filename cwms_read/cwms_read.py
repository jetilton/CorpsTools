# -*- coding: utf-8 -*-

import requests
import json
import pandas as pd
from datetime import datetime
from math import floor

def full_time(time_float):
    """
    helper function for time_delta_parse
    
    Arguments:          
        time_float -- Float of a time, example 3.2 weeks 
    
    Returns:        
        (time_float,remainder) -- tuple with the integer of original time float
                                  and the remainder as a float 
    
    """
    if time_float > 1:
        remainder = time_float - int(time_float)
        time_float = floor(time_float)
    else: 
        remainder = time_float
        time_float = 0
    return(time_float,remainder)

def time_delta_parse(time_delta):
    """
    Helper function for url_w_d_h_m
    
    Arguments:         
        time_delta -- time delta object
    
    Returns:        
        (weeks,days,hours,minutes) -- tuple integer of weeks, days, hours, minutes
    
    """
    seconds = time_delta.total_seconds()
    weeks = seconds/(60*60*24*7)
    weeks, remainder = full_time(weeks)
    days = remainder * 7
    days, remainder = full_time(days)
    hours = remainder * 24
    hours, remainder = full_time(hours)
    minutes = floor(remainder * 60)
    return (weeks,days,hours,minutes)

def url_w_d_h_m(week,day,hour,minute):
    """
    Helper function for time_window_url
    
    Arguments:   
        
        week -- # of weeks as string or integer
        day --  # of days as string or integer
        hour --  # of hours as string or integer
        minute --  # of minutes as string or integer
        
    Returns:    
        
       (week,day,hour,minute) -- tuple of string of weeks, days, hours, minutes with 
                                 added string component for url
    """
    
    if week<0:week = ''
    else: week = str(week)+'w'
    if day<0:day = ''
    else: day = str(day)+'d'
    if hour<0:hour = ''
    else: hour = str(hour)+'h'
    if minute<0:minute = ''
    else: minute = str(minute)+'m'   
    return(week,day,hour,minute)


def time_window_url(path, start_date, end_date, public=True, **kwargs):
    """
    helper function for cwms_read
    
    Arguments:  
        
        path -- cwms data path, 
        public -- boolean, 
        start_date -- date integer tuple format (YYYY, m, d)
        end_date -- date integer tuple format (YYYY, m, d)
        timezone -- optional keyword argument if time zone is specified.  
                    Defaults to 'PST' if nothing set
    Returns:
        
        url -- url string of CWMS data webservice for the specified 
               data path and time window
               
    """
    try:timezone = kwargs['timezone']
    except:timezone = 'PST'
    
    
    if public:
        url = r'http://pweb.crohms.org/dd/common/web_service/webexec/getjson?timezone=TIMEZONE_&backward=BACKWARD_WEEK_BACKWARD_DAY_BACKWARD_HOUR_BACKWARD_MINUTE_&forward=-FORWARD_WEEK_FORWARD_HOUR_FORWARD_MINUTE_&startdate=START_MONTH%2FSTART_DAY%2FSTART_YEAR+08%3A00&enddate=END_MONTH%2FEND_DAY%2FEND_YEAR+08%3A00&query=%5B%22PATH%22%2C%22PATH%22%5D'
    else:
        url = r'http://nwp-wmlocal2.nwp.usace.army.mil/common/web_service/webexec/getjson?query=%5B%22PATH%22%5D&startdate=START_MONTH%2FSTART_DAY%2FSTART_YEAR+00%3A00&enddate=END_MONTH%2FEND_DAY%2FEND_YEAR+00%3A00'

    sy,sm,sd = start_date
    start_date = datetime(sy,sm,sd)
    ey,em,ed = end_date
    end_date = datetime(ey,em,ed)
    url = url.replace('START_MONTH', str(start_date.month)).replace('START_DAY', str(start_date.day)).replace('START_YEAR', str(start_date.year))
    url = url.replace('END_MONTH', str(end_date.month)).replace('END_DAY', str(end_date.day)).replace('END_YEAR', str(end_date.year))
    url = url.replace('PATH', path).replace('TIMEZONE_', timezone)
    return url

    

def cwms_read(path, public, verbose = False, **kwargs):
    
    """
    A function to parse CWMS json data from webservice
        
    Positional Arguments: 
        path -- data path for web service (str), example: 'TDDO.Temp-Water.Inst.1Hour.0.GOES-REV' 
    
    Keyword Arguments:
        
        The web service can either get a lookback, which is just a number of 
        days from the current day, or a time window.  Two key word arguments are 
        needed for a time wondow, start_date, end_date.  The Timezone can also
        be set.
        
        lookback    --  The number of days from current day to grab data.
                        (int or str) 
                        example: 7
                        
        start_date  --  The start of a time window (tuple) formatted 
                        (year, month, day)
                        example: (2017, 3, 22)
                        
        end_date    --  The end of a time window (tuple) formatted 
                        (year, month, day)
                        example: (2017, 3, 22)
        
        timezone    --  "PST", "PDT", "MST", "MDT", "GMT"
                        
                        
    Returns:
        
        df -- A pandas dataframe with metadata from the webservice is returned.  
              Metadata is stored in df.__dict__['metadata'], the data is used in 
              some of the plotting functions.  The metadata is easily lost if a df
              is copied or transformed in some way.  It may be best to export the 
              metadata if it is needed.  meta = df.__dict__['metadata']
        
        
    """
    
    try:
        lookback = kwargs['lookback']
        end = datetime.now()
        start = end - datetime.timedelta(days=lookback)
        start_date = (start.year,start.month,start.day)
        end_date = (end.year,end.month,end.day)
        #url = r'http://pweb.crohms.org/dd/common/web_service/webexec/getjson?query=%5B%22PATH%22%5D&backward=LOOKBACKd'
        #url = url.replace('PATH', path).replace('LOOKBACK', str(lookback))
    except KeyError: 
        if verbose: print('No lookback, searching for start_data, end_date')
        try:
            start_date, end_date = kwargs['start_date'], kwargs['end_date']
            try: timezone = kwargs['timezone']
            except: timezone = 'PST'
            #url = time_window_url(path,start_date, end_date, public=public,timezone = timezone)
        except KeyError:
            raise ValueError('Set a lookback or time window with lookback = int, or start_date = (y,m,d), end_date = (y,m,d)')
    url = time_window_url(path,start_date, end_date, public=public,timezone = timezone)
    r = requests.get(url)
    json_data = json.loads(r.text)
   
    for site,data in json_data.items():
        lat = data['coordinates']['latitude']
        long = data['coordinates']['longitude']
        for path, vals in data['timeseries'].items():
            
            column_name = '_'.join(path.split('.')[:2])
            column_name = '_'.join(column_name.split('-'))
            try:path_data = vals['values']
            except KeyError: 
                
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
    try:        
        return df
    except UnboundLocalError:
        print('No data: ' + path)
        column_name = '_'.join(path.split('.')[:2])
        column_name = '_'.join(column_name.split('-'))
        return pd.DataFrame(columns = [column_name])
        
def merge(df1, df2):
    """
    Merges two dataframes created using cwms_read to preserve metadata
        
    Arguments: 
        df1 -- pandas.core.frame.DataFrame with .__dict__['metadata']
        df2 -- pandas.core.frame.DataFrame with .__dict__['metadata']
        
    Returns:
        df -- Merged pandas.core.frame.DataFrame with .__dict__['metadata']
    """
    try:
        meta = df1.__dict__['metadata']
    except KeyError:
        df1.__dict__['metadata'] = {}
        meta = df1.__dict__['metadata']
    try:
        meta2 = df2.__dict__['metadata']
    except KeyError:
        df2.__dict__['metadata'] = {}
        meta2 = df2.__dict__['metadata']
    meta.update(meta2)
   
    df = pd.concat([df1, df2], axis = 1)
    df.__dict__['metadata'] = meta
    return df
    


def get_cwms(paths, interval, verbose = False,public = True, **kwargs):
   
    """
    A function that calls cwms_read on a list to request multiple paths from 
    the CWMS webservice. Paths must be the same time interval, this is meant to 
    easily create a time series dataframe of multiple data
    
    Arguments:
        
        paths -- single string or list of string of CWMS data paths 
    
    Returns:
        
        df -- A pandas dataframe with metadata stored in df.__dict__['metadata']
        
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
        raise ValueError('Not all paths are the correct interval')
    
    df = pd.DataFrame()
    for path in paths:
        if verbose: print(path)
        df2 =cwms_read(path,public = public, **kwargs)
        if any(df2):df = df.pipe(merge, df2)
        
    return df

def catalog():
    
    """
    
    Requests the CWMS catalog.  Returns a large dict and not easy 
    wade through, it would be easier to go to a dataquery site to find 
    what you are looking for http://www.nwd-wc.usace.army.mil/dd/common/dataquery/www/
        
    Arguments: 
    
    Returns: dict
    
    """
    url = r'http://www.nwd-wc.usace.army.mil/dd/common/web_service/webexec/getjson?catalog=%5B%5D'
    r = requests.get(url)
    return json.loads(r.text)

def site_catalog(site):
    
    """
    Returns a dictionary of CWMS data paths for a particular site
    
    Arguments:
        site -- cwms site name, example TDDO
    
    Returns: 
        json.loads(r.text) -- dictionary of available site data
        
    """
    
    url = r'http://www.nwd-wc.usace.army.mil/dd/common/web_service/webexec/getjson?tscatalog=%5B%22SITE%22%5D'
    url = url.replace('SITE', site.upper())
    r = requests.get(url)
    return json.loads(r.text)

 


