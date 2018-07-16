# -*- coding: utf-8 -*-

import unittest
import pandas as pd
from cwms_read import get_cwms


class GetCwmsTest(unittest.TestCase):
    
    paths = [
    
        'MCN.Flow-Spill-Cap-Fish.Inst.~1Day.0.CENWDP-COMPUTED-PUB', 
        'MCN.Flow-Spill.Ave.1Hour.1Hour.CBT-REV',
        'MCPW.%-Saturation-TDG.Ave.~1Day.12Hours.CENWDP-COMPUTED-Combined-REV',
        'JDY.%-Saturation-TDG.Ave.~1Day.12Hours.CENWDP-COMPUTED-WAmethod-REV',
        
        'JDA.Flow-Spill-Cap-Fish.Inst.~1Day.0.CENWDP-COMPUTED-PUB', 
        'JDA.Flow-Spill.Ave.1Hour.1Hour.CBT-REV',
        'JHAW.%-Saturation-TDG.Ave.~1Day.12Hours.CENWDP-COMPUTED-Combined-REV',
        'TDA.%-Saturation-TDG.Ave.~1Day.12Hours.CENWDP-COMPUTED-WAmethod-REV',
         
        'TDA.Flow-Spill-Cap-Fish.Inst.~1Day.0.CENWDP-COMPUTED-PUB', 
        'TDA.Flow-Spill.Ave.1Hour.1Hour.CBT-REV',
        'TDDO.%-Saturation-TDG.Ave.~1Day.12Hours.CENWDP-COMPUTED-Combined-REV',
        'BON.%-Saturation-TDG.Ave.~1Day.12Hours.CENWDP-COMPUTED-WAmethod-REV',
    
        'BON.Flow-Spill-Cap-Fish.Inst.~1Day.0.CENWDP-COMPUTED-PUB', 
        'BON.Flow-Spill.Ave.1Hour.1Hour.CBT-REV',
        'CCIW.%-Saturation-TDG.Ave.~1Day.12Hours.CENWDP-COMPUTED-Combined-REV',
        
        
        ]
    col_names=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o']
    start_date = (2016, 5, 1)
    end_date = (2016, 7, 1)
    def test_public(self):
        data = get_cwms(self.paths, start_date = self.start_date, end_date = self.end_date, public = True, fill = True)
        
        self.assertTrue(isinstance(data, pd.DataFrame))
    
    def test_private(self):
        data = get_cwms(self.paths, start_date = self.start_date, end_date = self.end_date, public = False, fill = True)
        self.assertTrue(isinstance(data, pd.DataFrame))
        
    def test_column_order(self):
        data = get_cwms(self.paths, start_date = self.start_date, end_date = self.end_date, public = False, fill = True)
        self.assertTrue(self.paths == list(data.columns))
    def test_column_names(self):
        data = get_cwms(self.paths,col_names=self.col_names, start_date = self.start_date, end_date = self.end_date, public = False, fill = True)
        self.assertTrue(self.col_names == list(data.columns))

if __name__ == '__main__':
    unittest.main()



