#!/usr/bin/env python3

# it creates 2d-plots for temperature//wind-speed//particle_concentration distribution
# and it has a part, which enables to find and plot the electric field,
# created by the particles of the certain kind (or two kinds)
# the charge density has to be determined by the user

import os
import numpy as np
import matplotlib.pyplot as plt
import datetime
#from scipy.io import netcdf
import wrf

from wrf import getvar, ALL_TIMES
from netCDF4 import Dataset

x_lon = 45                                                                  # Index to d02 Aragats point
y_lat = 45                                                                  # Index to d02 Aragats point
           

x_min = 35; x_max = 56;  # it's borders of the drawn area for xz-diagrams
z_index_max = 30;   # it's the maximal index of height: 20 corresponds to approximately  10.2 km



#model_datetime = datetime.datetime(2018, 3, 4, 18, 0)            # Starting time for WRF modeling (hour, minute)

#model_datetime = None #datetime.datetime(2016, 5, 4, 0, 0)  # Starting time for WRF modeling
#model_period = None #datetime.timedelta(minutes=5)
#model_length = None

#current_folder = '/mnt/data-internal/reanalysis'    # this is the folder for the 2018-03-05 event
#current_folder = '/mnt/data-internal/newversion'
#current_folder = '/mnt/data-internal/Mansell'
#current_folder = '/mnt/data-internal/RDA_DS083.3'

#current_folder = '/mnt/data-internal/1minute'
current_folder = '/mnt/data-internal/nizhniy'

# this function is used in other files        
# =============================================================================
# def set_model_datetime(new_model_datetime, new_model_period):
# #     global model_datetime
# #     global model_period
# #     global model_length
#      model_datetime = new_model_datetime
#      model_period = datetime.timedelta(minutes=new_model_period)
#      file = get_wrf_file(model_datetime)
#      variable = file.variables['T2'].data[:]
#      model_length = len(variable[:, y_lat, x_lon])
# =============================================================================
   
def get_wrf_file(model_datetime):
 #   base_path = os.getenv('HOME')
     global current_folder
     path = os.path.join(current_folder) + '/' 
     path = os.path.join(path, datetime.datetime.strftime(model_datetime, '%Y%m%d%H'))
#    file = str(model_datetime.year)+ str(model_datetime.month) + str(model_datetime.day) + str(model_datetime.hour)    
     file = path  + '/wrfout_d02_'  + datetime.datetime.strftime(model_datetime, '%Y-%m-%d_%H:00:00')
     return Dataset(os.path.join(path, file))
 #    return Dataset(os.path.join(path, file))

#  number_of_time_points - it's the number of points in the time interval
 
    
def get_height(model_datetime, x_here):
     file = get_wrf_file(model_datetime)
     base_geopot =  wrf.getvar(file, 'PHB', None)  
     pert_geopot =  wrf.getvar(file, 'PH', None)
     height = (base_geopot + pert_geopot) / 9.81
     temp_height = height[0, :, y_lat, x_here]
     # "ground_height" is the minimal considered value of the altitude: it defines "zero-value" of "z"  (in metres)
     ground_height = height[0, 0, y_lat, x_lon]
     for current_index in range (0, len(temp_height)):
         temp_height[current_index] += -ground_height + 2
     return temp_height
 
    
    
# it's almost the same as get_height
# =============================================================================
# def get_geopotential_height(event_datetime, time_point_of_start  = 1):
#     time_index = get_index(event_datetime, time_point_of_start)
#     file = get_wrf_file()
#     temp_ph = file.variables['PH'].data[:]
#     temp_phb = file.variables['PHB'].data[:]
#     supposed_mountain_height = [3200] * 40
#     temp_height = ((temp_ph[time_index+ time_point_of_start, 0:(-1), y_lat, x_lon] + te#     model_datetime = datetime.datetime(2016, 6, 11, 0, 0)
#     event_finish_datetime = datetime.datetime(2016, 6, 12, 0, 0)
#     the_time_moment = datetime.datetime(2016, 6, 11, 11, 10) 
#     the_start_of_consideration = datetime.datetime(2016, 6, 11, 10, 0) 
#     the_end_of_consideration = datetime.datetime(2016, 6, 11, 16, 0) mp_phb[time_index+ time_point_of_start, 0:(-1), y_lat, x_lon])/9.81) - supposed_mountain_height
#     return temp_height/1000
# =============================================================================


# now we'll try to obtain "values of the altitude"
# =============================================================================
# def get_geopotential_height(event_datetime, number_of_time_points=1, time_point_of_start  = 1):
# # "file.variables['T']"  doesn't work!!!     
#     time_index = get_index(event_datetime, time_point_of_start + number_of_time_points )
#     ncfile = Dataset("/mnt/data-internal/reanalysis/2018030418/wrfout_d02_2018-03-04_18:00:00")
#     t_getvar =  getvar(ncfile, 'tc', timeidx = ALL_TIMES)
#     return t_getvar[time_index+ time_point_of_start:time_index+ time_point_of_start+ number_of_time_points, :, y_lat, x_lon]
# =============================================================================
    

def get_t_with_getvar(model_datetime, model_period, model_length, event_datetime, number_of_time_points=1):
# "file.variables['T']"  doesn't work!!!     
    global current_folder
    time_index = get_index(model_datetime, model_period, model_length, event_datetime, number_of_time_points )
    path = os.path.join(current_folder) + '/' 
    path = os.path.join(path, datetime.datetime.strftime(model_datetime, '%Y%m%d%H'))
    file_name = path  + '/wrfout_d02_'  + datetime.datetime.strftime(model_datetime, '%Y-%m-%d_%H:00:00')
    ncfile = Dataset(file_name)
#    ncfile = Dataset("/mnt/data-internal/reanalysis/2018030418/wrfout_d02_2018-03-04_18:00:00")
    t_getvar =  getvar(ncfile, 'tc', timeidx = ALL_TIMES)
    return t_getvar[time_index:time_index+ number_of_time_points, :, y_lat, x_lon]


def get_t_profile_in_certain_moment_of_time(z_index_max, model_datetime, model_period, model_length, the_time_moment):
      
