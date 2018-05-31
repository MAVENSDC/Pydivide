import pydivide
import pytplot
import numpy as np
import cdflib
import pandas as pd

# # Download KP test
#pydivide.download_files(filenames='mvn_kp_insitu_20151230_v09_r02.tab')
#pydivide.download_files(start_date='2017-06-18', end_date='2017-06-20')
#pydivide.download_files(start_date='2015-12-25', end_date='2015-12-27', iuvs=True)
#pydivide.download_files(start_date='2015-12-25', end_date='2015-12-27', new_files=True,exclude_orbit_file=True, iuvs=True)
#  
# #Download science files test
#pydivide.download_files(instruments=['swi', 'mag'], start_date='2015-12-25', end_date='2015-12-27', update_prefs=True)
#  
# 1D PLOT TIMEBAR
insitu, iuvs = pydivide.read('2015-12-26')
t = insitu['Time']
data = insitu['SPACECRAFT']['ALTITUDE']
pytplot.store_data('sgx',data = {'x':t, 'y':data})
pytplot.timebar(1451107201,'sgx',color='m',thick=5)
pytplot.tplot('sgx',pyqtgraph = True)

#PLOT TIMEBAR ALT
# insitu = pydivide.read('2017-06-19')
# t = insitu['Time']
# data = insitu['SPACECRAFT']['ALTITUDE']
# lat = insitu['SPACECRAFT']['SUB_SC_LATITUDE']
# pytplot.store_data('sc_lat', data={'x':t, 'y':lat})
# pytplot.store_data('sc_alt', data={'x':t, 'y':data})
# pytplot.options('sc_lat', 'link', ['alt', 'sc_alt'])
# pytplot.options('sc_lat','alt', 1)
# pytplot.timebar([1497841413,1497842413],'sc_lat',color='m',thick=10)
# pytplot.timebar([1497843413,1497844413],'sc_lat',color='g',thick=5)
# pytplot.timebar([1497839413,1497836413],'sc_lat',color='c',thick=7) 
#pytplot.tplot(['sc_lat'], pyqtgraph=True)

#MAP TIMEBAR
# insitu = pydivide.read('2017-06-19')
# t = insitu['Time']
# data = insitu['SPACECRAFT']['ALTITUDE']
# lat = insitu['SPACECRAFT']['SUB_SC_LATITUDE']
#  
# lon = insitu['SPACECRAFT']['SUB_SC_LONGITUDE']
# pytplot.store_data('sc_lat', data={'x':t, 'y':lat})
#  
# pytplot.store_data('sc_lon', data={'x':t, 'y':lon})
# pytplot.store_data('sc_alt', data={'x':t, 'y':data})
# pytplot.options('sc_alt', 'link', ['lat', 'sc_lat'])
# pytplot.options('sc_alt', 'link', ['lon', 'sc_lon'])
# pytplot.options('sc_alt','map', 1)
# pytplot.timebar([1497841413,1497842413],'sc_alt',color='m',thick=10)
# pytplot.timebar([1497843413,1497844413],'sc_alt',color='g',thick=5)
# pytplot.timebar([1497839413,1497836413],'sc_alt',color='c',thick=7)
# pytplot.tplot(['sc_alt'], pyqtgraph=True)

