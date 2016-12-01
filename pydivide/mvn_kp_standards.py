import math
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
import pytplot

def mvn_kp_standards(kp, 
                     list_plots=False,
                     all=False,
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
                     plot_title=None,
                     plot_color=None):
    
    if all:
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
    
    
    if (list == True):
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

    fig = plt.figure()
    fig.patch.set_facecolor('white')
    plot_array = []
    for i in range(max_num_plots):
        plot_array.append(fig.add_subplot(max_num_plots,1,i+1))
        box = plot_array[i].get_position()
        plot_array[i].set_position([.05, box.y0, box.width , box.height])

    #Font size for the legends
    fontP = FontProperties()
    fontP.set_size('medium')
    
    #The number plot we're plotting in the figure
    current_plot_number = 0
    names_to_plot=[]
    if euv:
        title = "EUV"
        try:
            if 'EUV' not in kp.keys():
                raise Exception("NoDataException")
            euv_dataframe = kp['EUV'].loc[:,['EUV Irradiance Lyman-alpha','EUV Irradiance 17-22 nm', 'EUV Irradiance 0.1-7.0 nm']]
            euv_dataframe.plot(kind='line', use_index=True, ax = plot_array[current_plot_number], title=title)
            pytplot.store_data('EUV', data={'x':kp['Time'], 'y':euv_dataframe})
            pytplot.options('EUV','legend_names',['EUV Irradiance Lyman-alpha','EUV Irradiance 17-22 nm', 'EUV Irradiance 0.1-7.0 nm'])
            names_to_plot.append('EUV')
            current_plot_number = current_plot_number + 1
            current_plot_number = current_plot_number + 1
            
        except Exception as x:
            if str(x) == "NoDataException":
                print("EUV is not in the Key Parameter Data Structure, " + title + " will not be plotted")
        
    if mag_mso:
        title = "MAG MSO"
        try:
            if 'MAG' not in kp.keys():
                raise Exception("NoDataException")
            
            mag_mso_dataframe = kp['MAG'].loc[:,['Magnetic Field MSO X','Magnetic Field MSO Y', 'Magnetic Field MSO Z']]
            mag_mso_dataframe['Magnetic Field Magnitude MSO'] = ((kp['MAG']['Magnetic Field MSO X']*kp['MAG']['Magnetic Field MSO X']) + (kp['MAG']['Magnetic Field MSO Y']*kp['MAG']['Magnetic Field MSO Y']) + (kp['MAG']['Magnetic Field MSO Z']*kp['MAG']['Magnetic Field MSO Z'])).apply(math.sqrt)
            mag_mso_dataframe.plot(kind='line', use_index=True, ax = plot_array[current_plot_number], title=title)
            pytplot.store_data('MAG MSO', data={'x':kp['Time'], 'y':mag_mso_dataframe})
            pytplot.options('MAG MSO','legend_names',['Magnetic Field MSO X','Magnetic Field MSO Y', 'Magnetic Field MSO Z', 'Magnetic Field Magnitude MSO'])
            names_to_plot.append('MAG MSO')
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("MAG is not in the Key Parameter Data Structure, " + title + " will not be plotted")

    if mag_geo:
        title = "MAG GEO"
        try:
            if 'MAG' not in kp.keys():
                raise Exception("NoDataException")
            mag_geo_dataframe = kp['MAG'].loc[:,['Magnetic Field GEO X','Magnetic Field GEO Y', 'Magnetic Field GEO Z']]
            mag_geo_dataframe['Magnetic Field Magnitude GEO'] = ((kp['MAG']['Magnetic Field GEO X']*kp['MAG']['Magnetic Field GEO X']) + (kp['MAG']['Magnetic Field GEO Y']*kp['MAG']['Magnetic Field GEO Y']) + (kp['MAG']['Magnetic Field GEO Z']*kp['MAG']['Magnetic Field GEO Z'])).apply(math.sqrt)
            mag_geo_dataframe.plot(kind='line', use_index=True, ax = plot_array[current_plot_number], title=title)
            pytplot.store_data('MAG GEO', data={'x':kp['Time'], 'y':mag_geo_dataframe})
            pytplot.options('MAG GEO','legend_names',['Magnetic Field GEO X','Magnetic Field GEO Y', 'Magnetic Field GEO Z', 'Magnetic Field Magnitude GEO'])
            names_to_plot.append('MAG GEO')
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
            mag_cone_dataframe_temp = kp['MAG'].loc[:,['Magnetic Field MSO X','Magnetic Field MSO Y', 'Magnetic Field MSO Z']]
            mag_cone_dataframe_temp['Clock Angle'] = (mag_cone_dataframe_temp['Magnetic Field MSO X'] / mag_cone_dataframe_temp['Magnetic Field MSO Y']).apply(math.atan) * 57.295776
            mag_cone_dataframe_temp['Cone Angle'] = ((mag_cone_dataframe_temp['Magnetic Field MSO X'].apply(abs)) / (((kp['MAG']['Magnetic Field MSO X']*kp['MAG']['Magnetic Field MSO X']) + (kp['MAG']['Magnetic Field MSO Y']*kp['MAG']['Magnetic Field MSO Y']) + (kp['MAG']['Magnetic Field MSO Z']*kp['MAG']['Magnetic Field MSO Z'])).apply(math.sqrt))).apply(math.acos) * 57.295776
            mag_cone_dataframe = mag_cone_dataframe_temp.loc[:,['Clock Angle','Cone Angle']]
            mag_cone_dataframe.plot(kind='line', use_index=True, ax = plot_array[current_plot_number], title=title)
            pytplot.store_data('MAG Cone', data={'x':kp['Time'], 'y':mag_cone_dataframe})
            pytplot.options('MAG Cone','legend_names',['Magnetic Clock Angle','Magnetic Cone Angle'])
            names_to_plot.append('MAG Cone')
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("MAG is not in the Key Parameter Data Structure, " + title + " will not be plotted")
        
    if mag_dir:
        title = "MAG Direction"
        try:
            if 'MAG' not in kp.keys():
                raise Exception("NoDataException")
            clat = (kp['SPACECRAFT']['GEO Latitude'] * 3.14159265/180).apply(math.cos)
            slat = (kp['SPACECRAFT']['GEO Latitude'] * 3.14159265/180).apply(math.sin)
            clon = (kp['SPACECRAFT']['GEO Longitude'] * 3.14159265/180).apply(math.cos)
            slon = (kp['SPACECRAFT']['GEO Longitude'] * 3.14159265/180).apply(math.sin)
            
            mag_rad_series = (kp['MAG']['Magnetic Field GEO X'] * clon * clat) + (kp['MAG']['Magnetic Field GEO Y'] * slon * clat) + (kp['MAG']['Magnetic Field GEO Z'] * slat)
            mag_dir_dataframe = mag_rad_series.to_frame(name='Radial')
            mag_dir_dataframe['Eastward'] = (kp['MAG']['Magnetic Field GEO X'] * slon * -1) + (kp['MAG']['Magnetic Field GEO Y'] * clon)
            mag_dir_dataframe['Northward'] = (kp['MAG']['Magnetic Field GEO X'] * clon * slat * -1) + (kp['MAG']['Magnetic Field GEO Y'] * slon * slat * -1) + (kp['MAG']['Magnetic Field GEO Z'] * clat)
            mag_dir_dataframe.plot(kind='line', use_index=True, ax = plot_array[current_plot_number], title=title)
            pytplot.store_data('MAG Direction', data={'x':kp['Time'], 'y':mag_dir_dataframe})
            pytplot.options('MAG Direction','legend_names',['Radial','Eastward','Northward'])
            names_to_plot.append('MAG Direction')
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("MAG is not in the Key Parameter Data Structure, " + title + " will not be plotted")
    
    if ngims_neutral:
        title = "NGIMS Neutrals"
        try:
            if 'NGIMS' not in kp.keys():
                raise Exception("NoDataException")
            kp['NGIMS'].loc[:,['Density He', 'Density O', 'Density CO', 'Density N2', 'Density NO', 'Density AR', 'Density C02']].plot(kind='line', use_index=True, logy=True, ax = plot_array[current_plot_number], title=title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("NGIMS is not in the Key Parameter Data Structure, " + title + " will not be plotted")
        
    if ngims_ions:
        title = "NGIMS IONS"
        try:
            if 'NGIMS' not in kp.keys():
                raise Exception("NoDataException")
            kp['NGIMS'].loc[:,['Density 32+', 'Density 44+', 'Density 30+', 'Density 16+', 'Density 28+', 'Density 12+', 'Density 17+', 'Density 14+']].plot(kind='line', use_index=True, logy=True, ax = plot_array[current_plot_number], title=title)
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
            kp['SPACECRAFT'].loc[:,['GEO Longitude', 'GEO Latitude', 'Solar Zenith Angle', 'Local Time', 'Mars Season (Ls)', 'Subsolar Point GEO Longitude', 'Subsolar Point GEO Latitude']].plot(kind='line', use_index=True, ax = plot_array[current_plot_number], title=title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("SPACECRAFT is not in the Key Parameter Data Structure, " + title + " will not be plotted")
        
    if eph_geo:
        title = "Spacecraft positon in GEO Coordinates"
        try:
            if 'SPACECRAFT' not in kp.keys():
                raise Exception("NoDataException")
            kp['SPACECRAFT'].loc[:,['GEO X', 'GEO Y', 'GEO Z', 'Altitude Aeroid']].plot(kind='line', use_index=True, ax = plot_array[current_plot_number], title=title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("SPACECRAFT is not in the Key Parameter Data Structure, " + title + " will not be plotted")
        
    if eph_mso:
        title = "Spacecraft positon in MSO Coordinates"
        try:
            if 'SPACECRAFT' not in kp.keys():
                raise Exception("NoDataException")
            kp['SPACECRAFT'].loc[:,['MSO X', 'MSO Y', 'MSO Z', 'Altitude Aeroid']].plot(kind='line', use_index=True, ax = plot_array[current_plot_number], title=title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("LPW is not in the Key Parameter Data Structure, " + title + " will not be plotted")
        
    if swea:
        title = "SWEA"
        try:
            if 'SWEA' not in kp.keys():
                raise Exception("NoDataException")
            kp['SWEA'].loc[:,['Flux, e- Parallel (5-100 ev)', 'Flux, e- Parallel (100-500 ev)', 'Flux, e- Parallel (500-1000 ev)', 'Flux, e- Anti-par (5-100 ev)', 'Flux, e- Anti-par (100-500 ev)', 'Flux, e- Anti-par (500-1000 ev)', 'Electron Spectrum Shape']].plot(kind='line', use_index=True, ax = plot_array[current_plot_number], title=title)
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
            sep_ion_dataframe = kp['SEP'].loc[:,['Ion Flux FOV 1 F','Ion Flux FOV 1 R','Ion Flux FOV 2 F','Ion Flux FOV 2 R']].fillna(0)
            sep_ion_dataframe['Sum'] = sep_ion_dataframe['Ion Flux FOV 1 F'] + sep_ion_dataframe['Ion Flux FOV 1 R'] + sep_ion_dataframe['Ion Flux FOV 2 F'] + sep_ion_dataframe['Ion Flux FOV 2 R']
            sep_ion_dataframe.plot(kind='line', use_index=True, ax = plot_array[current_plot_number], title=title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("SEP is not in the Key Parameter Data Structure, " + title + " will not be plotted")
        
    if sep_electron:
        title = "SEP Electrons"
        try:
            if 'SEP' not in kp.keys():
                raise Exception("NoDataException")
            sep_electron_dataframe = kp['SEP'].loc[:,['Electron Flux FOV 1 F','Electron Flux FOV 1 R','Electron Flux FOV 2 F','Electron Flux FOV 2 R']].fillna(0)
            sep_electron_dataframe['Sum'] = sep_electron_dataframe['Electron Flux FOV 1 F'] + sep_electron_dataframe['Electron Flux FOV 1 R'] + sep_electron_dataframe['Electron Flux FOV 2 F'] + sep_electron_dataframe['Electron Flux FOV 2 R']
            sep_electron_dataframe.plot(kind='line', use_index=True, ax = plot_array[current_plot_number], title=title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("SEP is not in the Key Parameter Data Structure, " + title + " will not be plotted")
        
    if wave:
        title = "E-Field"
        try:
            if 'LPW' not in kp.keys():
                raise Exception("NoDataException") 
        
            wave_dataframe = kp['LPW'].loc[:,['E-field Power 2-100 Hz','E-field Power 100-800 Hz','E-field Power 0.8-1.0 Mhz']]
            wave_dataframe['RMS Deviation'] = kp['MAG'].loc[:,['Magnetic Field RMS Dev']]
            
            #Whenever we do a log plot, the plotting routine stops if a column is full of NaNs.  So we need to check for 
            #this prior to plotting them.  For the record, Tplot just ignores all NaN data and doesn't plot it. 
            
            for KP in wave_dataframe.columns.values:
                if (len(wave_dataframe[KP][wave_dataframe[KP].apply(math.isnan)]) == len(wave_dataframe[KP])):
                    print(KP + " has no finite values and will not be plotted.")
                    wave_dataframe = wave_dataframe.drop(KP, 1)
            
            
            wave_dataframe.plot(kind='line', use_index=True, logy=True, ax = plot_array[current_plot_number], title=title)
            current_plot_number = current_plot_number + 1
        
        except Exception as x:
            if str(x) == "NoDataException":
                print("LPW is not in the Key Parameter Data Structure, " + title + " will not be plotted")
        
    if plasma_den:
        title = "Plasma Density"
        try:
            if 'SWIA' not in kp.keys() or 'STATIC' not in kp.keys() or 'LPW' not in kp.keys() or 'SWEA' not in kp.keys():
                raise Exception("NoDataException")
            plasma_den_dataframe = kp['STATIC'].loc[:,['H+ Density','O+ Density','O2+ Density']]
            plasma_den_dataframe['SWIA H+ Density'] = kp['SWIA'].loc[:,['H+ Density']]
            plasma_den_dataframe['Solar Wind Electron Density'] = kp['SWEA'].loc[:,['Solar Wind Electron Density']]
            plasma_den_dataframe['Electron Density'] = kp['LPW'].loc[:,['Electron Density']]
            
            #Whenever we do a log plot, the plotting routine stops if a column is full of NaNs.  So we need to check for 
            #this prior to plotting them.  For the record, Tplot just ignores all NaN data and doesn't plot it. 
            
            for KP in plasma_den_dataframe.columns.values:
                if (len(plasma_den_dataframe[KP][plasma_den_dataframe[KP].apply(math.isnan)]) == len(plasma_den_dataframe[KP])):
                    print(KP + " has no finite values and will not be plotted.")
                    plasma_den_dataframe = plasma_den_dataframe.drop(KP, 1)
            
            plasma_den_dataframe.plot(kind='line', use_index=True, logy=True, ax = plot_array[current_plot_number], title=title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("One or all of SWIA/STATIC/LPW/SWEA are not in the Key Parameter Data Structure, " + title + " will not be plotted")
         
    if plasma_temp:
        title = "Plasma Temperature"
        try:
            if 'SWIA' not in kp.keys() or 'STATIC' not in kp.keys() or 'LPW' not in kp.keys() or 'SWEA' not in kp.keys():
                raise Exception("NoDataException")
            plasma_temp_dataframe = kp['STATIC'].loc[:,['H+ Temperature','O+ Temperature','O2+ Temperature']]
            plasma_temp_dataframe['SWIA H+ Temperature'] = kp['SWIA'].loc[:,['H+ Temperature']]
            plasma_temp_dataframe['Solar Wind Electron Temperature'] = kp['SWEA'].loc[:,['Solar Wind Electron Temperature']]
            plasma_temp_dataframe['Electron Temperature'] = kp['LPW'].loc[:,['Electron Temperature']]
            
            #Whenever we do a log plot, the plotting routine stops if a column is full of NaNs.  So we need to check for 
            #this prior to plotting them.  For the record, Tplot just ignores all NaN data and doesn't plot it.    
            
            for KP in plasma_temp_dataframe.columns.values:
                if (len(plasma_temp_dataframe[KP][plasma_temp_dataframe[KP].apply(math.isnan)]) == len(plasma_temp_dataframe[KP])):
                    print(KP + " has no finite values and will not be plotted.")
                    plasma_temp_dataframe = plasma_temp_dataframe.drop(KP, 1)
            
            plasma_temp_dataframe.plot(kind='line', use_index=True, logy=True, ax = plot_array[current_plot_number], title=title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("One or all of SWIA/STATIC/LPW/SWEA are not in the Key Parameter Data Structure, " + title + " will not be plotted")
        
    if swia_h_vel:
        title = "SWIA H+ Velocity"
        try:
            if 'SWIA' not in kp.keys():
                raise Exception("NoDataException")
            swia_h_vel_dataframe = kp['SWIA'].loc[:,['H+ Flow Velocity MSO X', 'H+ Flow Velocity MSO Y', 'H+ Flow Velocity MSO Z']]
            swia_h_vel_dataframe['Magnitude'] = ((kp['SWIA']['H+ Flow Velocity MSO X']*kp['SWIA']['H+ Flow Velocity MSO X']) + (kp['SWIA']['H+ Flow Velocity MSO Y']*kp['SWIA']['H+ Flow Velocity MSO Y']) + (kp['SWIA']['H+ Flow Velocity MSO Z']*kp['SWIA']['H+ Flow Velocity MSO Z'])).apply(math.sqrt) 
            swia_h_vel_dataframe.plot(kind='line', use_index=True, ax = plot_array[current_plot_number], title=title)
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
            
            static_h_vel_dataframe = kp['STATIC'].loc[:,['H+ Direction MSO X', 'H+ Direction MSO Y', 'H+ Direction MSO Z']]
            static_h_vel_dataframe['Magnitude'] = ((kp['STATIC']['H+ Direction MSO X']*kp['STATIC']['H+ Direction MSO X']) + (kp['STATIC']['H+ Direction MSO Y']*kp['STATIC']['H+ Direction MSO Y']) + (kp['STATIC']['H+ Direction MSO Z']*kp['STATIC']['H+ Direction MSO Z'])).apply(math.sqrt) 
            static_h_vel_dataframe.plot(kind='line', use_index=True, ax = plot_array[current_plot_number], title=title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("STATIC is not in the Key Parameter Data Structure, " + title + " will not be plotted")
        
    if static_o2_vel:  
        title = "STATIC O2+ Velocity"
        try:
            if 'STATIC' not in kp.keys():
                raise Exception("NoDataException")
            static_o2_vel_dataframe = kp['STATIC'].loc[:,['O2+ Flow Velocity MSO X', 'O2+ Flow Velocity MSO Y', 'O2+ Flow Velocity MSO Z']]
            static_o2_vel_dataframe['Magnitude'] = ((kp['STATIC']['O2+ Flow Velocity MSO X']*kp['STATIC']['O2+ Flow Velocity MSO X']) + (kp['STATIC']['O2+ Flow Velocity MSO Y']*kp['STATIC']['O2+ Flow Velocity MSO Y']) + (kp['STATIC']['O2+ Flow Velocity MSO Z']*kp['STATIC']['O2+ Flow Velocity MSO Z'])).apply(math.sqrt) 
            static_o2_vel_dataframe.plot(kind='line', use_index=True, ax = plot_array[current_plot_number], title=title)
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
            kp['STATIC'].loc[:,['H+ Energy', 'He++ Energy', 'O+ Energy', 'O2+ Energy']].plot(kind='line', use_index=True, logy=True, ax = plot_array[current_plot_number], title=title)
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
            sun_bar_series = ((kp['SPACECRAFT']['MSO Y']*kp['SPACECRAFT']['MSO Y']) + (kp['SPACECRAFT']['MSO Z']*kp['SPACECRAFT']['MSO Z'])).apply(math.sqrt)
            sun_bar_series.name = "Sunlit/Eclipsed"
            index = 0
            for mso_x in kp['SPACECRAFT']['MSO X']:
                if mso_x < 0:
                    if sun_bar_series[index] < radius_mars:
                        sun_bar_series[index] = 0
                    else: 
                        sun_bar_series[index] = 1
                else:
                    sun_bar_series[index] = 1
                index = index+1
                    
            sun_bar_series.plot(kind='line', use_index=True, ylim=[-0.1,1.1], ax = plot_array[current_plot_number], title=title)
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
            solar_wind_dataframe = kp['SWIA'].loc[:,['Solar Wind Dynamic Pressure']]
            for KP in solar_wind_dataframe.columns.values:
                if (len(solar_wind_dataframe[KP][solar_wind_dataframe[KP].apply(math.isnan)]) == len(solar_wind_dataframe[KP])):
                    print(KP + " has no finite values and will not be plotted.")
                    solar_wind_dataframe = solar_wind_dataframe.drop(KP, 1)
            
            
            solar_wind_dataframe.plot(kind='line', use_index=True, logy=True, ax = plot_array[current_plot_number], title=title)
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
            ionosphere_dataframe = kp['SWEA'].loc[:,['Electron Spectrum Shape']]
            ionosphere_dataframe['Electron Spectrum Shape'] = ionosphere_dataframe['Electron Spectrum Shape'].apply(float)
            #Whenever we do a log plot, the plotting routine stops if a column is full of NaNs.  So we need to check for 
            #this prior to plotting them.  For the record, Tplot just ignores all NaN data and doesn't plot it.    
            
            
            if (len(ionosphere_dataframe['Electron Spectrum Shape'][ionosphere_dataframe['Electron Spectrum Shape'].apply(float).apply(math.isnan)]) == len(ionosphere_dataframe['Electron Spectrum Shape'])):
                print("Electron Spectrum Shape" + " has no finite values and will not be plotted.")
                ionosphere_dataframe = ionosphere_dataframe.drop(KP, 1)
            
            
            ionosphere_dataframe.plot(kind='line', use_index=True, logy=True, ax = plot_array[current_plot_number], title=title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("SWEA is not in the Key Parameter Data Structure, " + title + " will not be plotted")
        
    if sc_pot:
        title = "Spacecraft Potential"
        try:
            if 'LPW' not in kp.keys():
                raise Exception("NoDataException")
            kp['LPW'].loc[:,['Spacecraft Potential']].plot(kind='line', use_index=True, ax = plot_array[current_plot_number], title=title)
            current_plot_number = current_plot_number + 1
        except Exception as x:
            if str(x) == "NoDataException":
                print("LPW is not in the Key Parameter Data Structure, " + title + " will not be plotted")
    
    #Adjust the legends to appear on the right side
    for i in range(max_num_plots):
        plot_array[i].legend(loc='center left', bbox_to_anchor=(1, 0.5), prop=fontP)
    #Show the plot
    pytplot.tplot_options('wsize', [1000,200*(current_plot_number)])
    pytplot.tplot(names_to_plot)
    plt.show()