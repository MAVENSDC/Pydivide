import pydivide
import pytplot
import numpy as np
import cdflib
import pandas as pd

# # Download KP test
#pydivide.download_files(filenames='mvn_kp_insitu_20151230_v09_r02.tab')
#pydivide.download_files(start_date='2017-06-18', end_date='2017-06-20')
#pydivide.download_files(start_date='2015-06-01', end_date='2015-06-04',iuvs=True)
#pydivide.download_files(start_date='2016-01-19', end_date='2016-01-20')
#pydivide.download_files(start_date='2015-11-03', end_date='2015-11-04',iuvs=True)
#pydivide.download_files(start_date='2016-04-09', end_date='2016-04-11')

#pydivide.download_files(start_date='2015-12-25', end_date='2015-12-27')
#pydivide.download_files(start_date='2015-12-25', end_date='2015-12-27', new_files=True,exclude_orbit_file=True, iuvs=True)
  
# #Download science files test
#pydivide.download_files(instruments=['swi', 'mag'], start_date='2015-12-25', end_date='2015-12-27', update_prefs=True)
#  

# # 1D PLOT TIMEBAR
# insitu,iuvs = pydivide.read('2017-06-19','2017-06-20')
# t = insitu['Time']
# data = insitu['SPACECRAFT']['ALTITUDE']
# pytplot.store_data('sgx',data = {'x':t, 'y':data})
# pytplot.timebar(1497841413,'sgx',color='firebrick',thick=5)
# pytplot.timebar(1497842413,'sgx',color='indigo',thick=5)
# #pytplot.options(['a','b','c'],['sgx','sgx','sgx'])
# pytplot.tplot(['sgx','sgx','sgx'])
# pydivide.cleanup_files()
#PLOT TIMEBAR ALT
# insitu,iuvs = pydivide.read('2017-06-19')
# pydivide.tplot_varcreate(insitu)
# print(pytplot.data_quants)
# t = insitu['Time']
# data = insitu['SPACECRAFT']['ALTITUDE']
# lat = insitu['SPACECRAFT']['SUB_SC_LATITUDE']
# pytplot.store_data('sc_lat', data={'x':t, 'y':lat})
# pytplot.store_data('sc_alt', data={'x':t, 'y':data})
# pytplot.options('sc_lat', 'link', ['alt', 'sc_alt'])
# pytplot.options('sc_lat','alt', 1)
# pytplot.timebar([1497841413,1497842413],'sc_lat',color='papayawhip',thick=10)
# pytplot.timebar([1497843413,1497844413],'sc_lat',color='lavender',thick=5)
# pytplot.timebar([1497839413,1497836413],'sc_lat',color='cornflowerblue',thick=7) 
# pytplot.tplot(['sc_lat'],crosshair=False)

#MAP TIMEBAR
# insitu = pydivide.read('2017-06-19')
# pydivide.map2d(insitu,'spacecraft.altitude',basemap='mola',subsolar=True)
# 
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
# pytplot.timebar([1497841413,1497842413],'sc_alt',color='r',thick=10)
# pytplot.timebar([1497843413,1497844413],'sc_alt',color='g',thick=5)
# pytplot.timebar([1497839413,1497836413],'sc_alt',color='b',thick=7)
# pytplot.tplot(['sc_alt'])
# 
# ## SPEC TESTS
# pydivide.download_files(filenames="C:/temp/mavencdfs/mvn_swe_l2_svyspec_20170619_v04_r04.cdf")
# pydivide.download_files(filenames="C:/temp/mavencdfs/mvn_euv_l2_bands_20170619_v09_r03.cdf")
# pytplot.cdf_to_tplot(r"C:\Users\Elysia\Desktop\maven_code\maven_data\mvn_swe_l2_svyspec_20170619_v04_r04.cdf")
# #pytplot.cdf_to_tplot("C:\Users\Elysia\Desktop\maven_code\maven_data\mvn_swe_l2_svyspec_20170619_v04_r04.cdf")
# #pytplot.cdf_to_tplot("C:\Users\Elysia\Desktop\maven_code\maven_data\mvn_swe_l2_svyspec_20170619_v04_r04.cdf")
# pytplot.cdf_to_tplot(r"C:\Users\Elysia\Desktop\maven_code\maven_data\mvn_euv_l2_bands_20170619_v09_r03.cdf",prefix="mvn_euv_")
# pytplot.store_data('orbit', data={'x':[1497700000, 1498000000], 'y':[3350, 3360]})
# pytplot.store_data('mvn_euv_data2', data = ['mvn_euv_data','mvn_euv_data'])
# pytplot.options('diff_en_fluxes', 'colormap', 'magma')
# pytplot.options('diff_en_fluxes', 'ztitle', 'FLUX')
# pytplot.options('diff_en_fluxes', 'ytitle', 'Energy')
# pytplot.options("diff_en_fluxes", "spec", 1)
# pytplot.options("mvn_euv_data2" , 'legend_names', ['asdfghjkl', 'asdfghjkl', 'asdfghjkl','asdfghjkl','asdfghjkl','asdfghjkl','asdfghjkl'])
# pytplot.options("diff_en_fluxes" , 'panel_size', 1)
# pytplot.options('diff_en_fluxes', 'ylog', 1)
# pytplot.options('diff_en_fluxes', 'zlog', 1)
# pytplot.tplot_options('wsize', [1000,1000])
# pytplot.tplot_options('title', "MAVEN Orbit 3355")
# pytplot.tplot_options('title_size', 8)
# pytplot.timestamp('on')
# pytplot.timebar([1497839413,1497836413],'diff_en_fluxes',color='turquoise',thick=7)
# pytplot.timebar([1497839413,1497836413],'mvn_euv_data2',color='orchid',thick=7)
     