# get quantity of "name" microphysical fracture from 2m to 20 kilometers height : DIFFERENT HEIGHT AND TIME
    global current_folder
    time_index = get_index(model_datetime, model_period, model_length, the_time_moment, 1 )            
    path = os.path.join(current_folder) + '/' 
    path = os.path.join(path, datetime.datetime.strftime(model_datetime, '%Y%m%d%H'))
    file_name = path  + '/wrfout_d02_'  + datetime.datetime.strftime(model_datetime, '%Y-%m-%d_%H:00:00')
    ncfile = Dataset(file_name)
#    ncfile = Dataset("/mnt/data-internal/reanalysis/2018030418/wrfout_d02_2018-03-04_18:00:00")
    t_getvar =  getvar(ncfile, 'tc', timeidx = ALL_TIMES)
#    return t_getvar[time_index, :, y_lat, x_lon]
    return t_getvar[time_index, 0:z_index_max, y_lat, x_lon]


def get_t2(model_datetime, model_period, model_length, event_datetime, number_of_time_points=1):     
    '''
    get temperature at 2 meters level
    number_of_time_points is quantity of values in the time interval
    default number_of_time_points value is 1 - it's established in the function definition
    '''             
    time_index = get_index(model_datetime, model_period, model_length, event_datetime, number_of_time_points)
    file = get_wrf_file(model_datetime)
#    temp_t2 = file.variables['T2'].data[:] - 273.15
    temp_t2 = wrf.getvar(file, 'T2', None) - 273.15
 #   temp_t2 = wrf.getvar(file,"T2")
    return temp_t2[time_index : time_index + number_of_time_points, y_lat, x_lon]


def get_s_wind(model_datetime, model_period, model_length, event_datetime, time_point_of_start = 1, number_of_time_points = 1):
    time_index = get_index(model_datetime, model_period, model_length, event_datetime, time_point_of_start + number_of_time_points)
    file = get_wrf_file(model_datetime)
    u10 = file.variables['U10'].data[:]         #east-west
    v10 = file.variables['V10'].data[:]         #north-south
    wind = (u10 * u10 + v10 * v10) ** 0.5
    return wind[time_index+time_point_of_start:time_index+ time_point_of_start + number_of_time_points, y_lat, x_lon]
    

def get_wind(model_datetime, model_period, model_length, event_datetime,  number_of_time_points = 1):
    time_index = get_index(model_datetime, model_period, model_length, event_datetime, number_of_time_points)
    file = get_wrf_file(model_datetime)
    u = file.variables['U'].data[:, :, :, :-1]
    v = file.variables['V'].data[:, :, :-1, :]
    wind = (u * u + v * v) ** 0.5
    return wind[time_index:time_index + number_of_time_points, :, y_lat, x_lon]


def get_wind_ground_level(model_datetime, model_period, model_length, event_datetime,  number_of_time_points = 1):
    time_index = get_index(model_datetime, model_period, model_length, event_datetime, number_of_time_points)
    file = get_wrf_file(model_datetime)
    u = file.variables['U'].data[:, :, :, :-1]
    v = file.variables['V'].data[:, :, :-1, :]
    wind = (u * u + v * v) ** 0.5
    return wind[time_index:time_index + number_of_time_points, 0, y_lat, x_lon]


def get_wind_certain_level(model_datetime, model_period, model_length, event_datetime,  z_index, number_of_time_points = 1):
    time_index = get_index(model_datetime, model_period, model_length, event_datetime, number_of_time_points)
    file = get_wrf_file(model_datetime)
    u = file.variables['U'].data[:, :, :, :-1]    #(size: model_length, z_index, y_lat, x_lon)
    v = file.variables['V'].data[:, :, :-1, :]
    wind = (u * u + v * v) ** 0.5
    return wind[time_index:time_index + number_of_time_points, z_index, y_lat, x_lon]


def get_aux_speed_array(array_from_get_wind, aux_speed_height_number):
    min_v = min(array_from_get_wind)
    max_v = max(array_from_get_wind)
    aux_speed_array = [];
    for jj in range (0, aux_speed_height_number + 1):
         aux_speed_array.append( min_v + jj*( (max_v - min_v) /aux_speed_height_number) )
    return aux_speed_array



def get_ew_wind_xz(model_datetime, model_period, model_length, event_datetime, z_index_max):
    time_index = get_index(model_datetime, model_period, model_length, event_datetime, 0)
    file = get_wrf_file(model_datetime)
#    u = file.variables['U'].data[:, :, :, :-1] 
    u = wrf.getvar(file, 'U', None, meta=False)
    return u[time_index,  0:z_index_max, y_lat, x_min:x_max].transpose()

# =============================================================================
# def get_ns_wind_xz(model_datetime, model_period, model_length, event_datetime, z_index_max):
#     time_index = get_index(model_datetime, model_period, model_length, event_datetime, 0)
#     file = get_wrf_file(model_datetime)
#     u = file.variables['V'].data[:, :, :, :-1] 
#     return u[time_index,  0:z_index_max, y_lat, x_min:x_max].transpose()
# =============================================================================

def get_vertical_wind_xz(model_datetime, model_period, model_length, event_datetime, z_index_max):
    time_index = get_index(model_datetime, model_period, model_length, event_datetime,  0)
    file = get_wrf_file(model_datetime)
#    w_wind = file.variables['W'].data[:, :, :, :-1]
    w_wind = wrf.getvar(file, 'W', None, meta=False)
    return w_wind[time_index,  0:z_index_max, y_lat, x_min:x_max].transpose()



def get_s_pressure(model_datetime, model_period, model_length, event_datetime, number_of_time_points=1):
    '''
    get surface pressure
    '''
    time_index = get_index( model_datetime, model_period, model_length, event_datetime, number_of_time_points)
    file = get_wrf_file(model_datetime)
#    s_pressure = file.variables['PSFC'].data[:] / 100.
    s_pressure = wrf.getvar(file, 'PSFC', None, meta=False) /100.
    return s_pressure[time_index : time_index + number_of_time_points, y_lat, x_lon]


