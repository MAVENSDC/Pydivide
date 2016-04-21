import math

def mvn_kp_standards(kp, 
                     list=False,
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
                     plot_color=None,
                     help=False):
    
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
    
    
    if euv:
        kp['EUV'].loc[:,['EUV Irradiance Lyman-alpha','EUV Irradiance 17-22 nm', 'EUV Irradiance 0.1-7.0 nm']].plot(kind='line', use_index=True)
        
        
    if mag_mso:
        mag_mso_dataframe = kp['MAG'].loc[:,['Magnetic Field MSO X','Magnetic Field MSO Y', 'Magnetic Field MSO Z']]
        mag_mso_dataframe['Magnetic Field Magnitude MSO'] = ((kp['MAG']['Magnetic Field MSO X']*kp['MAG']['Magnetic Field MSO X']) + (kp['MAG']['Magnetic Field MSO Y']*kp['MAG']['Magnetic Field MSO Y']) + (kp['MAG']['Magnetic Field MSO Z']*kp['MAG']['Magnetic Field MSO Z'])).apply(math.sqrt)
        mag_mso_dataframe.plot(kind='line', use_index=True)


    if mag_geo:
        mag_geo_dataframe = kp['MAG'].loc[:,['Magnetic Field GEO X','Magnetic Field GEO Y', 'Magnetic Field GEO Z']]
        mag_geo_dataframe['Magnetic Field Magnitude GEO'] = ((kp['MAG']['Magnetic Field GEO X']*kp['MAG']['Magnetic Field GEO X']) + (kp['MAG']['Magnetic Field GEO Y']*kp['MAG']['Magnetic Field GEO Y']) + (kp['MAG']['Magnetic Field GEO Z']*kp['MAG']['Magnetic Field GEO Z'])).apply(math.sqrt)
        mag_geo_dataframe.plot(kind='line', use_index=True)
        
        
    if mag_cone:
        
        #Note, this plot ends up different from the IDL version, because of the way IDL calculates arctans.  Important, or not?
        mag_cone_dataframe = kp['MAG'].loc[:,['Magnetic Field MSO X','Magnetic Field MSO Y', 'Magnetic Field MSO Z']]
        mag_cone_dataframe['Clock Angle'] = (mag_cone_dataframe['Magnetic Field MSO X'] / mag_cone_dataframe['Magnetic Field MSO Y']).apply(math.atan) * 57.295776
        mag_cone_dataframe['Cone Angle'] = ((mag_cone_dataframe['Magnetic Field MSO X'].apply(abs)) / (((kp['MAG']['Magnetic Field MSO X']*kp['MAG']['Magnetic Field MSO X']) + (kp['MAG']['Magnetic Field MSO Y']*kp['MAG']['Magnetic Field MSO Y']) + (kp['MAG']['Magnetic Field MSO Z']*kp['MAG']['Magnetic Field MSO Z'])).apply(math.sqrt))).apply(math.acos) * 57.295776
        mag_cone_dataframe.loc[:,['Clock Angle','Cone Angle']].plot(kind='line', use_index=True)
        
        
    if mag_dir:
        clat = (kp['SPACECRAFT']['GEO Latitude'] * 3.14159265/180).apply(math.cos)
        slat = (kp['SPACECRAFT']['GEO Latitude'] * 3.14159265/180).apply(math.sin)
        clon = (kp['SPACECRAFT']['GEO Longitude'] * 3.14159265/180).apply(math.cos)
        slon = (kp['SPACECRAFT']['GEO Longitude'] * 3.14159265/180).apply(math.sin)
        
        mag_rad_series = (kp['MAG']['Magnetic Field GEO X'] * clon * clat) + (kp['MAG']['Magnetic Field GEO Y'] * slon * clat) + (kp['MAG']['Magnetic Field GEO Z'] * slat)
        mag_dir_dataframe = mag_rad_series.to_frame(name='Radial')
        mag_dir_dataframe['Eastward'] = (kp['MAG']['Magnetic Field GEO X'] * slon * -1) + (kp['MAG']['Magnetic Field GEO Y'] * clon)
        mag_dir_dataframe['Northward'] = (kp['MAG']['Magnetic Field GEO X'] * clon * slat * -1) + (kp['MAG']['Magnetic Field GEO Y'] * slon * slat * -1) + (kp['MAG']['Magnetic Field GEO Z'] * clat)
        mag_dir_dataframe.plot(kind='line', use_index=True)
    
    
    if ngims_neutral:
        kp['NGIMS'].loc[:,['Density He', 'Density O', 'Density CO', 'Density N2', 'Density NO', 'Density AR', 'Density C02']].plot(kind='line', use_index=True, logy=True)
        
        
    if ngims_ions:
        kp['NGIMS'].loc[:,['Density 32+', 'Density 44+', 'Density 30+', 'Density 16+', 'Density 28+', 'Density 12+', 'Density 17+', 'Density 14+']].plot(kind='line', use_index=True, logy=True)
        
        
    if eph_angle:
        #This plot makes no sense.  Why is Local Time plotted here, when it is not a measurement in degrees?  Why is Mars season/Subsolar Latitude plotted when they are essentially straight lines? 
        kp['SPACECRAFT'].loc[:,['GEO Longitude', 'GEO Latitude', 'Solar Zenith Angle', 'Local Time', 'Mars Season (Ls)', 'Subsolar Point GEO Longitude', 'Subsolar Point GEO Latitude']].plot(kind='line', use_index=True)
        
        
    if eph_geo:
        kp['SPACECRAFT'].loc[:,['GEO X', 'GEO Y', 'GEO Z', 'Altitude Aeroid']].plot(kind='line', use_index=True)
        
        
    if eph_mso:
        kp['SPACECRAFT'].loc[:,['MSO X', 'MSO Y', 'MSO Z', 'Altitude Aeroid']].plot(kind='line', use_index=True)
        
        
    if swea:
        kp['SWEA'].loc[:,['Flux, e- Parallel (5-100 ev)', 'Flux, e- Parallel (100-500 ev)', 'Flux, e- Parallel (500-1000 ev)', 'Flux, e- Anti-par (5-100 ev)', 'Flux, e- Anti-par (100-500 ev)', 'Flux, e- Anti-par (500-1000 ev)', 'Electron Spectrum Shape']].plot(kind='line', use_index=True)
        
        
    if sep_ion:
        #Need to fill in the NaNs as zero, otherwise the Sum will equal all Nans
        sep_ion_dataframe = kp['SEP'].loc[:,['Ion Flux FOV 1 F','Ion Flux FOV 1 R','Ion Flux FOV 2 F','Ion Flux FOV 2 R']].fillna(0)
        sep_ion_dataframe['Sum'] = sep_ion_dataframe['Ion Flux FOV 1 F'] + sep_ion_dataframe['Ion Flux FOV 1 R'] + sep_ion_dataframe['Ion Flux FOV 2 F'] + sep_ion_dataframe['Ion Flux FOV 2 R']
        sep_ion_dataframe.plot(kind='line', use_index=True)
        
        
    if sep_electron:
        sep_electron_dataframe = kp['SEP'].loc[:,['Electron Flux FOV 1 F','Electron Flux FOV 1 R','Electron Flux FOV 2 F','Electron Flux FOV 2 R']].fillna(0)
        sep_electron_dataframe['Sum'] = sep_electron_dataframe['Electron Flux FOV 1 F'] + sep_electron_dataframe['Electron Flux FOV 1 R'] + sep_electron_dataframe['Electron Flux FOV 2 F'] + sep_electron_dataframe['Electron Flux FOV 2 R']
        sep_electron_dataframe.plot(kind='line', use_index=True)
        
        
    if wave:
        wave_dataframe = kp['LPW'].loc[:,['E-field Power 2-100 Hz','E-field Power 100-800 Hz','E-field Power 0.8-1.0 Mhz']]
        wave_dataframe['RMS Deviation'] = kp['MAG'].loc[:,['Magnetic Field RMS Dev']]
        
        #Whenever we do a log plot, the plotting routine stops if a column is full of NaNs.  So we need to check for 
        #this prior to plotting them.  For the record, Tplot just ignores all NaN data and doesn't plot it. 
        
        for KP in wave_dataframe.columns.values:
            if (len(wave_dataframe[KP][wave_dataframe[KP].apply(math.isnan)]) == len(wave_dataframe[KP])):
                print KP + " has no finite values and will not be plotted."
                wave_dataframe = wave_dataframe.drop(KP, 1)
        
        
        wave_dataframe.plot(kind='line', use_index=True, logy=True)
        
        
    if plasma_den:
        plasma_den_dataframe = kp['STATIC'].loc[:,['H+ Density','O+ Density','O2+ Density']]
        plasma_den_dataframe['SWIA H+ Density'] = kp['SWIA'].loc[:,['H+ Density']]
        plasma_den_dataframe['Solar Wind Electron Density'] = kp['SWEA'].loc[:,['Solar Wind Electron Density']]
        plasma_den_dataframe['Electron Density'] = kp['LPW'].loc[:,['Electron Density']]
        
        #Whenever we do a log plot, the plotting routine stops if a column is full of NaNs.  So we need to check for 
        #this prior to plotting them.  For the record, Tplot just ignores all NaN data and doesn't plot it. 
        
        for KP in plasma_den_dataframe.columns.values:
            if (len(plasma_den_dataframe[KP][plasma_den_dataframe[KP].apply(math.isnan)]) == len(plasma_den_dataframe[KP])):
                print KP + " has no finite values and will not be plotted."
                plasma_den_dataframe = plasma_den_dataframe.drop(KP, 1)
        
        plasma_den_dataframe.plot(kind='line', use_index=True, logy=True)
        
         
    if plasma_temp:
        plasma_temp_dataframe = kp['STATIC'].loc[:,['H+ Temperature','O+ Temperature','O2+ Temperature']]
        plasma_temp_dataframe['SWIA H+ Temperature'] = kp['SWIA'].loc[:,['H+ Temperature']]
        plasma_temp_dataframe['Solar Wind Electron Temperature'] = kp['SWEA'].loc[:,['Solar Wind Electron Temperature']]
        plasma_temp_dataframe['Electron Temperature'] = kp['LPW'].loc[:,['Electron Temperature']]
        
        #Whenever we do a log plot, the plotting routine stops if a column is full of NaNs.  So we need to check for 
        #this prior to plotting them.  For the record, Tplot just ignores all NaN data and doesn't plot it.    
        
        for KP in plasma_temp_dataframe.columns.values:
            if (len(plasma_temp_dataframe[KP][plasma_temp_dataframe[KP].apply(math.isnan)]) == len(plasma_temp_dataframe[KP])):
                print KP + " has no finite values and will not be plotted."
                plasma_temp_dataframe = plasma_temp_dataframe.drop(KP, 1)
        
        plasma_temp_dataframe.plot(kind='line', use_index=True, logy=True)
        
        
    if swia_h_vel:
        swia_h_vel_dataframe = kp['SWIA'].loc[:,['H+ Flow Velocity MSO X', 'H+ Flow Velocity MSO Y', 'H+ Flow Velocity MSO Z']]
        swia_h_vel_dataframe['Magnitude'] = ((kp['SWIA']['H+ Flow Velocity MSO X']*kp['SWIA']['H+ Flow Velocity MSO X']) + (kp['SWIA']['H+ Flow Velocity MSO Y']*kp['SWIA']['H+ Flow Velocity MSO Y']) + (kp['SWIA']['H+ Flow Velocity MSO Z']*kp['SWIA']['H+ Flow Velocity MSO Z'])).apply(math.sqrt) 
        swia_h_vel_dataframe.plot(kind='line', use_index=True)
        
        
    if static_h_vel:
        #This is more like a direction, not a velocity.  The values are between 0 and 1.  
        
        static_h_vel_dataframe = kp['STATIC'].loc[:,['H+ Direction MSO X', 'H+ Direction MSO Y', 'H+ Direction MSO Z']]
        static_h_vel_dataframe['Magnitude'] = ((kp['STATIC']['H+ Direction MSO X']*kp['STATIC']['H+ Direction MSO X']) + (kp['STATIC']['H+ Direction MSO Y']*kp['STATIC']['H+ Direction MSO Y']) + (kp['STATIC']['H+ Direction MSO Z']*kp['STATIC']['H+ Direction MSO Z'])).apply(math.sqrt) 
        static_h_vel_dataframe.plot(kind='line', use_index=True)
        
        
    if static_o2_vel:  
        static_o2_vel_dataframe = kp['STATIC'].loc[:,['O2+ Flow Velocity MSO X', 'O2+ Flow Velocity MSO Y', 'O2+ Flow Velocity MSO Z']]
        static_o2_vel_dataframe['Magnitude'] = ((kp['STATIC']['O2+ Flow Velocity MSO X']*kp['STATIC']['O2+ Flow Velocity MSO X']) + (kp['STATIC']['O2+ Flow Velocity MSO Y']*kp['STATIC']['O2+ Flow Velocity MSO Y']) + (kp['STATIC']['O2+ Flow Velocity MSO Z']*kp['STATIC']['O2+ Flow Velocity MSO Z'])).apply(math.sqrt) 
        static_o2_vel_dataframe.plot(kind='line', use_index=True)
        
        
    if static_flux:
        #In the IDL Toolkit, it only plots O2PLUS_FLOW_VELOCITY_MSO_X/Y.  I'm assuming this is incorrect.
        # I have no idea what the right values to plot are.  
        x = 2
        
    if static_energy:
        kp['STATIC'].loc[:,['H+ Energy', 'He++ Energy', 'O+ Energy', 'O2+ Energy']].plot(kind='line', use_index=True, logy=True)
        
    if sun_bar:
        #Shows whether or not MAVEN is in the sun
        #1 if True
        #0 if False
        
        #Could there be a more efficient way of doing this?
        radius_mars = 3396.0 
        sun_bar_series = ((kp['SPACECRAFT']['MSO Y']*kp['SPACECRAFT']['MSO Y']) + (kp['SPACECRAFT']['MSO Z']*kp['SPACECRAFT']['MSO Z'])).apply(math.sqrt)
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
                
        sun_bar_series.plot(kind='line', use_index=True, ylim=[-0.1,1.1])
        
    if solar_wind:
        
        #Whenever we do a log plot, the plotting routine stops if a column is full of NaNs.  So we need to check for 
        #this prior to plotting them.  For the record, Tplot just ignores all NaN data and doesn't plot it.    
        solar_wind_dataframe = kp['SWIA'].loc[:,['Solar Wind Dynamic Pressure']]
        for KP in solar_wind_dataframe.columns.values:
            if (len(solar_wind_dataframe[KP][solar_wind_dataframe[KP].apply(math.isnan)]) == len(solar_wind_dataframe[KP])):
                print KP + " has no finite values and will not be plotted."
                solar_wind_dataframe = solar_wind_dataframe.drop(KP, 1)
        
        
        solar_wind_dataframe.plot(kind='line', use_index=True, logy=True)

        
    if ionosphere:
        
        #Need to convert to float first, not sure why it is not already
        ionosphere_dataframe = kp['SWEA'].loc[:,['Electron Spectrum Shape']]
        ionosphere_dataframe['Electron Spectrum Shape'] = ionosphere_dataframe['Electron Spectrum Shape'].apply(float)
        #Whenever we do a log plot, the plotting routine stops if a column is full of NaNs.  So we need to check for 
        #this prior to plotting them.  For the record, Tplot just ignores all NaN data and doesn't plot it.    
        
        
        if (len(ionosphere_dataframe['Electron Spectrum Shape'][ionosphere_dataframe['Electron Spectrum Shape'].apply(float).apply(math.isnan)]) == len(ionosphere_dataframe['Electron Spectrum Shape'])):
            print "Electron Spectrum Shape" + " has no finite values and will not be plotted."
            ionosphere_dataframe = ionosphere_dataframe.drop(KP, 1)
        
        
        ionosphere_dataframe.plot(kind='line', use_index=True, logy=True)
        
    if sc_pot:
        kp['LPW'].loc[:,['Spacecraft Potential']].plot(kind='line', use_index=True)
        
        