#insitu2, iuvs2 = pydivide.read('2015-12-26', instruments=['lpw', 'mag'])
#insitu3 = pydivide.read('2015-12-25', insitu_only=True)
#  
# #1D plots
# pydivide.plot(insitu, parameter='SPACECRAFT.geo_x')
# pydivide.plot(insitu, parameter='SPACECRAFT.GEO_X', list=True)
# pydivide.plot(insitu3, parameter='SPACECRAFT.GEO_X', time=['2015-12-25 3:45:00', '2015-12-25 15:15:00'])
# pydivide.plot(insitu2, parameter=['SPACECRAFT.GEO_X', 'spacecraft.ALTITUDE'], time=['2015-12-26 3:45:00', '2015-12-26 15:15:00'])
#  
# #Altitude plots
# pydivide.altplot(insitu, parameter=['LPW.ELECTRON_DENSITY'])
# pydivide.altplot(insitu, parameter=['LPW.ELECtRON_DENSITY', 'MAG.mso_Y'])
# pydivide.altplot(insitu, parameter=['LPW.ELECTRON_DENSITY', 'MAG.MSO_Y'], list=True)
#  
# #Binning Data
# insitu_out = pydivide.bin(insitu, 'SWIA.HPLUS_DENSITY', 'SPACECRAFT.ALTITUDE', binsize=10, avg=True, std=True)
# pytplot.store_data('testing123', data={'x':np.arange(len(insitu_out[0])), 'y':insitu_out[0]})
# pytplot.tplot('testing123')
# insitu_out = pydivide.bin(insitu, 'SWIA.HPLUS_DENSITY', 'SPACECRAFT.ALTITUDE', binsize=10, median=True, density=True)
#  
# #insitu search
# insitu2 = pydivide.insitu_search(insitu, 'spacecraft.altitude', min=3000, max=10000)
# print(len(insitu4['SPACECRAFT']))
#  
# #resampling
# swi_cdf = cdflib.CDF('C:/data_to_plot/mvn_swi_l2_coarsesvy3d_20160620_v01_r00.cdf')
# newtime = swi_cdf.varget('time_unix')
# insitu5 = pydivide.resample(insitu2, newtime)
# swi_cdf = cdflib.CDF('C:/data_to_plot/mvn_swi_l2_coarsesvy3d_20151226_v01_r00.cdf')
# newtime = swi_cdf.varget('time_unix')
# insitu6 = pydivide.resample(insitu2, newtime[0:1000])
# print(len(insitu6['SPACECRAFT']))
#  
# #Standards
# pydivide.standards(insitu3, sc_pot=True, plasma_temp=True, altitude=True, swea=True)
# pydivide.standards(insitu, mag_mso=True, eph_angle=True, static_flux=True, title='Random Plots')
# pydivide.standards(insitu, euv=True, ngims_ions=True, swea=True, sep_electron=True)
#  
#  
#Create Model Maps
#banana = pydivide.create_model_maps(altitude=170, file = 'C:/Mars Models/MGITM_LS090_F070_150812.nc', variable='o', saveFig=False)
#pydivide.create_model_maps(altitude=200, file = 'C:/Mars Models/MAMPS_LS180_F130_081216.nc', fill=True, numContours=10, variable='geo_x', saveFig=False)
#  
# #2D Maps
#pydivide.map2d(insitu, 'ngims.co2plus_density',  map_limit=[-60,90,60,270], mso=True)
#pydivide.map2d(insitu, 'SWIA.HPLUS_DENSITY', time = ['2015-12-26 3:45:00', '2015-12-26 15:15:00'], basemap='C:/Mars Models/ModelData_o2plus_200km.png', mso=True)
#pydivide.map2d(insitu, 'SWIA.HPLUS_DENSITY', time = ['2015-12-26 3:45:00', '2015-12-26 15:15:00'], basemap='C:/Mars Models/ModelData_o2plus_200km.png', mso=True, subsolar=True)
#  
# #Model Interpolation
#Sasdf = pydivide.interpol_model(insitu, file = 'C:/Mars Models/Elew_18_06_14_t00600.nc')
#asdf = pydivide.interpol_model(insitu2, file = 'C:/Mars Models/Heliosares_Ionos_Ls180_SolMean1_12_02_13.nc', nearest=True)

#pytplot.store_data('model_interp', data={'x':insitu['Time'], 'y':asdf['Ez']})
#pytplot.timebar('x','model_interp',databar = False, delete = False, color = 'black', thick = 1, dash = False)
#pytplot.tplot('model_interp',pyqtgraph = True)

#Corona Plots
#insitu,iuvs = pydivide.read('2016-01-19','2016-01-20')
#pydivide.corona(iuvs)
#pydivide.corona(iuvs, species = ['H', 'O', 'O_1304'], orbit_num = [2540, 2546], title='Testing1234')

# #Periapse Plots
# insitu,iuvs = pydivide.read('2015-06-02','2015-06-03')
# pydivide.periapse(iuvs, log=True, species='N2', orbit_num=1307)
