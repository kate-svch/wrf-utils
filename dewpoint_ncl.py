#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 17:01:29 2018

@author: kate-svch
"""

from __future__ import print_function

from netCDF4 import Dataset
from wrf import getvar, ALL_TIMES
import matplotlib.pyplot as plt
import pandas as pd     
import datetime   

import model2

x_lon = 45;   y_lat = 45;   


def get_dewpoint_t_profile_in_certain_moment_of_time(event_datetime, time_point_of_start  = 1):
      
# get quantity of "name" microphysical fracture from 2m to 20 kilometers height : DIFFERENT HEIGHT ANG TIME
   
    time_index = model2.get_index(event_datetime, time_point_of_start )
    ncfile = Dataset("/mnt/data-internal/reanalysis/2018030418/wrfout_d02_2018-03-04_18:00:00")
    t_dewpoint =  getvar(ncfile, 'td', units='degC', timeidx = ALL_TIMES)
    return t_dewpoint[time_index, :, y_lat, x_lon]



def dewpoint_in_time(event_datetime, number_of_time_points=1, time_point_of_start  = 1):
      
# get quantity of "name" microphysical fracture from 2m to 20 kilometers height : DIFFERENT HEIGHT ANG TIME
   
    time_index = model2.get_index(event_datetime, time_point_of_start + number_of_time_points )
    ncfile = Dataset("/mnt/data-internal/reanalysis/2018030418/wrfout_d02_2018-03-04_18:00:00")
    t_dewpoint =  getvar(ncfile, 'td', units='degC', timeidx = ALL_TIMES)
    return t_dewpoint[time_index+ time_point_of_start:time_index+ time_point_of_start+ number_of_time_points, 0, y_lat, x_lon]



def cloud_base_height_from_temperature_and_dp_profiles(event_datetime, model_height, time_point_of_start  = 1):
    temperature = model2.get_t_profile_in_certain_moment_of_time(event_datetime, time_point_of_start)
    t_dp = get_dewpoint_t_profile_in_certain_moment_of_time(event_datetime, time_point_of_start )
    initial_signum = (temperature[0] < t_dp[0])    
    for j_in_z in range(1, len(t_dp)):
        signum = (temperature[j_in_z] < t_dp[j_in_z])
        if signum != initial_signum : return (model_height[j_in_z - 1])
    return (-2);


def cloud_base_in_time(event_datetime, model_height,  number_of_time_points, time_point_of_start  = 1):
    
    cloud_base_height_t = [-1]*number_of_time_points;
    for j_in_time in range(0, number_of_time_points):
        cloud_base_height_t[j_in_time] = cloud_base_height_from_temperature_and_dp_profiles(event_datetime, model_height, time_point_of_start+j_in_time)
    return cloud_base_height_t    


def main():
    
#    x_lon = 45;  y_lat = 45;    
    event_datetime = datetime.datetime(2018, 3, 4, 18, 0) 
    
    time_point_of_start = 91;
    number_of_time_points = 25;
    start_hour = event_datetime.hour;    step = 1/12;
    
    model_height = model2.get_geopotential_height(event_datetime, time_point_of_start  = 1)     
    event_time = model2.create_time_array_in_hours(start_hour, event_datetime, number_of_time_points, step, time_point_of_start);

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
    plt.plot(model_height, model2.get_t_profile_in_certain_moment_of_time(event_datetime, time_point_of_start ), label = 'T')
    plt.plot(model_height, get_dewpoint_t_profile_in_certain_moment_of_time(event_datetime, time_point_of_start), label = 'Td')
    plt.legend(fontsize=20,loc=1)
    plt.show()
    
    print ('The value of cloud-height, estimated with use of temperature profiles, is ', cloud_base_height_from_temperature_and_dp_profiles(event_datetime, model_height, time_point_of_start  = 1), ' km.')
        
    plt.figure(figsize=(18,8))
    plt.title('Dewpoint-temperature, ground level' , fontsize=22)
    plt.xlabel('time', fontsize=20, horizontalalignment='right' )
    plt.ylabel('T, C', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
    plt.plot(event_time, dewpoint_in_time(event_datetime, number_of_time_points, time_point_of_start ))
    plt.show()
    
    
    
    start_date_str = '2018-03-05-01-30';    # this is time of start of the event, so EVERYWHERE BELOW "time_point_of_start = 0" !!!
    name_of_value = 'dewpoint'
    csv_data = pd.read_csv('/home/kate-svch/wrfmain/kate/reanalysis/csv_measurements/'+ start_date_str + '_' + name_of_value  + '.csv')
    
    
    plt.figure(figsize=(14,8))
    # this line draws the graph: y is values from the second column, x is numbers of the columns
    plt.plot(csv_data.iloc[:, 1])
    # here "1" is our chose of the column (the second one), ":" means "take every row"
    plt.title(name_of_value+ ' csv', fontsize=22)
    plt.xlabel('time', fontsize=20, horizontalalignment='right' )
    plt.ylabel('T, C', rotation='horizontal', fontsize=24, horizontalalignment='right', verticalalignment='top')
    plt.show()
    
    # temperature CSV is obtained with time-step of 1 minute
    #time_point_of_start = 91;
    time_point_of_start = 0;
    number_of_time_points =  int(len(csv_data)/5) 
    # THIS SHOULD BE MADE MORE UNIFORM!!!
    
    wrf_dewpoint_vector = model2.get_t2(event_datetime,  time_point_of_start=91, number_of_time_points=int(len(csv_data)/5) );
    
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
    
    
    coef = 5;
    long_wrf_dewpoint_vector = [0]*coef*len(wrf_dewpoint_vector)
    
    for jjj in range(0, len(wrf_dewpoint_vector)):
        for j_inside in range(0,coef):
            long_wrf_dewpoint_vector[coef*jjj + j_inside] = wrf_dewpoint_vector[jjj]
            
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
    plt.plot(csv_data.iloc[0:-1, 1], linewidth=3, label='csv')
    plt.plot( long_wrf_dewpoint_vector, linewidth=3, label='wrf')
    plt.legend(fontsize=20,loc=1)
    plt.show()
    
# =============================================================================
#     plt.figure(figsize=(18,8))
#     plt.title('spread-value in time, ground level' , fontsize=22)
#     plt.xlabel('time', fontsize=20, horizontalalignment='right' )
#     plt.ylabel('T, C', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#     plt.plot(event_time, (model2.get_t2(event_datetime,time_point_of_start, number_of_time_points) - dewpoint_in_time(event_datetime, number_of_time_points, time_point_of_start )))
#     plt.show()
# =============================================================================
    
    time_point_of_start = 91;
    
    plt.figure(figsize=(18,8))
    plt.title('Cloud-base height' , fontsize=22)
    plt.xlabel('time', fontsize=20, horizontalalignment='right' )
    plt.ylabel('H, km', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
    plt.plot(event_time[0:(-1)], cloud_base_in_time(event_datetime, model_height,  number_of_time_points, time_point_of_start), label = 'from profiles')
    plt.plot(event_time[0:(-1)], 0.125*(model2.get_t2(event_datetime,time_point_of_start, number_of_time_points) - dewpoint_in_time(event_datetime, number_of_time_points, time_point_of_start )), label = 'rough')
    plt.legend(fontsize=20,loc=1)
    plt.show()
    
    
if __name__ == '__main__':
    main()
    