#!/usr/bin/env python3

# it creates 2d-plots for temperature//wind-speed//particle_concentration distribution
# and it has a part, which enables to find and plot the electric field,
# created by the particles of the certain kind (or two kinds)
# the charge density has to be determined by the user

import os
import numpy as np
import matplotlib.pyplot as plt
import datetime
from scipy.io import netcdf

from wrf import getvar, ALL_TIMES
from netCDF4 import Dataset

x_lon = 45                                                                  # Index to d02 Aragats point
y_lat = 45                                                                  # Index to d02 Aragats point

             
model_datetime = datetime.datetime(2018, 3, 4, 18, 0)            # Starting time for WRF modeling (hour, minute)

# this function is used in other files
def set_model_datetime(new_model_datetime):
    global model_datetime
    model_datetime = new_model_datetime


def get_wrf_file():
 #   base_path = os.getenv('HOME')

#    path = os.path.join(base_path, 'wrfmain', 'kate', 'reanalysis')             # path to files
#    path = os.path.join(base_path, 'Thunder', 'Data', 'kate', 'reanalysis') 
    path = os.path.join('/mnt/data-internal/reanalysis') 
    
    # path = os.path.join(base_path, 'wrfmain', 'kate', 'forecast')             # path to files

    path = os.path.join(path, datetime.datetime.strftime(model_datetime, '%Y%m%d%H'))

    file = 'wrfout_d02_'                                                        # domain select
    # file = 'wrfout_d01_'           outside domain                                           # domain select

    file = file + datetime.datetime.strftime(model_datetime, '%Y-%m-%d_%H:00:00')
    return netcdf.netcdf_file(os.path.join(path, file), 'r')

#  number_of_time_points - it's the number of points in the time interval
 
    

def get_geopotential_height(event_datetime, time_point_of_start  = 1):
    time_index = get_index(event_datetime, time_point_of_start)
    file = get_wrf_file()
    temp_ph = file.variables['PH'].data[:]
    temp_phb = file.variables['PHB'].data[:]
    supposed_mountain_height = [3200] * 40
    temp_height = ((temp_ph[time_index+ time_point_of_start, 0:(-1), y_lat, x_lon] + temp_phb[time_index+ time_point_of_start, 0:(-1), y_lat, x_lon])/9.81) - supposed_mountain_height
    return temp_height/1000


# now we'll try to obtain "values of the altitude"
# =============================================================================
# def get_geopotential_height(event_datetime, number_of_time_points=1, time_point_of_start  = 1):
# # "file.variables['T']"  doesn't work!!!     
#     time_index = get_index(event_datetime, time_point_of_start + number_of_time_points )
#     ncfile = Dataset("/mnt/data-internal/reanalysis/2018030418/wrfout_d02_2018-03-04_18:00:00")
#     t_getvar =  getvar(ncfile, 'tc', timeidx = ALL_TIMES)
#     return t_getvar[time_index+ time_point_of_start:time_index+ time_point_of_start+ number_of_time_points, :, y_lat, x_lon]
# =============================================================================
    

def get_t_with_getvar(event_datetime, number_of_time_points=1, time_point_of_start  = 1):
# "file.variables['T']"  doesn't work!!!     
    time_index = get_index(event_datetime, time_point_of_start + number_of_time_points )
    ncfile = Dataset("/mnt/data-internal/reanalysis/2018030418/wrfout_d02_2018-03-04_18:00:00")
    t_getvar =  getvar(ncfile, 'tc', timeidx = ALL_TIMES)
    return t_getvar[time_index+ time_point_of_start:time_index+ time_point_of_start+ number_of_time_points, :, y_lat, x_lon]


def get_t_profile_in_certain_moment_of_time(event_datetime, time_point_of_start  = 1):
      
# get quantity of "name" microphysical fracture from 2m to 20 kilometers height : DIFFERENT HEIGHT ANG TIME
    time_index = get_index(event_datetime, time_point_of_start )
    ncfile = Dataset("/mnt/data-internal/reanalysis/2018030418/wrfout_d02_2018-03-04_18:00:00")
    t_getvar =  getvar(ncfile, 'tc', timeidx = ALL_TIMES)
    return t_getvar[time_index + time_point_of_start, :, y_lat, x_lon]


def get_t2(event_datetime, time_point_of_start=0, number_of_time_points=1):     
    '''
    get temperature at 2 meters level
    number_of_time_points is quantity of values in the time interval
    default number_of_time_points value is 1 - it's established in the function definition
    '''             
    time_index = get_index(event_datetime, time_point_of_start + number_of_time_points)
    file = get_wrf_file()
    temp_t2 = file.variables['T2'].data[:] - 273.15
    return temp_t2[time_index+ time_point_of_start:time_index+ time_point_of_start+ number_of_time_points, y_lat, x_lon]


