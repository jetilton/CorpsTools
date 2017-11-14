# -*- coding: utf-8 -*-
import copy
import pandas as pd


#def get_paths(ts_dict):
#    paths_dict = {}     
#    for interval,data in ts_dict.items():
#        paths = []
#        for columns, columns_data in data['column_data'].items():
#            paths.append(columns_data['path'])
#        paths_dict.update({interval:paths})
#    return paths_dict
#
#
#
#def merge_ts(ts_dict, new_ts_dict):
#    ts_dict = copy.deepcopy(ts_dict)
#    new_ts_dict = copy.deepcopy(new_ts_dict)
#    if not ts_dict:
#        return new_ts_dict
#    ts_paths = get_paths(ts_dict)
#    #new_ts_paths = get_paths(new_ts_dict)
#    for interval,data in new_ts_dict.items():
#        
#        try:ts_dict[interval]
#        except KeyError: 
#            ts_dict.update({interval:data})
#            continue
#        ts_df = ts_dict[interval]['df']
#        new_ts_df = new_ts_dict[interval]['df']
#        next_col_name = str((int(list(ts_df.columns)[-1])+1))
#        for column_name, column_data in data['column_data'].items():
#            if column_data['path'] not in ts_paths[interval]:
#                series = new_ts_df[column_name]
#                series.name = next_col_name
#                ts_df = pd.concat([ts_df, series], axis = 1)
#                ts_dict[interval]['column_data'].update({next_col_name:column_data})
#                next_col_name = str(int(next_col_name) + 1)
#            else: pass
#            ts_dict[interval]['df'] = ts_df
#    return ts_dict
#                
            
            

def get_paths(ts_dict):
    """
    Grabs all of the paths that are in a time series object
    these can be thought of as the column names for all of the interval df's
    """
    paths_dict = {}     
    for interval,data in ts_dict.items():
        paths = []
        for columns, columns_data in data.__dict__['metadata'].items():
            paths.append(columns_data['path'])
        paths_dict.update({interval:paths})
    return paths_dict

    
     
def merge_ts(ts1, ts2):
    if not ts1:
        ts1.update(ts2)
    
    df1_paths = get_paths(ts1)
    for interval, df in ts2.items():
        try:
            df1 = ts1[interval]
        except KeyError:
            ts1[interval] = df
            continue
        df2 = df
        df1_paths_interval = df1_paths[interval]
        df1_metadata = df1.__dict__['metadata']
        df2_metadata = df2.__dict__['metadata']
        next_col_name = str((int(list(df1.columns)[-1])+1))   
        for column_name, column_data in df2_metadata.items():
            if column_data['path'] not in df1_paths_interval:
                series = df2[column_name]
                series.name = next_col_name
                df1 = pd.concat([df1, series], axis = 1)
                df1_metadata.update({next_col_name:column_data})
                next_col_name = str(int(next_col_name) + 1)
            else: pass
        df1.metadata = df1_metadata
        ts1[interval] = df1
    return ts1