# -*- coding: utf-8 -*-

def check_obj(obj, obj_type):
    try:
        raise TypeError(obj)
    except TypeError as e:  # as e syntax added in ~python2.5
        if not isinstance(obj, obj_type):
            raise