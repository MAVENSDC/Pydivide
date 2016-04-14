#
#  Place whatever relevant header info is needed here
#  Including import statements
#
# Author: McGouldrick
#
# Version 0.3 (2016-Jan-12)
#   Modified range_select
#
# This will be a library of the DIVIDE IDL toolkit translated into python
#
# History:
#  v.0.1 (2015-Nov-30): Begun.  For a month, used IDL sav file, 
#         imported using scipy.io.readsav.
#    Wrote param_list, find_param_from_index, get_inst_obs_labels, 
#          make_time_labels, param_list, param_range, range_select, 
#          time_plot, alt_plot.
#  v.0.2 (2016-Jan-08)
#   Wrote read_insitu_file
#   Modified time_plot to work with read file (not sav file)
#   Modified alt_plot (ditto)
#   Modified param_list (ditto)
#   Modified param_range (ditto)
#
#-------------------------------------------------------------------
#
def param_list_sav( kp ):
    '''
    Return a listing of all parameters present in the given 
    insitu data dictionary/structure.

    Caveats:
        Rendered obsolete by param_list.
           (only works with data from IDL sav file)

    Input:
        kp: insitu kp data structure/dictionary imported from
            and IDL sav file
    Output:
        ParamList: a list of all contained items and their indices.
    '''
    index = 1
    ParamList = []
    for base_tag in kp.dtype.names:
        try:
            first_level_tags = kp[base_tag][0].dtype.names
            for first_level_tag in first_level_tags:
                ParamList.append("#%3d %s.%s" % 
                                 (index,base_tag,first_level_tag) )
                index = index + 1
        except:
            pass
    return ParamList

#---------------------------------------------------------------------

def param_list( kp ):
    '''
    Return a listing of all parameters present in the given 
    insitu data dictionary/structure.

    Input:
        kp: insitu kp data structure/dictionary read from file(s)
    Output:
        ParamList: a list of all contained items and their indices.
    '''
    import pandas as pd

    index = 1
    ParamList = []
    for base_tag in kp.keys():
        if isinstance(kp[base_tag], pd.DataFrame):
            for obs_tag in kp[base_tag].columns:
                ParamList.append("#%3d %s.%s" % 
                                 (index, base_tag, obs_tag ) )
                index = index + 1
        elif isinstance(kp[base_tag], pd.Series):
            ParamList.append("#%3d %s" % (index, base_tag) )
            index = index + 1
        else:
            print '*****WARNING*****'
            print 'Returning INCOMPLETE Parameter List'
            print 'Base tag neither DataFrame nor Series'
            print 'Plese check read_insitu_file definition'

    return ParamList

#---------------------------------------------------------------------

def param_range( kp, iuvs=None ):
    '''
    Print the range of times and orbits for the provided insitu data.
    If iuvs data are also provided, return only orbit numbers for IUVS data.

    Caveats:
        At present, not configured to handle (real) IUVS data.
        Current configuration of procedure assumes IUVS has identical 
            time information as in-situ.

    Input:
        kp: insitu kp data structure/dictionary
        iuvs: IUVS kp data strucure/dictionary
    Output:
        None: prints information to screen
    '''

    import numpy as np
#
# First, the case where insitu data are provided
#
#    if kp.dtype.names[0] == 'TIME_STRING':
    print "The loaded insitu KP data set contains data between"
    print( "   %s and %s" % ( np.array(kp['TimeString'])[0], 
                              np.array(kp['TimeString'])[-1]) )
    print "Equivalently, this corresponds to orbits"
    print ( "   %6d and %6d." % ( np.array(kp['Orbit'])[0], 
                                  np.array(kp['Orbit'])[-1]) )
#
#  Next, the case where IUVS data are provided
#
    iuvs_data = False
    iuvs_tags = ['CORONA_LO_HIGH','CORONA_LO_LIMB','CORONA_LO_DISK',
                 'CORONA_E_HIGH','CORONA_E_LIMB','CORONA_E_DISK',
                 'APOAPSE','PERIAPSE','STELLAR_OCC']
    if kp.keys() in iuvs_tags:
        print "The loaded IUVS KP data set contains data between orbits"
        print ( "   %6d and %6d." % ( np.array(kp['Orbit'])[0], 
                                      np.array(kp['Orbit'])[-1] ) )