def get_q(z_index_max, model_datetime, model_period, model_length, event_datetime, name, number_of_time_points=1):
   # get quantity of "name" microphysical fracture from 2m to 20 kilometers height : DIFFERENT HEIGHT AND TIME
   
    time_index = get_index(model_datetime, model_period, model_length, event_datetime,  number_of_time_points )
    file = get_wrf_file(model_datetime)
    vapor = wrf.getvar(file, name, None)
#    return vapor[time_index : time_index  + number_of_time_points, :, y_lat, x_lon]
    return vapor[time_index : time_index  + number_of_time_points, 0:z_index_max, y_lat, x_lon]
# we can see, that first coordinate is abscissa


def get_mass_density(z_index_max, model_datetime, model_period, model_length, event_datetime, name, number_of_time_points=1):
   # get quantity of "name" microphysical fracture from 2m to 20 kilometers height : DIFFERENT HEIGHT AND TIME
   
    time_index = get_index(model_datetime, model_period, model_length, event_datetime,  number_of_time_points )
    file = get_wrf_file(model_datetime)
    vapor = wrf.getvar(file, name, None) / (wrf.getvar(file, 'ALT', None))  
#    return vapor[time_index : time_index  + number_of_time_points, :, y_lat, x_lon]
    return vapor[time_index : time_index  + number_of_time_points, 0:z_index_max, y_lat, x_lon]



def get_q_profile_in_certain_moment_of_time(model_datetime, model_period, model_length, the_time_moment, name):
      
# get quantity of "name" microphysical fracture from 2m to 20 kilometers height : DIFFERENT HEIGHT
   
    time_index = get_index(model_datetime, model_period, model_length, the_time_moment, 1 )
    file = get_wrf_file(model_datetime)
    vapor = wrf.getvar(file, name, None)
    return vapor[time_index, :, y_lat, x_lon]



def get_q_xz(z_index_max, model_datetime, model_period, model_length, the_time_moment, name):
      
# get quantity of "name" microphysical fracture from 2m to 20 kilometers height: DIFFERENT HEIGHT ANG X-VALUE
   
    time_index = get_index(model_datetime, model_period, model_length, the_time_moment, 1)
    file = get_wrf_file(model_datetime)
    vapor = wrf.getvar(file, name, None)
#    vapor_xz = vapor[time_index , :, y_lat, :]
 
   # let's discover only the certain region along x-axis! 
    vapor_xz = vapor[time_index , 0:z_index_max, y_lat, 35:56]
        # we can see, that first coordinate is abscissa
    # let's transpose this array to have z-coordinate as the ordinate   
    vapor_xz = vapor_xz.transpose() 
    return vapor_xz
    
# EAST OR WEST - HOME IS BEST
def get_mass_density_xz(z_index_max, model_datetime, model_period, model_length, the_time_moment, name, y_index):
      
# get quantity of "name" microphysical fracture from 2m to 20 kilometers height: DIFFERENT HEIGHT ANG X-VALUE
   
    time_index = get_index(model_datetime, model_period, model_length, the_time_moment, 1)
    file = get_wrf_file(model_datetime)
    vapor = wrf.getvar(file, name, None) / (wrf.getvar(file, 'ALT', None))  
#    vapor_xz = vapor[time_index , :, y_lat, :] 
   # let's discover only the certain region along x-axis! 
    vapor_xz = vapor[time_index , 0:z_index_max, y_index, x_min:x_max]    
    #vapor_xz = vapor[time_index , 0:z_index_max, y_lat, :]    
        # we can see, that first coordinate is abscissa
    # let's transpose this array to have z-coordinate as the ordinate   
    vapor_xz = vapor_xz.transpose() 
    return vapor_xz



def get_mass_density_yz(z_index_max, model_datetime, model_period, model_length, the_time_moment, name):
      
# get quantity of "name" microphysical fracture from 2m to 20 kilometers height: DIFFERENT HEIGHT ANG X-VALUE
   
    time_index = get_index(model_datetime, model_period, model_length, the_time_moment, 1)
    file = get_wrf_file(model_datetime)
    vapor = wrf.getvar(file, name, None) / (wrf.getvar(file, 'ALT', None))  
#    vapor_xz = vapor[time_index , :, y_lat, :] 
   # let's discover only the certain region along x-axis! 
    vapor_yz = vapor[time_index , 0:z_index_max, x_min:x_max, x_lon]    
    #vapor_xz = vapor[time_index , 0:z_index_max, y_lat, :]    
        # we can see, that first coordinate is abscissa
    # let's transpose this array to have z-coordinate as the ordinate   
    vapor_yz = vapor_yz.transpose() 
    return vapor_yz



def get_mass_density_integral(z_index_max, model_datetime, model_period, model_length, event_datetime, name, number_of_time_points=1):
   # get quantity of "name" microphysical fracture from 2m to 20 kilometers height : DIFFERENT HEIGHT AND TIME
   
    time_index = get_index(model_datetime, model_period, model_length, event_datetime,  number_of_time_points )
    file = get_wrf_file(model_datetime)
    vapor = wrf.getvar(file, name, None) / (wrf.getvar(file, 'ALT', None)) 
    q_array = vapor[time_index , 0:z_index_max, y_lat, x_min:x_max]
    sum = 0
    for row in range (len(q_array)):
        for col in range(len(q_array[0])):
            sum = sum + q_array[row][col]
    return sum


# =============================================================================
#     time_index = get_index(event_datetime, 1 )
#     file = get_wrf_file()
#     vapor = file.variables[name].data[:] / 1
#     return vapor[time_index:time_index + number_of_the_time_point, :, y_lat, x_lon]
# =============================================================================
    
# the value is opposite to the dry air mass density
def get_alt(model_datetime, model_period, model_length, event_datetime, number_of_time_points = 1):
    time_index = get_index(model_datetime, model_period, model_length, event_datetime, number_of_time_points)
    file = get_wrf_file(model_datetime)
    temp_alt = file.variables['ALT'].data[:]
    return temp_alt[time_index : time_index + number_of_time_points, 0, y_lat, x_lon]



def el_field_q_int_z_t(z_index_max, model_datetime, model_period, model_length, event_datetime, name, charge,  number_of_time_points):
 # get ground value of electric field, cased by the certain part (name) of the air-column, integrated from 2m to 20 kilometers height
