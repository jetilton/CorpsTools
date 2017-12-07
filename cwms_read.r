library(lubridate)
library(data.table)
library(magrittr)
time_parse = function(time1, time2){
  
  time = as.numeric(difftime(time2,time1))
  forward_weeks = time / 7
  forward_days = (forward_weeks - as.integer(forward_weeks)) * 7
  forward_hours = (forward_days - as.integer(forward_days)) * 24
  forward_minutes = (forward_hours - as.integer(forward_hours)) * 60
  times = c(forward_weeks,forward_days,forward_hours,forward_minutes)
  v = c()
  for (i in 1:length(times)){
    v[i] = as.integer(times[i])
    
  }
  return(v)
}



time_window_url = function(path, start_date, end_date, timezone = 'PST'){
  url = 'http://nwp-wmlocal2.nwp.usace.army.mil/common/web_service/webexec/getjson?timezone=TIMEZONE&query=%5B%22PATH%22%2C%22PATH%22%5D&startdate=START_MONTH%2FSTART_DAY%2FSTART_YEAR+00%3A00&enddate=END_MONTH%2FEND_DAY%2FEND_YEAR+00%3A00'
  
  start_date = strptime(start_date,"%Y-%m-%d")
  end_date = strptime(end_date, "%Y-%m-%d")
  now = strptime(Sys.time(),"%Y-%m-%d %H:%M:%S")
  
  
  start = time_parse(start_date, now)
  end = time_parse(end_date, now)
  s_week = paste(start[1], 'w', sep ='')
  s_day = paste(start[2], 'd', sep ='')
  s_hour = paste(start[3], 'h', sep ='')
  s_minute = paste(start[4], 'm', sep ='')
  e_week = paste(end[1], 'w', sep ='')
  e_day = paste(end[2], 'd', sep ='')
  e_hour = paste(end[3], 'h', sep ='')
  e_minute = paste(end[4], 'm', sep ='')
  start_month = toString(month(start_date))
  start_day = toString(day(start_date))
  start_year = toString(year(start_date))
  end_month = toString(month(end_date))
  end_day = toString(day(end_date))
  end_year = toString(year(end_date))
  
  
  
  url = gsub('BACKWARD_WEEK_', s_week, url) %>% gsub('BACKWARD_DAY_',s_day,.) %>% 
      gsub('BACKWARD_HOUR_', s_hour, .) %>% gsub('BACKWARD_MINUTE_',s_minute, .) %>%
      gsub('FORWARD_WEEK_', e_week, .) %>% gsub('FORWARD_DAY_',e_day, .) %>% 
      gsub('FORWARD_HOUR_', e_hour, .) %>% gsub('FORWARD_MINUTE_',e_minute, .) %>% 
      gsub('START_MONTH', start_month,.) %>% gsub('START_DAY', start_day, .) %>%
      gsub('START_YEAR', start_year, .) %>% gsub('END_MONTH', end_month,.) %>%
      gsub('END_DAY', end_day, .) %>% gsub('END_YEAR', end_year, .)  %>% 
      gsub("PATH", path, .)  %>% gsub('TIMEZONE', timezone, .)
  
  
  return(url)
  
}


cwms_data_parse = function(data, column){
  value = data[column][[1]]
  return(value) 
}


cwms_to_dt = function(path, start_date, end_date, timezone = 'PST'){
  url = time_window_url(path, start_date, end_date, timezone = 'PST')
  data = rjson::fromJSON(file=url)
  paste(paste('`',path,sep=''),'`',sep='')
  x = data[[1]]$timeseries[[1]]$values
  name = strsplit(path, split = "\\.")[[1]]
  name = paste(name[1],name[2], sep = '_')
  dt = data.table(date = unlist(lapply(x,cwms_data_parse,1)), 
                  value = unlist(lapply(x,cwms_data_parse,2)))
  dt$value = as.numeric(dt$value)
  setnames(dt, c('date', name))
  dt$date = as.POSIXct(dt$date, format = "%Y-%m-%dT%H:%M:%S")
  return(dt)
}



get_cwms = function(paths, start_date, end_date, timezone = 'PST'){

  dt = lapply(paths,cwms_to_dt, start_date = start_date, end_date = end_date, timezone = timezone)
  return(Reduce(merge,dt))
}



