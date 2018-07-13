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



def get_aux_pressure_array(array_csv, array_wrf, aux_pressure_height_number):
    min_v = min( min(array_csv), min(array_wrf))
    max_v = max( max(array_csv), max(array_wrf))
    aux_pressure_array = [];
    for jj in range (0, aux_pressure_height_number + 1):
         aux_pressure_array.append( min_v + jj*( (max_v - min_v) /aux_pressure_height_number) )
    return aux_pressure_array



start_date_str = '2016-06-11-00-00'; 


#model_datetime = datetime.datetime(2016, 10, 29, 0, 0)
#event_finish_datetime = datetime.datetime(2016, 10, 30, 12, 0)
#the_time_moment = datetime.datetime(2016, 5, 4, 0, 0)


model_datetime = datetime.datetime(2016, 6, 11, 0, 0)
event_finish_datetime = datetime.datetime(2016, 6, 12, 00, 0)
the_time_moment = datetime.datetime(2016, 6, 11, 12, 0)
event_datetime = datetime.datetime(int(start_date_str[0:4]), int(start_date_str[5:7]), int(start_date_str[8:10]), int(start_date_str[11:13]), int(start_date_str[14:16]))  

# it's for time-marks at "pressure_comparison"
the_first_aux_time_moment = datetime.datetime(16, 6, 11, 10, 45)
the_second_aux_time_moment = datetime.datetime(16, 6, 11, 12, 25)  
aux_pressure_height_number = 10;
the_first_time_for_pressure_array = [the_first_aux_time_moment]*(aux_pressure_height_number + 1);  
the_second_time_for_pressure_array= [the_second_aux_time_moment]*(aux_pressure_height_number + 1);  

# it's for time-marks at "el_field"
the_first_field_time_moment = datetime.datetime(16, 6, 11, 9, 50)  + (the_second_aux_time_moment - the_first_aux_time_moment)
the_second_field_time_moment = datetime.datetime(16, 6, 11, 10, 5) + (the_second_aux_time_moment - the_first_aux_time_moment)
the_third_field_time_moment = datetime.datetime(16, 6, 11, 11, 10) + (the_second_aux_time_moment - the_first_aux_time_moment)
the_first_time_for_field_array = [the_first_field_time_moment]*(aux_pressure_height_number + 1);  
the_second_time_for_field_array= [the_second_field_time_moment]*(aux_pressure_height_number + 1);  
the_third_time_for_field_array= [the_third_field_time_moment]*(aux_pressure_height_number + 1);  


csv_folder = '/home/kate-svch/wrfmain/kate/reanalysis/csv_measurements/' + start_date_str + '/';
name_of_value = 'el_field'
csv_data = pd.read_csv(csv_folder + start_date_str + '_' + name_of_value  + '.csv')

lightning_time_array = []
lightning_field_array=[]
lightning_time_data = pd.read_csv('/home/kate-svch/Thunder/Aragats_measurements/2016/2016-06-11/Aragatz-20160611.loc')
for j_str in range (0, len(lightning_time_data)):
#for j_str in range (0, 1):
    j_year = int(lightning_time_data.iloc[j_str, 0][2:4])
    j_month = int(lightning_time_data.iloc[j_str, 0][5:7])
    j_day =  int(lightning_time_data.iloc[j_str, 0][8:10])
    j_hour =  int(lightning_time_data.iloc[j_str, 1][0:2])
    j_minute =  int(lightning_time_data.iloc[j_str, 1][3:5])
    j_second =   int(lightning_time_data.iloc[j_str, 1][6:8])
    j_datetime = datetime.datetime(j_year, j_month, j_day, j_hour, j_minute, j_second)    
    print(j_datetime)
    field_temp_array = model2.get_aux_speed_array(csv_data.iloc[:, 1], aux_pressure_height_number)
    for j_height in range (0, aux_pressure_height_number + 1):
        lightning_time_array.append(j_datetime);  
        lightning_field_array.append( field_temp_array[j_height])
#print(lightning_time_array)      
#print(lightning_field_array)  

## !!!! temporary_and_auxiliary

#the_time_moment = model_datetime
#the_first_aux_time_moment  = the_time_moment
#the_second_aux_time_moment =  the_time_moment
#the_first_field_time_moment =  the_time_moment
#the_second_field_time_moment =  the_time_moment
#
#the_first_aux_time_moment = datetime.datetime(17, 8, 17, 7, 15)
#the_second_aux_time_moment = datetime.datetime(17, 8, 17, 8, 20)  
#the_first_time_for_pressure_array = [the_first_aux_time_moment]*(aux_pressure_height_number + 1);  
#the_second_time_for_pressure_array= [the_second_aux_time_moment]*(aux_pressure_height_number + 1);  




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


z_vector = model2.get_height(model_datetime, 45)[:-1]
time_vector = [event_datetime + datetime.timedelta(minutes=wrf_step_minutes * i) for i in range(number_of_time_points )]    
    
    
x_values = [0] * 90
for j_x in range(0, len(x_values) ):
    x_values[j_x] = (j_x - 45)   


