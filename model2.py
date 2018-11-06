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
import wrf
from wrf import getvar, vinterp

from wrf import getvar, ALL_TIMES
from netCDF4 import Dataset


x_lon = 45                                                                  # Index to d02 Aragats point
y_lat = 45                                                                  # Index to d02 Aragats point
x_min = 44; x_max = 47; 
#x_min = 39; x_max = 52;  # it's borders of the drawn area for xz-diagrams
#z_index_max = 20;   # it's the maximal index of height: 20 corresponds to approximately  10.2 km

           
#model_datetime = datetime.datetime(2018, 3, 4, 18, 0)            # Starting time for WRF modeling (hour, minute)

#model_datetime = None #datetime.datetime(2016, 5, 4, 0, 0)  # Starting time for WRF modeling
#model_period = None #datetime.timedelta(minutes=5)
#model_length = None

#current_folder = '/mnt/data-internal/reanalysis'    # this is the folder for the 2018-03-05 event

current_folder = '/mnt/data-internal/newversion'
#current_folder = '/mnt/data-internal/Mansell'

#current_folder = '/mnt/data-internal/RDA_DS083.3'


# this function is used in other files            temp_t2 = file.variables['T2'].data[:] - 273.15
# =============================================================================
# def set_model_datetime(new_model_datetime, new_model_period):charge_starting_point = 19;   # minimal z_Inside_index: all the lower hydrometeors are suppposed to be uncharged (19 corresponds to 0.5 km)
# #     global model_datetime
# #     global model_period
# #     global model_length
#      model_datetime = new_model_datetime
#      model_period = datetime.timedelta(minutes=new_model_period)
#      file = get_wrf_file(model_datetime)x
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
     return netcdf.netcdf_file(os.path.join(path, file), 'r')
 #    return Dataset(os.path.join(path, file))

#  number_of_time_points - it's the number of points in the time interval
 
    
def get_height(model_datetime, x_here):
     file = get_wrf_file(model_datetime)
 #    base_geopot = file.variables['PHB'].data[:]
 #    pert_geopot = file.variables['PH'].data[:]
 #    height = (base_geopot + pert_geopot) / 9.81
     height = getvar(file, 'z', meta = False)
     temp_height = height[:, y_lat, x_here]
     # "ground_height" is the minimal considered value of the altitude: it defines "zero-value" of "z"  (in metres)
     ground_height = height[0, y_lat, x_lon]
     for current_index in range (0, len(temp_height)):
         temp_height[current_index] += -ground_height + 2
     return temp_height
 
    
def get_height_for_y(model_datetime, y_here):
     file = get_wrf_file(model_datetime)
 #    base_geopot = file.variables['PHB'].data[:]
 #    pert_geopot = file.variables['PH'].data[:]
 #    height = (base_geopot + pert_geopot) / 9.8ng around detector sire at1
     height = getvar(file, 'z', meta = False)
     temp_height = height[:, y_here, x_lon]
     # "ground_height" is the minimal considered value of the altitude: it defines "zero-value" of "z"  (in metres)the_time_moment_index
     ground_height = height[0, y_lat, x_lon]
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
#     supposed_mountain_height = [3200] * 40череда
#     temp_height = ((temp_ph[time_index+ time_point_of_start, 0:(-1), y_lat, x_lon] + temp_phb[time_index+ time_point_of_start, 0:(-1), y_lat, x_lon])/9.81) - supposed_mountain_height
#     return temp_height/1000x_min = 39; x_max = 52;  # it's borders of the drawn area for xz-diagrams
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
    temp_t2 = file.variables['T2'].data[:] - 273.15
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


def get_ew_wind_certain_level(model_datetime, model_period, model_length, event_datetime,  z_index, number_of_time_points = 1):
    time_index = get_index(model_datetime, model_period, model_length, event_datetime, number_of_time_points)
    file = get_wrf_file(model_datetime)
    u = file.variables['U'].data[:, :, :, :-1] 
    return u[time_index:time_index + number_of_time_points, z_index, y_lat, x_lon]

def get_ns_wind_certain_level(model_datetime, model_period, model_length, event_datetime,  z_index, number_of_time_points = 1):   
    time_index = get_index(model_datetime, model_period, model_length, event_datetime, number_of_time_points)
    file = get_wrf_file(model_datetime)
    v = file.variables['V'].data[:, :, :-1, :]
    return v[time_index:time_index + number_of_time_points, z_index, y_lat, x_lon]

def get_vertical_wind_certain_level(model_datetime, model_period, model_length, event_datetime,  z_index, number_of_time_points = 1):
    time_index = get_index(model_datetime, model_period, model_length, event_datetime, number_of_time_points)
    file = get_wrf_file(model_datetime)
    w_wind = file.variables['W'].data[:, :, :, :-1]
    return w_wind[time_index:time_index + number_of_time_points, z_index, y_lat, x_lon]



def get_ew_wind_xz(model_datetime, model_period, model_length, event_datetime, z_index_max):
    time_index = get_index(model_datetime, model_period, model_length, event_datetime, 0)
    file = get_wrf_file(model_datetime)
    u = file.variables['U'].data[:, :, :, :-1] 
    return u[time_index,  0:z_index_max, y_lat, x_min:x_max].transpose()