def get_wind(event_datetime, time_point_of_start=0, number_of_time_points = 1):
    time_index = get_index(event_datetime, time_point_of_start + number_of_time_points)
    file = get_wrf_file()
    u10 = file.variables['U10'].data[:]
    v10 = file.variables['V10'].data[:]
    wind = (u10 * u10 + v10 * v10) ** 0.5
    return wind[time_index+time_point_of_start:time_index+ time_point_of_start + number_of_time_points, y_lat, x_lon]


def get_s_pressure(event_datetime, time_point_of_start=0, number_of_time_points=1):
    '''
    get surface pressure
    '''
    time_index = get_index(event_datetime, time_point_of_start + number_of_time_points)
    file = get_wrf_file()
    s_pressure = file.variables['PSFC'].data[:] / 100
    return s_pressure[time_index+time_point_of_start:time_index+time_point_of_start + number_of_time_points, y_lat, x_lon]


def get_q(event_datetime, name, time_point_of_start  = 1, number_of_time_points=1):
      
# get quantity of "name" microphysical fracture from 2m to 20 kilometers height : DIFFERENT HEIGHT AND TIME
   
    time_index = get_index(event_datetime, time_point_of_start + number_of_time_points )
    file = get_wrf_file()
    vapor = file.variables[name].data[:] / 1
    return vapor[time_index:time_index + number_of_time_points, :, y_lat, x_lon]
# we can see, that first coordinate is abscissa


def get_q_profile_in_certain_moment_of_time(event_datetime, name, time_point_of_start  = 1):
      
# get quantity of "name" microphysical fracture from 2m to 20 kilometers height : DIFFERENT HEIGHT
   
    time_index = get_index(event_datetime, time_point_of_start )
    file = get_wrf_file()
    vapor = file.variables[name].data[:] / 1
    return vapor[time_index, :, y_lat, x_lon]



def get_q_xz(event_datetime, name, number_of_the_time_point = 1):
      
# get quantity of "name" microphysical fracture from 2m to 20 kilometers height: DIFFERENT HEIGHT ANG X-VALUE
   
    time_index = get_index(event_datetime, number_of_the_time_point)
    file = get_wrf_file()
    vapor = file.variables[name].data[:] / 1    
    vapor_xz = vapor[time_index + number_of_the_time_point, :, y_lat, :]
        # we can see, that first coordinate is abscissa
    # let's transpose this array to have z-coordinate as the ordinate
    
    vapor_xz = vapor_xz.transpose() 
    return vapor_xz
    
# =============================================================================
#     time_index = get_index(event_datetime, 1 )
#     file = get_wrf_file()
#     vapor = file.variables[name].data[:] / 1
#     return vapor[time_index:time_index + number_of_the_time_point, :, y_lat, x_lon]
# =============================================================================
    
# the value is opposite to the dry air mass density
def get_alt(event_datetime, time_point_of_start=0, number_of_time_points = 1):
    time_index = get_index(event_datetime, time_point_of_start + number_of_time_points)
    file = get_wrf_file()
    temp_alt = file.variables['ALT'].data[:]
    return temp_alt[time_index+time_point_of_start:time_index+ time_point_of_start + number_of_time_points, 0, y_lat, x_lon]



def el_field_q_int_z_t(event_datetime, name, charge,  number_of_time_points, time_point_of_start  = 1):
     
# get ground value of electric field, cased by the certain part (name) of the air-column, integrated from 2m to 20 kilometers height
#  only one column of air is considered, the impacts of parts ("layers of the column") with different z-values are summed
    
    charge *= 9*10**(9)
    
    time_index = get_index(event_datetime, time_point_of_start + number_of_time_points )
    file = get_wrf_file()
    vapor = file.variables[name].data[:] / 1    
    
    # vapor_tz = vapor[:, :, y_lat, x_lon]
    vapor_tz = vapor[time_index+ time_point_of_start:time_index + time_point_of_start + number_of_time_points, :, y_lat, x_lon]
    
    # for some reason, here the first coordinate corresponds to the ordinate
    # let's transpose this array to have z-coordinate as the ordinate
 #   vapor_tz = vapor_tz.transpose() 
  
    el_field_int_z_t = [0] * number_of_time_points
    for j in range(0, number_of_time_points):
        for z_sum_index in range(0, 40):
            el_field_int_z_t[j] += vapor_tz[j, z_sum_index]/((27+50*z_sum_index)**2)
        el_field_int_z_t[j] *= charge
    return el_field_int_z_t
    #return vapor_tz 
    
    