#
#  Finally, the case where both insitu and IUVS are provided
#
    if iuvs is not None: 
        print "The loaded IUVS KP data set contains data between orbits"
        print ( "   %6d and %6d." 
                % ( np.array(iuvs['Orbit'])[0], 
                    np.array(iuvs['Orbit'])[-1] ) )
        insitu_min, insitu_max = ( np.nanmin([kp['Orbit']]), 
                                   np.nanmax([kp['Orbit']]) )
        if ( np.nanmax([iuvs['Orbit']]) < insitu_min or 
             np.nanmin([iuvs['Orbit']]) > insitu_max ): 
            print "*** WARNING ***"
            print "There is NO overlap between the supplied insitu and IUVS"
            print "  data structures.  We cannot guarantee your safety "
            print "  should you attempt to display these IUVS data against"
            print "  these insitu-supplied emphemeris data."
    return # No information to return

#--------------------------------------------------------------------------

def range_select( kp, Time=None, Parameter=None, 
                  maximum=None, minimum=None ):
    '''
    Returns a subset of the input data based on the provided time
    and/or parameter criteria.  If neither Time nor Parameter filter
    information is provided, then no subselection of dta will occur.
    Any parameter used as a filtering criterion must be paired with 
    either a maximum and/or a minimum value.  Open ended bounds must 
    be indicated with either a value of 'None' or an empty string ('').

    Input:
        kp: insitu kp data structure/dictionary read from file(s)
        Time: two-element time range must be either strings of format
            'yyyy-mm-ddThh:mm:ss' or integers (orbit numbers)
        Parameter: Element of provided data structure/dictionary by
            which to filter data.  Parameter(s) must be either integer
            type (search by index) or string type (search by instrument
            name and observation type).  If multiple Parameters are used
            to filter the data, they must be provided as a list (mixing
            data types within a list is permitted).
        Maximum: maximum value of Parameter on which to filter.  A value of 
            None or '' will leave the Parameter filter unbounded above.
            The number of elements of Maximum *MUST* equal the number of
            elements of Parameter.
        Minimum: minimum value of Parameter on which to filter.  A value of 
            None or '' will leave the Parameter filter unbounded below.
            The number of elements of Minimum *MUST* equal the number of
            elements of Parameter.
    Output: a dictionary/structure containing the same elements as the provided
        one, but filtered according to the Time and Parameter options.

    ToDo: compartmentalize the filtering and/or argument checks.
    '''

    from divide_lib_test import insufficient_input_range_select
    from divide_lib_test import find_param_from_index
    from divide_lib_test import get_inst_obs_labels
    from datetime import datetime
    import numpy as np

    #  Initialize the filter_list
    filter_list = []

    # First, check the arguments
    if Time is None and Parameter is None:
        insufficient_input_range_select()
        print 'Neither Time nor Parameter provided'
        return kp
    elif Time is None:
        # Then only subset based on parameters
        # Need to check whether one or several Parameters given
        inst = []
        obs = []
        if type(Parameter) is int or type(Parameter) is str:
        # First, verify that at least one bound exists
            if minimum is None and maximum is None:
                insufficient_input_range_select()
                print 'No bounds set for parameter: %s' % Parameter
                return kp
            elif minimum is None:
            # Range only bounded above
                minimum = -np.Infinity
            elif maximum is None:
            # range only bounded below
                maximum = np.Infinity
            else:
            # Range bounded on both ends
                pass
            a,b = get_inst_obs_labels(kp,Parameter)
            inst.append(a)
            obs.append(b)
            nparam = 1 # necc?
        elif type(Parameter) is list:
            nparam = len(Parameter)
            for param in Parameter:
                a,b = get_inst_obs_labels(kp,param)
                inst.append(a)
                obs.append(b)
        else:
            print '*****ERROR*****'
            print 'Cannot identify given parameter: %s' % Parameter
            print 'Suggest using param_list(kp) to identify Parameter'
            print 'by index or by name'
            print 'Returning complete original data dictionary'
            return kp