#  only one column of air is considered, the impacts of parts ("layers of the column") with different z-values are summed
    
    charge *= 9*10**(9)    
    time_index = get_index(model_datetime, model_period, model_length, event_datetime, number_of_time_points )
    file = get_wrf_file(model_datetime)
    vapor = wrf.getvar(file, name, None) / (wrf.getvar(file, 'ALT', None))  
#    z_vector = get_height(model_datetime)[0:-1]  
    z_vector = get_height(model_datetime, x_lon)[0:z_index_max]             # "z_vector" outside this funciton is height-values in "km", here - in "m"
    # vapor_tz = vapor[:, :, y_lat, x_lon]
    vapor_tz = vapor[time_index : time_index  + number_of_time_points, :, y_lat, x_lon]
 
    el_field_int_z_t = [0] * number_of_time_points
    for j in range(2, number_of_time_points):
     #   for z_sum_index in range(0, 40):
        for z_sum_index in range(2, z_index_max):
            el_field_int_z_t[j] += vapor_tz[j, z_sum_index]/((z_vector[z_sum_index])**2)
        el_field_int_z_t[j] *= charge
    return el_field_int_z_t
    #return vapor_tz 
    


# this auxiliary function returns the dynamics of certain fraction concentration on the ground level:    
def get_q_ground(model_datetime, model_period, model_length, event_datetime, name, number_of_time_points=1):
   # get quantity of "name" microphysical fracture from 2m to 20 kilometers height : DIFFERENT HEIGHT AND TIME
   
    time_index = get_index(model_datetime, model_period, model_length, event_datetime,  number_of_time_points )
    file = get_wrf_file(model_datetime)
    vapor = wrf.getvar(file, name, None)
    return vapor[time_index : time_index  + number_of_time_points, 0, y_lat, x_lon]    

    
    
# let's make "array of time values" in seconds, instead of that in "units"
# it's not needed now because of "time-vector" construction    
# =============================================================================
# def create_time_array_in_hours(start_hour, event_datetime, number_of_time_points, step, time_point_of_start):
# # step is the quantity of hours in one "time unit"
# # if "time unit" = 5 min, then step = 1/12
# 
#     time_index = get_index(event_datetime, number_of_time_points )
#     time_array_in_hours = [start_hour * step] * number_of_time_points
#     
#     for j in range(0, number_of_time_points):
#         time_array_in_hours[j] += (time_index + j) * step
#     return time_array_in_hours
# 
# =============================================================================



def main():
    #
    # http://www.meteo.unican.es/wiki/cordexwrf/OutputVariables
    #
    wrf_step_minutes = 5;
    model_period = datetime.timedelta(minutes = wrf_step_minutes)
    
# LET'S CONSIDER THE EVENT OF MARCH!!        
# =============================================================================
#     model_datetime = datetime.datetime(2018, 3, 4, 18, 0)
#     model_period = datetime.timedelta(minutes = wrf_step_minutes)
# #    set_model_datetime(model_datetime , wrf_step_minutes)        # the second argument is the value of time step, in minutes
#     event_datetime = datetime.datetime(2018, 3, 5, 1, 30)     
#  # here we have an automatical "numnber_of_time_points"-initialization      z_array = np.zeros([40,z_index_max])
#     event_finish_datetime = datetime.datetime(2018, 3, 5, 3, 30)   
# =============================================================================
    

#    set_model_datetime(model_datetime , wrf_step_minutes)        # the second argument is the value of time step, in minutes
    
# =============================================================================
#     model_datetime = datetime.datetime(2016, 5, 4, 0, 0)
#     event_finish_datetime = datetime.datetime(2016, 5, 5, 0, 0)
# 
#     the_time_moment = datetime.datetime(2016, 5, 4, 12, 20) 
#     the_second_time_moment = datetime.datetime(2016, 5, 4, 18, 45) 
# =============================================================================
    
    
# =============================================================================
#     model_datetime = datetime.datetime(2016, 5, 4, 0, 0)
#     event_finish_datetime = datetime.datetime(2016, 5, 5, 0, 0)
# 
#     the_time_moment = datetime.datetime(2016, 5, 4, 19, 10) 
#     the_second_time_moment = datetime.datetime(2016, 5, 4, 15, 00)     
# =============================================================================

    
# =============================================================================
#     model_datetime = datetime.datetime(2016, 5, 11, 18, 0)
#     event_finish_datetime = datetime.datetime(2016, 5, 13, 0, 00)   
#     the_time_moment = datetime.datetime(2016, 5, 12, 5, 30)     
#     the_second_time_moment = datetime.datetime(2016, 5, 12, 10, 50) 
#     the_third_time_moment  = datetime.datetime(2016, 5, 12, 12, 25)     
#     the_fourth_time_moment = datetime.datetime(2016, 5, 12, 14, 0) 
#     the_fifth_time_moment = datetime.datetime(2016, 5, 12, 14, 45) 
# =============================================================================
    
    
# =============================================================================
#     model_datetime = datetime.datetime(2016, 10, 29, 0)
#     event_finish_datetime = datetime.datetime(2016, 10, 30, 12)
#     the_time_moment = datetime.datetime(2016, 10, 29, 7, 0)
#     the_second_time_moment  =  datetime.datetime(2016, 10, 29, 22, 10)
# =============================================================================
   
    
# =============================================================================
#     model_datetime = datetime.datetime(2016, 6, 11, 0, 0)
#   #  event_finish_datetime = datetime.datetime(2016, 6, 12, 0, 0)
#     event_finish_datetime = datetime.datetime(2016, 6, 11, 18, 0)
# 
#     the_time_moment = datetime.datetime(2016, 6, 11, 11, 46)  
#     the_second_time_moment = datetime.datetime(2016, 6, 11, 9, 50)     
#     the_third_time_moment  = datetime.datetime(2016, 6, 11, 10, 5)     
#     the_fourth_time_moment = datetime.datetime(2016, 6, 11, 11, 10) 
# =============================================================================

# =============================================================================
#     model_datetime = datetime.datetime(2018, 3, 30, 0,0)  
#     event_finish_datetime = datetime.datetime(2018, 3, 30, 18, 0)  
#     the_time_moment =   datetime.datetime(2018, 3, 30, 7, 0)   
# =============================================================================

