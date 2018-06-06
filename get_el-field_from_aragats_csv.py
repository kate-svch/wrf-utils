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
from math import ceil   # для округления вверх - rounding up  ^_^

from scipy.io import netcdf
import model2


x_lon = 45;  y_lat = 45;                                                             
                                                             
#start_date_str = '2018-03-05-01-30';    # this is time of start of the event, so EVERYWHERE "time_point_of_start = 0" !!!

start_date_str = '2016-04-26-12-00'; 

model_datetime = datetime.datetime(2016, 4, 26, 12, 0)
event_finish_datetime = datetime.datetime(2016, 4, 29, 00, 0) 
the_time_moment = datetime.datetime(2016, 4, 28, 2,  00 )   

event_datetime = datetime.datetime(int(start_date_str[0:4]), int(start_date_str[5:7]), int(start_date_str[8:10]), int(start_date_str[11:13]), int(start_date_str[14:16]))  

csv_folder = '/home/kate-svch/wrfmain/kate/reanalysis/csv_measurements/' + start_date_str + '/';
#path = os.path.join(current_folder) + '/' 
#path = os.path.join(path, datetime.datetime.strftime(model_datetime, '%Y%m%d%H'))


wrf_step_minutes = 5;
#model2.set_model_datetime(datetime.datetime(2018, 3, 4, 18, 0) , wrf_step_minutes)        # the second argument is the value of time step, in minutes

model_period = datetime.timedelta(minutes = wrf_step_minutes)

file = model2.get_wrf_file(model_datetime)
variable = file.variables['T2'].data[:]
model_length = len(variable[:, y_lat, x_lon])

 # here we have an automatical "numnber_of_time_points"-initialization  

number_of_time_points  = int ((event_finish_datetime - event_datetime)/datetime.timedelta(0, 0, 0, 0, wrf_step_minutes))  


z_vector = model2.get_height(model_datetime)[:-1]
time_vector = [event_datetime + datetime.timedelta(minutes=wrf_step_minutes * i) for i in range(number_of_time_points )]    
    
    
x_values = [0] * 90
for j_x in range(0, len(x_values) ):
    x_values[j_x] = (j_x - 45)   


name_of_value = 'temperature'
#field_data = pd.read_csv('/home/kate-svch/wrfmain/kate/reanalysis/datetime_and_01/electric_field/' + start_finish_date_str + '_el-field.csv')
csv_data = pd.read_csv(csv_folder + start_date_str + '_' + name_of_value  + '.csv')
csv_length = len(csv_data)
csv_time =  [0] * csv_length

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
#plt.locator_params(nbins=4)
plt.locator_params(axis='y', nbins=10)
plt.locator_params(axis='x', nbins=4)
plt.xlim(csv_time[0]  , csv_time[-1] )
plt.show()

# temperature CSV is obtained with time-step of 1 minute



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


wrf_temperature_vector = model2.get_t2(model_datetime, model_period, model_length, event_datetime, number_of_time_points);

coef = round( csv_length/  number_of_time_points)
long_wrf_temperature_vector = [0] * (csv_length)
preliminary_length = (number_of_time_points - 1)* coef 


for jjj in range(0, number_of_time_points - 1):
    for j_inside in range(0, coef):
        long_wrf_temperature_vector[coef*jjj + j_inside] = wrf_temperature_vector[jjj]

for one_more_j in range(preliminary_length, csv_length):      
    long_wrf_temperature_vector[one_more_j] =  wrf_temperature_vector[-1]    


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
plt.plot(csv_time, csv_data.iloc[:, 1], linewidth=3, label='csv')
#plt.yticks(np.arange(0.0, 3.0, step=0.5))
plt.plot(csv_time, long_wrf_temperature_vector, linewidth=3, label='wrf')
plt.locator_params(axis='y', nbins=10)
plt.locator_params(axis='x', nbins=6)
plt.xlim(csv_time[0]  , csv_time[-1] )
plt.legend(fontsize=20,loc=1)
plt.show()




# pressure CSV is obtained with time-step of 1 minute

name_of_value = 'pressure'
csv_data = pd.read_csv(csv_folder + start_date_str + '_' + name_of_value  + '.csv')
csv_length = len(csv_data)
csv_time =  [0] * csv_length

for jj in range (0, csv_length):
    jj_day =  int(csv_data.iloc[jj, 0][0:2])
    jj_hour =  int(csv_data.iloc[jj, 0][10:12])
    jj_minute =  int(csv_data.iloc[jj, 0][13:15])
    jj_second =  int(csv_data.iloc[jj, 0][16:18])
    jj_year = int(csv_data.iloc[jj, 0][7:9])
    jj_month = model_datetime.month
#    csv_time[jj] = csv_data.iloc[jj, 0][0:15]
    csv_time[jj]  = datetime.datetime(jj_year, jj_month, jj_day, jj_hour, jj_minute, jj_second)