#
# Should I move this below the Time conditional and move 
# Baselining of Filter List to above time
#
    else:
    # Time has been provided as a filtering agent
    # Determine whether Time is provided as strings or orbits
        if (len(Time) != 2):
            if Parameter is not None:
                print '*****WARNING*****'
                print 'Time must be provided as a two-element list'
                print 'of either strings (yyyy-mm-ddThh:mm:ss) '
                print 'or orbits.  Since a Parameter *was* provided,'
                print 'I will filter on that, but ignore the time input.'
            else:
            # Cannot proceed with filtering
                insufficient_input_range_select()
                print 'Time malformed (must be either a string of format'
                print 'yyyy-mm-ddThh:mm:ss or integer orbit)'
                print 'and no Parameter criterion given'
        else:
        # We have a two-element Time list: parse it
            if type(Time[0]) is not type(Time[1]):
                if Parameter is not None:
                    print '*****WARNING*****'
                    print 'Both elements of time must be same type'
                    print 'Only strings of format yyyy-mm-ddThh:mm:ss'
                    print 'or integers (orbit numbers) are allowed.'
                    print 'Ignoring time inputs; will filter ONLY'
                    print 'on Parameter inputs.'
                else:
                    print '*****ERROR*****'
                    print 'Both elements of Time must be same type'
                    print 'Only Strings of format yyyy-mm-ddThh:mm:ss'
                    print 'or integers (orbit numbers) are allowed.'
                    print 'Returning original unchanged data dictionary'
                    return kp
            elif type(Time[0]) is int:
            # Filter based on orbit number
                Min = min( Time )
                Max = max( Time )
                filter_list.append( kp['Orbit'] >= Min )
                filter_list.append( kp['Orbit'] <= Max )
            elif type( Time[0] ) is str:
            # Filter acc to string dat, need to parse it
                Time_dt = [datetime.strptime(i,'%Y-%m-%dT%H:%M:%S') 
                           for i in Time]
                Min = min( Time_dt )
                Max = max( Time_dt )
                kp_dt = [datetime.strptime(i,'%Y-%m-%dT%H:%M:%S')
                         for i in kp['TimeString'] ]
                delta_tmin = np.array( [ (i-Min).total_seconds()
                                        for i in kp_dt ] )
                delta_tmax = np.array( [ (i-Max).total_seconds()
                                         for i in kp_dt ] )
                filter_list.append( delta_tmin >= 0 )
                filter_list.append( delta_tmax <= 0 )
            else:
            # Time provided as other than string or Integer
                if Parameter is not None:
                    print '*****WARNING*****'
                    print 'Both elements of time must be same type'
                    print 'Only strings of format yyyy-mm-ddThh:mm:ss'
                    print 'or integers (orbit numbers) are allowed.'
                    print 'Ignoring time inputs; will filter ONLY'
                    print 'on Parameter inputs.'
                else:
                    print '*****ERROR*****'
                    print 'Both elements of Time must be same type'
                    print 'Only Strings of format yyyy-mm-ddThh:mm:ss'
                    print 'or integers (orbit numbers) are allowed.'
                    print 'Returning original unchanged data dictionary'
                    return kp
            # Now, we apply the Parameter selection
            inst = []
            obs = []
            if type(Parameter) is int or type(Parameter) is str:
            # Then we have a single Parameter to filter on
            # Verify that bounds info exists
                if minimum is None and maximum is None:
                    insufficient_input_range_select()
                    print 'No bounds set for parameter %s' % Parameter
                    print 'Applying only Time filtering'
                    Parameter = None
                elif minimum is None:
                    minimum = -np.Infinity # Unbounded below
                elif maximum is None:
                    maximum = np.Infinity # Unbounded above
                else:
                    pass # Range fully bounded
                a,b = get_inst_obs_labels(kp,Parameter)
                inst.append(a)
                obs.append(b)
                nparam = 1 # necessary?
            elif type(Parameter) is list:
                if ( len(Parameter) != len(minimum) or
                     len(Parameter) != len(maximum) ):
                    print '*****ERROR*****'
                    print '---range_select---'
                    print 'Number of minima and maxima provided'
                    print 'MUST match number of Parameters provided'
                    print 'You provided %4d Parameters' % len(Parameter)
                    print '             %4d minima' % len(minimum)
                    print '         and %4d maxima' % len(maximum)
                    print 'Filtering only on Time'
                    Parameter = None
                else:
                    nparam = len(Parameter)
                    for param in Parameter:
                        a,b = get_inst_obs_labels(kp,Parameter)
                        inst.append(a)
                        obs.append(b)
    #
    # Now, apply the filters
    #
    if Parameter is not None:
        inst_obs_minmax = zip( inst, obs, minimum, maximum )
        for inst,obs,Min,Max in inst_obs_minmax:
            filter_list.append( kp[inst][obs] >= Min )
            filter_list.append( kp[inst][obs] <= Max )
    #
    # Filter list built, apply to data
    #
    Filter = np.all( filter_list, axis=0 )
    new = {}
    for i in kp:
        temp = kp[i]
        new.update({i:temp[Filter]})
    return new

