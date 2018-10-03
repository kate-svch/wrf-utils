#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 16:22:09 2018

@author: kate-svch
"""
import datetime
import matplotlib.pyplot as plt
#initial_folder = '/home/kate-svch/Florida_KSC_electric_mill/2012-11-21/'
#file_name = '201211211430' + '.dat'

b2i = lambda d: int.from_bytes(d, byteorder='big', signed=True)

initial_folder = '/home/kate-svch/Florida_KSC_electric_mill/2012-11-22/'
file_name = '201211220000' + '.dat'
file_name_with_path = initial_folder + file_name
# =============================================================================
# with open(file_name_with_path, "rb") as binary_file:
#     # Read the whole file at once
# # =============================================================================
# #     data = binary_file.read()
# #     print(data)
# # =============================================================================
#     bytes_array = []
#     integers_array = []    
#     
#     for jjj in range (0, 50):
#         current_index = 2*jjj+12   
#         binary_file.seek(current_index)
#         print(current_index)   
#     
#         couple_bytes = binary_file.read(2)
#         bytes_array.append(couple_bytes)
# #        print(couple_bytes)    
    
#     # Create a signed int
#         signed_int_from_couple_of_bytes = int.from_bytes(couple_bytes, byteorder='big', signed=True)
#  #       print(signed_int_from_couple_of_bytes )   
#         integers_array.append(signed_int_from_couple_of_bytes) 
# print(bytes_array)
# print(integers_array)
# =============================================================================
number_of_field_mills = 3
number_of_files = 11
time_start = datetime.datetime(2012, 11, 22, 0, 0)
date_list = [time_start + x*datetime.timedelta(minutes=30) for x in range(0, number_of_files)]

array_of_arrays_of_field = []

for i in range(number_of_field_mills):
    array_of_arrays_of_field.append([])

for j_file in range (0, number_of_files):
    file_name = datetime.datetime.strftime(date_list[j_file], '%Y%m%d%H%M') + '.dat'
    file_name_with_path = initial_folder + file_name
    print(file_name)
    with open(file_name_with_path, "rb") as binary_file:
        while True:
            record = binary_file.read(7184)
            if record is None or len(record)<7184:
                break
        
    #        print(b2i(record[4:5]))
    #        print(b2i(record[5:6]))
    #        print(b2i(record[6:7]))
    #        print(b2i(record[7:8]))
    #        print(b2i(record[8:9]))
    #        print(b2i(record[9:10]))   # this 6 strings is date_and_time: in format yy-mm-dd-hh-mm-ss
                 
            # the maximal possible value of i is 63
            for j_mill in range(number_of_field_mills):
                o = 16+ j_mill*112  
                device_number = b2i(record[o:o+1])                   # the record for one moment and one field mill is 112-long
                if (device_number != (j_mill+1) ):
                    print('NUMBER OF THE FIELD MILL IS DEFINED INCORRECTLY: ')
                    print('device_number = ', device_number)
                    print('j_mill = ', j_mill)
    
                for j in range(50):
    #                print('   ', b2i(record[o+10+j*2:o+10+j*2+2]))
                    array_of_arrays_of_field[j_mill].append(b2i(record[o+10+j*2:o+10+j*2+2]))
    
            
            
for j_mill in range(number_of_field_mills):
#    print(array_of_arrays_of_field[j_mill])    
    plt.figure(figsize=(18,5))
    plt.title('Measurement results from electric field mill № ' + str(j_mill+1))
    plt.plot(array_of_arrays_of_field[j_mill])
    plt.show()            
    print('device_number = ', j_mill+1)