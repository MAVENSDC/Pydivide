import calendar
import numpy as np
from .utilities import param_dict
from .utilities import remove_inst_tag
from .utilities import get_latest_files_from_date_range, read_iuvs_file, get_latest_iuvs_files_from_date_range
from .utilities import get_header_info
from .utilities import orbit_time
from _collections import OrderedDict
import builtins

def mvn_kp_read(input_time, instruments = None, insitu_only=False):
    print("This procedure was renamed, just use read")
    x = read(input_time=input_time, instruments=instruments, insitu_only=insitu_only)
    return x

def read(input_time, instruments = None, insitu_only=False):
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
    
    if instruments != None:
        if not isinstance(instruments, builtins.list):
            instruments = [instruments]
    
    #Check for orbit num rather than time string
    if isinstance(input_time, builtins.list):
        if isinstance(input_time[0], int):
            input_time = orbit_time(input_time[0], input_time[1])
    elif isinstance(input_time, int):
        input_time = orbit_time(input_time)
    
    #Turn string input into datetime objects
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
    if filenames == [] and iuvs_filenames ==[]:
        print("No file found for this date range.")
        return
    
    kp_insitu = []
    if filenames != []:
        #Get column names from first file
        names, inst = get_header_info(filenames[0])
        #Strip off the first name for now (Time), and use that as the dataframe index.  
        #Seems to make sense for now, but will it always?
        names = names[1:len(names)]
        inst = inst[1:len(inst)]
        
        #
        # Break up dictionary into instrument groups
        #
        LPWgroup, EUVgroup, SWEgroup, SWIgroup, STAgroup, SEPgroup, MAGgroup, \
        NGIgroup, APPgroup, SCgroup = [],[],[],[],[],[],[],[],[],[]
    
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
            if 'LPW' not in instruments and 'lpw' not in instruments:
                DELETEgroups = DELETEgroups + LPWgroup
            if 'MAG' not in instruments and 'mag' not in instruments:
                DELETEgroups = DELETEgroups + MAGgroup
            if 'EUV' not in instruments and 'euv' not in instruments:
                DELETEgroups = DELETEgroups + EUVgroup 
            if 'SWI' not in instruments and 'swi' not in instruments:
                DELETEgroups = DELETEgroups + SWIgroup
            if 'SWE' not in instruments and 'swe' not in instruments:
                DELETEgroups = DELETEgroups + SWEgroup
            if 'NGI' not in instruments and 'ngi' not in instruments:
                DELETEgroups = DELETEgroups + NGIgroup
            if 'SEP' not in instruments and 'sep' not in instruments:
                DELETEgroups = DELETEgroups + SEPgroup
            if 'STA' not in instruments and 'sta' not in instruments:
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
                
        temp_unconverted = pd.concat(temp_data)
        
        #
        #Need to convert columns 
        #This is kind of a hack, but I can't figure out a better way for now
        #
        
        if 'SWEA.Electron Spectrum Shape' in temp_unconverted and 'NGIMS.Density NO' in temp_unconverted:
            temp = temp_unconverted.astype(dtype = {'SWEA.Electron Spectrum Shape':np.float64,
                                                    'NGIMS.Density NO':np.float64})
        elif 'SWEA.Electron Spectrum Shape' in temp_unconverted and 'NGIMS.Density NO' not in temp_unconverted:
            temp = temp_unconverted.astype(dtype = {'SWEA.Electron Spectrum Shape':np.float64})
        elif 'SWEA.Electron Spectrum Shape' not in temp_unconverted and 'NGIMS.Density NO' in temp_unconverted:
            temp = temp_unconverted.astype(dtype = {'NGIMS.Density NO':np.float64})
        else:
            temp = temp_unconverted
        #
        # Cut out the times not included in the date range
        #
        TimeUnix = [calendar.timegm(datetime.strptime(i,'%Y-%m-%dT%H:%M:%S')
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
        TimeUnix.index = temp.index
        Orbit = temp['SPICE.Orbit Number']
        IOflag = temp['SPICE.Inbound Outbound Flag']
    
        #
        # Build the sub-level DataFrames for the larger dictionary/structure
        #
        APP=temp[APPgroup]
        SPACECRAFT=temp[SCgroup]
        if instruments != None:
            if 'LPW' in instruments or 'lpw' in instruments:
                LPW=temp[LPWgroup]
            else:
                LPW=None
            if 'MAG' in instruments or 'mag' in instruments:
                MAG=temp[MAGgroup]
            else:
                MAG=None
            if 'EUV' in instruments or 'euv' in instruments:
                EUV=temp[EUVgroup] 
            else:
                EUV=None
            if 'SWE' in instruments or 'swe' in instruments:
                SWEA=temp[SWEgroup]
            else:
                SWEA=None
            if 'SWI' in instruments or 'swi' in instruments:
                SWIA=temp[SWIgroup]
            else:
                SWIA=None
            if 'NGI' in instruments or 'ngi' in instruments:
                NGIMS=temp[NGIgroup]
            else:
                NGIMS=None
            if 'SEP' in instruments or 'sep' in instruments:
                SEP=temp[SEPgroup]
            else:
                SEP=None
            if 'STA' in instruments or 'sta' in instruments:
                STATIC=temp[STAgroup]
            else:
                STATIC=None
        else:
            LPW=temp[LPWgroup]
            EUV=temp[EUVgroup]
            SWEA=temp[SWEgroup]
            SWIA=temp[SWIgroup]
            STATIC=temp[STAgroup]
            SEP=temp[SEPgroup]
            MAG=temp[MAGgroup]
            NGIMS=temp[NGIgroup]
        
        #
        # Strip out the duplicated instrument part of the column names
        # (this is a bit hardwired and can be improved)
        #
        for i in [LPW,EUV,SWEA,SWIA,SEP,STATIC,NGIMS,MAG,APP,SPACECRAFT]:
            if i is not None:
                i.columns = remove_inst_tag(i)
        
        if LPW is not None:
            LPW = LPW.rename(index=str, columns = param_dict)
        if EUV is not None:
            EUV = EUV.rename(index=str, columns = param_dict)
        if SWEA is not None:
            SWEA = SWEA.rename(index=str, columns = param_dict)
        if SWIA is not None:
            SWIA = SWIA.rename(index=str, columns = param_dict)
        if SEP is not None:
            SEP = SEP.rename(index=str, columns = param_dict)
        if STATIC is not None:
            STATIC = STATIC.rename(index=str, columns = param_dict)
        if NGIMS is not None:
            NGIMS = NGIMS.rename(index=str, columns = param_dict)
        if MAG is not None:
            MAG = MAG.rename(index=str, columns = param_dict)
        if APP is not None:
            APP = APP.rename(index=str, columns = param_dict)
        if SPACECRAFT is not None:
            SPACECRAFT = SPACECRAFT.rename(index=str, columns = param_dict)
        #
        # Clean up SPACECRAFT column names
        #
        #newcol = []
        #for oldcol in SPACECRAFT.columns:
        #    if oldcol.startswith('Spacecraft'):
        #        newcol.append(oldcol[len('Spacecraft '):])
        #    elif oldcol.startswith('Rot matrix MARS'):
        #        a,b = re.findall('\d{1}',oldcol)
        #        newcol.append('T%s%s' % (a,b))
        #    elif oldcol.startswith('Rot matrix SPC'):
        #        a,b = re.findall('\d{1}', oldcol)
        #        newcol.append('SPACECRAFT_T%s%s' % (a,b))
        #    else:
        #        newcol.append(oldcol)
        #SPACECRAFT.columns = newcol
        
        
        
        # Do not forget to save units
        # Define the list of first level tag names
        tag_names = ['TimeString','Time','Orbit','IOflag',
                     'LPW','EUV','SWEA','SWIA','STATIC',
                     'SEP','MAG','NGIMS','APP','SPACECRAFT']
        # Define list of first level data structures
        data_tags = [Time, TimeUnix, Orbit, IOflag, 
                     LPW, EUV, SWEA, SWIA, STATIC, 
                     SEP, MAG, NGIMS, APP, SPACECRAFT]
        kp_insitu = ( OrderedDict( zip( tag_names, data_tags ) ) )
    
    #Now for IUVS
    kp_iuvs = [] 
    if not insitu_only and iuvs_filenames:
        for file in iuvs_filenames:
            kp_iuvs.append(read_iuvs_file(file))
    if kp_iuvs == []:
        return kp_insitu
    else:
        return kp_insitu, kp_iuvs