# =============================================================================
#     model_datetime = datetime.datetime(2016, 7, 4, 12, 0)
#     event_finish_datetime = datetime.datetime(2016, 7, 5, 0, 0)
#     the_time_moment = datetime.datetime(2016, 7, 4, 16, 0)  
# =============================================================================

# =============================================================================
#     model_datetime = datetime.datetime(2018, 5, 29, 18, 0)
#     event_finish_datetime = datetime.datetime(2018, 5, 30, 6, 0)
#     the_time_moment = datetime.datetime(2018, 5, 29, 19, 55) 
#     the_start_of_consideration = datetime.datetime(2018, 5, 29, 18, 0) 
#     the_end_of_consideration = datetime.datetime(2018, 5, 30, 6, 0) 
# =============================================================================

############  nizhniy novgorod

    model_datetime = datetime.datetime(2016, 7, 4, 12, 0)
    event_finish_datetime = datetime.datetime(2016, 7, 5, 0, 0)
    the_time_moment = datetime.datetime(2016, 7, 4, 23, 0) 
    the_start_of_consideration = datetime.datetime(2016, 7, 4, 21, 0)
    the_end_of_consideration = datetime.datetime(2016, 7, 4, 23, 30)
    
    y_index = y_lat - 4;

# =============================================================================
#     model_datetime = datetime.datetime(2016, 7, 14, 6, 0)
#     event_finish_datetime = datetime.datetime(2016, 7, 14, 12, 0)
#     the_time_moment = datetime.datetime(2016, 7, 14, 10, 0) 
#     the_start_of_consideration = datetime.datetime(2016, 7, 14, 6, 0)
#     the_end_of_consideration = datetime.datetime(2016, 7, 14, 12, 0)
# =============================================================================
    
# =============================================================================
#     model_datetime = datetime.datetime(2016, 7, 16, 12, 0)
#     event_finish_datetime = datetime.datetime(2016, 7, 17, 0, 0)
#     the_time_moment = datetime.datetime(2016, 7, 16, 23, 0) 
#     the_start_of_consideration = datetime.datetime(2016, 7, 16, 12, 0)
#     the_end_of_consideration = datetime.datetime(2016, 7, 17, 0, 0) 
# =============================================================================
    
    

    the_second_time_moment  = the_time_moment
    the_third_time_moment=  the_time_moment
    the_fourth_time_moment =  the_time_moment

# =============================================================================
#     model_datetime = datetime.datetime(2017, 9, 29, 6, 0)
#     event_finish_datetime = datetime.datetime(2017, 9, 30, 0, 0)
# #    the_time_moment = datetime.datetime(2017, 9, 29, 18, 50) 
#     the_time_moment = datetime.datetime(2017, 9, 29, 19, 35)   
#     the_second_time_moment = datetime.datetime(2017, 9, 29, 20, 10)
# =============================================================================
    
           

   #  "event_datetime" could have any value from modelled time, or just be equal to "model_datetime"
#    event_datetime = datetime.datetime(2016, 4, 26, 12, 00)     
    event_datetime = model_datetime
    
    number_of_time_points  = int ((event_finish_datetime - event_datetime)/datetime.timedelta(0, 0, 0, 0, wrf_step_minutes))  + 1
    
    time_number_start = int ((the_start_of_consideration - event_datetime)/datetime.timedelta(0, 0, 0, 0, wrf_step_minutes))  
    time_number_end = int ((the_end_of_consideration - event_datetime)/datetime.timedelta(0, 0, 0, 0, wrf_step_minutes))  -1
    print('time_number_start = ', time_number_start)
    print('time_number_end = ', time_number_end)
    
#    time_number_start = 0
#    time_number_end = number_of_time_points - 1
    
   
    file = get_wrf_file(model_datetime)
    variable = wrf.getvar(file, 'T2', None)
    model_length = len(variable[:, y_lat, x_lon])  
    
    charge = 0.5*10**(-6);     
    
# =============================================================================
#     z_array = np.zeros([90,z_index_max])  
#     x_array = np.zeros([90,z_index_max])
#     for j_x in range(0, 90):
#         print (j_x)    
#         z_array[j_x,:] = get_height(model_datetime, j_x)[:z_index_max]/1000.
#         x_array[j_x,:] = np.ones([z_index_max]) * j_x - 45
# =============================================================================
        
    z_array = np.zeros([x_max - x_min, z_index_max])
    x_array = np.zeros([x_max - x_min, z_index_max])
    for j_x in range(x_min, x_max):
#        print (j_x)    
        z_array[j_x - x_min,:] = get_height(model_datetime, j_x)[:z_index_max]/1000.
        x_array[j_x - x_min,:] = np.ones([z_index_max]) * j_x - 45
        
        
   # let's try to determine time and height values properly     

    z_vector = get_height(model_datetime, x_lon)[0:z_index_max]/1000
    time_vector = [event_datetime + datetime.timedelta(minutes=wrf_step_minutes * i) for i in range(number_of_time_points)]    
    
   # name_array = ["QCLOUD", "QGRAUP", "QICE",  "QRAIN", "QSNOW","QVAPOR"]
    name_array = ["QCLOUD", "QGRAUP", "QICE",  "QRAIN", "QSNOW"]
   # name_array = ["QSNOW",  "QRAIN",  "QICE", "QGRAUP", "QCLOUD", "QHAIL"]
  #  height_for_wind_indexes_array = [0, 4, 5, 6, 7, 8, 10, 12, 13, 14, 15, 16, 17]
  
    #name_array = ["QGRAUP",  "QSNOW"]
   
 
# =============================================================================
#     vector_T_above_the_station = get_t_profile_in_certain_moment_of_time(z_index_max, model_datetime, model_period, model_length, the_time_moment) 
#     vector_LWC_above_the_station = get_mass_density_xz(z_index_max, model_datetime, model_period, model_length, the_time_moment, 'QCLOUD')[x_lon - x_min]
#     array_LWC = get_mass_density_xz(z_index_max, model_datetime, model_period, model_length, the_time_moment, 'QCLOUD')
#     
#     print('len(vector_T_above_the_station ) = ', len(vector_T_above_the_station ))
#     print('len(vector_LWC_above_the_station) = ', len(vector_LWC_above_the_station))
# #    print(len(array_LWC))
#     print('z_index_max = ', z_index_max)
# =============================================================================

    x_delta = 3   # выбор номера столба по x, считая в любую сторону от центра (от станции) (может быть любого знака)
    x_index = x_lon - x_min + x_delta    # выбор номера столба по x, считая от левого края
 # THIS IS DEW_POINT CURVES - IN THE AXIS "Temperature - Liquid_Water_Content"   
