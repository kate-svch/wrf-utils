#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 16:50:22 2018

@author: kate-svch
"""


import function_big_table_one_event
import datetime


import argparse    # we'll get the data of the event, as an argument

parser = argparse.ArgumentParser(description='Great Description To Be Here')

parser.add_argument('--time_start', '-s', action='store', dest='start', help='It is a date-time of the beginning of the event', type=str)

args = parser.parse_args()

# =============================================================================
# parameters = [(0, 0, 1),
#               (1, 2, 3)]
# 
# from os import system
# 
# for ts, te, n in parameters:
#     system("python3 ml_set_creator_local_0.py --time_start %s --time_end %s --set-number %s" % (ts, te, n))
# =============================================================================

# =============================================================================
# parameters = [('2016-05-04-00','2016-05-05-00', 36000 )];
# start = parameters[0][0];
# end = parameters[0][1];
# threshold = parameters[0][2];
# print (parameters[0][0], '   ', parameters[0][1], '   ' , str(parameters[0][2]))
# =============================================================================

#name_of_file = str(datetime.datetime.now());
#input_params = open('/home/kate-svch/Thunder/Aragats_measurements/test_input_list_of_events_with_thresholds.txt')

input_params = open('/home/kate-svch/Thunder/Aragats_measurements/input_txt_start_end_threshold/' + args.start + '.txt')

for line in input_params:
    start = line[0:13]
    end = line[16:29]
    
    short_name_of_detector = line[32:37]
    
    threshold = int(line[40:-1])
    
    #name_of_detector = 'Stand'
    #name_of_detector = 'NaI_2'
       
    #name_of_detector = 'Stand_1_upper_1cm'
    #name_of_detector = 'NaI_2'
    
    name_of_file = (start) + '_' + (end) + ' ' + str(threshold);
    #print(start, '   ', end, '  ', str(threshold))   
    function_big_table_one_event.find_the_event(start, end, threshold, short_name_of_detector);
    function_big_table_one_event.add_the_event_to_the_big_table(start, end, threshold, name_of_file);


 #   function_big_table_one_event.test_add_the_event(start, end, threshold, name_of_file);






