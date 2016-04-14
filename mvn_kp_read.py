import os
from mvn_kp_utilities import param_list_sav
from mvn_kp_utilities import param_list
from mvn_kp_utilities import param_range
from mvn_kp_utilities import range_select
from mvn_kp_utilities import insufficient_input_range_select
from mvn_kp_utilities import make_time_labels
from mvn_kp_utilities import get_inst_obs_labels
from mvn_kp_utilities import find_param_from_index
from mvn_kp_utilities import remove_inst_tag
from mvn_kp_utilities import kp_regex
from mvn_kp_utilities import get_latest_files_from_date_range
from mvn_kp_utilities import get_header_info
import mvn_kp_download_files_utilities as utils


def mvn_kp_read(input_time, instruments = None):
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
    import time
    from datetime import datetime, timedelta
    from dateutil.parser import parse
    
    # Get the file names from the date
    
    #Turn string input into datetime objects
    if type(input_time) is list:
        if "T" not in input_time[0]:
            input_time[0] = input_time[0] + 'T00:00:00'
        if "T" not in input_time[1]:
            input_time[1] = input_time[1] + 'T00:00:00'
        date1 = parse(input_time[0])
        date2 = parse(input_time[1])
    else:
        if "T" not in input_time:
            input_time = input_time + 'T00:00:00'
        date1 = parse(input_time)
        date2 = date1 + timedelta(days=1)
        
    date1_unix = time.mktime(date1.timetuple())
    date2_unix = time.mktime(date2.timetuple())
    
    filenames = get_latest_files_from_date_range(date1, date2)
    
    #Get column names from first file
    names, inst = get_header_info(filenames[0])
    #Strip off the first name for now (Time), and use that as the dataframe index.  
    #Seems to make sense for now, but will it always?
    names = names[1:len(names)-1]
    inst = inst[1:len(inst)-1]
    
    #
    # Break up dictionary into instrument groups
    #
    LPWgroup, EUVgroup, SWEgroup, SWIgroup, STAgroup, SEPgroup, MAGgroup, \
    NGIgroup, APPgroup, SCgroup = [],[],[],[],[],[],[],[],[],[]
    First = True
    for i,j in zip(inst,names):
        if re.match('^LPW$',i.strip()):
            LPWgroup.append(j)
        elif re.match('^LPW-EUV$',i.strip()):
            EUVgroup.append(j)
        elif re.match('^SWEA$',i.strip()):
            SWEgroup.append(j)
        elif re.match('^SWIA$',i.strip()):
            SWIgroup.append(j)
        elif re.match('^STATIC$',i.strip()):
            STAgroup.append(j)
        elif re.match('^SEP$',i.strip()):
            SEPgroup.append(j)
        elif re.match('^MAG$',i.strip()):
            MAGgroup.append(j)
        elif re.match('^NGIMS$',i.strip()):
            NGIgroup.append(j)
        elif re.match('^SPICE$',i.strip()):
            # NB Need to split into APP and SPACECRAFT
            if re.match('(.+)APP(.+)',j): 
                APPgroup.append(j)
            else: # Everything not APP is SC in SPICE
                # But do not include Orbit Num, or IO Flag
                # Could probably stand to clean this line up a bit
                if not re.match('(.+)(Orbit Number|Inbound Outbound Flag)',j):
                    SCgroup.append(j)
        else:
            pass
    
    DELETEgroups = []
    if instruments != None:
        if 'LPW' not in instruments:
            DELETEgroups = DELETEgroups + LPWgroup
        if 'MAG' not in instruments:
            DELETEgroups = DELETEgroups + MAGgroup
        if 'EUV' not in instruments:
            DELETEgroups = DELETEgroups + EUVgroup 
        if 'SWIA' not in instruments:
            DELETEgroups = DELETEgroups + SWIgroup
        if 'SWEA' not in instruments:
            DELETEgroups = DELETEgroups + SWEgroup
        if 'NGIMS' not in instruments:
            DELETEgroups = DELETEgroups + NGIgroup
        if 'SEP' not in instruments:
            DELETEgroups = DELETEgroups + SEPgroup
        if 'STATIC' not in instruments:
            DELETEgroups = DELETEgroups + STAgroup

    #Read in all relavent data into a pandas dataframe called "temp"
    temp_data = []
    for filename in filenames:
        # Determine number of header lines    
        nheader = 0
        for line in open(filename):
            if line.startswith('#'):
                nheader = nheader+1

        temp_data.append(pd.read_fwf(filename, skiprows=nheader, index_col=0, 
                           widths=[19]+len(names)*[16], names = names))
        for i in DELETEgroups:
            del temp_data[-1][i] 
            
    temp = pd.concat(temp_data)
    
    #
    # Cut out the times not included in the date range
    #
    TimeUnix = [time.mktime(datetime.strptime(i,'%Y-%m-%dT%H:%M:%S')
                                             .timetuple()) 
                for i in temp.index]
    start_index = 0
    for t in TimeUnix:
        if t >= date1_unix:
            break
        start_index = start_index + 1
    end_index = 0
    for t in TimeUnix:
        if t >= date2_unix:
            break
        end_index = end_index + 1 

    #
    # Assign the first-level only tags
    #
    TimeUnix = TimeUnix[start_index:end_index]
    temp = temp[start_index:end_index]       
    Time = temp.index
    TimeUnix = pd.Series(TimeUnix) # convert into Series for consistency
    Orbit = temp['SPICE.Orbit Number']
    IOflag = temp['SPICE.Inbound Outbound Flag']

    #
    # Build the sub-level DataFrames for the larger dictionary/structure
    #
    if instruments != None:
        APP=temp[APPgroup]
        SPACECRAFT=temp[SCgroup]
        if 'LPW' in instruments:
            LPW=temp[LPWgroup]
        if 'MAG' in instruments:
            MAG=temp[MAGgroup]
        if 'EUV' in instruments:
            EUV=temp[EUVgroup] 
        if 'SWEA' in instruments:
            SWEA=temp[SWEgroup]
        if 'SWIA' in instruments:
            SWIA=temp[SWIgroup]
        if 'NGIMS' in instruments:
            NGIMS=temp[NGIgroup]
        if 'SEP' in instruments:
            SEP=temp[SEPgroup]
        if 'STATIC' in instruments:
            STATIC=temp[STAgroup]
    else:
        LPW=temp[LPWgroup]
        EUV=temp[EUVgroup]
        SWEA=temp[SWEgroup]
        SWIA=temp[SWIgroup]
        STATIC=temp[STAgroup]
        SEP=temp[SEPgroup]
        MAG=temp[MAGgroup]
        NGIMS=temp[NGIgroup]
        APP=temp[APPgroup]
        SPACECRAFT=temp[SCgroup]
    
    LPW=temp[LPWgroup] if 'LPW' in instruments else None
    EUV=temp[EUVgroup] if 'EUV' in instruments else None
    SWEA=temp[SWEgroup] if 'SWEA' in instruments else None
    SWIA=temp[SWIgroup] if 'SWIA' in instruments else None
    STATIC=temp[STAgroup] if 'STATIC' in instruments else None
    SEP=temp[SEPgroup] if 'SEP' in instruments else None
    MAG=temp[MAGgroup] if 'MAG' in instruments else None
    NGIMS=temp[NGIgroup] if 'NGIMS' in instruments else None
    APP=temp[APPgroup]
    SPACECRAFT=temp[SCgroup]
    
    #
    # Strip out the duplicated instrument part of the column names
    # (this is a bit hardwired and can be improved)
    #
    for i in [LPW,EUV,SWEA,SWIA,SEP,STATIC,NGIMS,MAG,APP,SPACECRAFT]:
        if i is not None:
            i.columns = remove_inst_tag(i)

    #
    # Clean up SPACECRAFT column names
    #
    newcol = []
    for oldcol in SPACECRAFT.columns:
        if oldcol.startswith('Spacecraft'):
            newcol.append(oldcol[len('Spacecraft '):])
        elif oldcol.startswith('Rot matrix MARS'):
            a,b = re.findall('\d{1}',oldcol)
            newcol.append('T%s%s' % (a,b))
        elif oldcol.startswith('Rot matrix SPC'):
            a,b = re.findall('\d{1}', oldcol)
            newcol.append('SPACECRAFT_T%s%s' % (a,b))
        else:
            newcol.append(oldcol)
    SPACECRAFT.columns = newcol

    # Do not forget to save units
    # Define the list of first level tag names
    tag_names = ['TimeString','Time','Orbit','IOflag',
                 'LPW','EUV','SWEA','SWIA','STATIC',
                 'SEP','MAG','NGIMS','APP','SPACECRAFT']
    # Define list of first level data structures
    data_tags = [Time, TimeUnix, Orbit, IOflag, 
                 LPW, EUV, SWEA, SWIA, STATIC, 
                 SEP, MAG, NGIMS, APP, SPACECRAFT]
    # return a dictionary made from tag_names and data_tags
    return ( dict( zip( tag_names, data_tags ) ) )#, 
             #dict( zip( tag_names, unit ) ) )
