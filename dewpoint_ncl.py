#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 17:01:29 2018

@author: kate-svch
"""

from __future__ import print_function

import os
from netCDF4 import Dataset
from wrf import getvar, ALL_TIMES
import matplotlib.pyplot as plt
import pandas as pd     
import datetime   
from math import ceil        # rounding up  ^_^
from time import strptime  # it's needed to get month number for a given month name

import model2

x_lon = 45;   y_lat = 45;   

#current_folder = '/mnt/data-internal/reanalysis'    # this is the folder for the 2018-03-05 event

current_folder = '/mnt/data-internal/newversion'
#current_folder = '/mnt/data-internal/newversion/forecast'

def get_dewpoint_t_profile_in_certain_moment_of_time(model_datetime, model_period, model_length, the_time_moment):
      
# get quantity of "name" microphysical fracture from 2m to 20 kilometers height : DIFFERENT HEIGHT ANG TIME
   
    time_index = model2.get_index(model_datetime, model_period, model_length, the_time_moment, 1 )
    path = os.path.join(current_folder) + '/' 
    path = os.path.join(path, datetime.datetime.strftime(model_datetime, '%Y%m%d%H'))
    file_name = path  + '/wrfout_d02_'  + datetime.datetime.strftime(model_datetime, '%Y-%m-%d_%H:00:00')
    ncfile = Dataset(file_name)
    t_dewpoint =  getvar(ncfile, 'td', units='degC', timeidx = ALL_TIMES)
    return t_dewpoint[time_index, :, y_lat, x_lon]


def dewpoint_in_time(model_datetime, model_period, model_length, event_datetime, number_of_time_points):
      
# get quantity of "name" microphysical fracture from 2m to 20 kilometers height : DIFFERENT HEIGHT ANG TIME
   
    time_index = model2.get_index(model_datetime, model_period, model_length, event_datetime, number_of_time_points)
    path = os.path.join(current_folder) + '/' 
    path = os.path.join(path, datetime.datetime.strftime(model_datetime, '%Y%m%d%H'))
    file_name = path  + '/wrfout_d02_'  + datetime.datetime.strftime(model_datetime, '%Y-%m-%d_%H:00:00')
    ncfile = Dataset(file_name)
    t_dewpoint =  getvar(ncfile, 'td', units='degC', timeidx = ALL_TIMES)
    return t_dewpoint[time_index : time_index + number_of_time_points, 0, y_lat, x_lon]


def cloud_base_height_from_temperature_and_dp_profiles(model_datetime, model_period, model_length, the_time_moment, z_vector):
    
    temperature = model2.get_t_profile_in_certain_moment_of_time(model_datetime, model_period, model_length, the_time_moment)
    t_dp = get_dewpoint_t_profile_in_certain_moment_of_time(model_datetime, model_period, model_length, the_time_moment)
    initial_signum = (temperature[0] < t_dp[0])    
    for j_in_z in range(1, len(t_dp)):
        signum = (temperature[j_in_z] < t_dp[j_in_z])
        if signum != initial_signum : return (z_vector[j_in_z - 1])
    return (-2);


def cloud_base_in_time(model_datetime, model_period, model_length, number_of_time_points, z_vector):
    
    cloud_base_height_t = [-1]*number_of_time_points;
    for j_in_time in range(0, number_of_time_points):
        cloud_base_height_t[j_in_time] = cloud_base_height_from_temperature_and_dp_profiles(model_datetime, model_period, model_length, model_datetime + model_period*j_in_time, z_vector)
    return cloud_base_height_t    


def main():
    
#    x_lon = 45;  y_lat = 45;    
# =============================================================================
#     event_datetime = datetime.datetime(2018, 3, 4, 18, 0) 
#     
#     time_point_of_start = 91;
#     number_of_time_points = 25;
#     start_hour = event_datetime.hour;    step = 1/12;
#     
#     model_height = model2.get_geopotential_height(event_datetime, time_point_of_start  = 1)     
#     event_time = model2.create_time_array_in_hours(start_hour, event_datetime, number_of_time_points, step, time_point_of_start);
# =============================================================================
    
    
    
    wrf_step_minutes = 5;
    model_period = datetime.timedelta(minutes = wrf_step_minutes)
#model2.set_model_datetime(datetime.datetime(2018, 3, 4, 18, 0) , wrf_step_minutes)        # the second argument is the value of time step, in minutes

    model_datetime = datetime.datetime(2017, 10, 1, 6, 0)
    event_finish_datetime = datetime.datetime(2017, 10, 2, 12, 0) 
    the_time_moment = datetime.datetime(2017, 10, 1, 23, 00)       
  

    file = model2.get_wrf_file(model_datetime)
    variable = file.variables['T2'].data[:]
    model_length = len(variable[:, y_lat, x_lon])
    
    start_date_str = '2017-10-01-06-00';       # this is time of start of the event, so EVERYWHERE BELOW "time_point_of_start = 0" !!!
    event_datetime = datetime.datetime(int(start_date_str[0:4]), int(start_date_str[5:7]), int(start_date_str[8:10]), int(start_date_str[11:13]), int(start_date_str[14:16]))  
    csv_folder = '/home/kate-svch/wrfmain/kate/reanalysis/csv_measurements/' + start_date_str + '/';
    
     # here we have an automatical "numnber_of_time_points"-initialization  
    number_of_time_points  = int ((event_finish_datetime - event_datetime)/datetime.timedelta(0, 0, 0, 0, wrf_step_minutes))
      
       
    z_vector = model2.get_height(model_datetime)[:-1]/1000
    time_vector = [event_datetime + datetime.timedelta(minutes=wrf_step_minutes * i) for i in range(number_of_time_points )]    
    
    

# =============================================================================
#     plt.figure(figsize=(18,8))
#     plt.title('Dewpoint-temperature profile' , fontsize=22)
#     plt.xlabel('z, km', fontsize=20, horizontalalignment='right' )
#     plt.ylabel('T, C', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#     plt.plot(model_height, get_dewpoint_t_profile_in_certain_moment_of_time(event_datetime, time_point_of_start  = 1))
#     plt.show()
# =============================================================================
    
    plt.figure(figsize=(18,8))
    plt.title('Temperature and dewpoint profiles' , fontsize=22)
    plt.xlabel('z, km', fontsize=20, horizontalalignment='right' )
    plt.ylabel('T, C', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
    plt.plot(z_vector, model2.get_t_profile_in_certain_moment_of_time(model_datetime, model_period, model_length, the_time_moment ), label = 'T')
    plt.plot(z_vector, get_dewpoint_t_profile_in_certain_moment_of_time (model_datetime, model_period, model_length, the_time_moment), label = 'Td')
    plt.legend(fontsize=20,loc=1)
    plt.show()
    
    print ('The value of cloud-height, estimated with use of temperature profiles, is ', cloud_base_height_from_temperature_and_dp_profiles(model_datetime, model_period, model_length, the_time_moment, z_vector), ' km.')
        
    plt.figure(figsize=(18,8))
    plt.title('Dewpoint-temperature, ground level' , fontsize=22)
    plt.xlabel('time', fontsize=20, horizontalalignment='right' )
    plt.ylabel('T, C', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
    plt.plot(time_vector, dewpoint_in_time(model_datetime, model_period, model_length, event_datetime, number_of_time_points))
    plt.xlim(time_vector[0]  , time_vector[-1] )
    plt.show()
    
    
    name_of_value = 'dewpoint'
#    csv_folder = '/home/kate-svch/wrfmain/kate/reanalysis/csv_measurements/' + start_date_str + '/';
#    csv_data = pd.read_csv('/home/kate-svch/wrfmain/kate/reanalysis/csv_measurements/'+ start_date_str + '_' + name_of_value  + '.csv')
    csv_data = pd.read_csv(csv_folder + start_date_str + '_' + name_of_value  + '.csv')

    csv_length = len(csv_data)
    csv_time =  [0] * csv_length
    
# =============================================================================
#     if (number_of_time_points !=  int(csv_length/5) + 1 ) :
#         print('Different number_of_time_points for wrf and csv!!!')
# # THIS SHOULD BE MADE MORE UNIFORM!!!
# =============================================================================
    
    for jj in range (0, csv_length):
        jj_day =  int(csv_data.iloc[jj, 0][0:2])
        jj_hour =  int(csv_data.iloc[jj, 0][10:12])
        jj_minute =  int(csv_data.iloc[jj, 0][13:15])
        jj_second =  int(csv_data.iloc[jj, 0][16:18])
        jj_year = int(csv_data.iloc[jj, 0][7:9])
        jj_month = strptime(csv_data.iloc[jj, 0][3:6],'%b').tm_mon
    #    csv_time[jj] = csv_data.iloc[jj, 0][0:15]
        csv_time[jj]  = datetime.datetime(jj_year, jj_month, jj_day, jj_hour, jj_minute, jj_second)
    
    
    
    
    plt.figure(figsize=(14,8))
    # this line draws the graph: y is values from the second column, x is numbers of the columns
    plt.plot(csv_time, csv_data.iloc[:, 1])
    # here "1" is our chose of the column (the second one), ":" means "take every row"
    plt.title(name_of_value+ ' csv', fontsize=22)
    plt.xlabel('time', fontsize=20, horizontalalignment='right' )
    plt.ylabel('T, C', rotation='horizontal', fontsize=24, horizontalalignment='right', verticalalignment='top')
    plt.locator_params(axis='y', nbins=10)
    plt.locator_params(axis='x', nbins=4)
    plt.show()
    
    
    wrf_dewpoint_vector = model2.get_t2(model_datetime, model_period, model_length, event_datetime, number_of_time_points);
    
    # this is to get a test curve with wrf-temperature
    # =============================================================================
    # plt.figure(figsize=(14,8))
    # plt.title('WRF temperatures in time, ground level' , fontsize=22)
    # plt.xlabel('time', fontsize=20, horizontalalignment='right' )
    # plt.ylabel('T, C', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
    # plt.plot(wrf_temperature_vector, linewidth=3, label='wrf')
    # plt.legend(fontsize=20,loc=1)
    # plt.show()
    # 
    # =============================================================================
    
    
#    coef = 5;
    coef = round( csv_length/  number_of_time_points)
#    long_wrf_dewpoint_vector = [0] * ( coef*(len(wrf_dewpoint_vector) - 1) + 1)
    long_wrf_dewpoint_vector = [0] * ( csv_length)
    preliminary_length = (len(wrf_dewpoint_vector) - 1)* coef 
    
    for jjj in range(0, len(wrf_dewpoint_vector) - 1):
        for j_inside in range(0, coef):
            long_wrf_dewpoint_vector[coef*jjj + j_inside] = wrf_dewpoint_vector[jjj]

    for one_more_j in range(preliminary_length, csv_length):      
        long_wrf_dewpoint_vector[one_more_j] =  wrf_dewpoint_vector[-1]          
            
            
            
    # this is separate graph for WRF-temperature in points of csv-abscissa
    # =============================================================================
    # plt.figure(figsize=(14,8))
    # plt.title('WRF temperature in time, ground level' , fontsize=22)
    # plt.xlabel('time', fontsize=20, horizontalalignment='right' )
    # plt.ylabel('T, C', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
    # plt.plot(long_wrf_temperature_vector)
    # plt.show()
    # =============================================================================
    
    plt.figure(figsize=(14,8))
    plt.title('CSV and WRF dewpoint in time, ground level' , fontsize=22)
    plt.xlabel('time', fontsize=20, horizontalalignment='right' )
    plt.ylabel('T, C', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
    plt.plot(csv_time, csv_data.iloc[:, 1], linewidth=3, label='csv')
    plt.plot(csv_time, long_wrf_dewpoint_vector, linewidth=3, label='wrf')
    plt.locator_params(axis='y', nbins=10)
    plt.locator_params(axis='x', nbins=4)
    plt.legend(fontsize=20,loc=1)
    plt.show()
    

#  THIS SHOULD BE TUNED    
# =============================================================================
#     plt.figure(figsize=(18,8))
#     plt.title('Cloud-base height' , fontsize=22)
#     plt.xlabel('time', fontsize=20, horizontalalignment='right' )
#     plt.ylabel('H, km', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#     plt.plot(time_vector[:], cloud_base_in_time(model_datetime, model_period, model_length, number_of_time_points, z_vector), label = 'from profiles')
#     plt.plot(time_vector[:], 0.125*(model2.get_t2(model_datetime, model_period, model_length, event_datetime,  number_of_time_points) - dewpoint_in_time(model_datetime, model_period, model_length, event_datetime, number_of_time_points )), label = 'rough')
#     plt.legend(fontsize=20,loc=1)
#     plt.show()
# =============================================================================
    
    
if __name__ == '__main__':
    main()
    