# cwms_read

Python and R functions to call time series data from the [Corps Water Management System (CWMS) webserveice](https://github.com/gunnarleffler/hydroJSON).
CWMS is the automated information system supporting the USACE Water Management mission.
It integrates real-time data acquisition, database storage, flow forecasting of watershed runoff, reservoir operation decision support, river profile modeling, inundated area determination,
consequence /damage analysis, and information dissemination into a comprehensive suite of software supporting water management decision processes.  Inition develpment began in 1997 and is ongoing.  
[source](http://www.hec.usace.army.mil/FactSheets/CWMS/HEC_FactSheet_CWMS.pdf)

cwms_read consists of one simple function to export time series data from the CWMS database into either Python or R.  

## Mission
USACE is responsible for round-the-clock monitoring and operation of more than 700 reservoir, lock-and-dam projects.  
There is a need to provide real-time decision support for the USACE water management mission.
cwms_read intends to provide ease of access to CWMS data for scientists and engineers to be able to make data driven decisions.


### Prerequisites

#### Python 
    - Python 3.6+
    - Pandas
    - json
    - requests

This may work on Python 2.75, but it has not been tested.

or

#### R
    - R V?
    - lubridate
    - magrittr
    - data.table

### Installing

To run in Python activate the desired environment from the command line or create a new one.

##### Windows:
```
activate environment_name
```
###### Mac:
```
source activate environment_name
```
##### With pip:
```
pip install git+https://github.com/jetilton/cwms_read.git
```
or
```
pip install --upgrade git+https://github.com/jetilton/cwms_read.git
```

I am not as familiar with R.  The function in cwms_read.r is up and running, but it has not been tested.  Copy and paste the function into R and use it as a function instead of a required library.



#### Python Examples

##### get_cwms
The main function of this package is `get_cwms`, which requires a time series path name, a desired interval (hour, 6hour, daily), 
and either an integer lookback in days or a specified date interval.

```python
from cwms_read.cwms_read import get_cwms
import pandas as pd

path = 'TDDO.Temp-Water.Inst.1Hour.0.GOES-REV'

df1 = get_cwms(path, lookback = 7, public = True, fill = False)
df1.head()

Out[1]: 
                     TDDO_Temp_Water
date                                
2018-02-09 08:00:00           42.224
2018-02-09 09:00:00           42.188
2018-02-09 10:00:00           42.188
2018-02-09 11:00:00           42.152
2018-02-09 12:00:00           42.116




paths = paths = ['LGNW.Temp-Water.Inst.1Hour.0.GOES-REV','LGNW.Pres-Water-TotalGas.Inst.1Hour.0.GOES-REV',
                 'TDDO.Temp-Water.Inst.1Hour.0.GOES-REV','TDDO.Pres-Water-TotalGas.Inst.1Hour.0.GOES-REV']

df2 = get_cwms(paths, start_date = (2016, 3, 1), end_date = (2017, 3, 1), timezone = 'PST', fill = True)

df2.head()

Out[4]: 
                     LGNW_Pres_Water_TotalGas  LGNW_Temp_Water  \
date                                                             
2016-03-01 00:00:00                     762.0           40.748   
2016-03-01 01:00:00                     762.0           40.748   
2016-03-01 02:00:00                     762.0           40.766   
2016-03-01 03:00:00                     762.0           40.784   
2016-03-01 04:00:00                     762.0           40.784   

                     TDDO_Pres_Water_TotalGas  TDDO_Temp_Water  
date                                                            
2016-03-01 00:00:00                     768.0            42.75  
2016-03-01 01:00:00                     768.0            42.75  
2016-03-01 02:00:00                     768.0            42.76  
2016-03-01 03:00:00                     768.0            42.76  
2016-03-01 04:00:00                     770.0            42.76  

```

##### Metadata
The dataframes store metadata in `__dict__`

```python

df1.__dict__['metadata']

Out[5]: 
{'TDDO_Temp_Water': {'active_flag': 1,
  'count': 167,
  'duration': ' ',
  'end_timestamp': '2018-02-16T06:00:00',
  'interval': ' ',
  'lat': 45.60734258,
  'long': -121.1734044,
  'max_value': 42.224,
  'min_value': 40.892,
  'notes': '(1996-2018)',
  'parameter': 'Temp-Water',
  'path': 'TDDO.Temp-Water.Inst.1Hour.0.GOES-REV',
  'quality_type': 'string',
  'sigfig': 3,
  'site_quality': [],
  'start_timestamp': '2018-02-09T08:00:00',
  'tz_offset': -8,
  'units': 'F'}}

```

It is best to export this into a standalone dictionary because it can be lost during dataframe operations.

```python

df1 = df1.melt()


df1.__dict__['metadata']

Traceback (most recent call last):

  File "<ipython-input-8-898703322289>", line 1, in <module>
    df1.__dict__['metadata']

KeyError: 'metadata'
```
##### Catalogs
There are also two catalog options.  One to get all of the pathnames for a particular
site (`site_catalog()`), the other retrieves all available site paths (`catalog()`).


```python
site_catalog('tddo')


Out[3]: 
{'TDDO': {'HUC': '',
  'active_flag': 'T',
  'coordinates': {'datum': 'NAD83',
   'latitude': 45.60734258,
   'longitude': -121.1734044},
  'elevation': {'accuracy': 0.0,
   'datum': 'NGVD29',
   'method': '',
   'value': 0.0},
  'location_type': ' ',
  'name': 'Columbia R bl The Dalles Dam WQS',
  'responsibility': 'NWDP',
  'time_format': '%Y-%m-%dT%H:%M:%S%z',
  'timeseries': {'TDDO.%-Saturation-TDG.Inst.1Hour.0.GOES-COMPUTED-REV': {'notes': '(2005-2017)'},
   'TDDO.Depth-WQSensors.Inst.1Hour.0.GOES-REV': {'notes': '(2000-2017)'},
   'TDDO.Depth-WQSensors.Inst.1Hour.0.USGS-REV': {'notes': '(2007-2017)'},
   'TDDO.Flow.Inst.~30Minutes.0.USGS-RAW': {'notes': '(2003-2017)'},
   'TDDO.Pres-Air.Inst.1Hour.0.GOES-REV': {'notes': '(1996-2017)'},
   'TDDO.Pres-Air.Inst.1Hour.0.USGS-REV': {'notes': '(2007-2017)'},
   'TDDO.Pres-Water-TotalGas.Inst.1Hour.0.GOES-REV': {'notes': '(1996-2017)'},
   'TDDO.Pres-Water-TotalGas.Inst.1Hour.0.USGS-REV': {'notes': '(2007-2017)'},
   'TDDO.Stage.Inst.1Hour.0.GOES-RAW': {'notes': '(2010-2015)'},
   'TDDO.Stage.Inst.~30Minutes.0.USGS-RAW': {'notes': '(2014-2017)'},
   'TDDO.Temp-Water.Inst.1Hour.0.GOES-REV': {'notes': '(1996-2017)'},
   'TDDO.Temp-Water.Inst.1Hour.0.USGS-REV': {'notes': '(2007-2017)'}},
  'timezone': 'PST',
  'tz_offset': -8}}
  
  
  
cat = catalog() 
len(cat.keys())
Out[6]: 6002

```
A better way to explore unknown sites is to visit the [Northwest Division Dataquery website](http://pweb.crohms.org/dd/common/dataquery/www/index.html).
THis website allows for full name searches, and then will display the site's acronym.

## Authors

* **Jeff Tilton**

## Acknowledgments

* [Corps Water Management System (CWMS) webserveice](https://github.com/gunnarleffler/hydroJSON)

