# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pydivide

import math
import pytplot
from .utilities import param_dict

def mvn_kp_standards(kp, 
                     list_plots=False,
                     all_plots=False,
                     euv=False,
                     mag_mso=False,
                     mag_geo=False,
                     mag_cone=False,
                     mag_dir=False,
                     ngims_neutral=False,
                     ngims_ions=False,
                     eph_angle=False,
                     eph_geo=False,
                     eph_mso=False,
                     swea=False,
                     sep_ion=False,
                     sep_electron=False,
                     wave=False,
                     plasma_den=False,
                     plasma_temp=False,
                     swia_h_vel=False,
                     static_h_vel=False,
                     static_o2_vel=False,
                     static_flux=False,
                     static_energy=False,
                     sun_bar=False,
                     solar_wind=False,
                     ionosphere=False,
                     sc_pot=False,
                     altitude=False,
                     title='Standard Plots',
                     qt=True):
    print("This procedure was renamed, just use standards")
    standards(kp, 
              list_plots=list_plots,
              all_plots=all_plots,
              euv=euv,
              mag_mso=mag_mso,
              mag_geo=mag_geo,
              mag_cone=mag_cone,
              mag_dir=mag_dir,
              ngims_neutral=ngims_neutral,
              ngims_ions=ngims_ions,
              eph_angle=eph_angle,
              eph_geo=eph_geo,
              eph_mso=eph_mso,
              swea=swea,
              sep_ion=sep_ion,
              sep_electron=sep_electron,
              wave=wave,
              plasma_den=plasma_den,
              plasma_temp=plasma_temp,
              swia_h_vel=swia_h_vel,
              static_h_vel=static_h_vel,
              static_o2_vel=static_o2_vel,
              static_flux=static_flux,
              static_energy=static_energy,
              sun_bar=sun_bar,
              solar_wind=solar_wind,
              ionosphere=ionosphere,
              sc_pot=sc_pot,
              altitude=altitude,
              title=title,
              qt=qt)
    return

