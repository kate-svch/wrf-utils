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


start_date_str = '2016-06-11-00-00'; 


#model_datetime = datetime.datetime(2016, 10, 29, 0, 0)
#event_finish_datetime = datetime.datetime(2016, 10, 30, 12, 0)
#the_time_moment = datetime.datetime(2016, 5, 4, 0, 0)


# =============================================================================
# model_datetime = datetime.datetime(2017, 10, 10, 6)
# event_finish_datetime = datetime.datetime(2017, 10, 11, 00)
# the_time_moment = datetime.datetime(2017, 10, 10, 12, 30)
# #the_second_time_moment = datetime.datetime(2016, 5, 4, 18, 45) 
# 
# =============================================================================


model_datetime = datetime.datetime(2016, 6, 11, 0, 0)
event_finish_datetime = datetime.datetime(2016, 6, 12, 00, 0)
the_time_moment = datetime.datetime(2016, 6, 11, 10, 50)


event_datetime = datetime.datetime(int(start_date_str[0:4]), int(start_date_str[5:7]), int(start_date_str[8:10]), int(start_date_str[11:13]), int(start_date_str[14:16]))  

# it's for time-marks at "pressure_comparison"
#the_first_aux_time_moment = datetime.datetime(17, 10, 10, 12, 30)
#the_second_aux_time_moment = datetime.datetime(17, 10, 10, 12, 30)


the_first_aux_time_moment = datetime.datetime(2016, 6, 11, 9, 50)
the_second_aux_time_moment = datetime.datetime(2016, 6, 11, 11, 30)


aux_pressure_height_number = 10;
the_first_time_for_pressure_array = [the_first_aux_time_moment]*(aux_pressure_height_number + 1);  
the_second_time_for_pressure_array= [the_second_aux_time_moment]*(aux_pressure_height_number + 1);  

# it's for time-marks at "el_field"
# =============================================================================
# the_first_field_time_moment = datetime.datetime(17, 10, 10, 12, 30) + (the_second_aux_time_moment - the_first_aux_time_moment)
# the_second_field_time_moment = datetime.datetime(17, 10, 10, 14, 0)    + (the_second_aux_time_moment - the_first_aux_time_moment)
# the_third_field_time_moment = datetime.datetime(17, 10, 10, 14, 20) + (the_second_aux_time_moment - the_first_aux_time_moment)
# the_fourth_field_time_moment = datetime.datetime(17, 10, 10, 15, 55) + (the_second_aux_time_moment - the_first_aux_time_moment)
# the_fifth_field_time_moment = datetime.datetime(17, 10, 10, 17, 30) + (the_second_aux_time_moment - the_first_aux_time_moment)
# the_sixth_field_time_moment = datetime.datetime(17, 10, 10, 20, 15) + (the_second_aux_time_moment - the_first_aux_time_moment)
# =============================================================================


the_first_field_time_moment = datetime.datetime(16, 6, 11, 9, 50) + (the_second_aux_time_moment - the_first_aux_time_moment)
the_second_field_time_moment = datetime.datetime(16, 6, 11, 10, 5)    + (the_second_aux_time_moment - the_first_aux_time_moment)
the_third_field_time_moment = datetime.datetime(16, 6, 11, 11, 10) + (the_second_aux_time_moment - the_first_aux_time_moment)
the_fourth_field_time_moment = datetime.datetime(16, 6, 11, 11, 0)  + (the_second_aux_time_moment - the_first_aux_time_moment)
the_fifth_field_time_moment = datetime.datetime(17, 10, 10, 17, 30) + (the_second_aux_time_moment - the_first_aux_time_moment)
the_sixth_field_time_moment = datetime.datetime(17, 10, 10, 20, 15) + (the_second_aux_time_moment - the_first_aux_time_moment)

the_fifth_field_time_moment = the_fourth_field_time_moment 
the_sixth_field_time_moment = the_fourth_field_time_moment 


the_first_field_time_moment = datetime.datetime(16, 6, 11, 11, 00) 
the_second_field_time_moment = datetime.datetime(16, 6, 11, 11, 30)   
the_third_field_time_moment = datetime.datetime(16, 6, 11, 11, 45) 
the_fourth_field_time_moment = datetime.datetime(16, 6, 11, 12, 5)  


#the_first_field_time_moment = datetime.datetime(16,  6, 4, 12, 10) 
#the_second_field_time_moment = datetime.datetime(16, 6, 4, 15, 15) 
#the_third_field_time_moment = datetime.datetime(16, 6, 4, 12, 10) 
#the_fourth_field_time_moment = datetime.datetime(16, 6, 4, 12, 10) 

