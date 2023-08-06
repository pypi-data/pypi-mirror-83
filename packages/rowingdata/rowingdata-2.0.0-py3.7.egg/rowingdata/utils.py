from __future__ import absolute_import
import math
import numpy as np
import re
import time
import matplotlib
import iso8601
import os
import pytz
import pickle
import pandas as pd
import datetime
from math import sin,cos,atan2,sqrt
from pandas import Series,DataFrame

def ewmovingaverage(interval,window_size):
    # Experimental code using Exponential Weighted moving average

    intervaldf=DataFrame({'v':interval})
    idf_ewma1=intervaldf.ewm(span=window_size)
    idf_ewma2=intervaldf[::-1].ewm(span=window_size)

    i_ewma1=idf_ewma1.mean().ix[:,'v']
    i_ewma2=idf_ewma2.mean().ix[:,'v']

    interval2=np.vstack((i_ewma1,i_ewma2[::-1]))
    interval2=np.mean( interval2, axis=0) # average

    return interval2

def movingaverage(interval, window_size):
    window=np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

def geo_distance(lat1,lon1,lat2,lon2):
    """ Approximate distance and bearing between two points
    defined by lat1,lon1 and lat2,lon2
    This is a slight underestimate but is close enough for our purposes,
    We're never moving more than 10 meters between trackpoints

    Bearing calculation fails if one of the points is a pole. 
    
    """
    
    # radius of earth in km
    R=6373.0

    # pi
    pi=math.pi

    lat1=math.radians(lat1)
    lat2=math.radians(lat2)
    lon1=math.radians(lon1)
    lon2=math.radians(lon2)

    dlon=lon2 - lon1
    dlat=lat2 - lat1

    a=sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c=2 * atan2(sqrt(a), sqrt(1 - a))

    distance=R * c

    tc1=atan2(sin(lon2-lon1)*cos(lat2),
                cos(lat1)*sin(lat2)-sin(lat1)*cos(lat2)*cos(lon2-lon1))

    tc1=tc1 % (2*pi)

    bearing=math.degrees(tc1)

    return [distance,bearing]

def totimestamp(dt, epoch=datetime.datetime(1970,1,1,0,0,0,0,pytz.UTC)):
    try:
        td=dt - epoch
    except TypeError:
        dt = pytz.utc.localize(dt)
        td = dt - epoch
    # return td.total_seconds()
    return (td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6


def format_pace(x,pos=None):
    if np.isinf(x) or np.isnan(x):
        x=0
        
    min=int(x/60)
    sec=(x-min*60.)

    str1="{min:0>2}:{sec:0>4.1f}".format(
        min=min,
        sec=sec
    )

    return str1

def format_time(x,pos=None):


    min=int(x/60.)
    sec=int(x-min*60)

    str1="{min:0>2}:{sec:0>4.1f}".format(
        min=min,
        sec=sec,
        )

    return str1

def wavg(group, avg_name, weight_name):
    """ http://stackoverflow.com/questions/10951341/pandas-dataframe-aggregate-function-using-multiple-columns
    In rare instance, we may not have weights, so just return the mean. Customize this if your business case
    should return otherwise.
    """
    d = group[avg_name]
    w = group[weight_name]
    try:
        return (d * w).sum() / w.sum()
    except ZeroDivisionError:
        return d.mean()
