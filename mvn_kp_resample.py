import datetime
from scipy import interpolate
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
    #Prune the KP array to be between start and end times
    #
    if kp['LPW'] is not None:
        LPW=kp['LPW'][kp['Time'] > start_time and kp['Time'] < end_time]
    else:
        LPW=None
    if kp['MAG'] is not None:
        MAG=kp['MAG'][kp['Time'] > start_time and kp['Time'] < end_time]
    else:
        MAG=None
    if kp['EUV'] is not None:
        EUV=kp['EUV'][kp['Time'] > start_time and kp['Time'] < end_time] 
    else:
        EUV=None
    if kp['SWEA'] is not None:
        SWEA=kp['SWEA'][kp['Time'] > start_time and kp['Time'] < end_time]
    else:
        SWEA=None
    if kp['SWIA'] is not None:
        SWIA=kp['SWIA'][kp['Time'] > start_time and kp['Time'] < end_time]
    else:
        SWIA=None
    if kp['NGIMS'] is not None:
        NGIMS=kp['NGIMS'][kp['Time'] > start_time and kp['Time'] < end_time]
    else:
        NGIMS=None
    if kp['SEP'] is not None:
        SEP=kp['SEP'][kp['Time'] > start_time and kp['Time'] < end_time]
    else:
        SEP=None
    if kp['STATIC'] is not None:
        STATIC=kp['STATIC'][kp['Time'] > start_time and kp['Time'] < end_time]
    else:
        STATIC=None 
    APP=kp['APP'][kp['Time'] > start_time and kp['Time'] < end_time]
    SPACECRAFT=kp['SPACECRAFT'][kp['Time'] > start_time and kp['Time'] < end_time]
    IOflag=kp['IOFLAG'][kp['Time'] > start_time and kp['Time'] < end_time]
    Orbit=kp['Orbit'][kp['Time'] > start_time and kp['Time'] < end_time]
    Time=kp['Time'][kp['Time'] > start_time and kp['Time'] < end_time]
    
    
    #
    #Create the new arrays
    #
    old_time=kp['Time']
    
    #Orbit
    spline_function = interpolate.interp1d(old_time.as_matrix(), Orbit.as_matrix())
    Orbit = pd.Series(spline_function(time))
    for i in range(len(time)):
        Orbit.index[i] = datetime.datetime.fromtimestamp(time[i]).strftime('%Y-%m-%dT%H:%M:%S')

    #Instruments
    if LPW is not None:
        dataframe_initalized = False
        for obs in kp['LPW'].columns:
            spline_function = interpolate.interp1d(old_time.as_matrix(), kp['LPW'][obs].as_matrix())
            temp_series = pd.Series(spline_function(time))
            if not dataframe_initalized:
                temp_df = temp_series.to_frame(obs)
                dataframe_initalized = True
                for i in range(len(time)):
                    new_time_strings = []
                    new_time_strings.append(datetime.datetime.fromtimestamp(time[i]).strftime('%Y-%m-%dT%H:%M:%S'))
                temp_df['Time Index'] = pd.Series(new_time_strings)
            else:
                temp_df[obs] = temp_series
        temp_df.set_index('Time Index', drop=True, inplace=True)
        LPW=temp_df
        
        
    
    tag_names = ['TimeString','Time','Orbit','IOflag',
             'LPW','EUV','SWEA','SWIA','STATIC',
             'SEP','MAG','NGIMS','APP','SPACECRAFT']
    # Define list of first level data structures
    data_tags = [Time, TimeUnix, Orbit, IOflag, 
                 LPW, EUV, SWEA, SWIA, STATIC, 
                 SEP, MAG, NGIMS, APP, SPACECRAFT]
    # return a dictionary made from tag_names and data_tags
    kp_new = ( dict( zip( tag_names, data_tags ) ) )#,