# =============================================================================
# def el_field_q_int_zx_t(event_datetime, name, number_of_time_points, time_point_of_start  = 1):
#      
# # get ground value of electric field, cased by the certain part (name) of the air-column, integrated from 2m to 20 kilometers height
# #  (2*max_bx + 1) "columns" of air are summed - only x-coordinate is used to "integrate" the impact into field value
#    
#     max_bx = 0;
#     time_index = get_index(event_datetime, time_point_of_start )
#     file = get_wrf_file()
#     vapor = file.variables[name].data[:] / 1    
#     
#     # vapor_tzx = vapor[:, :, y_lat, x_lon]
#   #  vapor_tzx = vapor[time_index:time_index + number_of_time_points, :, y_lat, x_lon - max_bx : x_lon + max_bx + 1]
#     vapor_tzx = vapor[time_index:time_index + number_of_time_points, :, y_lat, :]
#     
#     # for some reason, here the first coordinate corresponds to the ordinate
#     # let's transpose this array to have z-coordinate as the ordinate
#   #  vapor_tzx = vapor_tz.transpose()     
#     el_field_int_zx_t = [0] * number_of_time_points
#     for time_j in range(0, number_of_time_points):
#         for x_delta in range( - max_bx,  + max_bx + 1): 
#             x_number = x_lon + x_delta;
#             for z_sum_index in range(0, 40):
#                 altitude = 27 + 50*z_sum_index;
#                 devider = pow(altitude,2) + pow((1000*x_delta),2)
#                 devider = pow(devider, 1.5)
#                 el_field_int_zx_t[time_j] += vapor_tzx[time_j, z_sum_index, x_number]*altitude/devider;
#     
#     return el_field_int_zx_t
#     #return vapor_tz 
# =============================================================================
    

# =============================================================================
# def el_field_q_int_zxy_t(event_datetime, name, number_of_time_points, time_point_of_start  = 1):
# #    el_field_diff_t is the relative difference between the field values, obtained in defferent way
# # now it returns the difference    
# # get ground value of electric field, cased by the certain part (name) of the air-column, integrated from 2m to 20 kilometers height
# #  (2*max_bx + 1)*(2*max_by + 1) columns of air are summed -  x- and y-coordinate are used to "integrate" the impact into field value  
#     max_bx = 2;
#     max_by = max_bx;
#     time_index = get_index(event_datetime, time_point_of_start )
#     file = get_wrf_file()
#     vapor = file.variables[name].data[:] / 1    
#     
#     vapor_tzxy = vapor[time_index:time_index + number_of_time_points, :, :, :]
#     
#     el_field_int_z_t = el_field_q_int_z_t(event_datetime, name, number_of_time_points, time_point_of_start  = 1)
#          
#     el_field_int_zxy_t = [0] * number_of_time_points
#     el_field_diff_t = [0] * number_of_time_points
#     for time_j in range(0, number_of_time_points):
#         for y_delta in range( - max_by,  + max_by + 1): 
#             y_number = y_lat + y_delta;
#             for x_delta in range( - max_bx,  + max_bx + 1): 
#                 x_number = x_lon + x_delta;
#                 for z_sum_index in range(0, 40):
#                     altitude = 27 + 50*z_sum_index;
#                     devider = pow(altitude,2) + pow((1000*x_delta),2) + pow((1000*y_delta),2)
#                     devider = pow(devider, 1.5)
#                     el_field_int_zxy_t[time_j] += vapor_tzxy[time_j, z_sum_index, x_number, y_number]*altitude/devider;
#         el_field_diff_t[time_j] =  (el_field_int_zxy_t[time_j] -  el_field_int_z_t[time_j])/ el_field_int_zxy_t[time_j];
#     
#     #return el_field_int_zxy_t
#     return el_field_diff_t
# =============================================================================
    

# let's make "array of time values" in seconds, instead of that in "units"
    
def create_time_array_in_hours(start_hour, event_datetime, number_of_time_points, step, time_point_of_start):
# step is the quantity of hours in one "time unit"
# if "time unit" = 5 min, then step = 1/12
    
    start_hour = start_hour * step;
    time_index = get_index(event_datetime, number_of_time_points )
    time_array_in_hours = [start_hour] * number_of_time_points
    
    for j in range(0, number_of_time_points):
        time_array_in_hours[j] += (time_index + j) * step
    return time_array_in_hours




