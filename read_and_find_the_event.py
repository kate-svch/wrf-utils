#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 14:18:35 2018

@author: kate-svch
"""

# reads csv-file about flux and makes  "0_or_1" array - "whether there was an event"

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd     
import datetime   
from time import strptime  # it's needed to get month number for a given month name
import csv


import argparse    # we'll get the data of the event, as an argument

parser = argparse.ArgumentParser(description='Great Description To Be Here')

parser.add_argument('--time_start', '-s', action='store', dest='start', help='It is a date-time of the beginning of the event', type=str)
parser.add_argument('--time_end', '-e', action='store', dest='end', help='It is a date-time of the end of the event', type=str)
parser.add_argument('--threshold', '-thr', action='store', dest='threshold', help='It is the threshold value for the current set', type=int)
parser.add_argument('--set-number', '-set', action='store', dest='set', help='It is the number of the set containing current event with the given threshold value', type=int)

args = parser.parse_args()

print("The event under consideration starts at " + args.start)
print("The event under consideration ends at " + args.end)
print("The threshold value is " + str(args.threshold))
print("The number of the set is " + str(args.set))

start_finish_date_str = args.start + '_' + args.end;
        
#initial_data = pd.read_csv('/home/kate-svch/wrfmain/kate/reanalysis/2016050400/ar_raw_2016-05-04_60cm_1.csv')

# DEFINE THE TIME INTERVAL HERE
#start_finish_date_str = '2016-05-04-00_2016-05-05-00';

#initial_data = pd.read_csv('/home/kate-svch/wrfmain/kate/reanalysis/csv_all/2016-04-26-12_2016-04-29-00_Stand_1_upper_1cm.csv')

initial_data = pd.read_csv('/home/kate-svch/wrfmain/kate/reanalysis/csv_all/' + start_finish_date_str + '_Stand_1_upper_1cm.csv')

#output_file  = open('/home/kate-svch/wrfmain/kate/reanalysis/datetime_and_01/2016-03-04-12_2016-03-05-12_dt_and_01.csv', "w")
#writer = csv.writer(output_file, delimiter='', quotechar='"', quoting=csv.QUOTE_ALL)
#writer = csv.writer(output_file, delimiter=' ')

output_file = '/home/kate-svch/wrfmain/kate/reanalysis/datetime_and_01/' + str(args.set) + '_set/' + start_finish_date_str + '_dt_and_01.csv'


# everything above the threshold we consider being "the flux", everything under it - isn't "the flux"
#threshold_value = 36000;
threshold_value = args.threshold;

# the following means that for "initial_moment = 1 min" - new time uniti turns out to be "resulting_moment = 10 min"
size_of_time_window = 10;

# this line prints the stuff from the file
#our_little_data.iloc[:]

whether_there_is_a_flux = [0] * (len(initial_data))

# those two are different units of time - "initial_moment" and "resulting_moment"
initial_moments_of_event = 0;
resulting_moments_of_event = 0;


new_length_of_data = len(initial_data) // size_of_time_window;

averaged_data = [0] * (new_length_of_data)
averaged_whether_there_is_a_flux = [0] * (new_length_of_data)


# this averaging will  be performed by obtainig the arithmetical mean
# let's make an averaged data (from initial_data - for count rate):
# =============================================================================
# for new_time_j in range(0, new_length_of_data):
#     current_averaged_value = 0;
#     for little_j in range(0, size_of_time_window ):
#         time_j = new_time_j*size_of_time_window + little_j
#         averaged_data[new_time_j] = averaged_data[new_time_j] + initial_data.iloc[time_j,1]
#         #print (whether_there_is_a_flux[time_j])
#         #print (little_j)
#     averaged_data[new_time_j] = averaged_data[new_time_j] / size_of_time_window;
# 
# # the following makes "whether_there_is_a_flux" from "initial_data.iloc[:, 1]" - withouot any averaging
# for time_j in range(0, len(initial_data) ):
#     if (initial_data.iloc[time_j,1] > threshold_value ):
#         whether_there_is_a_flux[time_j] = 1;
#         #print (whether_there_is_a_flux[time_j])
#         initial_moments_of_event = initial_moments_of_event + 1;
#         
# # the following makes "averaged_whether_there_is_a_flux" from "averaged_data" - just the result we need
# for new_time_j in range(0, new_length_of_data ):
#     if (averaged_data[new_time_j]  > threshold_value ):
#         averaged_whether_there_is_a_flux[new_time_j] = 1;
#         #print (whether_there_is_a_flux[time_j])
#         resulting_moments_of_event = resulting_moments_of_event + 1;       
# =============================================================================

# the following "averaging" is "nre value is maximum value from the corresponding time interval"
# =============================================================================
# let's make an averaged data (from initial_data - for count rate):
for new_time_j in range(0, new_length_of_data):
    current_averaged_value = 0;
    for little_j in range(0, size_of_time_window ):
        time_j = new_time_j*size_of_time_window + little_j
        if (initial_data.iloc[time_j,1] > averaged_data[new_time_j] ):
            averaged_data[new_time_j] = initial_data.iloc[time_j,1]

# the following makes "whether_there_is_a_flux" from "initial_data.iloc[:, 1]" - withouot any averaging
for time_j in range(0, len(initial_data) ):
    if (initial_data.iloc[time_j,1] > threshold_value ):
        whether_there_is_a_flux[time_j] = 1;
        #print (whether_there_is_a_flux[time_j])
        initial_moments_of_event = initial_moments_of_event + 1;
        
# the following makes "averaged_whether_there_is_a_flux" from "averaged_data" - just the result we need
for new_time_j in range(0, new_length_of_data ):
    if (averaged_data[new_time_j]  > threshold_value ):
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
#    output_file.write(str(array_of_datetimes[new_time_j]))
#    output_file.write('\n')
# the following is just a testing output
#    if (new_time_j < 10):
#        print (initial_data.iloc[time_j,0])
#        print (array_of_datetimes[new_time_j])
 
#output_file.close()

        
with open(output_file, "w") as output:
    for new_time_j in range(0, new_length_of_data ):
        output.write(str(array_of_datetimes[new_time_j]) + '      ' + str(averaged_whether_there_is_a_flux[new_time_j]) + '\n')


print('we have ' + str(initial_moments_of_event) + ' initial_moments of event')
print('we have ' + str(resulting_moments_of_event) + ' resulting_moments of event')
print('we have ' + str(resulting_moments_of_event*size_of_time_window) + ' "initial_moments" of event - AFTER THE AVERAGING')

   
# the following allows us to get (and print) datetimes (initial units) only
#date_times = [0] * (len(initial_data))
#for time_j in range(0, len(initial_data) ):
#    date_times[time_j] = initial_data.iloc[time_j,0][0:2]+'-'+'03-'+initial_data.iloc[time_j,0][7:9]+'_'+initial_data.iloc[time_j,0][10:18]
# to print all the time values in chosen format:
 #   print (date_times[time_j])


plt.figure(figsize=(14,8))
plt.plot(initial_data.iloc[:, 1])
# here "1" is our chose of the column (the second one), ":" means "take every row"
plt.title('Particle flux ', fontsize=22)
plt.xlabel('time', fontsize=20, horizontalalignment='right' )
plt.ylabel('Count rate', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
plt.show()

# Additional output: averaged flux and 0-1-results

# =============================================================================
# plt.figure(figsize=(14,8))
# plt.plot(averaged_data)
# plt.title('Averaged article flux, time_window = '+ str(size_of_time_window) + ' min', fontsize=22)
# plt.xlabel('time', fontsize=20, horizontalalignment='right' )
# plt.ylabel('Count rate', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
# plt.show()
# 
# plt.figure(figsize=(14,8))
# plt.plot( whether_there_is_a_flux)
# plt.title('whether_there_is_a_flux, threshold =  '+ str(threshold_value), fontsize=22)
# plt.xlabel('time', fontsize=20, horizontalalignment='right' )
# plt.ylabel('0_or_1', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
# plt.show()
# 
# plt.figure(figsize=(14,8))
# plt.plot( averaged_whether_there_is_a_flux)
# plt.title('averaged_whether_there_is_a_flux ', fontsize=22)
# plt.xlabel('time', fontsize=20, horizontalalignment='right' )
# plt.ylabel('0_or_1', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
# plt.show()
# =============================================================================