def get_ns_wind_xz(model_datetime, model_period, model_length, event_datetime, z_index_max):
    time_index = get_index(model_datetime, model_period, model_length, event_datetime, 0)
    file = get_wrf_file(model_datetime)
    u = file.variables['V'].data[:, :, :, :-1] 
    return u[time_index,  0:z_index_max, y_lat, x_min:x_max].transpose()

def get_vertical_wind_xz(model_datetime, model_period, model_length, event_datetime, z_index_max):
    time_index = get_index(model_datetime, model_period, model_length, event_datetime,  0)
    file = get_wrf_file(model_datetime)
    w_wind = file.variables['W'].data[:, :, :, :-1]
    return w_wind[time_index,  0:z_index_max, y_lat, x_min:x_max].transpose()


def get_s_pressure(model_datetime, model_period, model_length, event_datetime, number_of_time_points=1):
    '''
    get surface pressure
    '''
    time_index = get_index( model_datetime, model_period, model_length, event_datetime, number_of_time_points)
    file = get_wrf_file(model_datetime)
    s_pressure = file.variables['PSFC'].data[:] / 100
    return s_pressure[time_index : time_index + number_of_time_points, y_lat, x_lon]


def get_q(z_index_max, model_datetime, model_period, model_length, event_datetime, name, number_of_time_points=1):
   # get quantity of "name" microphysical fracture from 2m to 20 kilometers height : DIFFERENT HEIGHT AND TIME
   
    time_index = get_index(model_datetime, model_period, model_length, event_datetime,  number_of_time_points )
    file = get_wrf_file(model_datetime)
    vapor = file.variables[name].data[:] / 1
#    return vapor[time_index : time_index  + number_of_time_points, :, y_lat, x_lon]
    return vapor[time_index : time_index  + number_of_time_points, 0:z_index_max, y_lat, x_lon]
# we can see, that first coordinate is abscissa
    

def get_mass_density(z_index_max, model_datetime, model_period, model_length, event_datetime, name, number_of_time_points=1):
   # get quantity of "name" microphysical fracture from 2m to 20 kilometers height : DIFFERENT HEIGHT AND TIME
   
    time_index = get_index(model_datetime, model_period, model_length, event_datetime,  number_of_time_points )
    file = get_wrf_file(model_datetime)
    vapor = file.variables[name].data[:] / (file.variables['ALT'].data[:])  
#    return vapor[time_index : time_index  + number_of_time_points, :, y_lat, x_lon]
    return vapor[time_index : time_index  + number_of_time_points, 0:z_index_max, y_lat, x_lon]


def get_q_profile_in_certain_moment_of_time(model_datetime, model_period, model_length, the_time_moment, name):
      
# get quantity of "name" microphysical fracture from 2m to 20 kilometers height : DIFFERENT HEIGHT
   
    time_index = get_index(model_datetime, model_period, model_length, the_time_moment, 1 )
    file = get_wrf_file(model_datetime)
    vapor = file.variables[name].data[:] / 1
    return vapor[time_index, :, y_lat, x_lon]



def get_q_xz(z_index_max, model_datetime, model_period, model_length, the_time_moment, name):
      
# get quantity of "name" microphysical fracture from 2m to 20 kilometers height: DIFFERENT HEIGHT ANG X-VALUE
   
    time_index = get_index(model_datetime, model_period, model_length, the_time_moment, 1)
    file = get_wrf_file(model_datetime)
    vapor = file.variables[name].data[:] / 1    
#    vapor_xz = vapor[time_index , :, y_lat, :]  x_min = 39; x_max = 52;  # it's borders of the drawn area for xz-diagrams
   # let's discover only the certain region along x-axis! 
    vapor_xz = vapor[time_index , 0:z_index_max, y_lat, x_min:x_max]    
    #vapor_xz = vapor[time_index , 0:z_index_max, y_lat, :]    
        # we can see, that first coordinate is abscissa
    # let's transpose this array to have z-coordinate as the ordinate   
    vapor_xz = vapor_xz.transpose() 
    return vapor_xz



def get_mass_density_xz(z_index_max, model_datetime, model_period, model_length, the_time_moment, name):
      
# get quantity of "name" microphysical fracture from 2m to 20 kilometers height: DIFFERENT HEIGHT ANG X-VALUE
   
    time_index = get_index(model_datetime, model_period, model_length, the_time_moment, 1)
    file = get_wrf_file(model_datetime)
    vapor = file.variables[name].data[:] / (file.variables['ALT'].data[:])  
#    vapor_xz = vapor[time_index , :, y_lat, :] 
   # let's discover only the certain region along x-axis! 
    vapor_xz = vapor[time_index , 0:z_index_max, y_lat, x_min:x_max]    
    #vapor_xz = vapor[time_index , 0:z_index_max, y_lat, :]    
        # we can see, that first coordinate is abscissa
    # let's transpose this array to have z-coordinate as the ordinate   
    vapor_xz = vapor_xz.transpose() 
    return vapor_xz


def get_mass_density_yz(z_index_max, model_datetime, model_period, model_length, the_time_moment, name):
      
# get quantity of "name" microphysical fracture from 2m to 20 kilometers height: DIFFERENT HEIGHT ANG X-VALUE
   
    time_index = get_index(model_datetime, model_period, model_length, the_time_moment, 1)
    file = get_wrf_file(model_datetime)
    vapor = file.variables[name].data[:] / (file.variables['ALT'].data[:])  