#print(pytplot.data_quants['diff_en_fluxes'].data.head(20))
#print(np.asarray(pytplot.data_quants['diff_en_fluxes'].data))
#pytplot.tplot([0,3], var_label=2,crosshair=True,bokeh=True)

##OTHER
#insitu2, iuvs2 = pydivide.read('2015-12-26', instruments=['lpw', 'mag'])
#insitu3 = pydivide.read('2017-06-19', insitu_only=True)
#  
# #1D plots
insitu,iuvs = pydivide.read('2015-12-26')
# insitu_out = pydivide.bin(insitu, 'SWIA.HPLUS_DENSITY', 'SPACECRAFT.ALTITUDE', binsize=10, avg=True, std=True)
# pytplot.store_data('testing123', data={'x':np.arange(len(insitu_out[0])), 'y':insitu_out[0]})
# insitu = pydivide.read('2015-12-26')
# pydivide.plot(insitu, parameter='SPACECRAFT.geo_x')
# pytplot.timebar(1450000000,'testing123',color='cyan')
# pydivide.plot(insitu, parameter='SPACECRAFT.GEO_X', list=True)
# pydivide.plot(insitu3, parameter='SPACECRAFT.GEO_X', time=['2015-12-26 3:45:00', '2015-12-26 15:15:00'])
#pydivide.plot(insitu2, parameter=['SPACECRAFT.GEO_X', 'spacecraft.ALTITUDE'], time=['2015-12-26 3:45:00', '2015-12-26 15:15:00'])
#  
# #Altitude plots
# pydivide.altplot(insitu, parameter=['LPW.ELECTRON_DENSITY'])
# pydivide.altplot(insitu, parameter=['LPW.ELECTRON_DENSITY', 'MAG.MSO_Y'])
# pydivide.altplot(insitu, parameter=['LPW.ELECTRON_DENSITY', 'MAG.MSO_Y'], list=True)
#   
# #Binning Data
# insitu_out = pydivide.bin(insitu, 'SWIA.HPLUS_DENSITY', 'SPACECRAFT.ALTITUDE', binsize=10, avg=True, std=True)
# pytplot.store_data('testing123', data={'x':np.arange(len(insitu_out[0])), 'y':insitu_out[0]})
# pytplot.timebar(0.08,'testing123','maroon')
# print(pytplot.data_quants['testing123'].time_bar)
# pytplot.tplot('testing123')
# print("done")
# insitu_out = pydivide.bin(insitu, 'SWIA.HPLUS_DENSITY', 'SPACECRAFT.ALTITUDE', binsize=10, median=True, density=True)
#   
# #insitu search
# insitu2 = pydivide.insitu_search(insitu, 'spacecraft.altitude', min=3000, max=10000)
# print(len(insitu4['SPACECRAFT']))
  