#--------------------------------------------------------------------------

def insufficient_input_range_select():
    '''
    This error message is called if user calls range_select with
    inputs that result in neither a valid Time range nor a valid
    Parameter range capable of being determined

    ToDo: Is there a way to hide this from the help feature?
    '''
    print '*****ERROR*****'
    print 'Either a time criterion with two values.'
    print '  or a parameter name with maximum and/or'
    print '  minimum values must be provided.'
    print 'Returning the complete original data dictionary'

#--------------------------------------------------------------------------

def make_time_labels(kp):
    '''
    Convert the time strings to 2-line versions so that
    the date and time do not cause significant ovlerlap 
    or vertical length on the time(x) axis

    Input: 
        kp: insitu kp data structure/dictionary read from file(s)
    Output:
        a set of five strings to be used as x-axis time labels
    '''

    from datetime import datetime
    import numpy as np

    indices = kp['Time'].index.values
    t1 = kp['Time'][np.nanmin(kp['Time'].index.values)]
    t5 = kp['Time'][np.nanmax(kp['Time'].index.values)]
    tn = (t5-t1)/4*np.arange(5)
    tickval = [datetime.fromtimestamp(i+t1) for i in tn]
    ticklab = [i.strftime('%Y-%m-%d\n%H:%M:%S') for i in tickval]
    return tickval,ticklab

#--------------------------------------------------------------------------

def get_inst_obs_labels( kp, name ):
    '''
    Given parameter input in either string or integer format,
    identify the instrument name and observation type for use
    in accessing the relevant part of the data structure
    E.g.: 'LPW.EWAVE_LOW_FREQ' would be returned as
          ['LPW', 'EWAVE_LOW_FREQ']

    Input:
        kp: insitu kp data structure/dictionary read from file(s)
        name: string identifying a parameter.
            (Indices must be converted to inst.obs strings before
             calling this routine)
    Output:
        inst (1st arg): instrument identifier
        obs (2nd arg): observation type identifier
    '''

    from divide_lib_test import find_param_from_index as get_param

    # Need to ensure name is a string at this stage
    name = ('%s' % name)
    # Now, split at the dot (if it exists)
    tags = name.split('.')
    # And consider the various possibilities...
    if len(tags)==2:
        return tags
    elif len(tags)==1:
        try:
            int(tags[0])
            return (get_param(kp, tags[0])).split('.')
	except:
            print '*****ERROR*****'
            print '%s is an invalid parameter' % name
            print 'If only one value is provided, it must be an integer'
            return
    else:
        print '*****ERROR*****'
        print '%s is not a valid parameter' % name
        print 'because it has %1d elements' % len(tags)
        print 'Only 1 integer or string of form "a.b" are allowed.'
        print 'Please use .param_list attribute to find valid parameters'
        return

#--------------------------------------------------------------------------

def find_param_from_index( kp, index ):
    '''
    Given an integer index, find the name of the parameter

    Input: 
        kp: insitu kp data structure/dictionary read from file(s)
        index: the index of the desired parameter (integer type)
    Output:
        A string of form <instrument>.<observation>
        (e.g., LPW.EWAVE_LOW_FREQ)
    '''

    from divide_lib_test import param_list
    import re

    index = '#%3d' % int(index)
    plist = param_list(kp)
    found = False
    for i in plist:
        if re.search(index, i):
            return i[5:] # clip the '#123 ' string
    if not found:
        print '*****ERROR*****'
        print '%s not a valid index.' % index
        print 'Use param_list to list options'
        return