#    vapor_xz = vapor[time_index , :, y_lat, :] 
   # let's discover only the certain region along x-axis! 
    vapor_yz = vapor[time_index , 0:z_index_max, x_min:x_max, x_lon]    
    #vapor_xz = vapor[time_index , 0:z_index_max, y_lat, :]    
        # we can see, that first coordinate is abscissa
    # let's transpose this array to have z-coordinate as the ordinate   number_of_time_points
    vapor_yz = vapor_yz.transpose() 
    return vapor_yz




#let's get the "integral q-value" - to estimate the charge of particles of the type
def get_mass_density_integral(z_index_max, model_datetime, model_period, model_length, event_datetime, name, number_of_time_points=1):
   # get quantity of "name" microphysical fracture from 2m to 20 kilometers height : DIFFERENT HEIGHT AND TIME
   
    time_index = get_index(model_datetime, model_period, model_length, event_datetime,  number_of_time_points )
    file = get_wrf_file(model_datetime)
    vapor = file.variables[name].data[:] / (file.variables['ALT'].data[:])  
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
    vapor = file.variables[name].data[:] /  (file.variables['ALT'].data[:])       
#    z_vector = get_height(model_datetime)[0:-1]  
    z_vector = get_height(model_datetime, x_lon)[0:z_index_max]             # "z_vector" outside this funciton is height-values in "km", here - in "m"
    # vapor_tz = vapor[:, :, y_lat, x_lon]
    vapor_tz = vapor[time_index : time_index  + number_of_time_points, :, y_lat, x_lon]
 
    el_field_int_z_t = [0] * number_of_time_points
    for j in range(0, number_of_time_points):
     #   for z_sum_index in range(0, 40):
        for z_sum_index in range(1, z_index_max):
            el_field_int_z_t[j] += vapor_tz[j, z_sum_index]/((z_vector[z_sum_index])**2)
        el_field_int_z_t[j] *= charge
    return el_field_int_z_t
    #return vapor_tz 
    


# this auxiliary function returns the dynamics of certain fraction concentration on the ground level:    
def get_q_ground(model_datetime, model_period, model_length, event_datetime, name, number_of_time_points=1):
   # get quantity of "name" microphysical fracture from 2m to 20 kilometers height : DIFFERENT HEIGHT AND TIME
   
    time_index = get_index(model_datetime, model_period, model_length, event_datetime,  number_of_time_points )
    file = get_wrf_file(model_datetime)
    vapor = file.variables[name].data[:]
    return vapor[time_index : time_index  + number_of_time_points, 0, y_lat, x_lon]    

    
    
# let's make "array of time values" in seconds, instead of that in "units"
# it's not needed now because of "time-vector" construction    
# =============================================================================
# def create_time_array_in_hours(start_hour, event_datetime, number_of_time_points, step, time_point_of_start):
# # step is the quantity of hours in one "time unit"
# # if "time unit" = 5 min, then step = 1/12z_index_max
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
#     the_time_moment = datetime.datetime(2016, 5, 4, 11, 0) 
#     the_second_time_moment = datetime.datetime(2016, 5, 4, 15, 00)     
# =============================================================================
#    the_time_moment = datetime.datetime(2016, 5, 4, 19, 10) 
#    the_second_time_moment = datetime.datetime(2016, 5, 4, 18, 45) 
    
    
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
#     model_datetime = datetime.datetime(2016, 4, 26, 12, 0)
#     event_finish_datetime = datetime.datetime(2016, 4, 29, 0, 0)
# 
#     the_time_moment = datetime.datetime(2016, 4, 28, 2, 0) 
#     the_second_time_moment = datetime.datetime(2016, 4, 28, 2, 0) 
# =============================================================================
    
       
# =============================================================================
#     model_datetime = datetime.datetime(2016, 10, 29, 0)
#     event_finish_datetime = datetime.datetime(2016, 10, 30, 12)
#     the_time_moment = datetime.datetime(2016, 10, 29, 22, 10)
#     the_second_time_moment  =  datetime.datetime(2016, 10, 29, 22, 10)
# =============================================================================
     
    
    model_datetime = datetime.datetime(2016, 6, 11, 0, 0)
    event_finish_datetime = datetime.datetime(2016, 6, 12, 0, 0)

    the_time_moment = datetime.datetime(2016, 6, 11, 11, 10) 
    the_second_time_moment = datetime.datetime(2016, 6, 11, 9, 50)     
    the_third_time_moment  = datetime.datetime(2016, 6, 11, 10, 5)     
    the_fourth_time_moment = datetime.datetime(2016, 6, 11, 11, 10) 
    the_fifth_time_moment = datetime.datetime(2016, 5, 12, 14, 45) 


    the_second_time_moment  = the_time_moment
    the_third_time_moment=  the_time_moment
    the_fourth_time_moment =  the_time_moment
    the_fifth_time_moment = the_time_moment

# =============================================================================
#     model_datetime = datetime.datetime(2017, 9, 29, 6, 0)
#     event_finish_datetime = datetime.datetime(2017, 9, 30, 0, 0)
# #    the_time_moment = datetime.datetime(2017, 9, 29, 18, 50) 
#     the_time_moment = datetime.datetime(2017, 9, 29, 19, 35)   
#     the_second_time_moment = datetime.datetime(2017, 9, 29, 20, 10)array_loaded 
# =============================================================================
    
    
        
 # here we have an automatical "numnber_of_time_points"-initialization      
   #  "event_datetime" could have any value from modelled time, or just be equal to "model_datetime"
    event_datetime = model_datetime
    number_of_time_points  = int ((event_finish_datetime - event_datetime)/datetime.timedelta(0, 0, 0, 0, wrf_step_minutes))  + 1
    
   
   
    file = get_wrf_file(model_datetime)
    variable = file.variables['T2'].data[:]
    model_length = len(variable[:, y_lat, x_lon])      
