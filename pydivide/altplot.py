# Copyright 2019 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pydivide

from .utilities import get_inst_obs_labels, param_list, orbit_time, range_select
import pytplot
import builtins

def mvn_kp_altplot( kp, parameter=None, time=None, errors=None, 
              sameplot=True, list=False, title='Altitude Plot', qt=True):
    
    print("This procedure was renamed, just use altplot")
    altplot(kp,
            parameter=parameter,
            time=time,
            errors=errors,
            sameplot=sameplot,
            list=list,
            title=title,
            qt=qt)
    return 

def altplot(kp, 
            parameter=None, 
            time=None, 
            errors=None, 
            sameplot=True, 
            list=False, 
            title='Altitude Plot', 
            qt=True):
    

#     '''
#     Plot the provided data against spacecraft altitude. 
#     If time is not provided, plot the entire dataset. 
#   
#     Required Arguments:
#         kp: STRUCT
#             KP insitu data structure read from file(s).
#         parameter: INT, LIST, STR
#             Parameter(s) to be plotted. Can be provided as integer (by index) or string (by name: inst.obs). List may contain various data types.
#         bin_by: INT, STR
#             Parameters(index or name) by which to bin the specified Key Parameter.
#         binsize: INT, LIST
#             Bin size for each binning dimension. Number of elements must be equal to those in bin_by. 
#       
#     Optional Arguments:
#         time: [STR, STR] or [INT, INT]
#             Two-element list of strings or integers indicating the time range to be plotted. Currently, no checks if time range is within data. 
#         sameplot: BOOL 
#             If True, put all curves on same axes. If False, generate new axes for each plot. 
#         list: BOOL 
#             List all KP parameters instead of plotting. 
#         title: STR 
#             Sets plot title. Default is ‘Altitude Plot’. 
#         qt: BOOL 
#             If True, plot with PyQtGraph. If False, plot with bokeh. 
#               
#     Returns: 
#         None
#   
#     Examples: 
#         Plot LPW.ELECTRON_DENSITY and MAG.MSO_Y against spacecraft altitude. 
#         >> pydivide.altplot(insitu, parameter=['LPW.ELECTRON_DENSITY','MAG.MSO_Y'])
#           
#     '''
    
    if list:
        x = param_list(kp)
        for param in x:
            print(param)
        return
    
    #Check for orbit num rather than time string
    if isinstance(time, builtins.list):
        if isinstance(time[0], int):
            time = orbit_time(time[0], time[1])
    elif isinstance(time, int):
        time = orbit_time(time)
        
    # Check existence of parameter
    if parameter == None: 
        print("Must provide an index (or name) for param to be plotted.")
        return
    # Store instrument and observation of parameter(s) in lists
    inst = []
    obs = []
    if type(parameter) is int or type(parameter) is str:
        a,b = get_inst_obs_labels( kp, parameter )
        inst.append(a)
        obs.append(b)
    else:
        for param in parameter:
            a,b = get_inst_obs_labels(kp,param)
            inst.append(a)
            obs.append(b)
    inst_obs = builtins.list(zip( inst, obs ))

    # Check the time variable
    if time != None:
        kp = range_select(kp,time)

    # Generate the altitude array
    z = []
    index = 0
    for i in kp['TimeString']:
        z.append(kp['SPACECRAFT']['ALTITUDE'][index])
        index = index + 1
    
    pytplot.store_data('sc_alt', data={'x':kp['Time'] , 'y':z})
    # Cycle through the parameters, plotting each according to
    #  the given keywords
    #
    names_to_plot=[]
    legend_names = []
    iplot = 0 # subplot indexes on 1
    for inst,obs in inst_obs:
        #
        # First, generate the dependent array from data
        y = []
        index = 0
        for i in kp['TimeString']:
            y.append(kp[inst][obs][index])
            index = index + 1

        names_to_plot.append('%s.%s'%(inst,obs))
        legend_names.append(obs)
        
        pytplot.store_data(names_to_plot[iplot], data={'x':kp['Time'], 'y':y})
        pytplot.options(names_to_plot[iplot], 'link', ['alt', 'sc_alt'])
        pytplot.options(names_to_plot[iplot], 'alt', 1)

        

        iplot = iplot + 1
    

    if sameplot:
        pytplot_name=','.join(legend_names)
        pytplot.store_data(pytplot_name, data = names_to_plot)
        pytplot.options(pytplot_name, 'alt', 1)
        pytplot.options(pytplot_name, 'legend_names', legend_names)
        pytplot.tplot_options('title', title)
        pytplot.tplot_options('wsize', [1000,300])
        pytplot.tplot(pytplot_name, bokeh=not qt)
        pytplot.del_data(pytplot_name)
    else:
        pytplot.tplot_options('title', title)
        pytplot.tplot_options('wsize', [1000,300*(iplot-1)])
        pytplot.tplot(names_to_plot, bokeh=not qt)
        pytplot.del_data(names_to_plot)
    return