import datetime
from scipy import interpolate
import numpy as np
import pandas as pd

def mvn_kp_resample(kp, time, sc_only=False):
    
    new_total = len(time)
    start_time = time[0]
    end_time = time[new_total-1]
    
    if start_time < kp['Time'][0]:
        print 'The requested start time is before the earliest data point in the input data structure.'
        print 'This routine DOES NOT extrapolate. Please read in more KP data that covers the requested time span.'
        return
    
    if end_time > kp['Time'][len(kp['Time'])-1]:
        print 'The requested end time is after the latest data point in the input data structure.'
        print 'This routine DOES NOT extrapolate. Please read in more KP data that covers the requested time span.'
        return
    
    #
    #Set up the instrument dataframes
    #
    if kp['LPW'] is not None:
        LPW=kp['LPW']
    else:
        LPW=None
    if kp['MAG'] is not None:
        MAG=kp['MAG']
    else:
        MAG=None
    if kp['EUV'] is not None:
        EUV=kp['EUV']
    else:
        EUV=None
    if kp['SWEA'] is not None:
        SWEA=kp['SWEA']
    else:
        SWEA=None
    if kp['SWIA'] is not None:
        SWIA=kp['SWIA']
    else:
        SWIA=None
    if kp['NGIMS'] is not None:
        NGIMS=kp['NGIMS']
    else:
        NGIMS=None
    if kp['SEP'] is not None:
        SEP=kp['SEP']
    else:
        SEP=None
    if kp['STATIC'] is not None:
        STATIC=kp['STATIC']
    else:
        STATIC=None 
        
    APP=kp['APP']
    SPACECRAFT=kp['SPACECRAFT']
    IOflag=kp['IOflag']
    Orbit=kp['Orbit']
    Time=kp['TimeString']
    TimeUnix=kp['Time']
    
    
    #
    #Set up instrument list to make it easy to loop through the next parts
    #
    inst_names = ['LPW','EUV','SWEA','SWIA','STATIC',
         'SEP','MAG','NGIMS','APP','SPACECRAFT']
    inst_tags = [LPW, EUV, SWEA, SWIA, STATIC, 
             SEP, MAG, NGIMS, APP, SPACECRAFT]
    
    #
    #Create an array of the old times
    #
    old_time=TimeUnix
    
    #
    #Find the closest values for all nearest neighbor interpolations 
    #
    closest_values = []
    for k in range(len(time)):
        closest_value_index = np.absolute(old_time.as_matrix()-time[k]).argmin()
        closest_values.append((old_time.as_matrix()-time[k])[closest_value_index] + time[k])
        
    #
    #Get the new indexes of the dataframes based on the time 
    #
    new_time_strings =[]
    for i in range(len(time)):
        new_time_strings.append(datetime.datetime.fromtimestamp(time[i]).strftime('%Y-%m-%dT%H:%M:%S'))
    new_time_series = pd.Series(new_time_strings)
    
    #Orbit Series
    spline_function = interpolate.interp1d(old_time.as_matrix(), Orbit.as_matrix())
    temp_series = pd.Series(spline_function(time))
    temp_df = temp_series.to_frame('Orbit')
    temp_df['Time Index'] = new_time_series
    temp_df.set_index('Time Index', drop=True, inplace=True)
    Orbit=temp_df.iloc[:,0]
        
    #Time String Series
    temp_series = new_time_series
    temp_df = temp_series.to_frame('Time')
    temp_df['Time Index'] = new_time_series
    temp_df.set_index('Time Index', drop=True, inplace=True)
    Time=temp_df.iloc[:,0]
        
    #Time Unix Series
    temp_series = pd.Series(time)
    temp_df = temp_series.to_frame('Time')
    temp_df['Time Index'] = new_time_series
    temp_df.set_index('Time Index', drop=True, inplace=True)
    TimeUnix=temp_df.iloc[:,0]
        
    #IOFlag Series
    temp_series = []
    for k in range(len(time)):
        temp_series.append(kp['IOflag'][kp['Time'] == closest_values[k]])
    temp_series = pd.Series(temp_series)
    temp_df = temp_series.to_frame('IOflag')
    temp_df['Time Index'] = new_time_series
    temp_df.set_index('Time Index', drop=True, inplace=True)
    IOflag=temp_df.iloc[:,0]
    
    #
    #Instrument Dataframes
    #
    
    #For each instrument:
    for i in range(len(inst_names)):
        if inst_tags[i] is not None:
            dataframe_initalized = False
            #For each observation mode:
            for obs in kp[inst_names[i]].columns:
                column_is_string=False
                #Check if the observation is a string variable.  
                #If it is a string, you can't interpolate between two strings, so use nearest neighbor.
                #Else, use a cubic spline interpolation
                for j in range(len(kp[inst_names[i]][obs])):
                    #Note: Looking through all of these is REALLY SLOW
                    #Without hard coding the observation names that are strings, 
                    #is there a way to make t his faster?
                    if isinstance(kp[inst_names[i]][obs][j], basestring):
                        column_is_string = True
                        break
                    if isinstance(kp[inst_names[i]][obs][j], float) and np.isfinite(kp[inst_names[i]][obs][j]):
                        column_is_string = False
                        break
                if column_is_string:
                    temp_series = []
                    for k in range(len(time)):
                        temp_series.append(kp[inst_names[i]][obs][kp['Time'] == closest_values[k]])
                    temp_series = pd.Series(temp_series)
                else:
                    spline_function = interpolate.interp1d(old_time.as_matrix(), kp[inst_names[i]][obs].as_matrix())
                    temp_series = pd.Series(spline_function(time))
                #Turn the series into a dataframe if it hasn't been done yet.  
                #Else, add it to the dataframe
                if not dataframe_initalized:
                    temp_df = temp_series.to_frame(obs)
                    dataframe_initalized = True
                    temp_df['Time Index'] = new_time_series
                else:
                    temp_df[obs] = temp_series
            #Set the "Time Index" column as the index of the dataframe
            temp_df.set_index('Time Index', drop=True, inplace=True)
            inst_tags[i]=temp_df
    
    #
    #Set up and return the new KP data structure
    #
    tag_names = ['TimeString','Time','Orbit','IOflag',
     'LPW','EUV','SWEA','SWIA','STATIC',
     'SEP','MAG','NGIMS','APP','SPACECRAFT']
    # Define list of first level data structures
    data_tags = [Time, TimeUnix, Orbit, IOflag, 
                 inst_tags[0], inst_tags[1], inst_tags[2], inst_tags[3], inst_tags[4], 
                 inst_tags[5], inst_tags[6], inst_tags[7], APP, SPACECRAFT]
    # return a dictionary made from tag_names and data_tags
    kp_new = ( dict( zip( tag_names, data_tags ) ) )
    
    return kp_new