#--------------------------------------------------------------------------

def time_plot( kp, parameter=None, time=None, errors=None, 
              SamePlot=True, SubPlot=False, **kwargs ):
    '''
    Plot the provided data as a time series.
    For now, do not accept any error bar information.
    If time is not provided plot entire data set.

    Input:
        kp: insitu kp data structure/dictionary read from file(s)
        Time: Two-element list of strings or integers indicating the 
            range of Time to be plotted.  At present, there are no
            checks on whether provided Times are within provided data
        Parameter: The parameter(s) to be plotted.  Can be provided as
            integers (by index) or strings (by name: inst.obs).  If a 
            single parameter is provided, it must be an int or str.  If
            several are provided it must be a list.  A list may contain
            a mixture of data types.
        Errors: **Not Yet Implemented**
            Will be the Parameter(s) to use for the generation of error
            bars in the created plots.  Since each inst.obs *may* define
            its own unique useage of the 'quality flag', this will be a
            parameter-dependent determination, requiring an add'l routine.
        SamePlot: if True, put all curves on same axes
                  if False, generate new axes for each plot
        SubPlot: if True, stack plots with common x axis
                 if False and nplots > 1, make several distinct plots
    Output: None
        -> Generates plot(s) as requested.  But since there is no plot
           object returned, can not alter any plot subsequently (yet)

    ToDo: Provide mechanism for calculating and plotting error bars
          Return plot object(s) for subsequent editing?
    '''

    import matplotlib.pyplot as plt
    import numpy as np
    from datetime import datetime
    from divide_lib_test import range_select

    # Check existence of parameter
    if parameter == None: 
        print "Must provide an index (or name) for param to be plotted."
        return
    # Store instrument and observation of parameter(s) in lists
    inst = []
    obs = []
    if type(parameter) is int or type(parameter) is str:
        a,b = get_inst_obs_labels( kp, parameter )
        inst.append(a)
        obs.append(b)
        nparam = 1
    else:
        nparam = len(parameter)
        for param in parameter:
            a,b = get_inst_obs_labels(kp,param)
            inst.append(a)
            obs.append(b)
    inst_obs = zip( inst, obs )

    # Check the time variable
    if time == None:
        istart, iend = 0,np.count_nonzero(kp['Orbit'])-1
    else:
        istart,iend = range_select(kp,time)

    # Possible hack: Make the time array
    t = [datetime.strptime(i,'%Y-%m-%dT%H:%M:%S') 
         for i in kp['TimeString']]

    # Cycle through the parameters, plotting each according to
    #  the given keywords
    #
    iplot = 1 # subplot indexes on 1
    for inst,obs in inst_obs:
    # First, generate the dependent array from data
        y = kp[inst][obs]

    # Generate the plot
        if iplot == 1 or not SamePlot: a = plt.figure()

    # If subplots, need to add a subplot
        if SubPlot: ax = a.add_subplot(nparam,1,iplot)

    # Now, generate the plot
        plt.plot(t,y,label=('%s.%s'%(inst,obs)),**kwargs)

    # If subplots, and not last one, suppress x-axis labels
        if SubPlot and iplot < nparam: ax.axes.xaxis.set_ticklabels([])

    # If last plot, get the five time strings for labels
        if iplot == nparam or not SamePlot:
            xticknames, xticklab = make_time_labels(kp)

        # Print ticknames labels at 90 degree rotation
            plt.xticks(xticknames, xticklab, rotation=90 )

        # Add useful axis labels
            plt.xlabel('%s' % 'time')

    # Add descriptive plot title
        if SamePlot: plt.title('%s.%s' % (inst,obs))
        if not SubPlot: plt.ylabel('%s.%s' % (inst,obs) )

    # Increment plot number 
        iplot = iplot + 1

    # Add legend if necessary
    if iplot > 1 and SamePlot and not SubPlot: plt.legend()

    # Return plot object?

#--------------------------------------------------------------------------

