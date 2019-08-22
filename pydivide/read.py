# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pydivide

import calendar
import numpy as np
from .utilities import param_dict
from .utilities import remove_inst_tag
from .utilities import get_latest_files_from_date_range, read_iuvs_file, get_latest_iuvs_files_from_date_range
from .utilities import get_header_info
from .utilities import orbit_time
from _collections import OrderedDict
import builtins


def read(input_time, instruments=None, insitu_only=False):
    '''
    Read in a given filename in situ file into a dictionary object
    Optional keywords maybe used to downselect instruments returned
     and the time windows.

    Input:
        filename: Name of the in situ KP file to read in.
        time (Not Yet Implemeted): 
            Set a time bounds/filter on the data
            (this will be necessary when this is called by a wrapper that
             seeks to ingest all data within a range of dates that may
             be allowed to span multiple days (files) ).
        Instruments: (Not Yet Implemented)
            Optional keyword listing the instruments to include 
            in the returned dictionary/structure.
    Output:
        A dictionary (data structure) containing up to all of the columns
            included in a MAVEN in-situ Key parameter data file.

    ToDo: Implement Instrument selection ability
          Some repetition of effort here; maybe modularize parts of this?
    '''
    import pandas as pd
    import re
    from datetime import datetime, timedelta
    from dateutil.parser import parse
    
    if instruments is not None:
        if not isinstance(instruments, builtins.list):
            instruments = [instruments]
    
    # Check for orbit num rather than time string
    if isinstance(input_time, builtins.list):
        if isinstance(input_time[0], int):
            input_time = orbit_time(input_time[0], input_time[1])
    elif isinstance(input_time, int):
        input_time = orbit_time(input_time)
    
    # Turn string input into datetime objects
    if type(input_time) is list:
        if len(input_time[0]) <= 10:
            input_time[0] = input_time[0] + ' 00:00:00'
        if len(input_time[1]) <= 10:
            input_time[1] = input_time[1] + ' 00:00:00'
        date1 = parse(input_time[0])
        date2 = parse(input_time[1])
    else:
        if len(input_time) <= 10:
            input_time = input_time + ' 00:00:00'
        date1 = parse(input_time)
        date2 = date1 + timedelta(days=1)
        
    date1_unix = calendar.timegm(date1.timetuple())
    date2_unix = calendar.timegm(date2.timetuple())
    
    filenames = get_latest_files_from_date_range(date1, date2)
    iuvs_filenames = get_latest_iuvs_files_from_date_range(date1, date2)
    if not filenames and not iuvs_filenames:
        print("No file found for this date range.")
        return
    
    kp_insitu = []
    if filenames:
        # Get column names from first file
        names, inst = get_header_info(filenames[0])
        # Strip off the first name for now (Time), and use that as the dataframe index.
        # Seems to make sense for now, but will it always?
        names = names[1:len(names)]
        inst = inst[1:len(inst)]

        # Break up dictionary into instrument groups
        lpw_group, euv_group, swe_group, swi_group, sta_group, sep_group, mag_group, ngi_group, app_group, sc_group = \
            [], [], [], [], [], [], [], [], [], []
    
        for i, j in zip(inst, names):
            if re.match('^LPW$', i.strip()):
                lpw_group.append(j)
            elif re.match('^LPW-EUV$', i.strip()):
                euv_group.append(j)
            elif re.match('^SWEA$', i.strip()):
                swe_group.append(j)
            elif re.match('^SWIA$', i.strip()):
                swi_group.append(j)
            elif re.match('^STATIC$', i.strip()):
                sta_group.append(j)
            elif re.match('^SEP$', i.strip()):
                sep_group.append(j)
            elif re.match('^MAG$', i.strip()):
                mag_group.append(j)
            elif re.match('^NGIMS$', i.strip()):
                ngi_group.append(j)
            elif re.match('^SPICE$', i.strip()):
                # NB Need to split into APP and SPACECRAFT
                if re.match('(.+)APP(.+)', j):
                    app_group.append(j)
                else:  # Everything not APP is SC in SPICE
                    # But do not include Orbit Num, or IO Flag
                    # Could probably stand to clean this line up a bit
                    if not re.match('(.+)(Orbit Number|Inbound Outbound Flag)', j):
                        sc_group.append(j)
            else:
                pass
        
        delete_groups = []
        if instruments is not None:
            if 'LPW' not in instruments and 'lpw' not in instruments:
                delete_groups += lpw_group
            if 'MAG' not in instruments and 'mag' not in instruments:
                delete_groups += mag_group
            if 'EUV' not in instruments and 'euv' not in instruments:
                delete_groups += euv_group
            if 'SWI' not in instruments and 'swi' not in instruments:
                delete_groups += swi_group
            if 'SWE' not in instruments and 'swe' not in instruments:
                delete_groups += swe_group
            if 'NGI' not in instruments and 'ngi' not in instruments:
                delete_groups += ngi_group
            if 'SEP' not in instruments and 'sep' not in instruments:
                delete_groups += sep_group
            if 'STA' not in instruments and 'sta' not in instruments:
                delete_groups += sta_group
    
        # Read in all relavent data into a pandas dataframe called "temp"
        temp_data = []
        for filename in filenames:
            # Determine number of header lines    
            nheader = 0
            with open(filename) as f:
                for line in f:
                    if line.startswith('#'):
                        nheader += 1
        
                temp_data.append(pd.read_fwf(filename, skiprows=nheader, index_col=0,
                                             widths=[19] + len(names) * [16], names=names))
                for i in delete_groups:
                    del temp_data[-1][i] 
                
        temp_unconverted = pd.concat(temp_data)

        # Need to convert columns
        # This is kind of a hack, but I can't figure out a better way for now
        
        if 'SWEA.Electron Spectrum Shape' in temp_unconverted and 'NGIMS.Density NO' in temp_unconverted:
            temp = temp_unconverted.astype(dtype={'SWEA.Electron Spectrum Shape': np.float64,
                                                  'NGIMS.Density NO': np.float64})
        elif 'SWEA.Electron Spectrum Shape' in temp_unconverted and 'NGIMS.Density NO' not in temp_unconverted:
            temp = temp_unconverted.astype(dtype={'SWEA.Electron Spectrum Shape': np.float64})
        elif 'SWEA.Electron Spectrum Shape' not in temp_unconverted and 'NGIMS.Density NO' in temp_unconverted:
            temp = temp_unconverted.astype(dtype={'NGIMS.Density NO': np.float64})
        else:
            temp = temp_unconverted
        #
        # Cut out the times not included in the date range
        #
        time_unix = [calendar.timegm(datetime.strptime(i, '%Y-%m-%dT%H:%M:%S').timetuple()) for i in temp.index]
        start_index = 0
        for t in time_unix:
            if t >= date1_unix:
                break
            start_index += 1
        end_index = 0
        for t in time_unix:
            if t >= date2_unix:
                break
            end_index += 1

        # Assign the first-level only tags
        time_unix = time_unix[start_index:end_index]
        temp = temp[start_index:end_index]
        time = temp.index
        time_unix = pd.Series(time_unix)  # convert into Series for consistency
        time_unix.index = temp.index
        orbit = temp['SPICE.Orbit Number']
        io_flag = temp['SPICE.Inbound Outbound Flag']
    
        #
        # Build the sub-level DataFrames for the larger dictionary/structure
        #
        app = temp[app_group]
        spacecraft = temp[sc_group]
        if instruments is not None:
            if 'LPW' in instruments or 'lpw' in instruments:
                lpw = temp[lpw_group]
            else:
                lpw = None
            if 'MAG' in instruments or 'mag' in instruments:
                mag = temp[mag_group]
            else:
                mag = None
            if 'EUV' in instruments or 'euv' in instruments:
                euv = temp[euv_group]
            else:
                euv = None
            if 'SWE' in instruments or 'swe' in instruments:
                swea = temp[swe_group]
            else:
                swea = None
            if 'SWI' in instruments or 'swi' in instruments:
                swia = temp[swi_group]
            else:
                swia = None
            if 'NGI' in instruments or 'ngi' in instruments:
                ngims = temp[ngi_group]
            else:
                ngims = None
            if 'SEP' in instruments or 'sep' in instruments:
                sep = temp[sep_group]
            else:
                sep = None
            if 'STA' in instruments or 'sta' in instruments:
                static = temp[sta_group]
            else:
                static = None
        else:
            lpw = temp[lpw_group]
            euv = temp[euv_group]
            swea = temp[swe_group]
            swia = temp[swi_group]
            static = temp[sta_group]
            sep = temp[sep_group]
            mag = temp[mag_group]
            ngims = temp[ngi_group]
        
        #
        # Strip out the duplicated instrument part of the column names
        # (this is a bit hardwired and can be improved)
        #
        for i in [lpw, euv, swea, swia, sep, static, ngims, mag, app, spacecraft]:
            if i is not None:
                i.columns = remove_inst_tag(i)
        
        if lpw is not None:
            lpw = lpw.rename(index=str, columns=param_dict)
        if euv is not None:
            euv = euv.rename(index=str, columns=param_dict)
        if swea is not None:
            swea = swea.rename(index=str, columns=param_dict)
        if swia is not None:
            swia = swia.rename(index=str, columns=param_dict)
        if sep is not None:
            sep = sep.rename(index=str, columns=param_dict)
        if static is not None:
            static = static.rename(index=str, columns=param_dict)
        if ngims is not None:
            ngims = ngims.rename(index=str, columns=param_dict)
        if mag is not None:
            mag = mag.rename(index=str, columns=param_dict)
        if app is not None:
            app = app.rename(index=str, columns=param_dict)
        if spacecraft is not None:
            spacecraft = spacecraft.rename(index=str, columns=param_dict)

        # Do not forget to save units
        # Define the list of first level tag names
        tag_names = ['TimeString', 'Time', 'Orbit', 'IOflag',
                     'LPW', 'EUV', 'SWEA', 'SWIA', 'STATIC',
                     'SEP', 'MAG', 'NGIMS', 'APP', 'SPACECRAFT']
        # Define list of first level data structures
        data_tags = [time, time_unix, orbit, io_flag,
                     lpw, euv, swea, swia, static,
                     sep, mag, ngims, app, spacecraft]
        kp_insitu = (OrderedDict(zip(tag_names, data_tags)))
    
    # Now for IUVS
    kp_iuvs = [] 
    if not insitu_only and iuvs_filenames:
        for file in iuvs_filenames:
            kp_iuvs.append(read_iuvs_file(file))
    if not kp_iuvs:
        return kp_insitu
    else:
        return kp_insitu, kp_iuvs
