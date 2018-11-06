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
#x_min = 44; x_max = 47; 
x_min = 39; x_max = 52;  # it's borders of the drawn area for xz-diagrams
#z_index_max = 20;   # it's the maximal index of height: 20 corresponds to approximately  10.2 km

           
#model_datetime = datetime.datetime(2018, 3, 4, 18, 0)            # Starting time for WRF modeling (hour, minute)

#model_datetime = None #datetime.datetime(2016, 5, 4, 0, 0)  # Starting time for WRF modeling
#model_period = None #datetime.timedelta(minutes=5)
#model_length = None

#current_folder = '/mnt/data-internal/reanalysis'    # this is the folder for the 2018-03-05 event

current_folder = '/mnt/data-internal/newversion'
#current_folder = '/mnt/data-internal/Mansell'

#current_folder = '/mnt/data-internal/RDA_DS083.3'

   
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
    
  #  "event_datetime" could have any value from modelled time, or just be equal to "model_datetime"
#    event_datetime = datetime.datetime(2016, 4, 26, 12, 00)     



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
    
  #  "event_datetime" could have any value from modelled time, or just be equal to "model_datetime"
#    event_datetime = datetime.datetime(2016, 4, 26, 12, 00)     
    
  #  "event_datetime" could have any value from modelled time, or just be equal to "model_datetime"
#    event_datetime = datetime.datetime(2016, 4, 26, 12, 00)     
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


   
# the value is opposite to the dry air mass density
def get_alt(model_datetime, model_period, model_length, event_datetime, number_of_time_points = 1):
    time_index = get_index(model_datetime, model_period, model_length, event_datetime, number_of_time_points)
    file = get_wrf_file(model_datetime)
    temp_alt = file.variables['ALT'].data[:]
    return temp_alt[time_index : time_index + number_of_time_points, 0, y_lat, x_lon]


    


# this auxiliary function returns the dynamics of certain fraction concentration on the ground level:    
def get_q_ground(model_datetime, model_period, model_length, event_datetime, name, number_of_time_points=1):
   # get quantity of "name" microphysical fracture from 2m to 20 kilometers height : DIFFERENT HEIGHT AND TIME
   
    time_index = get_index(model_datetime, model_period, model_length, event_datetime,  number_of_time_points )
    file = get_wrf_file(model_datetime)
    vapor = file.variables[name].data[:]
    return vapor[time_index : time_index  + number_of_time_points, 0, y_lat, x_lon]    

    

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

    the_start_of_consideration = datetime.datetime(2016, 6, 11, 10, 0) 
    the_end_of_consideration = datetime.datetime(2016, 6, 11, 16, 0) 
    
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
    number_of_time_points  = int ((the_end_of_consideration - the_start_of_consideration)/datetime.timedelta(0, 0, 0, 0, wrf_step_minutes))  + 1
    
   
   
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
    
    
    height_array_zero_on_the_ground = np.arange(height_min , height_max,  0.02) # in kmdatetime.timedelta(0, 0, 0, 0, wrf_step_minutes))
      # we write "z_array" in file just once - in assumption, that it is  one and the same array for each "name" (type of hydrometeors)
#    np.save('/home/kate-svch/Thunder/Aragats_measurements/py-codes/z_and_dens_arrays/z_array_' + datetime.datetime.strftime(the_time_moment, '%Y-%m-%d_%H:00:00') +'.npy', np.array(height_array_zero_on_the_ground))
    
 
    z_index_max = 20;   # it's the maximal index of height: 20 corresponds to approximately  10.2 km

    z_vector = get_height(model_datetime, x_lon)[0:z_index_max]/1000
    time_vector = [event_datetime + datetime.timedelta(minutes=wrf_step_minutes * i) for i in range(number_of_time_points)]    
    ground_height = height[0, y_lat, x_lon]
    
