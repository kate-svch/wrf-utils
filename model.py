#!/usr/bin/env python3
import os
import numpy as np
import matplotlib.pyplot as plt
import datetime
from scipy.io import netcdf

x_lon = 46  # Index to d02 Aragats point
y_lat = 46  # Index to d02 Aragats point

model_datetime = None #datetime.datetime(2016, 5, 4, 0, 0)  # Starting time for WRF modeling
model_period = None #datetime.timedelta(minutes=5)
model_length = None

def set_model_datetime(new_model_datetime, new_model_period):
    global model_datetime
    global model_period
    global model_length
    model_datetime = new_model_datetime
    model_period = datetime.timedelta(minutes=new_model_period)
    file = get_wrf_file()
    variable = file.variables['T2'].data[:]
    model_length = len(variable[:, y_lat, x_lon])


def get_wrf_file():
    base_path = os.getenv('HOME')

    path = os.path.join(base_path, 'wrfmain', 'kate', 'reanalysis')  # path to files
    # path = os.path.join(base_path, 'wrfmain', 'kate', 'forecast')             # path to files

    path = os.path.join(path, datetime.datetime.strftime(model_datetime, '%Y%m%d%H'))

    file = 'wrfout_d02_'  # domain select
    # file = 'wrfout_d01_'                                                      # domain select

    file = file + datetime.datetime.strftime(model_datetime, '%Y-%m-%d_%H:00:00')
    return netcdf.netcdf_file(os.path.join(path, file), 'r')


def get_t2(event_datetime, vector=1):
    time_index = get_index(event_datetime, vector)
    file = get_wrf_file()
    temp_m2 = file.variables['T2'].data[:] - 273.15
    return temp_m2[time_index:time_index + vector, y_lat, x_lon]


def get_s_wind(event_datetime, vector=1):
    time_index = get_index(event_datetime, vector)
    file = get_wrf_file()
    u10 = file.variables['U10'].data[:]
    v10 = file.variables['V10'].data[:]
    wind = (u10 * u10 + v10 * v10) ** 0.5
    return wind[time_index:time_index + vector, y_lat, x_lon]


def get_s_pressure(event_datetime, vector=1):
    time_index = get_index(event_datetime, vector)
    file = get_wrf_file()
    s_pressure = file.variables['PSFC'].data[:] / 100
    return s_pressure[time_index:time_index + vector, y_lat, x_lon]


def get_wind(event_datetime, vector=1):
    time_index = get_index(event_datetime, vector)
    file = get_wrf_file()
    u = file.variables['U'].data[:, :, :, :1]
    v = file.variables['V'].data[:, :, :1, :]
    wind = (u * u + v * v) ** 0.5
    return wind[time_index:time_index + vector, :, y_lat, x_lon]


def get_q(event_datetime, vector=1, name='QVAPOR'):
    time_index = get_index(event_datetime, vector)
    file = get_wrf_file()
    vapor = file.variables[name].data[:] / 1
    alt = file.variables['ALT'].data[:]
    real_vapor_dens = vapor / alt
    return real_vapor_dens[time_index:time_index + vector, :, y_lat, x_lon]


def get_height():
    file = get_wrf_file()
    base_geopot = file.variables['PHB'].data[:]
    pert_geopot = file.variables['PH'].data[:]
    height = (base_geopot + pert_geopot) / 9.81
    return height[0, :, y_lat, x_lon]


def main():
    #
    # http://www.meteo.unican.es/wiki/cordexwrf/OutputVariables
    #
    set_model_datetime(datetime.datetime(2016,5,4,0,0), 5)
    event_datetime = datetime.datetime(2016, 5, 4, 12, 00)
    time_frames = 42  # nubmer of time points

    y = get_height()[:-1]
    x = [event_datetime + datetime.timedelta(minutes=10 * i) for i in range(time_frames)]

    # plt.plot(x, get_t2(event_datetime, vector=time_frames))
    # plt.plot(x, get_s_wind(event_datetime, vector=time_frames))
    # plt.plot(x, get_s_pressure(event_datetime, vector=time_frames))
    plt.contourf(x, y, np.array(get_wind(event_datetime, vector=time_frames)).transpose())
    # plt.contourf(x, y, np.array(get_q(event_datetime, vector=time_frames, name="QICE")).transpose())
    # plt.contourf(x, y, np.array(get_q(event_datetime, vector=time_frames, name="QSNOW")).transpose())
    # plt.contourf(x, y, np.array(get_q(event_datetime, vector=time_frames, name="QVAPOR")).transpose())
    # plt.contourf(x, y, np.array(get_q(event_datetime, vector=time_frames, name="QRAIN")).transpose())
    # plt.contourf(x, y, np.array(get_q(event_datetime, vector=time_frames, name="QGRAUP")).transpose())
    # plt.contourf(x, y, np.array(get_q(event_datetime, vector=time_frames, name="QCLOUD")).transpose())

    plt.colorbar()
    plt.show()


def get_index(event_datetime, vector):
    global model_period
    global model_length 
    if event_datetime < model_datetime:
        raise Exception("Event datetime is less then modeling")
    if event_datetime + model_period * vector > model_datetime + model_length * model_period:
        raise Exception("Event datetime is more then modeling")
    time_delta = event_datetime - model_datetime
    return int(time_delta.seconds / model_period.seconds)


if __name__ == '__main__':
    main()