# INTERPOLATION parameters are defined here   convert to a non-
    
    path = os.path.join(current_folder) + '/' 
    path = os.path.join(path, datetime.datetime.strftime(model_datetime, '%Y%m%d%H'))
    file_name = path  + '/wrfout_d02_'  + datetime.datetime.strftime(model_datetime, '%Y-%m-%d_%H:00:00')
    ncfile = Dataset(file_name)
    
    
    height = getvar(file, 'z', meta = False)
    height_min =  0.12  #km
    height_max = 8
    mnt_from_msl = height[0, y_lat, x_lon]/1000.  # высота станции над mean sea level
    
    height_array_for_interp = np.arange(height_min + mnt_from_msl, height_max + mnt_from_msl, 0.02)   # in km
    start_level = 'ght_msl' # above_mean_sea_level ; 'ght_agl' - above ground level    
    
    
    height_array_zero_on_the_ground = np.arange(height_min , height_max,  0.02) # in km
      # we write "z_array" in file just once - in assumption, that it is  one and the same array for each "name" (type of hydrometeors)
    np.save('/home/kate-svch/Thunder/Aragats_measurements/py-codes/z_and_dens_arrays/z_array_' + datetime.datetime.strftime(the_time_moment, '%Y-%m-%d_%H:00:00') +'.npy', np.array(height_array_zero_on_the_ground))
    
    

    z_index_max = 26;   # it's the maximal index of height: 20 corresponds to approximately  10.2 km



    charge = 0.5*10**(-6);     
        
   # let's try to determine time and height values properly     

    z_vector = get_height(model_datetime, x_lon)[0:z_index_max]/1000
    time_vector = [event_datetime + datetime.timedelta(minutes=wrf_step_minutes * i) for i in range(number_of_time_points)]    
    
    np.save('/home/kate-svch/Thunder/Aragats_measurements/py-codes/z_and_dens_arrays/z_vector_' + datetime.datetime.strftime(the_time_moment, '%Y-%m-%d_%H:00:00') +'.npy', np.array(z_vector))
    
    
    
   # name_array = ["QCLOUD", "QGRAUP", "QICE",  "QRAIN", "QSNOW","QVAPOR"]
   # name_array = ["QCLOUD", "QGRAUP", "QICE",  "QRAIN", "QSNOW"]
#    name_array = ["QSNOW",  "QRAIN",  "QICE", "QGRAUP", "QCLOUD", "ALT"]
 #   name_array = ["QSNOW",  "QRAIN",  "QICE", "QGRAUP", "QCLOUD"]
    
    name_array = ["QSNOW", "QGRAUP"]
    
    height_for_wind_indexes_array = [0, 4, 5, 6, 7, 8, 10, 12, 13, 14,  15]

    aux_speed_height_number = 10;
    time_of_event_for_wind_array = [the_time_moment]*(aux_speed_height_number + 1);  
    the_second_time_of_event_for_wind_array = [the_second_time_moment]*(aux_speed_height_number + 1);  
    the_third_time_of_event_for_wind_array = [the_third_time_moment]*(aux_speed_height_number + 1);  
    the_fourth_time_of_event_for_wind_array = [the_fourth_time_moment]*(aux_speed_height_number + 1);  
    the_fifth_time_of_event_for_wind_array = [the_fifth_time_moment]*(aux_speed_height_number + 1);  
    

    # the following three lines are the automatical determination of "number_of_time_points"   - the time-length of the data 
#    file = get_wrf_file()
#    temp_n_array = file.variables[name].data[:] / 1
#    number_of_time_points = len(temp_n_array[:, 0, y_lat, x_lon]); 
    
    
# let's determine z-values: for all the times (we hope, it doesn't really change)
# =============================================================================
#     model_height = get_geopotential_height(event_datetime, time_point_of_start  = 1)    
#     event_time = create_time_array_in_hours(start_hour, event_datetime, number_of_time_Interpolation points, step, time_point_of_start);
# =============================================================================


# IT'S WIND CONSIDERATION
# =============================================================================
#     for z_index in height_for_wind_indexes_array:
# 
#     #    z_index = 0;   # 12 leads to 5.9 km, 16 - 8 km, 20 - 10.2 km
#         z_chosen_height = z_vector[z_index]   
#                      /home/kate-svch/Thunder/Aragats_measurements/py-codes
#         ground_height = height[0, y_lat, x_lon]
# 
#         array_from_get_wind = get_wind_certain_level(model_datetime, model_period, model_length, event_datetime, z_index, number_of_time_points)
#         plt.figure(figsize=(18,8))
#         plt.title('Horizontal Wind-speed in time, altitude = ' + str(z_chosen_height) + ' km' + ' (above gr.)'+ ' z_ind = ' + str(z_index), fontsize=22)
#         plt.xlabel('time', fontsize=20, horizontalalignment='right' )
#         plt.ylabel(r'$v, \frac{m}{s}$', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#         plt.plot(time_vector, array_from_get_wind, linewidth=3 )
#         plt.plot(time_of_event_for_wind_array, get_aux_speed_array(array_from_get_wind, aux_speed_height_number), label = str(the_time_moment))
#         plt.plot(the_second_time_of_event_for_wind_array, get_aux_speed_array(array_from_get_wind, aux_speed_height_number), label = str(the_second_time_moment))
#         plt.plot(the_third_time_of_event_for_wind_array, get_aux_speed_array(array_from_get_wind, aux_speed_height_number), label = str(the_third_time_moment))
#         plt.plot(the_fourth_time_of_event_for_wind_array, get_aux_speed_array(array_from_get_wind, aux_speed_height_number), label = str(the_fourth_time_moment))
#         plt.legend(fontsize=20,loc=1)
#         plt.show()   
#          
# 
#         
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
#  #       plt.plot(the_fifth_time_of_event_for_wind_array, get_aux_speed_array(array_from_get_wind, aux_speed_height_number), label = str(the_fifth_time_moment))
#         plt.legend(fontsize=20,loc=1)
#         plt.show()   
# =============================================================================

    ground_height = height[0, y_lat, x_lon]