name_of_value = 'temperature'
#field_data = pd.read_csv('/home/kate-svch/wrfmain/kate/reanalysis/datetime_and_01/electric_field/' + start_finish_date_str + '_el-field.csv')
csv_data = pd.read_csv(csv_folder + start_date_str + '_' + name_of_value + '.csv')
csv_folder = '/home/kate-svch/wrfmain/kate/reanalysis/csv_measurements/' + start_date_str + '/';
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
# this line draws the graph: y is values from the second column, x is numbers of the columnsthe_first_field_time_moment
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



aux_pressure_array = get_aux_pressure_array(csv_data.iloc[:, 1], wrf_pressure_vector, aux_pressure_height_number)


plt.figure(figsize=(14,8))
plt.title('CSV and WRF pressures in time, ground level' , fontsize=22)
plt.xlabel('time', fontsize=20, horizontalalignment='right' )
plt.ylabel(name_of_value, rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
plt.plot(csv_time, csv_data.iloc[:, 1], linewidth=3, label='csv')
plt.plot(csv_time, long_wrf_pressure_vector, linewidth=3, label='wrf')
plt.plot(the_first_time_for_pressure_array, aux_pressure_array, linewidth=1, label = str(the_first_aux_time_moment))
plt.plot(the_second_time_for_pressure_array, aux_pressure_array, linewidth=1, label = str(the_second_aux_time_moment))
plt.locator_params(axis='y', nbins=10)
plt.locator_params(axis='x', nbins=6)
plt.xlim(csv_time[0]  , csv_time[-1] )
plt.legend(fontsize=20,loc=1)
plt.show()

print('Time-shift is ', the_second_aux_time_moment - the_first_aux_time_moment)




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
plt.plot(the_first_time_for_field_array, model2.get_aux_speed_array(csv_data.iloc[:, 1], aux_pressure_height_number), label = str(the_first_field_time_moment))
plt.plot(the_second_time_for_field_array, model2.get_aux_speed_array(csv_data.iloc[:, 1], aux_pressure_height_number), label = str(the_second_field_time_moment))
plt.plot(the_third_time_for_field_array, model2.get_aux_speed_array(csv_data.iloc[:, 1], aux_pressure_height_number), label = str(the_third_field_time_moment))

plt.plot(lightning_time_array[0: (aux_pressure_height_number + 1)], lightning_field_array[jp*(aux_pressure_height_number + 1) : (jp+1)*(aux_pressure_height_number + 1)], color = '#0aafb1', label = 'lightnings')    
for jp in range (1, len(lightning_time_data)):
    plt.plot(lightning_time_array[jp*(aux_pressure_height_number + 1) : (jp+1)*(aux_pressure_height_number + 1)], lightning_field_array[jp*(aux_pressure_height_number + 1) : (jp+1)*(aux_pressure_height_number + 1)], color = '#0aafb1')    
       
plt.title(name_of_value+ ' csv', fontsize=22)
plt.locator_params(axis='y', nbins=10)
plt.locator_params(axis='x', nbins=6)
plt.xlabel('time', fontsize=20, horizontalalignment='right' )
plt.ylabel(r'$\frac{kV}{m}$', rotation='horizontal', fontsize=24, horizontalalignment='right', verticalalignment='top')
#plt.xlim(csv_time[0]  , csv_time[-1] )
plt.xlim(csv_time[30000]  , csv_time[60000] )
plt.legend(fontsize=20,loc=1)
plt.show()





#         array_from_get_wind = get_vertical_wind_certain_level(model_datetime, model_period, model_length, event_datetime, z_index, number_of_time_points)
#         plt.figure(figsize=(18,8))
#         plt.title('Vertical Wind-speed in time, altitude = ' + str(z_chosen_height) + ' km' + ' (above gr.)'+ ' z_ind = ' + str(z_index), fontsize=22)
#         plt.xlabel('time', fontsize=20, horizontalalignment='right' )
#         plt.ylabel(r'$v, \frac{m}{s}$', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#         plt.plot(time_vector, array_from_get_wind, linewidth=3) 
#         plt.plot(time_of_event_for_wind_array, get_aux_speed_array(array_from_get_wind, aux_speed_height_number), label = str(the_time_moment))
#         plt.plot(the_second_time_of_event_for_wind_array, get_aux_speed_array(array_from_get_wind, aux_speed_height_number), label = str(the_second_time_moment))
#         plt.plot(the_third_time_of_event_for_wind_array, get_aux_speed_array(array_from_get_wind, aux_speed_height_number), label = str(the_third_time_moment))
#         plt.plot(the_fourth_time_of_event_for_wind_array, get_aux_speed_array(array_from_get_wind, aux_speed_height_number), label = str(the_fourth_time_moment))
#         plt.legend(fontsize=20,loc=1)
#         plt.show()   


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