def main():
    #
    # http://www.meteo.unican.es/wiki/cordexwrf/OutputVariables
    #
   # event_datetime = datetime.datetime(2016, 3, 4, 12, 0)
   
    event_datetime = model_datetime;   
    start_hour = event_datetime.hour;    step = 1/12;
    
    charge = 0.5*10**(-3);     

    x_values = [0] * 90
    for j_x in range(0, len(x_values) ):
        x_values[j_x] = (j_x - 45)
     
    #print(get_q(event_datetime, number_of_time_points = 2))
    # theta = file.variables['T'].data[:] + 300
    # pressure = file.variables['P'].data[:]
    # pressure_B = file.variables['PB'].data[:]
    # ptot = pressure + pressure_B
    # temp = theta * (ptot / 1000)


    #name="QICE"
    #name="QSNOW"
    #name="QVAPOR"
    #name="QRAIN"
    #name="QGRAUP"
    name="QCLOUD"


    
    # the following three lines are the automatical determination of "number_of_time_points"   - the time-length of the data 
#    file = get_wrf_file()
#    temp_n_array = file.variables[name].data[:] / 1
#    number_of_time_points = len(temp_n_array[:, 0, y_lat, x_lon]); 
#    time_point_of_start = 0;
    number_of_time_points = 25; 
    time_point_of_start = 91;
    
