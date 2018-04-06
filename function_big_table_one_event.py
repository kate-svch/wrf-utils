#!/usr/bin/env python3
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from scipy.io import netcdf
from time import strptime  # it's needed to get month number for a given month name
import csv
import model2



# THE SIZE OF THE TIME WINDOW IS DETERMINED HERE, in the text of program, DIRECTLY!!!

# this is just like "ml_set_creator_local_0.py" and "read_and_find_the_event" together and in a form of functions:
# the present functions enable to get the big table with all the information needed for ml-analysis
# swrf-data is obtained with use of function from "model2.py"
# the eventual result - the "big table" with the information about all the events fron some set could be made by multiple use of functions from this file
# multiple use of this file is organised by "run_parameters.py", which gets datetimes and thresholds of chosen events from text-file.

# everything above the threshold we consider being "the flux", everything under it - isn't "the flux"
# "start" and "end" are strings, "threshold" is an integer

def find_the_event(start, end, threshold, short_name_of_detector):
    print("The event under consideration starts at " + start)
    print("The event under consideration ends at " + end)
    print("The threshold value is " + str(threshold))
    
    
    start_finish_date_str = start + '_' + end;
#    name_of_detector = 'Stand_1_upper_1cm'
    #name_of_detector = 'NaI_2'
    
    name_of_detector = 'aaa';
    
    if (short_name_of_detector ==  'NaI_2'):
        name_of_detector = 'NaI_2';
        
    if (short_name_of_detector == 'Stand'):
         name_of_detector = 'Stand_1_upper_1cm'
         

    initial_data = pd.read_csv('/home/kate-svch/wrfmain/kate/reanalysis/csv_all/' + start_finish_date_str + '_' + name_of_detector + '.csv')
    output_file = '/home/kate-svch/wrfmain/kate/reanalysis/datetime_and_01/test_tables/' + start_finish_date_str + '_' + str(threshold) + '_dt_and_01.csv'
    # the following means that for "initial_time_unit = 1 min" - new time uniti turns out to be "resulting_time_unit = 10 min"
    size_of_time_window = 10;
    
    # those two are different units of time - "initial_time_unit" and "resulting_time_unit"
    initial_moments_of_event = 0;
    resulting_moments_of_event = 0;
    
    new_length_of_data = len(initial_data) // size_of_time_window;
    
    averaged_data = [0] * (new_length_of_data)
    averaged_whether_there_is_a_flux = [0] * (new_length_of_data)
    
    
    # the following "averaging" is "nre value is maximum value from the corresponding time interval"
    # =============================================================================
    # let's make an averaged data (from initial_data - for count rate):
    for new_time_j in range(0, new_length_of_data):
