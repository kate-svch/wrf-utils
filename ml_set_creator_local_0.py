#!/usr/bin/env python3
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from scipy.io import netcdf
import model2

# it makes the big table with use of file with "time_01" data (made by "read_and_find_the_event.py") and wrf-data (with means of "model2.py")



import argparse    # we'll get the data of the event, as an argument

parser = argparse.ArgumentParser(description='Great Description To Be Here')

parser.add_argument('--time_start', '-s', action='store', dest='start', help='It is a date-time of the beginning of the event', type=str)
parser.add_argument('--time_end', '-e', action='store', dest='end', help='It is a date-time of the end of the event', type=str)
parser.add_argument('--set-number', '-set', action='store', dest='set', help='It is the number of the set containing current event with the given threshold value', type=str)

args = parser.parse_args()

print("The event under consideration starts at " + args.start)
print("The event under consideration ends at " + args.end)

year = int(args.start[0:4])
month = int(args.start[5:7])
day =  int(args.start[8:10])
hour = int(args.start[11:13])
dt_start = datetime.datetime(year, month, day, hour) 
start_finish_date_str = args.start + '_' + args.end;

#print('Date-time of the beginning of the event is ' + str(dt_start)) 
#print('start_finish_date_str is '+ start_finish_date_str);

# DEFINE THE TIME INTERVAL HERE
#start_finish_date_str = '2016-05-04-00_2016-05-05-00';

#model_datetime = datetime.datetime(2016, 4, 26, 12, 0)


model_datetime = dt_start;
model2.set_model_datetime(model_datetime)


# this is a file made by "read_and_find_the_event.py" - times and 0-1-s
#events = '/home/kate-svch/wrfmain/kate/reanalysis/datetime_and_01/3_set/' + start_finish_date_str + '_dt_and_01.csv'

#output_file = '/home/kate-svch/wrfmain/kate/reanalysis/datetime_and_01/big_tables_about_events/' + start_finish_date_str + '_big_table.csv'


events = pd.read_csv('/home/kate-svch/wrfmain/kate/reanalysis/datetime_and_01/'+ str(args.set) +'_set/' + start_finish_date_str + '_dt_and_01.csv', delimiter='     ', names=['date', 'TGE'])

events['fulltime'] = pd.to_datetime(events.date, format='%Y-%m-%d %H:%M:%S')

events['t2'] = np.nan
events['s_wind'] = np.nan

q_vapor = model2.get_q(model_datetime, name='QVAPOR')
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
     
    events['t2'].iloc[ii] = model2.get_t2(date)[0]
    events['s_wind'].iloc[ii] = model2.get_s_wind(date)[0]
    for i in range(len(q_vapor[0])):
        events['qvapor_'+str(i).zfill(2)].iloc[ii] = model2.get_q(date, name='QVAPOR')[0][i]
        events['qsnow_'+str(i).zfill(2)].iloc[ii] = model2.get_q(date, name='QSNOW')[0][i]
        events['qice_'+str(i).zfill(2)].iloc[ii] = model2.get_q(date, name='QICE')[0][i]
        events['qrain_'+str(i).zfill(2)].iloc[ii] = model2.get_q(date, name='QRAIN')[0][i]
        events['qgraup_'+str(i).zfill(2)].iloc[ii] = model2.get_q(date, name='QGRAUP')[0][i]
        events['qcloud_'+str(i).zfill(2)].iloc[ii] = model2.get_q(date, name='QCLOUD')[0][i]
        print (i)



    print(events.head())

events.to_csv('/home/kate-svch/wrfmain/kate/reanalysis/datetime_and_01/big_tables_about_events/' + start_finish_date_str + '_table.csv')
