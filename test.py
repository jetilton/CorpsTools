# -*- coding: utf-8 -*-

import unittest
from CorpsTools import CWMSHydro
import CorpsTools
from TimeSeriesObj import TimeSeriesObj
import pandas 

c = CWMSHydro(7)

class CWMSHydroMethods(unittest.TestCase):
    
    def test_instance(self):
        
        self.assertTrue(isinstance(c, CorpsTools.CWMSHydro))
        
    def test_catalog(self):
        
        cat = c.catalog()
        self.assertTrue(isinstance(cat, dict))
        self.assertTrue(bool(cat))
        self.assertTrue(c.catalog()==c.cat)
        
    def test_sites(self):
        
        sites = c.sites()
        self.assertTrue(isinstance(sites, list))
        self.assertTrue(bool(sites))
    
    def test_site_catalog(self):
        
        site_cat = c.site_catalog('GCL')
        self.assertTrue(isinstance(site_cat, dict))
        self.assertTrue(bool(site_cat))
        
    def test_get_ts(self):
        path = 'GCL.Elev-Forebay.Ave.~1Day.1Day.CBT-REV'
        path_list = ['TDDO.Temp-Water.Inst.1Hour.0.GOES-REV','TDDO.Pres-Water-TotalGas.Inst.1Hour.0.GOES-REV']
        ts = c.get_ts(path, merge = False)
        c.get_ts(path, merge = True)
        self.assertTrue(isinstance(ts, TimeSeriesObj))
        self.assertTrue(isinstance(c.ts['daily'], pandas.core.frame.DataFrame))
        ts = c.get_ts(path_list)
        c.get_ts(path_list, merge = True)
        self.assertTrue(isinstance(c.ts['hourly'], pandas.core.frame.DataFrame))
        self.assertTrue(len(c.ts['hourly'].columns)==2)
        
        
    def test_merge(self):
        """
        Need more merge tests, '6hours'
        """
        path = 'TDDO.Temp-Water.Inst.1Hour.0.GOES-REV'
        path2 = 'TDDO.Pres-Water-TotalGas.Inst.1Hour.0.GOES-REV'
        ts = c.get_ts(path)
        ts2 = c.get_ts(path2)
        c.merge(ts)
        c.merge(ts2)
        df_hourly = c.ts['hourly']
        df_daily = c.ts['daily']
        self.assertTrue(isinstance(c.ts, TimeSeriesObj))
        self.assertTrue(len(c.ts.keys()) ==2)
        self.assertTrue(isinstance(df_daily,pandas.core.frame.DataFrame))
        self.assertTrue(isinstance(df_hourly,pandas.core.frame.DataFrame))
        with self.assertRaises(KeyError):
            c.ts['6hours']
    
    def test_plot(self):
        pass
            

if __name__ == '__main__':
    unittest.main()