# =============================================================================
#     curves_names = ['Saunders et al 2006', 'Pereyra et al. 2000', 'Takahashi 1978', 'Saunders and Peck 1998']
#     curves_colors = [(0.5, 0, 0.9, 1), (0., 0, 1, 1), (0., 0.6, 0., 1), (0.9, 0.3, 0, 1)]
#     curves_styles = ['-','-.',':','--']
#     
#     curves_array_T = []; curves_array_LWC = []
#     
#     curves_array_T.append ( [-18, -16, -14.6, -13.5, -13, -12.7, -13,  -14, -16, -18 ]) 
#     curves_array_LWC.append( [0.1, 0.39, 0.6, 0.92, 1.25, 1.6, 2.0, 2.55, 3.05, 3.6] )
#     
#     curves_array_T.append ([-18, -14.5, -13.7, -13.4, -13.5, -14.5, -18, -21, -24.5 ])
#     curves_array_LWC.append ( [0.1, 0.45, 0.6, 0.8, 0.92, 1.25, 1.95, 2.5, 3.0 ] )
#     
#     curves_array_T.append ([-30, -25, -21, -18, -13.5, -11.3, -9.5, -8.85, -8.9, -10.7, -13.7, -17.9, -21, -25, -30 ])
#     curves_array_LWC.append ( [0.08, 0.09, 0.12, 0.16, 0.26, 0.4, 0.58, 0.75, 0.95, 1.25, 1.6, 1.85, 2.04, 2.15, 2.2] )
#       
#     curves_array_T.append ([-30, -26.6, -25, -24.5, -22.0, -21.0, -19.1, -18, -16, -14.6, -13.5, -12.5, -10.0, -5.0, -2.5 ])
#     curves_array_LWC.append ( [0.6, 1.0, 1.15, 1.17, 1.1, 1.0, 0.85, 0.77, 0.64, 0.59,  0.54, 0.48, 0.4, 0.38, 0.37] )
#     
#     plt.figure(figsize=(16,10))
#     for curve_number in range (0, len(curves_array_T)):
#         plt.plot(curves_array_T[curve_number], curves_array_LWC[curve_number], linewidth=4, label = curves_names[curve_number], color =  curves_colors[curve_number], linestyle = curves_styles[curve_number])
# #    plt.title('Diagram for Reverse_Curve', fontsize=22)
#     plt.xlabel('T, C', fontsize=25, horizontalalignment='right' )
#     plt.ylabel('LWC,' + r'$\frac{gr}{m^3}$', rotation='horizontal', fontsize=25, horizontalalignment='right', verticalalignment='top')
#     plt.tick_params(axis='both', which='minor', labelsize=25)
#     plt.tick_params(axis='both', which='major', labelsize=25)
#     plt.legend(fontsize=25,loc=2)
#     plt.axis('normal')    
#     plt.xlim(0, -30)  # decreasing temperature
#     plt.ylim(0, 4)  # decreasing time 
#     plt.show()  
#     
#     
#     
#     plt.figure(figsize=(16,10))
#     plt.plot(get_t_profile_in_certain_moment_of_time(z_index_max, model_datetime, model_period, model_length, the_time_moment), 10**(3)*(get_mass_density_xz(z_index_max, model_datetime, model_period, model_length, the_time_moment, 'QCLOUD')[x_index] + get_mass_density_xz(z_index_max, model_datetime, model_period, model_length, the_time_moment, 'QRAIN')[x_index]), linewidth=7, label = 'QCLOUD + QRAIN ' + str(the_time_moment), color = (0,0,0,1))
#     for curve_number in range (0, len(curves_array_T)):
#         plt.plot(curves_array_T[curve_number], curves_array_LWC[curve_number], linewidth=4, label = curves_names[curve_number], color =  curves_colors[curve_number], linestyle = curves_styles[curve_number])
# #    plt.plot(get_t_profile_in_certain_moment_of_time(z_index_max, model_datetime, model_period, model_length, the_time_moment), 10**(3)*get_mass_density_xz(z_index_max, model_datetime, model_period, model_length, the_time_moment, 'QCLOUD')[x_index], linewidth=4, label = 'QCLOUD '+str(the_time_moment), color =  (0, 0, 0, 0.7), linestyle = '--')   
# #    plt.title('Diagram for Reverse_Curve', fontsize=22)
#     plt.xlabel('T, C', fontsize=20, horizontalalignment='right' )
#     plt.ylabel('LWC,' + r'$\frac{gr}{m^3}$', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#     plt.legend(fontsize=20,loc=2)
#     plt.axis('normal')    
#     plt.xlim(0, -30)  # decreasing temperature
#     plt.ylim(0, 4)  # decreasing time 
#     plt.show()     
# =============================================================================
    
    
    
    
    
    
    
    
#    plt.figure(figsize=(18,8))
#    picture_T_LWC_cloud_rain =  plt.plot(get_t_profile_in_certain_moment_of_time(z_index_max, model_datetime, model_period, model_length, the_time_moment), 10**(3)*(get_mass_density_xz(z_index_max, model_datetime, model_period, model_length, the_time_moment, 'QCLOUD')[x_index] + get_mass_density_xz(z_index_max, model_datetime, model_period, model_length, the_time_moment, 'QRAIN')[x_index]), linewidth=3, label = str(the_time_moment), color =  (1, 0.4, 0, 1))   
#    plt.title('Diagram for Reverse_Curve '+ str(the_time_moment) + ', QCLOUD + QRAIN', fontsize=22)
#    plt.xlabel('T, C', fontsize=20, horizontalalignment='right' )
#    plt.ylabel('LVC,' + r'$\frac{gr}{m^3}$', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#    plt.axis('normal')    
#    plt.show() 
    
  
#    IT IS WIND SPEED DISTRIBUTION IN THE VERTICAL PLANE
# =============================================================================
#     wind_array_ew_xz = get_ew_wind_xz(model_datetime, model_period, model_length, the_time_moment, z_index_max);
#     wind_array_vertical_xz = get_vertical_wind_xz(model_datetime, model_period, model_length, the_time_moment, z_index_max);
#     M = 0.1 / np.sqrt(wind_array_ew_xz**2 + wind_array_vertical_xz**2)
#     N = np.sqrt(wind_array_ew_xz**2 + wind_array_vertical_xz**2)
#     plt.rc('xtick', labelsize=18) 
#     plt.rc('ytick', labelsize=18) 
#     pic_wind_xz_with_arrows = plt.figure(figsize=(18,8))
#     plt.title("pivot='mid'; every third arrow; units='inches'")
#     widths = np.linspace(0, 1, 100)
#     wind_z_points = [5,6,7,8, 9,10, 11,12,13,14, 15,16, 17,18, 19]
#     Q = plt.quiver(x_array[:, wind_z_points], z_array[:, wind_z_points],  M[:,wind_z_points] * wind_array_ew_xz[:, wind_z_points],  M[:,wind_z_points] * wind_array_vertical_xz[:, wind_z_points], N[:,wind_z_points], cmap=plt.cm.YlGnBu)
# #    Q = plt.streamplot(x_array[0, :], z_array[:, 0],  wind_array_ew_xz[:, :],  wind_array_vertical_xz[:, :])
#     qk = plt.quiverkey(Q, 0.9, 0.9, 2, r'$2 \frac{m}{s}$', labelpos='E', coordinates='figure')
#     plt.scatter(x_arind_array_ew_xz = get_ew_wind_xz(model_datetime, model_period, model_length, the_time_moment, z_index_max);ray, z_array, color='r', s=5)
#     plt.xlabel('x, km', fontsize=20, horizontalalignment='right' )
#     plt.ylabel('z, km', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#     plt.colorbar(Q) 
#     plt.show()
# =============================================================================

    
 # IT IS TEMPERATURE PROFILES   