the_first_time_for_field_array = [the_first_field_time_moment]*(aux_pressure_height_number + 1);  
the_second_time_for_field_array= [the_second_field_time_moment]*(aux_pressure_height_number + 1);  
the_third_time_for_field_array= [the_third_field_time_moment]*(aux_pressure_height_number + 1);  
the_fourth_time_for_field_array= [the_fourth_field_time_moment]*(aux_pressure_height_number + 1);  
the_fifth_time_for_field_array= [the_fifth_field_time_moment]*(aux_pressure_height_number + 1);  
the_sixth_time_for_field_array= [the_sixth_field_time_moment]*(aux_pressure_height_number + 1);  


csv_folder = '/home/kate/wrfmain-local/kate/reanalysis/csv_measurements/' + start_date_str + '/';
name_of_value = 'el_field'
csv_data = pd.read_csv(csv_folder + start_date_str + '_' + name_of_value  + '.csv')

lightning_time_array = []
lightning_field_array=[]
lightning_time_data = pd.read_csv('/home/kate/Thunder/Aragats_measurements/2016/2016-06-11/Aragatz-20160611.loc')
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





print('Time-shift is ', the_second_aux_time_moment - the_first_aux_time_moment)


# el-field CSV is obtained with time-step of 1 second

name_of_value = 'el_field'
csv_data = pd.read_csv(csv_folder + start_date_str + '_' + name_of_value  + '.csv')
csv_length = len(csv_data)
csv_time =  [0] * csv_length

#time_start_index =  csv_length*11//24;
#time_finish_index =  csv_length*16//24;

#time_start_index =  csv_length*93//192;
#time_finish_index =  csv_length*96//192;
time_start_index =  csv_length*3//8
time_finish_index =  csv_length*6//8


for jj in range (0, csv_length):
    jj_day =  int(csv_data.iloc[jj, 0][0:2])
    jj_hour =  int(csv_data.iloc[jj, 0][10:12])
    jj_minute =  int(csv_data.iloc[jj, 0][13:15])
    jj_second =  int(csv_data.iloc[jj, 0][16:18])
    jj_year = int(csv_data.iloc[jj, 0][7:9])
    jj_month = model_datetime.month
#    csv_time[jj] = csv_data.iloc[jj, 0][0:15]
    csv_time[jj]  = datetime.datetime(jj_year, jj_month, jj_day, jj_hour, jj_minute, jj_second)

plt.figure(figsize=(16,8))
plt.plot(csv_time[:], csv_data.iloc[: , 1])

   
for jp in range (1, len(lightning_time_data)):
    plt.plot(lightning_time_array[jp*(aux_pressure_height_number + 1) : (jp+1)*(aux_pressure_height_number + 1)], lightning_field_array[jp*(aux_pressure_height_number + 1) : (jp+1)*(aux_pressure_height_number + 1)], color = '#0aafb1')    
       
                                  
plt.plot(the_first_time_for_field_array, model2.get_aux_speed_array(csv_data.iloc[:, 1], aux_pressure_height_number), linewidth=3, label = str(the_first_field_time_moment), color =  (1, 0.4, 0, 1))
plt.plot(the_second_time_for_field_array, model2.get_aux_speed_array(csv_data.iloc[:, 1], aux_pressure_height_number), linewidth=3, label = str(the_second_field_time_moment), color =  (0.9, 0, 0.4, 1))
plt.plot(the_third_time_for_field_array, model2.get_aux_speed_array(csv_data.iloc[:, 1], aux_pressure_height_number), linewidth=3, label = str(the_third_field_time_moment), color =  (0.5, 0.9, 0, 1))                               
plt.plot(the_fourth_time_for_field_array, model2.get_aux_speed_array(csv_data.iloc[:, 1], aux_pressure_height_number), linewidth=3, label = str(the_fourth_field_time_moment))                             
#plt.plot(the_fifth_time_for_field_array, model2.get_aux_speed_array(csv_data.iloc[:, 1], aux_pressure_height_number), linewidth=3, label = str(the_fifth_field_time_moment))                             
#plt.plot(the_sixth_time_for_field_array, model2.get_aux_speed_array(csv_data.iloc[:, 1], aux_pressure_height_number), linewidth=3, label = str(the_sixth_field_time_moment))                              
                               
plt.rc('xtick', labelsize=22) 
plt.rc('ytick', labelsize=14)
plt.title(name_of_value+ ' csv', fontsize=22)
plt.locator_params(axis='y', nbins=10)
plt.locator_params(axis='x', nbins=6)
#plt.xlabel('time', fontsize=23, horizontalalignment='right' )
plt.ylabel(r'$\frac{kV}{m}$', rotation='horizontal', fontsize=26, horizontalalignment='right', verticalalignment='top')
#plt.xlim(csv_time[0]  , csv_time[-1] )
plt.xlim(csv_time[time_start_index], csv_time[time_finish_index] )   
#plt.ylim()
plt.legend(fontsize=20,loc=1)
plt.show()