# =============================================================================         
#         
#         array_from_get_wind =  get_ew_wind_certain_level(model_datetime, model_period, model_length, event_datetime, z_index, number_of_time_points)
#         plt.figure(figsize=(18,8))
#         plt.title('East-West Wind-speed in time, altitude = ' + str(z_chosen_height) +Interpolation  ' km' + ' (above gr.)'+ ' z_ind = ' + str(z_index), fontsize=22)
#         plt.xlabel('time', fontsize=20, horizontalalignment='right' )
#         plt.ylabel(r'$v, \frac{m}{s}$', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#         plt.plot(time_vector, array_from_get_wind, linewidth=3 )
#         plt.plot(time_of_event_for_wind_array, get_aux_speed_array(array_from_get_wind, aux_speed_height_number), label = str(the_time_moment))
#         plt.plot(the_second_time_of_event_for_wind_array, get_aux_speed_array(array_from_get_wind, aux_speed_height_number), label = str(the_second_time_moment))
#         plt.plot(the_third_time_of_event_for_wind_array, get_aux_speed_array(array_from_get_wind, aux_speed_height_number), label = str(the_third_time_moment))
#         plt.plot(the_fourth_time_of_event_for_wind_array, get_aux_speed_array(array_from_get_wind, aux_speed_height_number), label = str(the_fourth_time_moment))
#         plt.legend(fontsize=20,loc=1)
#         plt.show() z_index_max
#         
#         array_from_get_wind = get_ns_wind_certain_level(model_datetime, model_period, model_length, event_datetime, z_index, number_of_time_points)
#         plt.figure(figsize=(18,8))
#         plt.title('North-South Wind-speed in time, altitude = ' + str(z_chosen_height) + ' km' + ' (above gr.)'+ ' z_ind = ' + str(z_index), fontsize=22)
#         plt.xlabel('time', fontsize=20, horizontalalignment='right' )
#         plt.ylabel(r'$v, \frac{m}{s}$', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#         plt.plot(time_vector, array_from_get_wind, linewidth=3 )
#         plt.plot(time_of_event_for_wind_array, get_aux_speed_array(array_from_get_wind, aux_speed_height_number), label = str(the_time_moment))
#         plt.plot(the_second_time_of_event_for_wind_array, get_aux_speed_array(array_from_get_wind, aux_speed_height_number), label = str(the_second_time_moment))
#         plt.plot(the_third_time_of_event_for_wind_array, get_aux_speed_array(array_from_get_wind, aux_speed_height_number), label = str(the_third_time_moment))
#         plt.plot(the_fourth_time_of_event_for_wind_array, get_aux_speed_array(array_from_get_wind, aux_speed_height_number), label = str(the_fourth_time_moment))
#         plt.legend(fontsize=20,loc=1)height_array_for_interp 
#         plt.show()        z_index_max = 26;  
# =============================================================================




# =============================================================================
#     z_index = 8;  
#     z_chosen_height = z_vector[z_index]
#     
#     plt.figure(figsize=(18,8))
#     plt.title('Wind-speed in time, altitude = ' + str(z_chosen_height) + ' km' + ' (above gr.)', fontsize=22)
#     plt.xlabel('time', fontsize=20, horizontalalignment='right' )
#     plt.ylabel(r'$v, \frac{m}{s}$', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#     plt.plot(time_vector, get_wind_certain_level(model_datetime, model_period, model_length, event_datetime, z_index, number_of_time_points))
#     plt.show()  temp_height
# 
# =============================================================================
    
