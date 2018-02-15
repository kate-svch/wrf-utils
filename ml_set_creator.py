#!/usr/bin/env python3
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from scipy.io import netcdf
import model


model_datetime = datetime.datetime(2016, 5, 4, 0, 0)
model.set_model_datetime(model_datetime)

events = pd.read_csv('testdata.csv', delimiter='     ', names=['date', 'TGE'])

events['fulltime'] = pd.to_datetime(events.date, format='%Y-%m-%d %H:%M:%S')

events['t2'] = np.nan
events['s_wind'] = np.nan

q_vapor = model.get_q(model_datetime, name='QVAPOR')
for i in range(len(q_vapor[0])):
    events['qvapor_'+str(i).zfill(2) ] = np.nan
    events['qsnow_'+str(i).zfill(2) ] = np.nan
    events['qice_'+str(i).zfill(2) ] = np.nan
    events['qrain_'+str(i).zfill(2) ] = np.nan
    events['qgraup_'+str(i).zfill(2) ] = np.nan
    events['qcloud_'+str(i).zfill(2) ] = np.nan
    
for ii, d in events.iterrows():
    print (ii)
    date = d.fulltime
     
    events['t2'].iloc[ii] = model.get_t2(date)[0]
    events['s_wind'].iloc[ii] = model.get_s_wind(date)[0]
    for i in range(len(q_vapor[0])):
        events['qvapor_'+str(i).zfill(2)].iloc[ii] = model.get_q(date, name='QVAPOR')[0][i]
        events['qsnow_'+str(i).zfill(2)].iloc[ii] = model.get_q(date, name='QSNOW')[0][i]
        events['qice_'+str(i).zfill(2)].iloc[ii] = model.get_q(date, name='QICE')[0][i]
        events['qrain_'+str(i).zfill(2)].iloc[ii] = model.get_q(date, name='QRAIN')[0][i]
        events['qgraup_'+str(i).zfill(2)].iloc[ii] = model.get_q(date, name='QGRAUP')[0][i]
        events['qcloud_'+str(i).zfill(2)].iloc[ii] = model.get_q(date, name='QCLOUD')[0][i]
        print (i)



    print(events.head())

events.to_csv('traindata.csv')
