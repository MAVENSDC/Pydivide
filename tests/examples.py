import pydivide
import pytplot
import numpy as np
import pds_cdf
import pandas as pd
# Download KP test
pydivide.mvn_kp_download_files(filenames='mvn_kp_insitu_20151230_v09_r02.tab')
pydivide.mvn_kp_download_files(start_date='2015-12-25', end_date='2015-12-27')
pydivide.mvn_kp_download_files(start_date='2015-12-25', end_date='2015-12-27', new_files=True, update_prefs=True, exclude_orbit_file=True)

#Download science files test
pydivide.mvn_kp_download_sci_files(instruments=['swi', 'mag'], start_date='2015-12-25', end_date='2015-12-27', update_prefs=True)

#Read in data
insitu, iuvs = pydivide.mvn_kp_read('2015-12-26')
insitu2, iuvs2 = pydivide.mvn_kp_read('2015-12-26', instruments=['lpw', 'mag'])
insitu3, iuvs3 = pydivide.mvn_kp_read('2015-12-25', insitu_only=True)

#1D plots
pydivide.mvn_kp_plot(insitu, parameter='SPACECRAFT.geo_x')
pydivide.mvn_kp_plot(insitu, parameter='SPACECRAFT.GEO_X', list=True)
pydivide.mvn_kp_plot(insitu3, parameter='SPACECRAFT.GEO_X', time=['2015-12-25 3:45:00', '2015-12-25 15:15:00'])
pydivide.mvn_kp_plot(insitu2, parameter=['SPACECRAFT.GEO_X', 'spacecraft.ALTITUDE'], time=['2015-12-26 3:45:00', '2015-12-26 15:15:00'])

#Altitude plots
pydivide.mvn_kp_altplot(insitu, parameter=['LPW.ELECTRON_DENSITY'])
pydivide.mvn_kp_altplot(insitu, parameter=['LPW.ELECtRON_DENSITY', 'MAG.mso_Y'])
pydivide.mvn_kp_altplot(insitu, parameter=['LPW.ELECTRON_DENSITY', 'MAG.MSO_Y'], list=True)

#Binning Data
insitu_out = pydivide.mvn_kp_bin(insitu, 'SWIA.HPLUS_DENSITY', 'SPACECRAFT.ALTITUDE', binsize=10, avg=True, std=True)
pytplot.store_data('testing123', data={'x':np.arange(len(insitu_out[0])), 'y':insitu_out[0]})
pytplot.tplot('testing123')
insitu_out = pydivide.mvn_kp_bin(insitu, 'SWIA.HPLUS_DENSITY', 'SPACECRAFT.ALTITUDE', binsize=10, median=True, density=True)

#insitu search
insitu4 = pydivide.mvn_kp_insitu_search(insitu2, 'spacecraft.altitude', min=3000, max=10000)
print(len(insitu4['SPACECRAFT']))

#resampling
swi_cdf = pds_cdf.CDF('C:/data_to_plot/mvn_swi_l2_coarsesvy3d_20160620_v01_r00.cdf')
newtime = swi_cdf.varget('time_unix')
insitu5 = pydivide.mvn_kp_resample(insitu2, newtime)
swi_cdf = pds_cdf.CDF('C:/data_to_plot/mvn_swi_l2_coarsesvy3d_20151226_v01_r00.cdf')
newtime = swi_cdf.varget('time_unix')
insitu6 = pydivide.mvn_kp_resample(insitu2, newtime[0:1000])
print(len(insitu6['SPACECRAFT']))

#Standards
pydivide.mvn_kp_standards(insitu3, sc_pot=True, plasma_temp=True, altitude=True, swea=True)
pydivide.mvn_kp_standards(insitu, mag_mso=True, eph_angle=True, static_flux=True, title='Random Plots')
pydivide.mvn_kp_standards(insitu, euv=True, ngims_ions=True, swea=True, sep_electron=True)


#Create Model Maps
pydivide.mvn_kp_create_model_maps(altitude=170, file = 'C:/Mars Models/MGITM_LS090_F070_150812.nc')
pydivide.mvn_kp_create_model_maps(altitude=200, file = 'C:/Mars Models/MAMPS_LS180_F130_081216.nc', fill=True, numContours=10)

#2D Maps
pydivide.mvn_kp_map2d(insitu, 'ngims.co2plus_density’',  map_limit=[-60,90,60,270], mso=True)
pydivide.mvn_kp_map2d(insitu, 'SWIA.HPLUS_DENSITY', time = ['2015-12-26 3:45:00', '2015-12-26 15:15:00'], basemap='C:/Mars Models/ModelData_o2plus_200km.png', mso=True)
pydivide.mvn_kp_map2d(insitu, 'SWIA.HPLUS_DENSITY', time = ['2015-12-26 3:45:00', '2015-12-26 15:15:00'], basemap='C:/Mars Models/ModelData_o2plus_200km.png', mso=True, subsolar=True)

#Model Interpolation
asdf = pydivide.mvn_kp_interpol_model(insitu, file = 'C:/Mars Models/Elew_18_06_14_t00600.nc')
print(asdf['Ey'][1000])
asdf = pydivide.mvn_kp_interpol_model(insitu2, file = 'C:/Mars Models/Heliosares_Ionos_Ls180_SolMean1_12_02_13.nc', nearest=True)