def standards(kp, 
              list_plots=False,
              all_plots=False,
              euv=False,
              mag_mso=False,
              mag_geo=False,
              mag_cone=False,
              mag_dir=False,
              ngims_neutral=False,
              ngims_ions=False,
              eph_angle=False,
              eph_geo=False,
              eph_mso=False,
              swea=False,
              sep_ion=False,
              sep_electron=False,
              wave=False,
              plasma_den=False,
              plasma_temp=False,
              swia_h_vel=False,
              static_h_vel=False,
              static_o2_vel=False,
              static_flux=False,
              static_energy=False,
              sun_bar=False,
              solar_wind=False,
              ionosphere=False,
              sc_pot=False,
              altitude=False,
              title='Standard Plots',
              qt=True):

    if all_plots:
        euv = True
        mag_mso = True
        mag_geo = True
        mag_cone = True
        mag_dir = True
        ngims_neutral = True
        ngims_ions = True
        eph_angle = True
        eph_geo = True
        eph_mso = True
        swea = True
        sep_ion = True
        sep_electron = True
        wave = True
        plasma_den = True
        plasma_temp = True
        swia_h_vel = True
        static_h_vel = True
        static_o2_vel = True
        static_flux = True
        static_energy = True
        sun_bar = True
        solar_wind = True
        ionosphere = True
        sc_pot = True
    
    
    if list_plots:
        print("all: Generate all 25 plots")
        print("euv: EUV irradiance in each of three bands")
        print("mag_mso: Magnetic field, MSO coordinates")
        print("mag_geo: Magnetic field, Geographic coordinates")
        print("mag_cone: Magnetic clock and cone angles, MSO coordinates")
        print("mag_dir: Magnetic field: radial, horizontal, northward, and eastward components")
        print("ngims_neutral: Neutral atmospheric component densities")
        print("ngims_ions: Ionized atmospheric component densities")
        print("eph_angle: Spacecraft ephemeris information")
        print("eph_geo: Spacecraft position in geographic coordinates")
        print("eph_mso: Spacecraft position in MSO coordinates")
        print("swea: electron parallel/anti-parallel fluxes")
        print("sep_ion: Ion Energy fluxes")
        print("sep_electron: Electron Energy fluxes")
        print("wave: Electric field wave power")
        print("plasma_den: Plasma densities")
        print("plasma_temp: Plasma Temperatures")
        print("swia_h_vel: H+ Flow velocity in MSO coordinates from SWIA")
        print("static_h_vel: H+ flow velocity in MSO coordinates from STATIC")
        print("static_o2_vel: O2+ flow velocity in MSO coords from STATIC")
        print("static_flux: H+/He++ and Pick-up Ion omni-directional fluxes")
        print("static_energy: H+/He++ and Pick-up Ion characteristic energies")
        print("sun_bar: Indication of whether MAVEn is in sunlight")
        print("solar_wind: solar wind dynamic pressure")
        print("ionosphere: Electron Spectrum shape parameter")
        print("sc_pot: Spacecraft potential")
        return 
    
    # Set up the plots to be underneath each other
    max_num_plots = sum([euv, mag_mso, mag_geo, mag_cone, mag_dir, 
                        ngims_neutral, ngims_ions, eph_angle, eph_geo, 
                        eph_mso, swea, sep_ion, sep_electron, wave, 
                        plasma_den, plasma_temp, swia_h_vel, static_h_vel, 
                        static_o2_vel, static_flux, static_energy, sun_bar, 
                        solar_wind, ionosphere, sc_pot])
    
    if (max_num_plots == 0):
        print("Please specify a plot to generate.")
        return
    
    #The number plot we're plotting in the figure
    current_plot_number = 0
    names_to_plot=[]
    
    pytplot.xlim(float(kp['Time'][0]), float(kp['Time'][-1]))
    
    if euv:
        title = "EUV"
        try:
            if 'EUV' not in kp.keys():
                raise Exception("NoDataException")
            euv_dataframe = kp['EUV'].loc[:,[param_dict['EUV Irradiance Lyman-alpha'],param_dict['EUV Irradiance 17-22 nm'], param_dict['EUV Irradiance 0.1-7.0 nm']]]
            pytplot.store_data(title, data={'x':kp['Time'], 'y':euv_dataframe})
            pytplot.options(title,'legend_names',['EUV Irradiance Lyman-alpha','EUV Irradiance 17-22 nm', 'EUV Irradiance 0.1-7.0 nm'])
            names_to_plot.append(title)
            current_plot_number = current_plot_number + 1            
        except Exception as x:
            if str(x) == "NoDataException":
                print("EUV is not in the Key Parameter Data Structure, " + title + " will not be plotted")
        
    if mag_mso:
        title = "MAG MSO"
        try:
            if 'MAG' not in kp.keys():
                raise Exception("NoDataException")
            
            mag_mso_dataframe = kp['MAG'].loc[:,[param_dict['Magnetic Field MSO X'],param_dict['Magnetic Field MSO Y'], param_dict['Magnetic Field MSO Z']]]
            mag_mso_dataframe['Magnetic Field Magnitude MSO'] = ((kp['MAG'][param_dict['Magnetic Field MSO X']]*kp['MAG'][param_dict['Magnetic Field MSO X']]) + (kp['MAG'][param_dict['Magnetic Field MSO Y']]*kp['MAG'][param_dict['Magnetic Field MSO Y']]) + (kp['MAG'][param_dict['Magnetic Field MSO Z']]*kp['MAG'][param_dict['Magnetic Field MSO Z']])).apply(math.sqrt)
            pytplot.store_data(title, data={'x':kp['Time'], 'y':mag_mso_dataframe})
            pytplot.options(title,'legend_names',['Magnetic Field MSO X','Magnetic Field MSO Y', 'Magnetic Field MSO Z', 'Magnetic Field Magnitude MSO'])
            names_to_plot.append(title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("MAG is not in the Key Parameter Data Structure, " + title + " will not be plotted")

    if mag_geo:
        title = "MAG GEO"
        try:
            if 'MAG' not in kp.keys():
                raise Exception("NoDataException")
            mag_geo_dataframe = kp['MAG'].loc[:,[param_dict['Magnetic Field GEO X'],param_dict['Magnetic Field GEO Y'], param_dict['Magnetic Field GEO Z']]]
            mag_geo_dataframe['Magnetic Field Magnitude GEO'] = ((kp['MAG'][param_dict['Magnetic Field GEO X']]*kp['MAG'][param_dict['Magnetic Field GEO X']]) + (kp['MAG'][param_dict['Magnetic Field GEO Y']]*kp['MAG'][param_dict['Magnetic Field GEO Y']]) + (kp['MAG'][param_dict['Magnetic Field GEO Z']]*kp['MAG'][param_dict['Magnetic Field GEO Z']])).apply(math.sqrt)
            pytplot.store_data(title, data={'x':kp['Time'], 'y':mag_geo_dataframe})
            pytplot.options(title,'legend_names',['Magnetic Field GEO X','Magnetic Field GEO Y', 'Magnetic Field GEO Z', 'Magnetic Field Magnitude GEO'])
            names_to_plot.append(title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("MAG is not in the Key Parameter Data Structure, " + title + " will not be plotted")
        
    if mag_cone:
        title = "MAG Cone"
        try:
            if 'MAG' not in kp.keys():
                raise Exception("NoDataException")
            #Note, this plot ends up different from the IDL version, because of the way IDL calculates arctans.  Important, or not?
            mag_cone_dataframe_temp = kp['MAG'].loc[:,[param_dict['Magnetic Field MSO X'],param_dict['Magnetic Field MSO Y'], param_dict['Magnetic Field MSO Z']]]
            mag_cone_dataframe_temp['Clock Angle'] = (mag_cone_dataframe_temp[param_dict['Magnetic Field MSO X']] / mag_cone_dataframe_temp[param_dict['Magnetic Field MSO Y']]).apply(math.atan) * 57.295776
            mag_cone_dataframe_temp['Cone Angle'] = ((mag_cone_dataframe_temp[param_dict['Magnetic Field MSO X']].apply(abs)) / (((kp['MAG'][param_dict['Magnetic Field MSO X']]*kp['MAG'][param_dict['Magnetic Field MSO X']]) + (kp['MAG'][param_dict['Magnetic Field MSO Y']]*kp['MAG'][param_dict['Magnetic Field MSO Y']]) + (kp['MAG'][param_dict['Magnetic Field MSO Z']]*kp['MAG'][param_dict['Magnetic Field MSO Z']])).apply(math.sqrt))).apply(math.acos) * 57.295776
            mag_cone_dataframe = mag_cone_dataframe_temp.loc[:,['Clock Angle','Cone Angle']]
            pytplot.store_data(title, data={'x':kp['Time'], 'y':mag_cone_dataframe})
            pytplot.options(title,'legend_names',['Magnetic Clock Angle','Magnetic Cone Angle'])
            names_to_plot.append(title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("MAG is not in the Key Parameter Data Structure, " + title + " will not be plotted")
        
    if mag_dir:
        title = "MAG Direction"
        try:
            if 'MAG' not in kp.keys():
                raise Exception("NoDataException")
            clat = (kp['SPACECRAFT']['SUB_SC_LATITUDE'] * 3.14159265/180).apply(math.cos)
            slat = (kp['SPACECRAFT']['SUB_SC_LATITUDE'] * 3.14159265/180).apply(math.sin)
            clon = (kp['SPACECRAFT']['SUB_SC_LONGITUDE'] * 3.14159265/180).apply(math.cos)
            slon = (kp['SPACECRAFT']['SUB_SC_LONGITUDE'] * 3.14159265/180).apply(math.sin)
            
            mag_rad_series = (kp['MAG'][param_dict['Magnetic Field GEO X']] * clon * clat) + (kp['MAG'][param_dict['Magnetic Field GEO Y']] * slon * clat) + (kp['MAG'][param_dict['Magnetic Field GEO Z']] * slat)
            mag_dir_dataframe = mag_rad_series.to_frame(name='Radial')
            mag_dir_dataframe['Eastward'] = (kp['MAG'][param_dict['Magnetic Field GEO X']] * slon * -1) + (kp['MAG'][param_dict['Magnetic Field GEO Y']] * clon)
            mag_dir_dataframe['Northward'] = (kp['MAG'][param_dict['Magnetic Field GEO X']] * clon * slat * -1) + (kp['MAG'][param_dict['Magnetic Field GEO Y']] * slon * slat * -1) + (kp['MAG'][param_dict['Magnetic Field GEO Z']] * clat)
            pytplot.store_data(title, data={'x':kp['Time'], 'y':mag_dir_dataframe})
            pytplot.options(title,'legend_names',['Radial','Eastward','Northward'])
            names_to_plot.append(title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("MAG is not in the Key Parameter Data Structure, " + title + " will not be plotted")
    
    if ngims_neutral:
        title = "NGIMS Neutrals"
        try:
            if 'NGIMS' not in kp.keys():
                raise Exception("NoDataException")
            ngims_neutrals_dataframe=kp['NGIMS'].loc[:,[param_dict['Density He'], param_dict['Density O'], param_dict['Density CO'], param_dict['Density N2'], param_dict['Density NO'], param_dict['Density Ar'], param_dict['Density CO2']]]
            pytplot.store_data(title, data={'x':kp['Time'], 'y':ngims_neutrals_dataframe})
            pytplot.options(title,'legend_names',['Density He', 'Density O', 'Density CO', 'Density N2', 'Density NO', 'Density Ar', 'Density CO2'])
            pytplot.options(title, 'ylog', 1)
            names_to_plot.append(title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("NGIMS is not in the Key Parameter Data Structure, " + title + " will not be plotted")
        
    if ngims_ions:
        title = "NGIMS IONS"
        try:
            if 'NGIMS' not in kp.keys():
                raise Exception("NoDataException")
            ngims_ion_dataframe = kp['NGIMS'].loc[:,[param_dict['Density 32+'], param_dict['Density 44+'], param_dict['Density 30+'], param_dict['Density 16+'], param_dict['Density 28+'], param_dict['Density 12+'], param_dict['Density 17+'], param_dict['Density 14+']]]
            pytplot.store_data(title, data={'x':kp['Time'], 'y':ngims_ion_dataframe})
            pytplot.options(title,'legend_names',['Density 32+', 'Density 44+', 'Density 30+', 'Density 16+', 'Density 28+', 'Density 12+', 'Density 17+', 'Density 14+'])
            pytplot.options(title, 'ylog', 1)
            names_to_plot.append(title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("NGIMS is not in the Key Parameter Data Structure, " + title + " will not be plotted")
        
    if eph_angle:
        title = "Spacecraft Ephemeris Information"
        try:
            if 'SPACECRAFT' not in kp.keys():
                raise Exception("NoDataException")
            #This plot makes no sense.  Why is Local Time plotted here, when it is not a measurement in degrees?  Why is Mars season/Subsolar Latitude plotted when they are essentially straight lines? 
            sc_eph_dataframe = kp['SPACECRAFT'].loc[:,['SUB_SC_LONGITUDE', 'SUB_SC_LATITUDE', 'SZA', 'LOCAL_TIME', 'MARS_SEASON', 'SUBSOLAR_POINT_GEO_LONGITUDE', 'SUBSOLAR_POINT_GEO_LATITUDE']]
            pytplot.store_data(title, data={'x':kp['Time'], 'y':sc_eph_dataframe})
            pytplot.options(title,'legend_names',['GEO Longitude', 'GEO Latitude', 'Solar Zenith Angle', 'Local Time', 'Mars Season (Ls)', 'Subsolar Point GEO Longitude', 'Subsolar Point GEO Latitude'])
            names_to_plot.append(title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("SPACECRAFT is not in the Key Parameter Data Structure, " + title + " will not be plotted")
        
    if eph_geo:
        title = "Spacecraft positon in GEO Coordinates"
        try:
            if 'SPACECRAFT' not in kp.keys():
                raise Exception("NoDataException")
            sc_pos_dataframe = kp['SPACECRAFT'].loc[:,['GEO_X', 'GEO_Y', 'GEO_Z', 'ALTITUDE']]
            pytplot.store_data(title, data={'x':kp['Time'], 'y':sc_pos_dataframe})
            pytplot.options(title,'legend_names',['GEO X', 'GEO Y', 'GEO Z', 'Altitude Aeroid'])
            names_to_plot.append(title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("SPACECRAFT is not in the Key Parameter Data Structure, " + title + " will not be plotted")
        
    if eph_mso:
        title = "Spacecraft positon in MSO Coordinates"
        try:
            if 'SPACECRAFT' not in kp.keys():
                raise Exception("NoDataException")
            sc_pos_mso_dataframe = kp['SPACECRAFT'].loc[:,'MSO_X', 'MSO_Y', 'MSO_Z', 'ALTITUDE']
            pytplot.store_data(title, data={'x':kp['Time'], 'y':sc_pos_mso_dataframe})
            pytplot.options(title,'legend_names',['MSO X', 'MSO Y', 'MSO Z', 'Altitude Aeroid'])
            names_to_plot.append(title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("LPW is not in the Key Parameter Data Structure, " + title + " will not be plotted")
        
    if swea:
        title = "SWEA"
        try:
            if 'SWEA' not in kp.keys():
                raise Exception("NoDataException")
            swea_dataframe = kp['SWEA'].loc[:,[param_dict['Flux, e- Parallel (5-100 ev)'], param_dict['Flux, e- Parallel (100-500 ev)'], param_dict['Flux, e- Parallel (500-1000 ev)'], param_dict['Flux, e- Anti-par (5-100 ev)'], param_dict['Flux, e- Anti-par (100-500 ev)'], param_dict['Flux, e- Anti-par (500-1000 ev)'], param_dict['Electron Spectrum Shape']]]
            pytplot.store_data(title, data={'x':kp['Time'], 'y':swea_dataframe})
            pytplot.options(title,'legend_names',['Flux, e- Parallel (5-100 ev)', 'Flux, e- Parallel (100-500 ev)', 'Flux, e- Parallel (500-1000 ev)', 'Flux, e- Anti-par (5-100 ev)', 'Flux, e- Anti-par (100-500 ev)', 'Flux, e- Anti-par (500-1000 ev)', 'Electron Spectrum Shape'])
            names_to_plot.append(title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("SWEA is not in the Key Parameter Data Structure, " + title + " will not be plotted")
        
    if sep_ion:
        title = "SEP Ions"
        try:
            if 'SEP' not in kp.keys():
                raise Exception("NoDataException")
            #Need to fill in the NaNs as zero, otherwise the Sum will equal all Nans
            sep_ion_dataframe = kp['SEP'].loc[:,[param_dict['Ion Flux FOV 1 F'],param_dict['Ion Flux FOV 1 R'],param_dict['Ion Flux FOV 2 F'],param_dict['Ion Flux FOV 2 R']]].fillna(0)
            sep_ion_dataframe['Sum'] = sep_ion_dataframe[param_dict['Ion Flux FOV 1 F']] + sep_ion_dataframe[param_dict['Ion Flux FOV 1 R']] + sep_ion_dataframe[param_dict['Ion Flux FOV 2 F']] + sep_ion_dataframe[param_dict['Ion Flux FOV 2 R']]
            pytplot.store_data(title, data={'x':kp['Time'], 'y':sep_ion_dataframe})
            pytplot.options(title,'legend_names',['Ion Flux FOV 1 F','Ion Flux FOV 1 R','Ion Flux FOV 2 F','Ion Flux FOV 2 R', 'Sum'])
            names_to_plot.append(title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("SEP is not in the Key Parameter Data Structure, " + title + " will not be plotted")
        
    if sep_electron:
        title = "SEP Electrons"
        try:
            if 'SEP' not in kp.keys():
                raise Exception("NoDataException")
            sep_electron_dataframe = kp['SEP'].loc[:,[param_dict['Electron Flux FOV 1 F'],param_dict['Electron Flux FOV 1 R'],param_dict['Electron Flux FOV 2 F'],param_dict['Electron Flux FOV 2 R']]].fillna(0)
            sep_electron_dataframe['Sum'] = sep_electron_dataframe[param_dict['Electron Flux FOV 1 F']] + sep_electron_dataframe[param_dict['Electron Flux FOV 1 R']] + sep_electron_dataframe[param_dict['Electron Flux FOV 2 F']] + sep_electron_dataframe[param_dict['Electron Flux FOV 2 R']]
            pytplot.store_data(title, data={'x':kp['Time'], 'y':sep_electron_dataframe})
            pytplot.options(title,'legend_names',['Electron Flux FOV 1 F','Electron Flux FOV 1 R','Electron Flux FOV 2 F','Electron Flux FOV 2 R', 'Sum'])
            names_to_plot.append(title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("SEP is not in the Key Parameter Data Structure, " + title + " will not be plotted")
        
    if wave:
        title = "E-Field"
        try:
            if 'LPW' not in kp.keys():
                raise Exception("NoDataException") 
        
            wave_dataframe = kp['LPW'].loc[:,[param_dict['E-field Power 2-100 Hz'],param_dict['E-field Power 100-800 Hz'],param_dict['E-field Power 0.8-1.0 Mhz']]]
            wave_dataframe['RMS Deviation'] = kp['MAG'].loc[:,[param_dict['Magnetic Field RMS Dev']]]
            
            #Whenever we do a log plot, the plotting routine stops if a column is full of NaNs.  So we need to check for 
            #this prior to plotting them.  For the record, Tplot just ignores all NaN data and doesn't plot it. 
            
            #for KP in wave_dataframe.columns.values:
            #    if (len(wave_dataframe[KP][wave_dataframe[KP].apply(math.isnan)]) == len(wave_dataframe[KP])):
            #        print(KP + " has no finite values and will not be plotted.")
            #        wave_dataframe = wave_dataframe.drop(KP, 1)
            
            
            pytplot.store_data(title, data={'x':kp['Time'], 'y':wave_dataframe})
            pytplot.options(title,'legend_names',['E-field Power 2-100 Hz','E-field Power 100-800 Hz','E-field Power 0.8-1.0 Mhz','RMS Deviation'])
            pytplot.options(title,'ylog',1)
            names_to_plot.append(title)
            current_plot_number = current_plot_number + 1
        
        except Exception as x:
            if str(x) == "NoDataException":
                print("LPW is not in the Key Parameter Data Structure, " + title + " will not be plotted")
        
    if plasma_den:
        title = "Plasma Density"
        try:
            if 'SWIA' not in kp.keys() or 'STATIC' not in kp.keys() or 'LPW' not in kp.keys() or 'SWEA' not in kp.keys():
                raise Exception("NoDataException")
            plasma_den_dataframe = kp['STATIC'].loc[:,[param_dict['H+ Density'],param_dict['O+ Density'],param_dict['O2+ Density']]]
            plasma_den_dataframe['SWIA H+ Density'] = kp['SWIA'].loc[:,[param_dict['H+ Density']]]
            plasma_den_dataframe['Solar Wind Electron Density'] = kp['SWEA'].loc[:,[param_dict['Solar Wind Electron Density']]]
            plasma_den_dataframe['Electron Density'] = kp['LPW'].loc[:,param_dict[['Electron Density']]]
            
            #Whenever we do a log plot, the plotting routine stops if a column is full of NaNs.  So we need to check for 
            #this prior to plotting them.  For the record, Tplot just ignores all NaN data and doesn't plot it. 
            
            #for KP in plasma_den_dataframe.columns.values:
            #    if (len(plasma_den_dataframe[KP][plasma_den_dataframe[KP].apply(math.isnan)]) == len(plasma_den_dataframe[KP])):
            #        print(KP + " has no finite values and will not be plotted.")
            #        plasma_den_dataframe = plasma_den_dataframe.drop(KP, 1)
            
            pytplot.store_data(title, data={'x':kp['Time'], 'y':plasma_den_dataframe})
            pytplot.options(title,'legend_names',['H+ Density','O+ Density','O2+ Density','SWIA H+ Density', 'Solar Wind Electron Density','Electron Density'])
            pytplot.options(title,'ylog',1)
            names_to_plot.append(title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("One or all of SWIA/STATIC/LPW/SWEA are not in the Key Parameter Data Structure, " + title + " will not be plotted")
         
    if plasma_temp:
        title = "Plasma Temperature"
        try:
            if 'SWIA' not in kp.keys() or 'STATIC' not in kp.keys() or 'LPW' not in kp.keys() or 'SWEA' not in kp.keys():
                raise Exception("NoDataException")
            plasma_temp_dataframe = kp['STATIC'].loc[:,[param_dict['H+ Temperature'],param_dict['O+ Temperature'],param_dict['O2+ Temperature']]]
            plasma_temp_dataframe['SWIA H+ Temperature'] = kp['SWIA'].loc[:,[param_dict['H+ Temperature']]]
            plasma_temp_dataframe['Solar Wind Electron Temperature'] = kp['SWEA'].loc[:,[param_dict['Solar Wind Electron Temperature']]]
            plasma_temp_dataframe['Electron Temperature'] = kp['LPW'].loc[:,[param_dict['Electron Temperature']]]
            
            #Whenever we do a log plot, the plotting routine stops if a column is full of NaNs.  So we need to check for 
            #this prior to plotting them.  For the record, Tplot just ignores all NaN data and doesn't plot it.    
            
            #for KP in plasma_temp_dataframe.columns.values:
            #    if (len(plasma_temp_dataframe[KP][plasma_temp_dataframe[KP].apply(math.isnan)]) == len(plasma_temp_dataframe[KP])):
            #        print(KP + " has no finite values and will not be plotted.")
            #        plasma_temp_dataframe = plasma_temp_dataframe.drop(KP, 1)
            
            pytplot.store_data(title, data={'x':kp['Time'], 'y':plasma_temp_dataframe})
            pytplot.options(title,'legend_names',['H+ Temperature','O+ Temperature','O2+ Temperature', 'SWIA H+ Temperature','Solar Wind Electron Temperature','Electron Temperature'])
            pytplot.options(title,'ylog',1)
            names_to_plot.append(title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("One or all of SWIA/STATIC/LPW/SWEA are not in the Key Parameter Data Structure, " + title + " will not be plotted")
        
    if swia_h_vel:
        title = "SWIA H+ Velocity"
        try:
            if 'SWIA' not in kp.keys():
                raise Exception("NoDataException")
            swia_h_vel_dataframe = kp['SWIA'].loc[:,[param_dict['H+ Flow Velocity MSO X'], param_dict['H+ Flow Velocity MSO Y'], param_dict['H+ Flow Velocity MSO Z']]]
            swia_h_vel_dataframe['Magnitude'] = ((kp['SWIA'][param_dict['H+ Flow Velocity MSO X']]*kp['SWIA'][param_dict['H+ Flow Velocity MSO X']]) + (kp['SWIA'][param_dict['H+ Flow Velocity MSO Y']]*kp['SWIA'][param_dict['H+ Flow Velocity MSO Y']]) + (kp['SWIA'][param_dict['H+ Flow Velocity MSO Z']]*kp['SWIA'][param_dict['H+ Flow Velocity MSO Z']])).apply(math.sqrt) 
            pytplot.store_data(title, data={'x':kp['Time'], 'y':swia_h_vel_dataframe})
            pytplot.options(title,'legend_names',['H+ Flow Velocity MSO X', 'H+ Flow Velocity MSO Y', 'H+ Flow Velocity MSO Z', 'Magnitude'])
            names_to_plot.append(title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("SWIA is not in the Key Parameter Data Structure, " + title + " will not be plotted")
        
    if static_h_vel:
        title = "STATIC H+ Velocity"
        try:
            if 'STATIC' not in kp.keys():
                raise Exception("NoDataException")
            #This is more like a direction, not a velocity.  The values are between 0 and 1.  
            
            static_h_vel_dataframe = kp['STATIC'].loc[:,[param_dict['H+ Direction MSO X'], param_dict['H+ Direction MSO Y'], param_dict['H+ Direction MSO Z']]]
            static_h_vel_dataframe['Magnitude'] = ((kp['STATIC'][param_dict['H+ Direction MSO X']]*kp['STATIC'][param_dict['H+ Direction MSO X']]) + (kp['STATIC'][param_dict['H+ Direction MSO Y']]*kp['STATIC'][param_dict['H+ Direction MSO Y']]) + (kp['STATIC'][param_dict['H+ Direction MSO Z']]*kp['STATIC'][param_dict['H+ Direction MSO Z']])).apply(math.sqrt) 
            pytplot.store_data(title, data={'x':kp['Time'], 'y':static_h_vel_dataframe})
            pytplot.options(title,'legend_names',['H+ Direction MSO X', 'H+ Direction MSO Y', 'H+ Direction MSO Z', 'Magnitude'])
            names_to_plot.append(title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("STATIC is not in the Key Parameter Data Structure, " + title + " will not be plotted")
        
    if static_o2_vel:  
        title = "STATIC O2+ Velocity"
        try:
            if 'STATIC' not in kp.keys():
                raise Exception("NoDataException")
            static_o2_vel_dataframe = kp['STATIC'].loc[:,[param_dict['O2+ Flow Velocity MSO X'], param_dict['O2+ Flow Velocity MSO Y'], param_dict['O2+ Flow Velocity MSO Z']]]
            static_o2_vel_dataframe['Magnitude'] = ((kp['STATIC'][param_dict['O2+ Flow Velocity MSO X']]*kp['STATIC'][param_dict['O2+ Flow Velocity MSO X']]) + (kp['STATIC'][param_dict['O2+ Flow Velocity MSO Y']]*kp['STATIC'][param_dict['O2+ Flow Velocity MSO Y']]) + (kp['STATIC'][param_dict['O2+ Flow Velocity MSO Z']]*kp['STATIC'][param_dict['O2+ Flow Velocity MSO Z']])).apply(math.sqrt) 
            pytplot.store_data(title, data={'x':kp['Time'], 'y':static_o2_vel_dataframe})
            pytplot.options(title,'legend_names',['O2+ Flow Velocity MSO X', 'O2+ Flow Velocity MSO Y', 'O2+ Flow Velocity MSO Z', 'Magnitude'])
            names_to_plot.append(title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("STATIC is not in the Key Parameter Data Structure, " + title + " will not be plotted")
        
    if static_flux:
        title = "STATIC Flux"
        try:
            if 'STATIC' not in kp.keys():
                raise Exception("NoDataException")
            
            
            
            #In the IDL Toolkit, it only plots O2PLUS_FLOW_VELOCITY_MSO_X/Y.  I'm assuming this is incorrect.
            # I have no idea what the right values to plot are.  
            
            
            
            
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("STATIC is not in the Key Parameter Data Structure, " + title + " will not be plotted")
        
    if static_energy:
        title = "STATIC Characteristic Energies"
        try:
            if 'STATIC' not in kp.keys():
                raise Exception("NoDataException")
            sta_char_eng_dataframe = kp['STATIC'].loc[:,[param_dict['H+ Energy'], param_dict['He++ Energy'], param_dict['O+ Energy'], param_dict['O2+ Energy']]]
            pytplot.store_data(title, data={'x':kp['Time'], 'y':sta_char_eng_dataframe})
            pytplot.options(title,'legend_names',['H+ Energy', 'He++ Energy', 'O+ Energy', 'O2+ Energy'])
            pytplot.options(title,'ylog',1)
            names_to_plot.append(title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("STATIC is not in the Key Parameter Data Structure, " + title + " will not be plotted")
        
    if sun_bar:
        title = "Sunbar"
        try:
            if 'SPACECRAFT' not in kp.keys():
                raise Exception("NoDataException")
            #Shows whether or not MAVEN is in the sun
            #1 if True
            #0 if False
            
            #Could there be a more efficient way of doing this?
            radius_mars = 3396.0 
            sun_bar_series = ((kp['SPACECRAFT']['MSO_Y']*kp['SPACECRAFT']['MSO_Y']) + (kp['SPACECRAFT']['MSO_Z']*kp['SPACECRAFT']['MSO_Z'])).apply(math.sqrt)
            sun_bar_series.name = "Sunlit/Eclipsed"
            index = 0
            for mso_x in kp['SPACECRAFT']['MSO_X']:
                if mso_x < 0:
                    if sun_bar_series[index] < radius_mars:
                        sun_bar_series[index] = 0
                    else: 
                        sun_bar_series[index] = 1
                else:
                    sun_bar_series[index] = 1
                index = index+1
                    
            pytplot.store_data(title, data={'x':kp['Time'], 'y':sun_bar_series})
            pytplot.ylim(title, -0.1,1.1)
            #pytplot.options(title,'legend_names',)
            names_to_plot.append(title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("SPACECRAFT is not in the Key Parameter Data Structure, " + title + " will not be plotted")
        
    if solar_wind:
        title = "Solar Wind"
        try:
            if 'SWIA' not in kp.keys():
                raise Exception("NoDataException")
            #Whenever we do a log plot, the plotting routine stops if a column is full of NaNs.  So we need to check for 
            #this prior to plotting them.  For the record, Tplot just ignores all NaN data and doesn't plot it.    
            solar_wind_dataframe = kp['SWIA'].loc[:,[param_dict['Solar Wind Dynamic Pressure']]]
            #for KP in solar_wind_dataframe.columns.values:
            #    if (len(solar_wind_dataframe[KP][solar_wind_dataframe[KP].apply(math.isnan)]) == len(solar_wind_dataframe[KP])):
            #        print(KP + " has no finite values and will not be plotted.")
            #        solar_wind_dataframe = solar_wind_dataframe.drop(KP, 1)
            
            pytplot.store_data(title, data={'x':kp['Time'], 'y':solar_wind_dataframe})
            pytplot.options(title,'ylog',1)
            names_to_plot.append(title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("SWIA is not in the Key Parameter Data Structure, " + title + " will not be plotted")
        
    if ionosphere:
        title = "Ionosphere"
        try:
            if 'SWEA' not in kp.keys():
                raise Exception("NoDataException")
            #Need to convert to float first, not sure why it is not already
            ionosphere_dataframe = kp['SWEA'].loc[:,[param_dict['Electron Spectrum Shape']]]
            ionosphere_dataframe['Electron Spectrum Shape'] = ionosphere_dataframe[param_dict['Electron Spectrum Shape']].apply(float)
            #Whenever we do a log plot, the plotting routine stops if a column is full of NaNs.  So we need to check for 
            #this prior to plotting them.  For the record, Tplot just ignores all NaN data and doesn't plot it.    
            
            
            #if (len(ionosphere_dataframe['Electron Spectrum Shape'][ionosphere_dataframe['Electron Spectrum Shape'].apply(float).apply(math.isnan)]) == len(ionosphere_dataframe['Electron Spectrum Shape'])):
            #    print("Electron Spectrum Shape" + " has no finite values and will not be plotted.")
            #    ionosphere_dataframe = ionosphere_dataframe.drop(KP, 1)
            
            pytplot.store_data(title, data={'x':kp['Time'], 'y':ionosphere_dataframe})
            pytplot.options(title,'ylog',1)
            names_to_plot.append(title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("SWEA is not in the Key Parameter Data Structure, " + title + " will not be plotted")
        
    if sc_pot:
        title = "Spacecraft Potential"
        try:
            if 'LPW' not in kp.keys():
                raise Exception("NoDataException")
            sc_pot_dataframe = kp['LPW'].loc[:,[param_dict['Spacecraft Potential']]]
            pytplot.store_data(title, data={'x':kp['Time'], 'y':sc_pot_dataframe})
            #pytplot.options('MAG Direction','legend_names',['Radial','Eastward','Northward'])
            names_to_plot.append(title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("LPW is not in the Key Parameter Data Structure, " + title + " will not be plotted")
                
                
    if altitude:
        title = "Spacecraft Altitude"
        try:
            altitude_dataframe = kp['SPACECRAFT'].loc[:,['ALTITUDE']]
            pytplot.store_data(title, data={'x':kp['Time'], 'y':altitude_dataframe})
            #pytplot.options('MAG Direction','legend_names',['Radial','Eastward','Northward'])
            names_to_plot.append(title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("LPW is not in the Key Parameter Data Structure, " + title + " will not be plotted")
    
    #Show the plot
    pytplot.tplot_options('wsize', [1000,300*(current_plot_number)])
    pytplot.tplot_options('title', title)
    pytplot.tplot(names_to_plot, qt=qt)
    pytplot.del_data(names_to_plot)
    
    return