fig = plt.figure(figsize=(14,8))
plt.plot(csv_time, csv_data.iloc[:, 1])
plt.title(name_of_value+ ' csv', fontsize=22)
plt.locator_params(axis='y', nbins=10)
plt.locator_params(axis='x', nbins=6)
plt.xlabel('time', fontsize=20, horizontalalignment='right' )
plt.ylabel('kPa', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#fig.autofmt_xdate()       # this can make tick-labels nonparallel to the axis
plt.show()

wrf_pressure_vector = model2.get_s_pressure(model_datetime, model_period, model_length, event_datetime, number_of_time_points);
coef = round( csv_length/  number_of_time_points)
long_wrf_pressure_vector = [0] * (csv_length)
preliminary_length = (number_of_time_points - 1)* coef 

for jjj in range(0, number_of_time_points - 1):
    for j_inside in range(0, coef):
        long_wrf_pressure_vector[coef*jjj + j_inside] = wrf_pressure_vector[jjj]

for one_more_j in range(preliminary_length, csv_length):      
    long_wrf_pressure_vector[one_more_j] =  wrf_pressure_vector[-1]    



       

plt.figure(figsize=(14,8))
plt.title('CSV and WRF pressures in time, ground level' , fontsize=22)
plt.xlabel('time', fontsize=20, horizontalalignment='right' )
plt.ylabel(name_of_value, rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
plt.plot(csv_time, csv_data.iloc[:, 1], linewidth=3, label='csv')
plt.plot(csv_time, long_wrf_pressure_vector, linewidth=3, label='wrf')
plt.locator_params(axis='y', nbins=10)
plt.locator_params(axis='x', nbins=6)
plt.xlim(csv_time[0]  , csv_time[-1] )
plt.legend(fontsize=20,loc=1)
plt.show()



# el-field CSV is obtained with time-step of 1 second

name_of_value = 'el_field'
csv_data = pd.read_csv(csv_folder + start_date_str + '_' + name_of_value  + '.csv')
csv_length = len(csv_data)
csv_time =  [0] * csv_length

for jj in range (0, csv_length):
    jj_day =  int(csv_data.iloc[jj, 0][0:2])
    jj_hour =  int(csv_data.iloc[jj, 0][10:12])
    jj_minute =  int(csv_data.iloc[jj, 0][13:15])
    jj_second =  int(csv_data.iloc[jj, 0][16:18])
    jj_year = int(csv_data.iloc[jj, 0][7:9])
    jj_month = model_datetime.month
#    csv_time[jj] = csv_data.iloc[jj, 0][0:15]
    csv_time[jj]  = datetime.datetime(jj_year, jj_month, jj_day, jj_hour, jj_minute, jj_second)

plt.figure(figsize=(14,8))
plt.plot(csv_time, csv_data.iloc[:, 1])
plt.title(name_of_value+ ' csv', fontsize=22)
plt.locator_params(axis='y', nbins=10)
plt.locator_params(axis='x', nbins=6)
plt.xlabel('time', fontsize=20, horizontalalignment='right' )
plt.ylabel(r'$\frac{kV}{m}$', rotation='horizontal', fontsize=24, horizontalalignment='right', verticalalignment='top')
plt.xlim(csv_time[0]  , csv_time[-1] )
plt.show()


charge = 2.3*10**(-2);

# =============================================================================
# #name="QICE"
# #name="QSNOW"
# name="QVAPOR"
# #name="QRAIN"
# #name="QGRAUP"
# #name="QCLOUD"
# 
# 
# 
# 
# plt.figure(figsize=(18,8))
# picture1 = plt.contourf(time_vector, z_vector, np.array(model2.get_q(model_datetime, model_period, model_length, event_datetime, name, number_of_time_points)).transpose())
# # event_datetime is the time of start of the interesting time-area,it could not coincide with the start of wrf-calculation time-area
# plt.colorbar(picture1) 
# plt.title('Mass density of '+ name, fontsize=22)
# plt.xlabel('time', fontsize=20, horizontalalignment='right' )
# plt.ylabel('altitude', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
# #    plt.axis('image')
# plt.axis('normal')  
# plt.show()
# 
# 
# 
# plt.figure(figsize=(18,8))
# 
# # Let's look on the upper picture - t-z particles distribution, 
# # and choose the time-point under interest (one of the values on the time-axis)
# # then just use "number_of_the_time_point = that_chosen_value",
# # and we'll get x-z particles distribuation - on the lower picture    
# picture2 =  plt.contourf(x_values, z_vector, np.array(   model2.get_q_xz(model_datetime, model_period, model_length, the_time_moment, name )).transpose())
# plt.colorbar(picture2) 
# plt.title('Mass density of '+ name, fontsize=22)
# plt.xlabel('x', fontsize=20, horizontalalignment='right' )
# plt.ylabel('altitude', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
# plt.axis('normal')
# plt.show()
# =============================================================================



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

