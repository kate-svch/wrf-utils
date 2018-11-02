#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 12:23:46 2018

@author: kate-svch
"""
from math import*
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
import time
import datetime

import matplotlib as mpl

# noninterpolated: z_vector, dens_array
# interpolated: z_array, dens_array_interpolated

  # инициализация констант
coef_k = 9*10**(9)    
MountainHeight=3.2;    # needed for critical_field calculation: height of the ground surface asl, in km
first_considered_index = 0;

dx = 1;  #латеральный размер ячейки, он же - эффективный радиус заряженных слоёв, в км
R = dx
# fraction_number = 0, 1 - correcponds to GRAUP and SNOW - correspondingly


the_time_moment = datetime.datetime(2016, 6, 11, 11, 10) 
# LET'S LOAD ALL THE ARRAYS - from files made by "model2.py"
z_vector = np.load('/home/kate-svch/Thunder/Aragats_measurements/py-codes/z_and_dens_arrays/z_vector_' + datetime.datetime.strftime(the_time_moment, '%Y-%m-%d_%H:00:00') +'.npy')
z_array = np.load('/home/kate-svch/Thunder/Aragats_measurements/py-codes/z_and_dens_arrays/z_array_' + datetime.datetime.strftime(the_time_moment, '%Y-%m-%d_%H:00:00') +'.npy')
dz = (z_array[1] - z_array[0])  #  km


name_array = ['QGRAUP', 'QSNOW']
hydrometeors_type_quantity = len(name_array)
charge_coef_array = [(10)*10**(0),(-8)*10**(0)]

density_array_interpolated = [0,0]
density_array_noninterp = [0,0]
for jjj in range(0, len(name_array)):
    name = name_array[jjj]
    density_array_interpolated[jjj] = np.load('/home/kate-svch/Thunder/Aragats_measurements/py-codes/z_and_dens_arrays/dens_array_interpolated_' + name + '_'+ datetime.datetime.strftime(the_time_moment, '%Y-%m-%d_%H:00:00') +'.npy')    
    density_array_interpolated[jjj] = density_array_interpolated[jjj][first_considered_index : -1]
    density_array_noninterp[jjj] = np.load('/home/kate-svch/Thunder/Aragats_measurements/py-codes/z_and_dens_arrays/dens_array_' + name + '_'+ datetime.datetime.strftime(the_time_moment, '%Y-%m-%d_%H:00:00') +'.npy')    
    density_array_noninterp[jjj] = density_array_noninterp[jjj][first_considered_index : -1]

print('len(z_vector) = ' + str(len(z_vector)))
print('len(density_array_noninterp[0]) = ' + str(len(density_array_noninterp[0])))

#density_array = density_array_interpolated
density_array = density_array_noninterp;        z_array = z_vector;

z_array = z_array[first_considered_index:]

print('len(z_array) = ' + str(len(z_array)))

def zsignum(z, zInside):
    return 2*((-z+zInside)>0)-1;

# расстояние подставляется в километрах
# результата получается в kV//m (отсюда множитель 10**(-3))
# деление на площадь ячейки- чобы из заряда, измеряемого в C (из model2.py - плотность с коэффициентом - и есть заряд!) - получить пов.плотность заряда диска   
def Elementary_field_function_POINT_z(fraction_number, z_index, z_Inside_index, density_array):
    return 10**(-9)*coef_k*charge_coef_array[fraction_number]*density_array[fraction_number][z_Inside_index]*zsignum(z_array[z_index],z_array[z_Inside_index]) / ((z_array[z_index]-z_array[z_Inside_index])**2 )


def Elementary_field_function_POINT_z_Mirror(fraction_number, z_index, z_Inside_index, density_array):
    return 10**(-9)*coef_k*charge_coef_array[fraction_number]*density_array[fraction_number][z_Inside_index] / ((z_array[z_index]+z_array[z_Inside_index])**2 )
    


def Elementary_field_function_DISK_z(fraction_number, z_index, z_Inside_index, density_array):
    return 10**(-9)*2*coef_k*charge_coef_array[fraction_number]*density_array[fraction_number][z_Inside_index]/dx/dx *(zsignum(z_array[z_index],z_array[z_Inside_index]) + (z_array[z_index]-z_array[z_Inside_index])/sqrt( R**2 + (z_array[z_index]-z_array[z_Inside_index])**2 ) )


def Elementary_field_function_DISK_z_Mirror(fraction_number, z_index, z_Inside_index, density_array):
    return -10**(-9)*2*coef_k*charge_coef_array[fraction_number]*density_array[fraction_number][z_Inside_index]/dx/dx *(-1 + (z_array[z_index]+z_array[z_Inside_index])/sqrt( R**2 + (z_array[z_index]+z_array[z_Inside_index])**2 ) )


 # определим функцию, возвращающую поле по данным на данной высоте (заданной индексом) - от всех типов гидрометеоров, с учётом отражения
     # с использованием вышезаданной плотности заряда
#      electric field sstrength in kV/m
def Field_in_z_DISK_function(z_index, density_array):
    field_z=0;    
    for bbb in range (0, hydrometeors_type_quantity ):
        for z_Inside_index in range (0, len(z_array)): 
            if (z_index != z_Inside_index):
                field_z +=  Elementary_field_function_DISK_z(bbb, z_index, z_Inside_index, density_array)
                field_z +=  Elementary_field_function_DISK_z_Mirror(bbb,  z_index, z_Inside_index, density_array)
    return field_z;    


def Field_in_z_POINT_function(z_index, density_array):
    field_z=0;    
    for bbb in range (0, hydrometeors_type_quantity ):
        for z_Inside_index in range (0, len(z_array)): 
            if (z_index != z_Inside_index):
                field_z +=  Elementary_field_function_POINT_z(bbb, z_index, z_Inside_index, density_array)
                field_z +=  Elementary_field_function_POINT_z_Mirror(bbb,  z_index, z_Inside_index, density_array)
    return field_z;   


# строим график плотности заряда
# =============================POINT================================================
# for hydrometeor_type_ind in range (0, hydrometeors_type_quantity): 
#     plt.figure(figsize=(12,4))
#     plt.plot( density_array[hydrometeor_type_ind], z_array, linewidth = 3)
#     plt.title('Density profile of ' + name_array[hydrometeor_type_ind] + ''+ str(the_time_moment), fontsize=22)
#     plt.xlabel('density, some units', fontsize=20, horizontalalignment='right' )
#     plt.ylabel('z, km', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#     plt.axis('normal')    
#     plt.show()    
# =============================================================================
    
# specific charges of all the fractions - in the same axes    
plt.figure(figsize=(12,4))
plt.title('Charge-density profile ' + str(the_time_moment), fontsize=22)
for hydrometeor_type_ind in range (0, hydrometeors_type_quantity): 
    plt.plot( charge_coef_array[hydrometeor_type_ind]*density_array[hydrometeor_type_ind], z_array, linewidth = 3, label = name_array[hydrometeor_type_ind])   
plt.xlabel('charge-density, '+ r'$\frac{c}{m^3}$', fontsize=20, horizontalalignment='right' )
plt.ylabel('z, km', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
plt.axis('normal')
plt.legend(fontsize=20,loc=1)    
plt.show()      

print('len(z_vector) = ' + str(len(z_vector)))
# let's look at the "elementary_field_function"'s work:
z_Inside_index = 10;  

for fraction_number in range(0, hydrometeors_type_quantity):
    
    elem_field_func_DISK_z_result = [];    # ЭТО ПОЛЕ ОТ ОДНОЙ ЯЧЕЙКИ ЗАРЯДА - с фиксированным z_Inside_index
    elem_field_func_DISK_z_Mirror_result = [];
    elem_field_func_POINT_z_result = [];   
    elem_field_func_POINT_z_Mirror_result = [];
    
    for z_index in range(0, len(z_array)):
    #for z_index in range(0, z_Inside_index):
    #    z_array_one_part.append(z_array[z_index])
        elem_field_func_DISK_z_Mirror_result.append(Elementary_field_function_DISK_z_Mirror(fraction_number, z_index, z_Inside_index, density_array))
        elem_field_func_POINT_z_Mirror_result.append(Elementary_field_function_POINT_z_Mirror(fraction_number, z_index, z_Inside_index, density_array))
        if (z_Inside_index != z_index):
            elem_field_func_DISK_z_result.append(Elementary_field_function_DISK_z(fraction_number, z_index, z_Inside_index, density_array))        
            elem_field_func_POINT_z_result.append(Elementary_field_function_POINT_z(fraction_number, z_index, z_Inside_index, density_array))    
        else:    
            elem_field_func_DISK_z_result.append(0)
            elem_field_func_POINT_z_result.append(0)
    
    
# =============================================================================
#     plt.figure(figsize=(12,4))
#     plt.title('POINT: Elementary_field_function_z(' + str(name_array[fraction_number]) + ', z_index, ' + str(z_Inside_index) + ', ' + str(the_time_moment), fontsize=22)
# #    plt.plot(elem_field_func_DISK_z_result,  z_array, linewidth = 3, label = 'DISK '+name_array[fraction_number])   
#     plt.plot(elem_field_func_POINT_z_result,  z_array, linewidth = 3, label = 'POINT '+name_array[fraction_number])   
#     plt.xlabel('electric_field, '+ r'$\frac{kV}{m}$', fontsize=20, horizontalalignment='right' )
#     plt.ylabel('z, km', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#     plt.axis('normal')
#     plt.legend(fontsize=20,loc=1)    
#     plt.show()  
# =============================================================================
    
    plt.figure(figsize=(12,4))
    plt.title('DISK: Elementary_field_function_z(' + str(name_array[fraction_number]) + ', z_index, ' + str(z_Inside_index) + ', ' + str(the_time_moment), fontsize=22)
    plt.plot(elem_field_func_DISK_z_result,  z_array, linewidth = 3, label = 'DISK '+name_array[fraction_number])   
#    plt.plot(elem_field_func_POINT_z_result,  z_array, linewidth = 3, label = 'POINT '+name_array[fraction_number])   
    plt.xlabel('electric_field, '+ r'$\frac{kV}{m}$', fontsize=20, horizontalalignment='right' )
    plt.ylabel('z, km', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
    plt.axis('normal')
    plt.legend(fontsize=20,loc=1)    
    plt.show()  
    
# =============================================================================
#     plt.figure(figsize=(12,4))
#     plt.title('POINT and DISK: Elementary_field_function_z(' + str(name_array[fraction_number]) + ', z_index, ' + str(z_Inside_index) + ', ' + str(the_time_moment), fontsize=22)
#     plt.plot(elem_field_func_DISK_z_result,  z_array, linewidth = 3, label = 'DISK '+name_array[fraction_number])   
#     plt.plot(elem_field_func_POINT_z_result,  z_array, linewidth = 3, label = 'POINT '+name_array[fraction_number])   
#     plt.xlabel('electric_field, '+ r'$\frac{kV}{m}$', fontsize=20, horizontalalignment='right' )
#     plt.ylabel('z, km', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#     plt.axis('normal')
#     plt.legend(fontsize=20,loc=1)    
#     plt.show()  
#         
#     plt.figure(figsize=(12,4))
#     plt.title('POINT: Elementary_field_function_DISK_z_Mirror(' + str(name_array[fraction_number]) + ', z_index, ' + str(z_Inside_index) + ', ' + str(the_time_moment), fontsize=22)
# #    plt.plot(elem_field_func_DISK_z_Mirror_result,  z_array
#     plt.plot(elem_field_func_POINT_z_Mirror_result,  z_array, linewidth = 3, label = 'POINT '+name_array[fraction_number])   
#     plt.xlabel('electric_field, '+ r'$\frac{kV}{m}$', fontsize=20, horizontalalignment='right' )
#     plt.ylabel('z, km', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#     plt.axis('normal')
#     plt.legend(fontsize=20,loc=1)    
#     plt.show()  
# =============================================================================
    
    plt.figure(figsize=(12,4))
    plt.title('DISK: Elementary_field_function_DISK_z_Mirror(' + str(name_array[fraction_number]) + ', z_index, ' + str(z_Inside_index) + ', ' + str(the_time_moment), fontsize=22)
    plt.plot(elem_field_func_DISK_z_Mirror_result,  z_array, linewidth = 3,label = 'DISK '+name_array[fraction_number])   
#    plt.plot(elem_field_func_POINT_z_Mirror_result,  z_array, linewidth = 3, label = 'POINT '+name_array[fraction_number])   
    plt.xlabel('electric_field, '+ r'$\frac{kV}{m}$', fontsize=20, horizontalalignment='right' )
    plt.ylabel('z, km', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
    plt.axis('normal')
    plt.legend(fontsize=20,loc=1)    
    plt.show()     
    
# =============================================================================
#     plt.figure(figsize=(12,4))
#     plt.title('POINT and DISK: Elementary_fR = 0.1 ;  # эффективный радиус заряженных слоёв в кмield_function_DISK_z_Mirror(' + str(name_array[fraction_number]) + ', z_index, ' + str(z_Inside_index) + ', ' + str(the_time_moment), fontsize=22)
#     plt.plot(elem_field_func_DISK_z_Mirror_result,  z_array, linewidth = 3,label = 'DISK '+name_array[fraction_number])   
#     plt.plot(elem_field_func_POINT_z_Mirror_result,  z_array, linewidth = 3, label = 'POINT '+name_array[fraction_number])   
#     plt.xlabel('electric_field, '+ r'$\frac{kV}{m}$', fontsize=20, horizontalalignment='right' )density_array[jjj]
#     plt.ylabel('z, km', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
#     plt.axis('normal')
#     plt.legend(fontsize=20,loc=1)    
#     plt.show()  
# =============================================================================
  

             


field_critical_negative=[];
field_profile_DISK = [];
field_profile_POINT = [];
for z_ind in range(0, len(z_array)):
    current_z = z_array[z_ind]
    field_critical_negative.append(10**(-3)*(-2.76e5)*0.87**((current_z + MountainHeight)))
    field_profile_DISK.append(Field_in_z_DISK_function(z_ind, density_array))
    field_profile_POINT.append(Field_in_z_POINT_function(z_ind, density_array))    
    
print('z_array size = ' + str(len(z_array)))   
print('field_profile size = ' + str(len(z_array)))   

print('z_array[0] = ' + str(z_array[0]))

fig = plt.figure(figsize=(18,10))    
plt.title('field_profile_DISK, ' + str(the_time_moment), fontsize=22)
plt.plot(field_profile_DISK, z_array, linewidth=3, label='field_profile DISK')
#plt.plot(field_profile_POINT, z_array, linewidth=3, label='field_profile POINT')
#plt.plot(field_critical_negative, z_array, linewidth=3, label='-critical')
#plt.plot(z_range, field_critical_positive, linewidth=3, label='+critical')
plt.xlabel(r'$\frac{kV}{m}$', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
plt.ylabel('z, km', rotation='horizontal', fontsize=20, horizontalalignment='right', verticalalignment='top')
plt.legend(fontsize=20,loc=1)
plt.show()    
    