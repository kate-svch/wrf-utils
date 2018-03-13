#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 12:51:08 2018

@author: kate-svch
"""


# reads csv-file about electric field, temperature, wind-speed, pressure; and gets graphs
# we'll draw values from csv-measurements and from wrf-reanalysis
#  all values for wrf-reanalysis are obtained with time step of  5 minutes

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd     
import datetime   
from time import strptime  # it's needed to get month number for a given month name
import csv

from scipy.io import netcdf
import model2


x_lon = 45;  y_lat = 45;                                                             
                                                             
start_date_str = '2018-03-05-01-30';    # this is time of start of the event, so EVERYWHERE "time_point_of_start = 0" !!!
#model_datetime = datetime.datetime(2018, 3, 4, 18, 0)  
event_datetime = datetime.datetime(int(start_date_str[0:4]), int(start_date_str[5:7]), int(start_date_str[8:10]), int(start_date_str[11:13]), int(start_date_str[14:16]))  

name_of_value = 'temperature'
#field_data = pd.read_csv('/home/kate-svch/wrfmain/kate/reanalysis/datetime_and_01/electric_field/' + start_finish_date_str + '_el-field.csv')
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

wrf_temperature_vector = model2.get_t2(event_datetime,  time_point_of_start, number_of_time_points);

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
long_wrf_temperature_vector = [0]*coef*len(wrf_temperature_vector)

for jjj in range(0, len(wrf_temperature_vector)):
    for j_inside in range(0,coef):
        long_wrf_temperature_vector[coef*jjj + j_inside] = wrf_temperature_vector[jjj]
        
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
plt.title('CSV and WRF temperatures in time, ground level' , fontsize=22)
plt.xlabel('time', fontsize=20, horizontalalignment='right' )
plt.ylabel('T, C', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
plt.plot(csv_data.iloc[0:-1, 1], linewidth=3, label='csv')
plt.plot( long_wrf_temperature_vector, linewidth=3, label='wrf')
plt.legend(fontsize=20,loc=1)
plt.show()




# pressure CSV is obtained with time-step of 1 minute

name_of_value = 'pressure'
csv_data = pd.read_csv('/home/kate-svch/wrfmain/kate/reanalysis/csv_measurements/'+ start_date_str + '_' + name_of_value  + '.csv')

plt.figure(figsize=(14,8))
plt.plot(csv_data.iloc[:, 1])
plt.title(name_of_value+ ' csv', fontsize=22)
plt.xlabel('time', fontsize=20, horizontalalignment='right' )
plt.ylabel(name_of_value, rotation='horizontal', fontsize=24, horizontalalignment='right', verticalalignment='top')
plt.show()

wrf_pressure_vector = model2.get_s_pressure(event_datetime,  time_point_of_start, number_of_time_points);
coef = 5;
long_wrf_pressure_vector = [0]*coef*len(wrf_pressure_vector)

for jjj in range(0, len(wrf_pressure_vector)):
    for j_inside in range(0,coef):
        long_wrf_pressure_vector[coef*jjj + j_inside] = wrf_pressure_vector[jjj]

plt.figure(figsize=(14,8))
plt.title('CSV and WRF pressures in time, ground level' , fontsize=22)
plt.xlabel('time', fontsize=20, horizontalalignment='right' )
plt.ylabel(name_of_value, rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
plt.plot(csv_data.iloc[0:-1, 1], linewidth=3, label='csv')
plt.plot( long_wrf_pressure_vector, linewidth=3, label='wrf')
plt.legend(fontsize=20,loc=1)
plt.show()



# el-field CSV is obtained with time-step of 1 second

name_of_value = 'el_field'
csv_data = pd.read_csv('/home/kate-svch/wrfmain/kate/reanalysis/csv_measurements/'+ start_date_str + '_' + name_of_value  + '.csv')

plt.figure(figsize=(14,8))
plt.plot(csv_data.iloc[:, 1])
plt.title(name_of_value+ ' csv', fontsize=22)
plt.xlabel('time', fontsize=20, horizontalalignment='right' )
plt.ylabel(r'$\frac{kV}{m}$', rotation='horizontal', fontsize=24, horizontalalignment='right', verticalalignment='top')
plt.show()


charge = 2.3*10**(-2);

#name="QICE"
#name="QSNOW"
name="QVAPOR"
#name="QRAIN"
#name="QGRAUP"
#name="QCLOUD"
file = model2.get_wrf_file()
temp_n_array = file.variables[name].data[:] / 1
#number_of_time_points = len(temp_n_array[:, 0, y_lat, x_lon]); 
time_point_of_start = 0;
#time_point_of_start = 91;
number_of_time_points =  25;   # THIS SHOULD BE MADE UNIFORM!!


plt.figure(figsize=(18,8))
picture1 = plt.contourf(np.array(model2.get_q(event_datetime, name, time_point_of_start , number_of_time_points )).transpose())

plt.colorbar(picture1) 
plt.title('Mass density of '+ name, fontsize=22)
plt.xlabel('time', fontsize=20, horizontalalignment='right' )
plt.ylabel('altitude', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#    plt.axis('image')
plt.axis('normal')
   
plt.show()

plt.figure(figsize=(18,8))

# Let's look on the upper picture - t-z particles distribution, 
# and choose the time-point under interest (one of the values on the time-axis)
# then just use "number_of_the_time_point = that_chosen_value",
# and we'll get x-z particles distribuation - on the lower picture    

picture2 = plt.contourf(np.array(   model2.get_q_xz(event_datetime, name, number_of_the_time_point = 100)).transpose())
   
plt.colorbar(picture2) 
plt.title('Mass density of '+ name, fontsize=22)
plt.xlabel('x', fontsize=20, horizontalalignment='right' )
plt.ylabel('altitude', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
plt.axis('normal')

plt.show()


# =============================================================================
# wrf_pressure_vector = model2.get_s_pressure(event_datetime,  time_point_of_start, number_of_time_points);
# coef = 5*60;
# long_wrf_pressure_vector = [0]*coef*len(wrf_pressure_vector)
# 
# for jjj in range(0, len(wrf_pressure_vector)):
#     for j_inside in range(0,coef):
#         long_wrf_pressure_vector[coef*jjj + j_inside] = wrf_pressure_vector[jjj]
# 
# plt.figure(figsize=(14,8))
# plt.title('CSV and WRF pressures in time, ground level' , fontsize=22)
# plt.xlabel('time', fontsize=20, horizontalalignment='right' )
# plt.ylabel(name_of_value+ ' csv', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
# plt.plot(csv_data.iloc[0:-1, 1], linewidth=3, label='csv')
# plt.plot( long_wrf_pressure_vector, linewidth=3, label='wrf')
# plt.legend(fontsize=20,loc=1)
# plt.show()
# 
# =============================================================================