# =============================================================================
#     plt.figure(figsize=(18,8))
#     plt.title('Temperature profile'+ ', '+ str(the_time_moment) , fontsize=22)
#     plt.xlabel('z, km', fontsize=20, horizontalalignment='right' )
#     plt.ylabel('T, C', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#     plt.plot(z_vector, get_t_profile_in_certain_moment_of_time(z_index_max, model_datetime, model_period, model_length, the_time_moment), linewidth=3, label = str(the_time_moment), color =  (1, 0.4, 0, 1))   
    
#     plt.figure(figsize=(18,8))
#     plt.title('Temperature profile'+ ', '+ str(the_time_moment) , fontsize=22)
#     plt.xlabel('z, km', fontsize=20, horizontalalignment='right' )
#     plt.ylabel('T, C', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
# #    plt.plot(z_vector, get_t_profile_in_certain_moment_of_time(z_index_max, model_datetime, model_period, model_length, the_time_moment), linewidth=3, label = str(the_time_moment), color =  (1, 0.4, 0, 1))
#     plt.plot(z_vector, get_t_profile_in_certain_moment_of_time(z_index_max, model_datetime, model_period, model_length, the_second_time_moment), linewidth=3, label = str(the_second_time_moment), color =  (0.9, 0, 0.4, 1))
#     plt.plot(z_vector, get_t_profile_in_certain_moment_of_time(z_index_max, model_datetime, model_period, model_length, the_third_time_moment), linewidth=3, label = str(the_third_time_moment), color =  (0.5, 0.9, 0, 1))
#     plt.plot(z_vector, get_t_profile_in_certain_moment_of_time(z_index_max, model_datetime, model_period, model_length, the_fourth_time_moment), linewidth=3, label = str(the_fourth_time_moment))    
#     plt.legend(fontsize=20,loc=1)
#     plt.show()
# =============================================================================
    



  #  "event_datetime" could have any value from modelled time, or just be equal to "model_datetime"
#    event_datetime = datetime.datetime(2016, 4, 26, 12, 00)     
   
    file = get_wrf_file(model_datetime)
    variable = wrf.getvar(file, 'T2', None)
    model_length = len(variable[:, y_lat, x_lon])  
    
#    number_of_time_points = 25; 

    charge = 0.5*10**(-3);     
    
# =============================================================================
#     z_array = np.zeros([90,z_index_max])  
#     x_array = np.zeros([90,z_index_max])
#     for j_x in range(0, 90):
#         print (j_x)    
#         z_array[j_x,:] = get_height(model_datetime, j_x)[:z_index_max]/1000.
#         x_array[j_x,:] = np.ones([z_index_max]) * j_x - 45
# =============================================================================

        
# =============================================================================
#     plt.figure(figsize=(18,8))
#     plt.title('Value opposite to the dry air density, ground level' , fontsize=22)
#     plt.xlabel('time', fontsize=20, horizontalalignment='right' )
#     plt.ylabel(r'$\frac{m^3}{kg}$', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#     plt.plot(get_alt(event_datetime,time_point_of_start, number_of_time_points))
#     plt.show()
# =============================================================================
    
    
#    time_number_start = number_of_time_points* (3)//(7)
#    time_number_finish = number_of_time_points* 8//9  
    
    for name in name_array:
        
# =============================================================================
#         plt.figure(figsize=(18,8))
#         plt.title(name + ' profile in certain moment of time' , fontsize=22)
#         plt.xlabel('z, km', fontsize=20, horizontalalignment='right' )
#         plt.ylabel(name, rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#         plt.plot(z_vector, get_q_profile_in_certain_moment_of_time(model_datetime, model_period, model_length, the_time_moment, name))
#         plt.show()
# =============================================================================
    
        
        plt.figure(figsize=(18,8))
