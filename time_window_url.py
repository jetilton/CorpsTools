from datetime import datetime
from math import floor

def full_time(time_float):
    if time_float > 1:
        remainder = time_float - int(time_float)
        time_float = floor(time_float)
    else: 
        remainder = time_float
        time_float = 0
    return(time_float,remainder)

def time_delta_parse(time_delta):
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
    
    if week<0:week = ''
    else: week = str(week)+'w'
    if day<0:day = ''
    else: day = str(day)+'d'
    if hour<0:hour = ''
    else: hour = str(hour)+'h'
    if minute<0:minute = ''
    else: minute = str(minute)+'m'   
    return(week,day,hour,minute)

def time_window_url(path, start_date, end_date, **kwargs):
    try:timezone = kwargs['timezone']
    except:timezone = 'PST'
    url = r'http://www.nwd-wc.usace.army.mil/dd/common/web_service/webexec/getjson?timezone=TIMEZONE_&backward=WEEK_DAY_HOUR_MINUTE_&forward=-END_WEEK_END_HOUR_END_MINUTE_&startdate=START_MONTH%2FSTART_DAY%2FSTART_YEAR+08%3A00&enddate=END_MONTH%2FEND_DAY%2FEND_YEAR+08%3A00&query=%5B%22PATH%22%2C%22PATH%22%5D'
    sy,sm,sd = start_date
    start_date = datetime(sy,sm,sd)
    ey,em,ed = end_date
    end_date = datetime(ey,em,ed)
    s_week,s_day,s_hour,s_minute = time_delta_parse(datetime.now() - start_date)
    s_week,s_day,s_hour,s_minute=url_w_d_h_m(s_week,s_day,s_hour,s_minute)
    e_week,e_day,e_hour,e_minute = time_delta_parse(datetime.now() - end_date)
    e_week,e_day,e_hour,e_minute=url_w_d_h_m(e_week,e_day,e_hour,e_minute)
    url = url.replace('END_WEEK_', s_week).replace('DAY_',s_day).replace('HOUR_', s_hour).replace('MINUTE_',s_minute)
    url = url.replace('WEEK_', s_week).replace('END_DAY_',s_day).replace('END_HOUR_', s_hour).replace('END_MINUTE_',s_minute)
    url = url.replace('START_MONTH', str(start_date.month)).replace('START_DAY', str(start_date.day)).replace('START_YEAR', str(start_date.year))
    url = url.replace('END_MONTH', str(end_date.month)).replace('END_DAY', str(end_date.day)).replace('END_YEAR', str(end_date.year))
    url = url.replace('PATH', path).replace('TIMEZONE_', timezone)
    return url
    
    
