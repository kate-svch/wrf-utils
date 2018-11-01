#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 10:43:32 2018

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
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx


csv_folder = '/home/kate-svch/oscillo_csv/' 
max_number = 5;
#csv_data = pd.read_csv(csv_folder + '3_Ch' + str(number) + '.csv')



#color_array = ['y', 'b', 'violet', 'g']
color_array = ['#F9F807', '#00faff', '#ff02fa', '#05e400']
#multiplayer_array = [1, 1.8 , 3, -0.052]
multiplayer_array = [1, 1, 1, 1]


# =============================================================================
# #for j_str in range (0, len(csv_data)):
# for j_str in range (6, 12):
#     x_array.append(csv_data.iloc[j_str, 3])
#     y_first_value_array.append(csv_data.iloc[j_str, 4])
#     print (csv_data.iloc[j_str, 3])
#     print(csv_data.iloc[j_str, 4])
# 
# =============================================================================

plt.figure(figsize=(14,8))

for number in range(1, max_number):    
    txt_file = csv_folder + '3_Ch' + str(number) + '.txt'
    file_we_opened = open(txt_file, 'r')
    lines_array = file_we_opened.readlines()
    file_we_opened.close() 
    
    number_of_extra_lines = 0
    
    index_min = (len(lines_array) - number_of_extra_lines) *48//100
    index_max = (len(lines_array) - number_of_extra_lines) *57//100
    
    output_file = csv_folder + 'temp_'+ str(number) +'.csv'
    
    with open(output_file, "w") as output:
        #for j_str in range(6, len(lines_array) ):
        for j_str in range(number_of_extra_lines + index_min, number_of_extra_lines + index_max ):    
            if (lines_array[j_str][3] == '-'):
                x_str = lines_array[j_str][3:19]
                y_str = lines_array[j_str][20:]
            else:  
                x_str = lines_array[j_str][3:18]
                y_str = lines_array[j_str][19:]
            x_str = x_str.replace(',', '.')
            y_str = y_str.replace(',', '.')
            output.write(x_str + ',' + y_str)
        output.write(x_str + ',' + y_str)    
       
            
    
    csv_data = pd.read_csv(output_file)
    x_array = csv_data.iloc[:, 0];
    y_first_value_array = csv_data.iloc[:, 1];
    
    
    float_x_array = [];
    float_y_first_value_array = []
    
    for jj in range(0, len(x_array)):
        float_x_array.append(float(x_array[jj]))
        float_y_first_value_array.append(float(y_first_value_array[jj]))
            
    float_x_array = np.array(float_x_array)  
    float_y_first_value_array  = np.array(float_y_first_value_array)
    
    
    temp_x_array = float_x_array.reshape(1000, 45)    
    temp_y_first_value_array  = float_y_first_value_array.reshape(1000, 45)  
    
    x_array = temp_x_array.mean(axis = 1)
    y_first_value_array = temp_y_first_value_array.mean(axis = 1)



    plt.plot( csv_data.iloc[:, 0], multiplayer_array[number-1]*csv_data.iloc[:, 1], color = color_array[number-1], label = str(number))



#print('I have allready done it!')


# =============================================================================
# plt.title(name_of_value+ ' csv', fontsize=22)
# plt.xlabel('time', fontsize=20, horizontalalignment='right' )
# plt.ylabel('T, C', rotation='horizontal', fontsize=24, horizontalalignment='right', verticalalignment='top')
# #plt.locator_params(nbins=4)
# plt.locator_params(axis='y', nbins=10)
    
plt.locator_params(axis='x', nbins=4)
plt.legend(fontsize=20,loc=1)
# =============================================================================
plt.show()


                          
# =============================================================================
# plt.plot(the_first_time_for_field_array, model2.get_aux_speed_array(csv_data.iloc[:, 1], aux_pressure_height_number), linewidth=3, label = str(the_first_field_time_moment), color =  (1, 0.4, 0, 1))
# =============================================================================
