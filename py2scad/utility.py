"""
Copyright 2010  IO Rodeo Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import math

TAB_WIDTH = 4
#DEG2RAD = math.pi/180.0
#RAD2DEG = 180.0/math.pi
#DEG2RAD = math.degrees
#RAD2DEG = math.radians
DEG2RAD = math.radians
RAD2DEG = math.degrees

# Utility functions -----------------------------------------------------------
""" Depreciated!
def float_list2(v):
    _v = float_list(v)
    assert len(_v) == 2, 'v must be convertable to a length2 list'
    return _v

def float_list3(v):
    _v = float_list(v)
    assert len(_v) == 3, 'v must be convertible to a length 3 list'
    return _v

def float_list4(v):
    _v = float_list(v)
    assert len(_v) == 4, 'v must be convertible to a length 4 list'
    return _v

def float_list(v):
    _v = list(v)
    _v = [float(x) for x in _v]
    return _v
"""

def val_to_str(val ,tab_level=0):
    """Ensure misc values are nicely formatted."""
    tab_str = '' + ' '*TAB_WIDTH*tab_level
    if type(val) == str:
        return tab_str + val
    try: # For sequence types produce a comma seperated listing
        iter(val) # prescribed way to check for iteration...
        # Just because I like the fixed width numbers
        str_val = list()
        for item in val:
            if type(item) != str: # Format as float, five decimals precision
                item = "{0:0.5f}".format(item)
            str_val.append(item)
        return tab_str + '[' + ', '.join("{0}".format(item) for item in str_val) + ']'
    except TypeError: # Format as float, five decimals precision
        return tab_str + "{0:0.5f}".format(val)


def write_obj_list(obj_list, filename, fn=100):
    fid = open(filename,'w')
    fid.write('$fn=%d;\n'%(fn,))
    for obj in obj_list:
        fid.write('%s\n'%(obj,))
    fid.close()
