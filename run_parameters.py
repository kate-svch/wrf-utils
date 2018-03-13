#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 16:50:22 2018

@author: kate-svch
"""


import function_big_table_one_event
import datetime

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

name_of_file = str(datetime.datetime.now());
input_params = open('/home/kate-svch/Thunder/Aragats_measurements/test_input_list_of_events_with_thresholds.txt')
for line in input_params:
    start = line[0:13]
    end = line[16:29]
    threshold = int(line[32:-1])
    #print(start, '   ', end, '  ', str(threshold))   
    function_big_table_one_event.find_the_event(start, end, threshold);
    function_big_table_one_event.add_the_event_to_the_big_table(start, end, threshold, name_of_file);
 #   function_big_table_one_event.test_add_the_event(start, end, threshold, name_of_file);






