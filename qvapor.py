import numpy as np
from wrf import getvar, vinterp
from netCDF4 import Dataset
import matplotlib.pyplot as plt

# берёт файл с готовыми результатами расчёта и интерполирует их на эквидистантную сетку - произвольную, мелкую - по высоте, строит график плотности от высоты, в файл не пишет


path ='/mnt/data-internal/newversion/2017092906/wrfout_d02_2017-09-29_06:00:00'

ncfile = Dataset(path)

name = 'QVAPOR'
start_level = 'ght_msl' # above_mean_sea_level ; 'ght_agl' - above ground level


m_density_array = getvar(ncfile, name, timeidx = 100,  meta=False)

z = getvar(ncfile, 'z',  meta=False)  # высоты точек, в которых посчитано, в метрах





height_array_for_interp = np.arange(0.02, 6, 0.02)   # in km

interpolated_m_dens = vinterp(ncfile, m_density_array, start_level, height_array_for_interp)

plt.plot(m_density_array[:, 45, 45], z[:, 45, 45]/1000)
plt.plot(interpolated_m_dens[:, 45, 45], height_array_for_interp)


plt.show()



