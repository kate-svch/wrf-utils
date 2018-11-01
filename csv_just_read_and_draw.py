#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 10:43:32 2018

@author: kate-svch
"""

# СТРОИТ ОБЩУЮ ЧАСТЬ НЕСКОЛЬКИХ ЗАВИСИМОСТЕЙ В ОДНИХ ОСЯХ В ОБЩЕЙ ЧАСТИ СУЩЕСТВОВАНИЯ ВСЕХ ЗАВИСИМОСТЕЙ

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


csv_folder = '/home/kate-svch/Wada_data/source_wada_et_al/figure1' 

names_array = ['efm', 'godot', 'growth']
max_number = len(names_array);

#max_number = 1

#color_array = ['y', 'b', 'violet', 'g']
#color_array = ['#F9F807', '#00faff', '#ff02fa', '#05e400']
color_array = ['r', 'g', 'b', 'violet']
#multiplayer_array = [1, 1.8 , 3, -0.052]
multiplayer_array = [80, 1, 1]

#start_number = len(pd.read_csv(csv_folder + '/' + names_array[0] + '.csv')) * 1//4
#finish_number = len(pd.read_csv(csv_folder + '/' + names_array[0] + '.csv')) * 3//4

start_number_value_str = (pd.read_csv(csv_folder + '/' + names_array[0] + '.csv')).iloc[0,0]
finish_number_value_str = (pd.read_csv(csv_folder + '/' + names_array[0] + '.csv')).iloc[-1,0]

start_number_value =  datetime.time(int(start_number_value_str[0:2]), int(start_number_value_str[3:5]), int(start_number_value_str[6:8]), int(start_number_value_str[9:10])*10**5)
finish_number_value =  datetime.time(int(finish_number_value_str[0:2]), int(finish_number_value_str[3:5]), int(finish_number_value_str[6:8]), int(finish_number_value_str[9:10])*10**5)

fig, ax = plt.subplots(figsize = (16,6))

for number in range(0, max_number):    
#for number in range(1, 2):    
    csv_file_name = csv_folder + '/' + names_array[number] + '.csv'
    csv_data = pd.read_csv(csv_file_name)
    this_is_x_array = [] 
    
    for jjj in range(0, len(csv_data)):
        this_x_str = csv_data.iloc[jjj, 0]
        this_is_x_array.append(datetime.time(int(this_x_str[0:2]), int(this_x_str[3:5]), int(this_x_str[6:8]), int(this_x_str[9:10])*10**5))
        
    if (names_array[number] == 'efm'):
        ax.plot(this_is_x_array, multiplayer_array[number]*csv_data.iloc[:, 1], color = color_array[number], label = str(names_array[number]))
    else:     
        ax.plot(this_is_x_array, multiplayer_array[number]*csv_data.iloc[:, 2], color = color_array[number], label = str(names_array[number]))
    start, end = ax.get_xlim()
    ax.xaxis.set_ticks(np.arange(start, end, 0.1))
    
    current_x_min_str = csv_data.iloc[0, 0]
    current_x_max_str = csv_data.iloc[-1, 0] 
    current_x_min = datetime.time(int(current_x_min_str[0:2]), int(current_x_min_str[3:5]), int(current_x_min_str[6:8]), int(current_x_min_str[9:10])*10**5)
    current_x_max = datetime.time(int(current_x_max_str[0:2]), int(current_x_max_str[3:5]), int(current_x_max_str[6:8]), int(current_x_max_str[9:10])*10**5)
    
    if (current_x_min > start_number_value):
        start_number_value = current_x_min
    if (current_x_max < finish_number_value):
        finish_number_value = current_x_max 



# =============================================================================
# plt.title(name_of_value+ ' csv', fontsize=22)
# plt.xlabel('time', fontsize=20, horizontalalignment='right' )
# plt.ylabel('T, C', rotation='horizontal', fontsize=24, horizontalalignment='right', verticalalignment='top')
# plt.locator_params(nbins=4)
#plt.locator_params(axis='y', nbins=10)
plt.xlim(start_number_value, finish_number_value)
plt.locator_params(axis='x', nbins=4)
plt.legend(fontsize=20,loc=1)
# =============================================================================
plt.show()

                          