# =============================================================================
#     plt.figure(figsize=(18,8))    
#     plt.title('Temperature in time, ground level' , fontsize=22)
#     plt.xlabel('time', fontsize=20, horizontalalignment='right' )
#     plt.ylabel('T, C', rotation='horizontal', he_fifth_time_momentfontsize=20, horizontalalignment='right', verticalalignment='top')
#     plt.plot(time_vector, get_t2(model_datetime, model_period, model_length, event_datetime, number_of_time_points=number_of_time_points))
#     plt.xlim(event_datetime  , event_datetime + datetime.timedelta(m+ '_' + name + inutes=wrf_step_minutes * (number_of_time_points - 1))  )
#     plt.show()
#       
#     plt.figure(figsize=(18,8))the_time_moment
#     picture_t_getvar = plt.contourf(time_vector, z_vector, np.array(get_t_with_getvar(model_datetime, model_period, model_length, event_datetime, number_of_time_points)).transpose())
#     plt.colorbar(picture_t_getvar) 
#     plt.title('Temperature distribution', fontsize=22)
#     plt.xlabel('time', fontsize=20, horizontalalignment='right' )
#     plt.ylabel('z, km', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
# #    plt.axis('image')
#     plt.axis('normal')      array_loaded 
#     plt.show()    
#     
#     
#         plt.figure(figsize=(18,8))
#     plt.title('Wind-speed in time, ground level' , fontsize=22)
#     plt.xlabel('time', fontsize=20, horizontalalignment='right' )
#     plt.ylabel(r'$v, \frac{m}{s}$', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#     plt.plot(time_vector, get_wind_ground_level(model_datetime, model_period, model_length, event_datetime, number_of_time_points))
#     plt.show()
#     
#     
#     plt.figure(figsize=(18,8))#    plt.ylim(-8, 8 )  
#     plt.title('Pressure in time, ground level' , fontsize=22)
#     plt.xlabel('time', fontsize=20, horizontalalignment='right' )
#     plt.ylabel('kPa', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#     plt.plot(time_vector, get_s_pressure(model_datetime, model_period, model_length, event_datetime, number_of_time_points))
#     plt.show()array_loaded 
# =============================================================================
    
    
  
    plt.figure(figsize=(18,8))
    plt.title('Temperature profile'+ ', '+ str(the_time_moment) , fontsize=22)
    plt.xlabel('z, km', fontsize=20, horizontalalignment='right' )
    plt.ylabel('T, C', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
    plt.plot(z_vector, get_t_profile_in_certain_moment_of_time(z_index_max, model_datetime, model_period, model_length, the_time_moment), linewidth=3, label = str(the_time_moment), color =  (1, 0.4, 0, 1))   
    plt.show()

    
    
    plt.figure(figsize=(18,8))
    plt.title('Temperature profile'+ ', '+ str(the_time_moment) , fontsize=22)
    plt.xlabel('z, km', fontsize=20, horizontalalignment='right' )
    plt.ylabel('T, C', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#    plt.plot(z_vector, get_t_profile_in_certain_moment_of_time(z_index_max, model_datetime, model_period, model_length, the_time_moment), linewidth=3, label = str(the_time_moment), color =  (1, 0.4, 0, 1))
    plt.plot(z_vector, get_t_profile_in_certain_moment_of_time(z_index_max, model_datetime, model_period, model_length, the_second_time_moment), linewidth=3, label = str(the_second_time_moment), color =  (0.9, 0, 0.4, 1))
    plt.plot(z_vector, get_t_profile_in_certain_moment_of_time(z_index_max, model_datetime, model_period, model_length, the_third_time_moment), linewidth=3, label = str(the_third_time_moment), color =  (0.5, 0.9, 0, 1))
    plt.plot(z_vector, get_t_profile_in_certain_moment_of_time(z_index_max, model_datetime, model_period, model_length, the_fourth_time_moment), linewidth=3, label = str(the_fourth_time_moment))    
    plt.legend(fontsize=20,loc=1)
    plt.show()
    
  #  "event_datetime" could have any value from modelled time, or just be equal to "model_datetime"
#    event_datetime = datetime.datetime(2016, 4, 26, 12, 00)     
    event_datetime = model_datetime
    
    
 # here we have an automatical "numnber_of_time_points"-initialization      
    number_of_time_points  = int ((event_finish_datetime - event_datetime)/datetime.timedelta(0, 0, 0, 0, wrf_step_minutes))  + 1
   
    file = get_wrf_file(model_datetime)
    variable = file.variables['T2'].data[:]
    model_length = len(variable[:, y_lat, x_lon])  
    
#    number_of_time_points = 25; 

    charge = 0.5*10**(-6);     
    
# =============================================================================
#     z_array = np.zeros([90,z_index_max])  
#     x_array = np.zeros([90,z_index_max])
#     for j_x in range(0, 90):
#         print (j_x)    x_array[j_x - x_min,:] = np.ones([z_index_max]) * j_x - 45
#         z_array[j_x,:] = get_height(model_datetime, j_x)[:z_index_max]/1000.
#         x_array[j_x,:] = np.ones([z_index_max]) * j_x - 45
# =============================================================================
    
    
    z_array = np.zeros([x_max - x_min, z_index_max])   # it's for x-dependencies, for fixed y-value!
    x_array = np.zeros([x_max - x_min, z_index_max])
    y_array = np.zeros([x_max - x_min, z_index_max])
    z_for_y_array = np.zeros([x_max - x_min, z_index_max]) 
    
    for j_x in range(x_min, x_max):
#        print (j_x)    
        x_array[j_x - x_min,:] = np.ones([z_index_max]) * j_x - 45
        z_array[j_x - x_min,:] = get_height(model_datetime, j_x)[:z_index_max]/1000.
        y_array[j_x - x_max,:] = np.ones([z_index_max]) * j_x - 45
        z_for_y_array[j_x - x_min,:] = get_height_for_y(model_datetime, j_x)[:z_index_max]/1000.
# =============================================================================
#     plt.figure(figsize=(18,8))
#     plt.title('Value opposite to the dry air density, ground level' , fontsize=22)
#     plt.xlabel('time', fontsize=20, horizontalalignment='right' )
#     plt.ylabel(r'$\frac{m^3}{kg}$', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#     plt.plot(get_alt(event_datetime,time_point_of_start, number_of_time_points))
#     plt.show()
# =============================================================================
    
    
    time_number_start = number_of_time_points* 3//8
    time_number_finish = number_of_time_points* 5//8
    
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
        picture_mass = plt.contourf(time_vector[time_number_start:time_number_finish], z_vector, np.array(get_mass_density(z_index_max, model_datetime, model_period, model_length, event_datetime, name, number_of_time_points)).transpose()[:, time_number_start:time_number_finish])
        plt.colorbar(picture_mass, format =  "%0.6f" )
        plt.title('Density: '+ name, fontsize=22)
        plt.xlabel('time', fontsize=20, horizontalalignment='right' )
        plt.ylabel('z, km', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
    #    plt.axis('image')
        plt.axis('normal')       
        plt.show()
        
                     
        
    # Let's look on the upper picture - t-z particles distribution, 
    # and choose the time-point under interest (one of the values on the time-axis)
    # then just use "number_of_the_time_point = that_chosen_value",z_index_max
    # and we'll get x-z particles distribuation - on the lower picture    
        
  #      picture2 =  plt.contourf(x_values, z_vector, np.array(   get_q_xz(z_index_max, model_datetime, model_period, model_length, the_time_moment, name )).transpose())    
   

   #  print (z_array)  
     
     
        plt.figure(figsize=(18,8))        
        picture2 =  plt.contourf(x_array, z_array, np.array(   get_mass_density_xz(z_index_max, model_datetime, model_period, model_length, the_time_moment, name )))
        plt.colorbar(picture2, format =  "%0.6f") 
        plt.title('Density: '+ name + '  '+ str(the_time_moment), fontsize=22)
        plt.xlabel('x, km', fontsize=20, horizontalalignment='right' )
        plt.ylabel('z, km', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
        plt.axis('normal')    
        plt.show()
        
        print('Integral quantity of ', name, ' is: ',  get_mass_density_integral(z_index_max, model_datetime, model_period, model_length, the_time_moment, name ))
   
       
        m_density_array = getvar(ncfile, name, timeidx = get_index(model_datetime, model_period, model_length, the_time_moment, 1 ) ,  meta=False)
        interpolated_m_dens = vinterp(ncfile, m_density_array, start_level, height_array_for_interp)
    
        plt.figure(figsize=(18,8))        
 #       picture2 =  plt.contourf(height_array_for_interp, x_array, interpolated_m_dens[:,  y_lat, x_min:x_max])
        picture2 =  plt.contourf( interpolated_m_dens[:,  y_lat, x_min:x_max])
        plt.colorbar(picture2, format =  "%0.6f") 
        plt.title('INTERPOLATED density: '+ name + '  '+ str(the_time_moment), fontsize=22)
        plt.xlabel('x, ind', fontsize=20, horizontalalignment='right' )
        plt.ylabel('z, ind', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
        plt.axis('normal')    
        plt.show()
        
        
        plt.figure(figsize=(18,8))        
        picture2 =  plt.contourf(y_array, z_for_y_array, np.array(   get_mass_density_yz(z_index_max, model_datetime, model_period, model_length, the_time_moment, name )))
        plt.colorbar(picture2, format =  "%0.6f") 
        plt.title('YZ_Density: '+ name + '  '+ str(the_time_moment), fontsize=22)
        plt.xlabel('y, km', fontsize=20, horizontalalignment='right' )
        plt.ylabel('z, km', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
        plt.axis('normal')    
        plt.show()    
               
        
        plt.figure(figsize=(18,8))        
 #       picture2 =  plt.contourf(height_array_for_interp, x_array, interpolated_m_dens[:,  y_lat, x_min:x_max])
        picture2 =  plt.contourf( interpolated_m_dens[:,  x_min:x_max, x_lon])
        plt.colorbar(picture2, format =  "%0.6f") 
        plt.title('YZ_INTERPOLATED density: '+ name + '  '+ str(the_time_moment), fontsize=22)
        plt.xlabel('y, ind', fontsize=20, horizontalalignment='right' )
        plt.ylabel('z, ind', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
        plt.axis('normal')    
        plt.show()
        
                  
        density_3D_array =   interpolated_m_dens[:,  x_min:x_max, x_min:x_max]
  
 #       print(density_3D_array[:, -1, 1])
        
#        print(density_3D_array)
 
        np.save('/home/kate-svch/Thunder/Aragats_measurements/py-codes/z_and_dens_arrays/dens_array_' + name + '_'+ datetime.datetime.strftime(the_time_moment, '%Y-%m-%d_%H:00:00') +'.npy', np.array(m_density_array[0:z_index_max+1, x_lon-x_min, y_lat-x_min]))
 
        
        np.save('/home/kate-svch/Thunder/Aragats_measurements/py-codes/interpolated_densities/int_dens_' + datetime.datetime.strftime(the_time_moment, '%Y-%m-%d_%H:00:00') + '_' + name + '.npy', np.array(density_3D_array ))
 #       np.save('filename.npy', np.array(density_3D_array))

    
        np.save('/home/kate-svch/Thunder/Aragats_measurements/py-codes/z_and_dens_arrays/dens_array_interpolated_' + name + '_'+ datetime.datetime.strftime(the_time_moment, '%Y-%m-%d_%H:00:00') +'.npy', np.array(density_3D_array[:, x_lon-x_min, y_lat-x_min]))
        
    
    
    
# =============================================================================
#         plt.figure(figsize=(14,8))
#         plt.plot(time_vector, np.array(    get_q_ground(model_datetime, model_period, model_length, event_datetime, name, number_of_time_points)))
#         plt.title(name + ' concentration at the ground level', fontsize=22)
#         plt.xlabel('time', fontsize=20, horizontalalignment='right' )
# #        plt.ylabel('??', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')          
#         plt.xlim(time_vector[0], time_vector[-1] )
# =============================================================================
    
    
        time_length = len(time_vector)
        time_start_index =  time_length*11//36;
        time_finish_index =  time_length*25//36;
    
    
    
        plt.figure(figsize=(14,8))
        plt.plot(time_vector, np.array(el_field_q_int_z_t(z_index_max, model_datetime, model_period, model_length, event_datetime, name, charge, number_of_time_points)))
        plt.title('Electric field created by '+ name, fontsize=22)
        plt.xlabel('time', fontsize=20, horizontalalignment='right' )
        plt.ylabel('El_field, some_unit', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')          
        plt.xlim(time_vector[0], time_vector[-1] )
   #     plt.xlim(time_vector[time_start_index]  , time_vector[time_finish_index] )
        plt.show()
   

    
#    the_time_moment = the_second_time_moment;
    
    plt.figure(figsize=(18,8))
    picture_ns_wind_xz =  plt.contourf(x_array, z_array, np.array(get_ns_wind_xz(model_datetime, model_period, model_length, the_time_moment, z_index_max)))
    plt.colorbar(picture_ns_wind_xz, format =  "%1.0f") 
    plt.title('South-North wind, ' + '  '+ str(the_time_moment), fontsize=22)
    plt.xlabel('x, km', fontsize=20, horizontalalignment='right' )
    plt.ylabel('z, km', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
    plt.axis('normal')    
    plt.show()
    
    plt.figure(figsize=(18,8))
    picture_ew_wind_xz =  plt.contourf(x_array, z_array, np.array(get_ew_wind_xz(model_datetime, model_period, model_length, the_time_moment, z_index_max)))
    plt.colorbar(picture_ew_wind_xz, format =  "%1.0f") 
    plt.title('West-East wind, ' + '  '+ str(the_time_moment), fontsize=22)
    plt.xlabel('x, km', fontsize=20, horizontalalignment='right' )
    plt.ylabel('z, km', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
    plt.axis('normal')    
    plt.show()
    
    plt.figure(figsize=(18,8))
    picture_vertical_wind_xz =  plt.contourf(x_array, z_array, np.array(get_vertical_wind_xz(model_datetime, model_period, model_length, the_time_moment, z_index_max)))
    plt.colorbar(picture_vertical_wind_xz, format =  "%1.0f") 
    plt.title('Vertical wind, ' + '  '+ str(the_time_moment), fontsize=22)
    plt.xlabel('x, km', fontsize=20, horizontalalignment='right' )
    plt.ylabel('z, km', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
    plt.axis('normal')    
    plt.show()
    
  
    
    
 # let's draw the sum of fields, created by two kinds of cloud-particles
    name1 = "QSNOW"
    name2 = "QGRAUP"
    charge1 = -8*10**(0);
    charge2 = 10*10**(0);
    plt.figure(figsize=(8,12))
    sum_of_fields = 10**(-3)*(np.array(el_field_q_int_z_t(z_index_max, model_datetime, model_period, model_length, event_datetime, name1, charge1, number_of_time_points)) + np.array(el_field_q_int_z_t(z_index_max, model_datetime, model_period, model_length, event_datetime, name2, charge2, number_of_time_points)))
    plt.plot(time_vector, sum_of_fields)
    plt.title('Electric field created by '+ name1 + ' and ' + name2, fontsize=22)
    plt.xlabel('time', fontsize=20, horizontalalignment='right' )
    plt.ylabel(r'$\frac{kV}{m}$', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#    plt.xlim(time_vector[0], time_vector[-1] )    
    plt.xlim(time_vector[time_start_index], time_vector[time_finish_index] )   
    plt.ylim(-8, 8 )     
    plt.show()
    
    the_time_moment_index = get_index(model_datetime, model_period, model_length, the_time_moment, 1 )
    print('the_time_moment_index = '+str(the_time_moment_index))
  
    print('Ground-level el.field at '+ str(the_time_moment)+' = '+str(sum_of_fields[the_time_moment_index]))
    
    
    name1 = "QSNOW"
    name2 = "QGRAUP"
    plt.figure(figsize=(14,8)) 
    plt.plot(time_vector, 10**(-3)*(np.array(el_field_q_int_z_t(z_index_max, model_datetime, model_period, model_length, event_datetime, name1, charge1, number_of_time_points))), label = name1)
    plt.plot(time_vector, 10**(-3)*( np.array(el_field_q_int_z_t(z_index_max, model_datetime, model_period, model_length, event_datetime, name2, charge2, number_of_time_points))), label = name2)
    plt.title('Electric fields created by '+ name1 + ' and ' + name2, fontsize=22)
    plt.xlabel('time', fontsize=20, horizontalalignment='right' )
    plt.ylabel(r'$\frac{kV}{m}$', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#    plt.xlim(time_vector[0], time_vector[-1] )    
    plt.xlim(time_vector[time_start_index], time_vector[time_finish_index] )   
#    plt.ylim(-40, 40 )   
    plt.legend(fontsize=20,loc=1)
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