def alt_plot( kp, parameter=None, time=None, errors=None, 
              SamePlot=True, SubPlot=False, **kwargs ):
    '''
    Plot the provided data plotted against spacecraft altitude.
    For now, do not accept any error bar information.
    If time is not provided plot entire data set.

    Input:
        kp: insitu kp data structure/dictionary read from file(s)
        Time: Two-element list of strings or integers indicating the 
            range of Time to be plotted.  At present, there are no
            checks on whether provided Times are within provided data
        Parameter: The parameter(s) to be plotted.  Can be provided as
            integers (by index) or strings (by name: inst.obs).  If a 
            single parameter is provided, it must be an int or str.  If
            several are provided it must be a list.  A list may contain
            a mixture of data types.
        Errors: **Not Yet Implemented**
            Will be the Parameter(s) to use for the generation of error
            bars in the created plots.  Since each inst.obs *may* define
            its own unique useage of the 'quality flag', this will be a
            parameter-dependent determination, requiring an add'l routine.
        SamePlot: if True, put all curves on same axes
                  if False, generate new axes for each plot
        SubPlot: if True, stack plots with common x axis
                 if False and nplots > 1, make several distinct plots
    Output: None
        -> Generates plot(s) as requested.  But since there is no plot
           object returned, can not alter any plot subsequently (yet)

    ToDo: Provide mechanism for calculating and plotting error bars
          Return plot object(s) for subsequent editing?
    '''

    import matplotlib.pyplot as plt
    import numpy as np
    from datetime import datetime
    from divide_lib_test import range_select

    # Check existence of parameter
    if parameter == None: 
        print "Must provide an index (or name) for param to be plotted."
        return
    # Store instrument and observation of parameter(s) in lists
    inst = []
    obs = []
    if type(parameter) is int or type(parameter) is str:
        a,b = get_inst_obs_labels( kp, parameter )
        inst.append(a)
        obs.append(b)
        nparam = 1
    else:
        nparam = len(parameter)
        for param in parameter:
            a,b = get_inst_obs_labels(kp,param)
            inst.append(a)
            obs.append(b)
    inst_obs = zip( inst, obs )

    # Check the time variable
    if time == None:
        istart, iend = 0,np.count_nonzero(kp['Orbit'])-1
    else:
        istart,iend = range_select(kp,time)

    # Generate the altitude array
    z = []
    index = 0
    for i in kp['TimeString']:
        z.append(kp['SPACECRAFT']['Altitude Aeroid'][index])
        index = index + 1

    # Cycle through the parameters, plotting each according to
    #  the given keywords
    #
    iplot = 1 # subplot indexes on 1
    for inst,obs in inst_obs:
        #
        # First, generate the dependent array from data
        y = []
        index = 0
        for i in kp['TimeString']:
            y.append(kp[inst][obs][index])
            index = index + 1

    # Generate the plot
        if iplot == 1 or not SamePlot: a = plt.figure()

    # If subplots, need to add a subplot
        if SubPlot: ax = a.add_subplot(1,nparam,iplot)

    # Now, generate the plot
#orig        plt.plot(y,z,label=('%s.%s'%(inst,obs)))
        plt.plot(y,z,label=('%s.%s'%(inst,obs)),**kwargs)

    # If subplots, and not last one, suppress x-axis labels
        if SubPlot and iplot > 1 : 
            ax.axes.yaxis.set_ticklabels([])
        else:
            plt.ylabel('altitude[km]')
 
    # Add descriptive plot title
        if SubPlot or nparam == 1 or not SamePlot: 
            plt.title('%s.%s' % (inst,obs))
        else:
            plt.legend()

    # Increment plot number 
        iplot = iplot + 1

    # Return plot object?

#------------------------------------------------------------------------------