# resampling
# swi_cdf = cdflib.CDF('C:/data_to_plot/mvn_swi_l2_coarsesvy3d_20160620_v01_r00.cdf')
# newtime = swi_cdf.varget('time_unix')
# insitu5 = pydivide.resample(insitu2, newtime)
# swi_cdf = cdflib.CDF('C:/data_to_plot/mvn_swi_l2_coarsesvy3d_20151226_v01_r00.cdf')
# newtime = swi_cdf.varget('time_unix')
# insitu6 = pydivide.resample(insitu2, newtime[0:1000])
# print(len(insitu6['SPACECRAFT']))
#  
# #Standards
# pydivide.standards(insitu,all_plots=True)
# pydivide.standards(insitu3, sc_pot=True, plasma_temp=True, altitude=True, swea=True)
# pydivide.standards(insitu, mag_mso=True, eph_angle=True, static_flux=True, title='Example Title')
# pydivide.standards(insitu, euv=True, ngims_ions=True, swea=True, sep_electron=True)
#  
#  
#Create Model Maps
#banana = pydivide.create_model_maps(altitude=170, file = 'C:/Users/Elysia/Desktop/maven_code/maven_data/MAMPS_LS180_F130_081216.nc', variable='geo_x', saveFig=True)
#pydivide.create_model_maps(altitude=200, file = 'C:/Users/Elysia/Desktop/maven_code/maven_data/MAMPS_LS180_F130_081216.nc', fill=True, variable='geo_x', saveFig=False)
#  
# #2D Maps
#pydivide.map2d(insitu,'spacecraft.altitude',mso=True)
pydivide.map2d(insitu,'spacecraft.altitude',basemap='mola')
#pydivide.map2d(insitu, 'ngims.co2plus_density',  map_limit=[-60,90,60,270], mso=True)
#pydivide.map2d(insitu, 'SWIA.HPLUS_DENSITY', time = ['2015-12-26 3:45:00', '2015-12-26 15:15:00'], basemap='C:/Mars Models/ModelData_o2plus_200km.png', mso=True)
#pydivide.map2d(insitu, 'SWIA.HPLUS_DENSITY', time = ['2015-12-26 3:45:00', '2015-12-26 15:15:00'], basemap='C:/Mars Models/ModelData_o2plus_200km.png', mso=True, subsolar=True)
#  
# #Model Interpolation
#Sasdf = pydivide.interpol_model(insitu, file = 'C:/Mars Models/Elew_18_06_14_t00600.nc')
# asdf = pydivide.interpol_model(insitu2, file = 'C:/Mars Models/Heliosares_Ionos_Ls180_SolMean1_12_02_13.nc', nearest=True)
# 
# pytplot.store_data('model_interp', data={'x':insitu['Time'], 'y':asdf['Ez']})
# pytplot.timebar('x','model_interp',databar = False, delete = False, color = 'black', thick = 1, dash = False)
# pytplot.tplot('model_interp',pyqtgraph = True)

#Corona Plots
# insitu,iuvs = pydivide.read('2016-01-19','2016-01-20')
# pydivide.corona(iuvs)
# pydivide.corona(iuvs, species = ['H', 'O', 'O_1304'], orbit_num = [2540, 2546], title='Example Title')

#Occultation Plots
#insitu,iuvs = pydivide.read('2015-11-03','2015-11-04')
# pydivide.occultation(iuvs)
#pydivide.occultation(iuvs,orbit_num = [2135], title='Example Title')

# #Periapse Plots
#insitu,iuvs = pydivide.read('2015-06-02','2015-06-03')
# pydivide.periapse(iuvs, species='N2', orbit_num=1307)

#PLOT
#insitu,iuvs = pydivide.read('2015-12-26')
#insitu = pydivide.read('2016-04-10')
#pydivide.plot(insitu,parameter='swia.hplus_density')
#pydivide.plot(insitu,parameter=['swia.hplus_density','spacecraft.altitude'],SamePlot=True)
#pydivide.plot(insitu,parameter='swia.hplus_density',time=['2016-04-10 02:00:00','2016-04-10 12:00:00'])
#pydivide.plot(insitu,parameter='spacecraft.geo_x')

#Read Model Results
#model = pydivide.read_model_results('C:/Users/Elysia/Desktop/maven_code/maven_data/MGITM_LS270_F130_150519.nc')
#model = pydivide.read_model_results('C:/Users/Elysia/Desktop/maven_code/maven_data/Heliosares_Ionos_Ls270_SolMax1_26_01_15.nc')
#print(model)