#        picture_mass = plt.contourf(time_vector, z_vector, np.array(get_mass_density(z_index_max, model_datetime, model_period, model_length, event_datetime, name, number_of_time_points)).transpose())   
        picture_mass = plt.contourf(time_vector[time_number_start:time_number_end], z_vector, np.array(get_mass_density(z_index_max, model_datetime, model_period, model_length, event_datetime, name, number_of_time_points)).transpose()[:, time_number_start:time_number_end])
        plt.colorbar(picture_mass, format =  "%0.6f" ) 
        plt.title('Density: '+ name, fontsize=22)
        plt.xlabel('time', fontsize=20, horizontalalignment='right' )
        plt.ylabel('z, km', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
    #    plt.axis('image')
        plt.axis('normal')     
#        plt.xlim(time_vector[time_number_start], time_vector[time_number_end] )
        plt.show()
                     
        
    # Let's look on the upper picture - t-z particles distribution, 
    # and choose the time-point under interest (one of the values on the time-axis)
    # then just use "number_of_the_time_point = that_chosen_value",
    # and we'll get x-z particles distribuation - on the lower picture    
        
  #      picture2 =  plt.contourf(x_values, z_vector, np.array(   get_q_xz(z_index_max, model_datetime, model_period, model_length, the_time_moment, name )).transpose())    
   

# EAST OR WEST     
        plt.figure(figsize=(22, 7))
        picture2 =  plt.contourf(x_array, z_array, np.array(    get_mass_density_xz(z_index_max, model_datetime, model_period, model_length, the_time_moment, name, y_index )))
        plt.colorbar(picture2, format =  "%0.6f") 
        plt.title('Density: '+ name + '  '+ str(the_time_moment), fontsize=22)
        plt.xlabel('x, km', fontsize=20, horizontalalignment='right' )
        plt.ylabel('z, km', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
        plt.axis('normal')
        plt.show()
        
# SOUTH OR NORTH        
# =============================================================================
#         plt.figure(figsize=(22, 7))
#         picture3 =  plt.contourf(x_array, z_array, np.array(    get_mass_density_yz(z_index_max, model_datetime, model_period, model_length, the_time_moment, name )))
#         plt.colorbar(picture3, format =  "%0.6f") 
#         plt.title('Density: '+ name + '  '+ str(the_time_moment), fontsize=22)
#         plt.xlabel('y, km', fontsize=20, horizontalalignment='right' )
#         plt.ylabel('z, km', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#         plt.axis('normal')
#         plt.show()
# =============================================================================
    
    
        plt.figure(figsize=(14,8))
        plt.plot(time_vector[time_number_start:time_number_end], np.array(el_field_q_int_z_t(z_index_max, model_datetime, model_period, model_length, event_datetime, name, charge, number_of_time_points))[time_number_start:time_number_end])
        plt.title('Electric field created by '+ name, fontsize=22)
        plt.xlabel('time', fontsize=20, horizontalalignment='right' )
        plt.ylabel('El_field, some_unit', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')          
        plt.xlim(time_vector[time_number_start], time_vector[time_number_end] )
   #     plt.xlim(time_vector[time_start_index]  , time_vector[time_finish_index] )
        plt.show()
       
    
    
 # let's draw the sum of fields, created by two kinds of cloud-particles
    name1 = "QSNOW"
    name2 = "QGRAUP"
    charge1 = -40*10**(1);
    charge2 = 120*10**(1);
    plt.figure(figsize=(14,8)) 
    sum_of_fields = 10**(-3)*(np.array(el_field_q_int_z_t(z_index_max, model_datetime, model_period, model_length, event_datetime, name1, charge1, number_of_time_points)) + np.array(el_field_q_int_z_t(z_index_max, model_datetime, model_period, model_length, event_datetime, name2, charge2, number_of_time_points)))
    plt.plot(time_vector[time_number_start:time_number_end], sum_of_fields[time_number_start:time_number_end])
    plt.title('Electric field created by '+ name1 + ' and ' + name2, fontsize=22)
    plt.xlabel('time', fontsize=20, horizontalalignment='right' )
    plt.ylabel(r'$\frac{kV}{m}$', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
    plt.xlim(time_vector[time_number_start], time_vector[time_number_end] )    
  #  plt.ylim(-8, 8 )   
    plt.show()
  
    

 # let's draw the sum of fields, created by three kinds of cloud-particles
# =============================================================================
#     name1 = "QGRAUP"
#     name2 = "QSNOW"
#     name3 = "QCLOUD"
#     charge1 = +3.5*10**(-5);
#     charge2 = 0.8*10**(-3);
#     charge3 = 0.5*10**(-4);#     model_datetime = datetime.datetime(2016, 10, 29, 0)
#     event_finish_datetime = datetime.datetime(2016, 10, 30, 12)
#     the_time_moment = datetime.datetime(2016, 10, 29, 22, 10)
#     the_second_time_moment  =  datetime.datetime(2016, 10, 29, 22, 10)
#     plt.figure(figsize=(14,8)) 
#     sum_of_fields = np.array(el_field_q_int_z_t(model_datetime, model_period, model_length, event_datetime, name1, charge1, number_of_time_points)) + np.array(el_field_q_int_z_t(model_datetime, model_period, model_length, event_datetime, name2, charge2, number_of_time_points)) + np.array(el_field_q_int_z_t(model_datetime, model_period, model_length, event_datetime, name3, charge3, number_of_time_points))
#     plt.plot(time_vector, sum_of_fields)
#     plt.title('Electric field created by '+ name1 + ', ' + name2 + ' and ' + name3, fontsize=22)
#     plt.xlabel('time', fontsize=20, horizontalalignment='right' )
#     plt.ylabel('El_field, some_unit', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#     plt.xlim(time_vector[0], time_vector[-1] )    
#     plt.show()
# =============================================================================



def get_index(model_datetime, model_period, model_length, event_datetime, vector):        # in what follows "vector" is called "number of time points"
    
 ## returns numnber of time-point, which corresponds to "event_datetime"   
    
#     global model_length 
     if event_datetime < model_datetime:
         raise Exception("Event datetime is less then modeling")
     if event_datetime + model_period * vector > model_datetime + model_length * model_period:
         raise Exception("Event datetime is more then modeling")
     time_delta = event_datetime - model_datetime
     return int(time_delta.seconds / model_period.seconds)


if __name__ == '__main__':
    main()


# just type
#  runfile('/home/kate-svch/Thunder/Aragats measurements/model2.py')