#        current_averaged_value = 0;
        for little_j in range(0, size_of_time_window ):
            time_j = new_time_j*size_of_time_window + little_j
            if (initial_data.iloc[time_j,1] > averaged_data[new_time_j] ):
                averaged_data[new_time_j] = initial_data.iloc[time_j,1]
            
    # the following makes "averaged_whether_there_is_a_flux" from "averaged_data" - just the result we need
    for new_time_j in range(0, new_length_of_data ):
        if (averaged_data[new_time_j]  > threshold):
            averaged_whether_there_is_a_flux[new_time_j] = 1;
            #print (whether_there_is_a_flux[time_j])
            resulting_moments_of_event = resulting_moments_of_event + 1;       
    # =============================================================================
    
    
    # here we make an array of datetime-objects for corresponding to "averaged_data" and "averaged_whether_there_is_a_flux" moments
    
    array_of_datetimes = [0] * (new_length_of_data)
            
    for new_time_j in range(0, new_length_of_data ):
        time_j = new_time_j*size_of_time_window + size_of_time_window//2;
        time_init_format = initial_data.iloc[time_j,0]
        year = 2000 + int(time_init_format[7])*10 + int(time_init_format[8])  # we could use int(time_init_format[7:9]) instead, if we wanted to
        day =  int(time_init_format[0])*10 + int(time_init_format[1])
        month = strptime(time_init_format[3:6],'%b').tm_mon
        hour = int(time_init_format[10])*10 + int(time_init_format[11])
        minute = int(time_init_format[13])*10 + int(time_init_format[14])
        array_of_datetimes[new_time_j] = datetime.datetime(year, month, day, hour, minute)   
    
            
    with open(output_file, "w") as output:
        for new_time_j in range(0, new_length_of_data ):
            output.write(str(array_of_datetimes[new_time_j]) + '      ' + str(averaged_whether_there_is_a_flux[new_time_j]) + '\n')
    
    
    print('we have ' + str(initial_moments_of_event) + ' initial_moments of event')
    print('we have ' + str(resulting_moments_of_event) + ' resulting_moments of event')
    print('we have ' + str(resulting_moments_of_event*size_of_time_window) + ' "initial_moments" of event - AFTER THE AVERAGING')
    
       
    plt.figure(figsize=(14,8))
    plt.plot(initial_data.iloc[:, 1])
    plt.title('Particle flux ', fontsize=22)
    plt.xlabel('time', fontsize=20, horizontalalignment='right' )
    plt.ylabel('Count rate', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
    plt.show()
    
    # Additional output: averaged flux and 0-1-results
    plt.figure(figsize=(14,8))
    plt.plot(averaged_data)
    plt.title('Averaged particle flux, time_window = '+ str(size_of_time_window) + ' min', fontsize=22)
    plt.xlabel('time', fontsize=20, horizontalalignment='right' )
    plt.ylabel('Count rate', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
    plt.show()
    
    plt.figure(figsize=(14,8))
    plt.plot( averaged_whether_there_is_a_flux)
    plt.title('averaged_whether_there_is_a_flux, threshold =  '+ str(threshold), fontsize=22)
    plt.xlabel('time', fontsize=20, horizontalalignment='right' )
    plt.ylabel('0_or_1', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
    plt.show()




def add_the_event_to_the_big_table(start, end, threshold, name_of_file):
# this file is used as "events" in what follows
#input_event_01_data = '/home/kate-svch/wrfmain/kate/reanalysis/datetime_and_01/current_set/' + start_finish_date_str + '_' + str(threshold) + '_dt_and_01.csv'

    print("The event under consideration starts at " + start)
    print("The event under consideration ends at " + end)
    
    x_lon = 45                                                                  # Index to d02 Aragats point
    y_lat = 45  
        
    year = int(start[0:4])
    month = int(start[5:7])
    day =  int(start[8:10])
    hour = int(start[11:13])
    dt_start = datetime.datetime(year, month, day, hour) 
    start_finish_date_str = start + '_' + end;
    
    model_datetime = dt_start;
#    model2.set_model_datetime(model_datetime)    
    wrf_step_minutes = 5;
    model_period = datetime.timedelta(minutes = wrf_step_minutes)
  
    file = model2.get_wrf_file(model_datetime)
    variable = file.variables['T2'].data[:]
    model_length = len(variable[:, y_lat, x_lon])
    
    
    # this is a file made by the previous function (find_the_event(start, end, threshold)) from this file:- times and 0-1-s
    events = pd.read_csv('/home/kate-svch/wrfmain/kate/reanalysis/datetime_and_01/test_tables/' + start_finish_date_str + '_' + str(threshold) + '_dt_and_01.csv', delimiter='     ', names=['date', 'TGE'])
    #events = pd.read_csv('/home/kate-svch/wrfmain/kate/reanalysis/datetime_and_01/current_set/' + start_finish_date_str + '_' + str(threshold) + '_dt_and_01.csv', delimiter='     ')
    events['fulltime'] = pd.to_datetime(events.date, format='%Y-%m-%d %H:%M:%S')
    
    events['t2'] = np.nan
    events['s_wind'] = np.nan
    
    q_vapor = model2.get_q(model_datetime, model_period, model_length, model_datetime, name='QVAPOR')
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
         
        events['t2'].iloc[ii] = model2.get_t2(model_datetime, model_period, model_length, date)[0]
        events['s_wind'].iloc[ii] = model2.get_s_wind(model_datetime, model_period, model_length, date)[0]        
        for i in range(len(q_vapor[0])):
            events['qvapor_'+str(i).zfill(2)].iloc[ii] = model2.get_q(model_datetime, model_period, model_length,date, name='QVAPOR')[0][i]
            events['qsnow_'+str(i).zfill(2)].iloc[ii] = model2.get_q(model_datetime, model_period, model_length,date, name='QSNOW')[0][i]
            events['qice_'+str(i).zfill(2)].iloc[ii] = model2.get_q(model_datetime, model_period, model_length,date, name='QICE')[0][i]
            events['qrain_'+str(i).zfill(2)].iloc[ii] = model2.get_q(model_datetime, model_period, model_length,date, name='QRAIN')[0][i]
            events['qgraup_'+str(i).zfill(2)].iloc[ii] = model2.get_q(model_datetime, model_period, model_length,date, name='QGRAUP')[0][i]
            events['qcloud_'+str(i).zfill(2)].iloc[ii] = model2.get_q(model_datetime, model_period, model_length,date, name='QCLOUD')[0][i]
            print (i)
        
        print(events.head())
    
    events.to_csv('/home/kate-svch/wrfmain/kate/reanalysis/datetime_and_01/big_tables_for_separate_events/' + name_of_file  + '_big_table.csv', mode='a')
    

# this test functioni just takes one file as "events" and rewrites it to the other file
def test_add_the_event(start, end, threshold, name_of_file):
# this file is used as "events" in what follows
#input_event_01_data = '/home/kate-svch/wrfmain/kate/reanalysis/datetime_and_01/current_set/' + start_finish_date_str + '_' + str(threshold) + '_dt_and_01.csv'

    print("The event under consideration starts at " + start)
    print("The event under consideration ends at " + end)
    
    year = int(start[0:4])
    month = int(start[5:7])
    day =  int(start[8:10])
    hour = int(start[11:13])
    dt_start = datetime.datetime(year, month, day, hour) 
    start_finish_date_str = start + '_' + end;
    
    model_datetime = dt_start;
#    model2.set_model_datetime(model_datetime)    
    wrf_step_minutes = 5;
    model_period = datetime.timedelta(minutes = wrf_step_minutes)
  
    file = model2.get_wrf_file(model_datetime)
    variable = file.variables['T2'].data[:]
    model_length = len(variable[:, y_lat, x_lon])
    
    
    # this is a file made by the previous function (find_the_event(start, end, threshold)) from this file:- times and 0-1-s
    events = pd.read_csv('/home/kate-svch/wrfmain/kate/reanalysis/datetime_and_01/current_set/' + start_finish_date_str + '_' + str(threshold) + '_dt_and_01.csv', delimiter='     ', names=['date', 'TGE'])
#    events = pd.read_csv('/home/kate-svch/wrfmain/kate/reanalysis/datetime_and_01/current_set/' + start_finish_date_str + '_' + str(threshold) + '_dt_and_01.csv', delimiter='     ')
    
    
    events.to_csv('/home/kate-svch/wrfmain/kate/reanalysis/datetime_and_01/big_tables_for_sets_of_events/' + name_of_file + '_big_table.csv', mode='a')    
