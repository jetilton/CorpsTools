# -*- coding: utf-8 -*-

dictionary = t['hourly']



describe_dict = {}
for column,value in dictionary['column_data'].items():
    
    column_name = value['path']
    parameter = value['parameter']
    units = value['units']
    