# let's determine z-values: for all the times (we hope, it doesn't really change)
    model_height = get_geopotential_height(event_datetime, time_point_of_start  = 1)    
    event_time = create_time_array_in_hours(start_hour, event_datetime, number_of_time_points, step, time_point_of_start);
        
     
    plt.figure(figsize=(18,8))
    picture_t_getvar = plt.contourf(event_time, model_height, np.array(get_t_with_getvar(event_datetime, number_of_time_points, time_point_of_start)).transpose())
    plt.colorbar(picture_t_getvar) 
    plt.title('Temperature distribution', fontsize=22)
    plt.xlabel('time', fontsize=20, horizontalalignment='right' )
    plt.ylabel('z, km', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#    plt.axis('image')
    plt.axis('normal')      
    plt.show()    
    
        
    plt.figure(figsize=(18,8))
    plt.title('Temperature profile' , fontsize=22)
    plt.xlabel('z, km', fontsize=20, horizontalalignment='right' )
    plt.ylabel('T, C', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
    plt.plot(model_height, get_t_profile_in_certain_moment_of_time(event_datetime, time_point_of_start))
    plt.show()
        
# =============================================================================
#     plt.figure(figsize=(18,8))
#     plt.title('Value opposite to the dry air density, ground level' , fontsize=22)
#     plt.xlabel('time', fontsize=20, horizontalalignment='right' )
#     plt.ylabel(r'$\frac{m^3}{kg}$', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#     plt.plot(get_alt(event_datetime,time_point_of_start, number_of_time_points))
#     plt.show()
# =============================================================================
    
    plt.figure(figsize=(18,8))
    plt.title('Temperature in time, ground level' , fontsize=22)
    plt.xlabel('time', fontsize=20, horizontalalignment='right' )
    plt.ylabel('T, C', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
    plt.plot(event_time, get_t2(event_datetime,time_point_of_start, number_of_time_points))
    plt.show()
    
    
    plt.figure(figsize=(18,8))
    plt.title('Wind-speed in time, ground level' , fontsize=22)
    plt.xlabel('time', fontsize=20, horizontalalignment='right' )
    plt.ylabel('speed', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
    plt.plot(event_time, get_wind(event_datetime, time_point_of_start,number_of_time_points))
    plt.show()
    
    
    plt.figure(figsize=(18,8))
    plt.title('Pressure in time, ground level' , fontsize=22)
    plt.xlabel('time', fontsize=20, horizontalalignment='right' )
    plt.ylabel('speed', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
    plt.plot(event_time, get_s_pressure(event_datetime, time_point_of_start,number_of_time_points))
    plt.show()


    # plt.plot(get_wind(event_datetime, number_of_time_points = 36))
    # plt.plot(get_s_pressure(event_datetime, number_of_time_points = 36))
    

    plt.figure(figsize=(18,8))
    plt.title(name + ' profile in certain moment of time' , fontsize=22)
    plt.xlabel('z, km', fontsize=20, horizontalalignment='right' )
    plt.ylabel(name, rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
    plt.plot(model_height, get_q_profile_in_certain_moment_of_time(event_datetime, name, time_point_of_start  = 6))
    plt.show()

       
    
#    number_of_time_points = 361;   # it's 289 for twenty-four hours of measurements
    
    plt.figure(figsize=(18,8))
    picture_mass = plt.contourf(event_time, model_height,np.array(get_q(event_datetime, name, time_point_of_start, number_of_time_points)).transpose())   
    plt.colorbar(picture_mass) 
    plt.title('Mass density of '+ name, fontsize=22)
    plt.xlabel('time', fontsize=20, horizontalalignment='right' )
    plt.ylabel('z, km', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#    plt.axis('image')
    plt.axis('normal')
       
    plt.show()
    
    plt.figure(figsize=(18,8))
    
# Let's look on the upper picture - t-z particles distribution, 
# and choose the time-point under interest (one of the values on the time-axis)
# then just use "number_of_the_time_point = that_chosen_value",
# and we'll get x-z particles distribuation - on the lower picture    
    
    picture2 =  plt.contourf(x_values, model_height, np.array(   get_q_xz(event_datetime, name, number_of_the_time_point = 234 )).transpose())
   
    plt.colorbar(picture2) 
    plt.title('Mass density of '+ name, fontsize=22)
    plt.xlabel('x, km', fontsize=20, horizontalalignment='right' )
    plt.ylabel('z, km', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
    plt.axis('normal')
    
    plt.show()
    

    plt.figure(figsize=(14,8))
    
   # picture1 = plt.contourf(np.array(get_q(event_datetime, name, number_of_time_points = 4)).transpose())
  #  picture1 = plt.contourf(np.array(    get_q_xz(event_datetime, name, number_of_the_time_point = 1)).transpose())
   
  # следующая строка - отладочный вывод для построения   "return vapor_tz" из "el_field_q_int_z_t"
  #picture1 = plt.contourf(np.array(el_field_q_int_z_t(event_datetime, name, number_of_time_points  = 4)))
#    plt.colorbar(picture1) 
 #   plt.title('Mass density of '+ name, fontsize=22)
#    plt.xlabel('time', fontsize=20, horizontalalignment='right' )
#    plt.ylabel('altitude', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#    plt.axis('image')
    
    # Let's get some xz-diagrams
    #plt.contourf(np.array(get_q_xz(event_datetime, number_of_the_time_point = 1, name="QVAPOR")))
    
    # Let's get some field t-diagrams
 
    #plt.plot(np.array(el_field_q_int_z_t(event_datetime, name, number_of_time_points  = 288)))
    
    step = 1/12;      # it corresponds to the step value of 5 minutes
    step *= 60; # if we wants the axis to coincide with one from the measurement results
    plt.plot(event_time, np.array(el_field_q_int_z_t(event_datetime, name, charge, number_of_time_points, time_point_of_start)))
    
    #picture1 = plt.plot(np.array(el_field_q_int_zx_t(event_datetime, name, number_of_time_points  = 60)))
    #picture1 = plt.plot(np.array(el_field_q_int_zxy_t(event_datetime, name, number_of_time_points  = 60)))
    plt.title('Electric field created by '+ name, fontsize=22)
    plt.xlabel('time', fontsize=20, horizontalalignment='right' )
    plt.ylabel('El_field, some_unit', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')           
    plt.show()
    
 # let's draw the sum of fields, created by two kinds of cloud-particles
# =============================================================================
#     name1 = "QRAIN"
#     name2 = "QGRAUP"
#     charge1 = 15*10**(-3);
#     charge2 = 0.5*10**(-3);
#     plt.figure(figsize=(14,8)) 
#     sum_of_fields = np.array(el_field_q_int_z_t(event_datetime, name1, charge1, number_of_time_points)) + np.array(el_field_q_int_z_t(event_datetime, name2, charge2, number_of_time_points))
#     plt.plot(create_time_array_in_hours(start_hour, event_datetime, number_of_time_points, step, time_point_of_start  = 1), sum_of_fields)
#     plt.title('Electric field created by '+ name1 + ' and ' + name2, fontsize=22)
#     plt.xlabel('time', fontsize=20, horizontalalignment='right' )
#     plt.ylabel('El_field, some_unit', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#     
#     plt.show()
# =============================================================================



def get_index(event_datetime, max_time_value ):
# THE RESULT, WHICH WILL BE RETURNED, DOESN'T DEPEND ON "max_time_value" VALUE
#     "max_time_value" is used only to check, that such a value is "inside the data"
    if event_datetime < model_datetime:
        raise Exception("Event datetime is less then modeling")
    # hours = 15 ! What does it mean: "hours = 15" ?    
    if event_datetime + datetime.timedelta(seconds=600 * max_time_value ) > model_datetime + datetime.timedelta(hours=74):
        raise Exception("Event datetime is more then modeling")
    time_delta = event_datetime - model_datetime
    return int(time_delta.seconds / 600)


if __name__ == '__main__':
    main()


# just type
#  runfile('/home/kate-svch/Thunder/Aragats measurements/model2.py')