#    np.save('/home/kate-svch/Thunder/Aragats_measurements/py-codes/z_and_dens_arrays/z_vector_' + datetime.datetime.strftime(the_time_moment, '%Y-%m-%d_%H:00:00') +'.npy', np.array(z_vector))
    
    name_array = ["QSNOW", "QGRAUP"]
    event_datetime = model_datetime
    

   
    file = get_wrf_file(model_datetime)
    variable = file.variables['T2'].data[:]
    model_length = len(variable[:, y_lat, x_lon])  


    
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


    for j_time in range(0, number_of_time_points):
        the_time_moment = the_start_of_consideration + j_time*(datetime.timedelta(0, 0, 0, 0, wrf_step_minutes))
        
        for name in name_array:
    
            
    # =============================================================================
    #         plt.figure(figsize=(18,8))
    #         picture_mass = plt.contourf(time_vector, z_vector, np.array(get_mass_density(z_index_max, model_datetime, model_period, model_length, event_datetime, name, number_of_time_points)).transpose())   
    #         plt.colorbar(picture_mass, format =  "%0.6f" )
    #         plt.title('Density: '+ name, fontsize=22)
    #         plt.xlabel('time', fontsize=20, horizontalalignment='right' )
    #         plt.ylabel('z, km', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
    #     #    plt.axis('image')
    #         plt.axis('normal')       
    #         plt.show()
    # =============================================================================
         
            figure_xz_raw = plt.figure(figsize=(18,8))        
            picture2 =  plt.contourf(x_array, z_array, np.array(   get_mass_density_xz(z_index_max, model_datetime, model_period, model_length, the_time_moment, name )))
            plt.colorbar(picture2, format =  "%0.6f") 
            plt.title('Density: '+ name + '  '+ str(the_time_moment), fontsize=22)
            plt.xlabel('x, km', fontsize=20, horizontalalignment='right' )
            plt.ylabel('z, km', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
            plt.axis('normal')    
            plt.show()
            
            print('Integral quantity of ', name, ' is: ',  get_mass_density_integral(z_index_max, model_datetime, model_period, model_length, the_time_moment, name ))
            aux_year = event_datetime.year
            aux_folder_for_fig = datetime.datetime.strftime(the_time_moment, '%Y-%m-%d')
            figure_xz_raw.savefig('/home/kate-svch/Thunder/Aragats_measurements/'+str(aux_year)+'/'+aux_folder_for_fig+'/dens_in_space_raw_'+name+'/raw_xz_'+name+'_'+datetime.datetime.strftime(the_time_moment, '%Y-%m-%d_%H-%M')+'.png')
           
            m_density_array = getvar(ncfile, name, timeidx = get_index(model_datetime, model_period, model_length, the_time_moment, 1 ) ,  meta=False)
            interpolated_m_dens = vinterp(ncfile, m_density_array, start_level, height_array_for_interp)
        
            figure_xz_interp = plt.figure(figsize=(18,8))        
     #       picture2 =  plt.contourf(height_array_for_interp, x_array, interpolated_m_dens[:,  y_lat, x_min:x_max])
            picture2 =  plt.contourf( interpolated_m_dens[:,  y_lat, x_min:x_max])
            plt.colorbar(picture2, format =  "%0.6f") 
            plt.title('INTERPOLATED density: '+ name + '  '+ str(the_time_moment), fontsize=22)
            plt.xlabel('x, ind', fontsize=20, horizontalalignment='right' )
            plt.ylabel('z, ind', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
            plt.axis('normal')    
            plt.show()
            figure_xz_interp.savefig('/home/kate-svch/Thunder/Aragats_measurements/'+str(aux_year)+'/'+aux_folder_for_fig+'/dens_in_space_interp_'+name+'/xz_interp'+name+'_'+datetime.datetime.strftime(the_time_moment, '%Y-%m-%d_%H-%M')+'.png')

            
    # =============================================================================
    #         plt.figure(figsize=(18,8))        
    #         picture2 =  plt.contourf(y_array, z_for_y_array, np.array(   get_mass_density_yz(z_index_max, model_datetime, model_period, model_length, the_time_moment, name )))
    #         plt.colorbar(picture2, format =  "%0.6f") 
    #         plt.title('YZ_Density: '+ name + '  '+ str(the_time_moment), fontsize=22)
    #         plt.xlabel('y, km', fontsize=20, horizontalalignment='right' )
    #         plt.ylabel('z, km', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
    #         plt.axis('normal')    
    #         plt.show()    
    #                
    #         
    #         plt.figure(figsize=(18,8))        
    #  #       picture2 =  plt.contourf(height_array_for_interp, x_array, interpolated_m_dens[:,  y_lat, x_min:x_max])
    #         picture2 =  plt.contourf( interpolated_m_dens[:,  x_min:x_max, x_lon])
    #         plt.colorbar(picture2, format =  "%0.6f") 
    #         plt.title('YZ_INTERPOLATED density: '+ name + '  '+ str(the_time_moment), fontsize=22)
    #         plt.xlabel('y, ind', fontsize=20, horizontalalignment='right' )
    #         plt.ylabel('z, ind', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
    #         plt.axis('normal')    
    #         plt.show()
    # =============================================================================
            
                      
    # =============================================================================
    #         density_3D_array =   interpolated_m_dens[:,  x_min:x_max, x_min:x_max]
    #         np.save('/home/kate-svch/Thunder/Aragats_measurements/py-codes/z_and_dens_arrays/dens_array_' + name + '_'+ datetime.datetime.strftime(the_time_moment, '%Y-%m-%d_%H:00:00') +'.npy', np.array(m_density_array[0:z_index_max+1, x_lon-x_min, y_lat-x_min])) 
    #         np.save('/home/kate-svch/Thunder/Aragats_measurements/py-codes/interpolated_densities/int_dens_' + datetime.datetime.strftime(the_time_moment, '%Y-%m-%d_%H:00:00') + '_' + name + '.npy', np.array(density_3D_array ))
    #         np.save('/home/kate-svch/Thunder/Aragats_measurements/py-codes/z_and_dens_arrays/dens_array_interpolated_' + name + '_'+ datetime.datetime.strftime(the_time_moment, '%Y-%m-%d_%H:00:00') +'.npy', np.array(density_3D_array[:, x_lon-x_min, y_lat-x_min]))         
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