def read_insitu_file( filename, instruments = None, time=None ):
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
    from datetime import datetime

    # Determine number of header lines
    nheader = 0
    for line in open(filename):
        if line.startswith('#'):
            nheader = nheader+1

    #
    # Parse the header (still needs special case work)
    #
    ReadParamList = False
    index_list = []
    fin = open(filename)
    icol = -2 # Counting header lines detailing column names
    iname = 1 # for counting seven lines with name info
    ncol = -1 # Dummy value to allow reading of early headerlines?
    col_regex = '#\s(.{16}){%3d}' % ncol # needed for column names
    for iline in range(nheader):
        line = fin.readline()
        if re.search('Number of parameter columns',line): 
            ncol = int(re.split("\s{3}",line)[1])
            col_regex = '#\s(.{16}){%3d}' % ncol # needed for column names
        elif re.search('Line on which data begins',line): 
            nhead_test = int(re.split("\s{3}",line)[1])-1
        elif re.search('Number of lines',line): 
            ndata = int(re.split("\s{3}",line)[1])
        elif re.search('PARAMETER',line):
            ReadParamList = True
            ParamHead = iline
        elif ReadParamList:
            icol = icol + 1
            if icol > ncol: ReadParamList = False
        elif re.match(col_regex,line):
            # OK, verified match now get the values
            temp = re.findall('(.{16})',line[3:])
            if iname == 1: index = temp
            elif iname == 2: obs1 = temp
            elif iname == 3: obs2 = temp
            elif iname == 4: obs3 = temp
            elif iname == 5: inst = temp
            elif iname == 6: unit = temp
            elif iname == 7: FormatCode = temp
            else: 
                print 'More lines in data descriptor than expected.'
                print 'Line %d' % iline
            iname = iname + 1
        else:
            pass

    #
    # Generate the names list.
    # NB, there are special case redundancies in there
    # (e.g., LPW: Electron Density Quality (min and max))
    # ****SWEA FLUX electron QUALITY *****
    #
    First = True
    Parallel = None
    names = []
    for h,i,j,k in zip(inst,obs1,obs2,obs3):
        combo_name = (' '.join([i.strip(),j.strip(),k.strip()])).strip()
        if re.match('^LPW$',h.strip()):
        # Max and min error bars use same name in column
        # SIS says first entry is min and second is max
            if re.match('(Electron|Spacecraft)(.+)Quality', combo_name):
                if First:
                    combo_name = combo_name + ' Min'
                    First = False
                else:
                    combo_name = combo_name + ' Max'
                    First = True
        elif re.match('^SWEA$',h.strip()):
        # electron flux qual flags do not indicate whether parallel or anti
        # From context it is clear; but we need to specify in name
            if re.match('.+Parallel.+',combo_name): Parallel = True
            elif re.match('.+Anti-par',combo_name): Parallel = False
            else: pass
            if re.match('Flux, e-(.+)Quality', combo_name ):
                if Parallel: 
                    p = re.compile( 'Flux, e- ' )
                    combo_name = p.sub('Flux, e- Parallel ',combo_name)
                else:
                    p = re.compile( 'Flux, e- ' )
                    combo_name = p.sub('Flux, e- Anti-par ',combo_name)
        # Add inst to names to avoid ambiguity
        # Will need to remove these after splitting
        names.append('.'.join([h.strip(),combo_name]))
        names[0] = 'Time'

    #
    # Now close the file and read the data section into a temporary DataFrame
    #
    fin.close()
    temp = pd.read_fwf(filename, skiprows=nheader, index_col=False, 
                       widths=[19]+ncol*[16], names = names)

    #
    # Assign the first-level only tags
    #
    Time = temp['Time']
    TimeUnix = [time.mktime(datetime.strptime(i,'%Y-%m-%dT%H:%M:%S')
                                             .timetuple()) 
                for i in temp['Time']]
    TimeUnix = pd.Series(TimeUnix) # convert into Series for consistency
    Orbit = temp['SPICE.Orbit Number']
    IOflag = temp['SPICE.Inbound Outbound Flag']

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

    #
    # Build the sub-level DataFrames for the larger dictionary/structure
    #
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

    #
    # Strip out the duplicated instrument part of the column names
    # (this is a bit hardwired and can be improved)
    #
    for i in [LPW,EUV,SWEA,SWIA,SEP,STATIC,NGIMS,MAG,APP,SPACECRAFT]:
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
    return ( dict( zip( tag_names, data_tags ) ), 
             dict( zip( tag_names, unit ) ) )

#------------------------------------------------------------------------------

def remove_inst_tag(df):
    '''
    Remove the leading part of the column name that includes the instrument
    identifier for use in creating the parameter names for the toolkit.

    Input:
        A DataFrame produced from the insitu KP data
    Output:
        A new set of column names
    '''

    newcol = []
    for i in df.columns:
        if( len(i.split('.'))>=2):
            j = i.split('.')
            newcol.append('.'.join(j[1:]))

    return newcol
