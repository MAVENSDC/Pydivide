# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pydivide

#888888888888888
#80808
from .utilities import get_inst_obs_labels, param_list, orbit_time
import pytplot
import pandas as pd
import builtins

def mvn_kp_plot( kp, parameter=None, time=None, errors=None, 
                 SamePlot=True, list=False, title = '', qt=True):
    print("This procedure was renamed, just use plot")
    plot(kp=kp, 
         parameter=parameter, 
         time=time, 
         errors=errors, 
         SamePlot=SamePlot, 
         list=list, 
         title=title,
         qt=qt)
    return

def plot( kp, parameter=None, time=None, errors=None, 
          SamePlot=True, list=False, title = '', qt=True):
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
          
    '''
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
        nparam = 1
    else:
        nparam = len(parameter)
        for param in parameter:
            a,b = get_inst_obs_labels(kp,param)
            inst.append(a)
            obs.append(b)
    inst_obs = builtins.list(zip( inst, obs ))


    # Cycle through the parameters, plotting each according to
    #  the given keywords
    #
    iplot = 1 # subplot indexes on 1
    y_list=[]
    legend_names=[]
    for inst_temp,obs_temp in inst_obs:
    # First, generate the dependent array from data
        y = kp[inst_temp][obs_temp]
        if SamePlot:
            y_list.append(y)
            legend_names.append(obs_temp)
        else:
            pytplot.store_data(obs_temp, data={'x':kp['Time'], 'y':y})
            # Add descriptive plot title
            pytplot.options(obs_temp, 'ytitle', '%s.%s' % (inst,obs) )
        # Increment plot number 
        iplot = iplot + 1
    if time is not None:
        pytplot.xlim(time[0], time[1])
    
    if SamePlot:
        pytplot_name=''.join(legend_names)
        result = pd.concat(y_list, axis=1, join_axes=[y_list[0].index])
        pytplot.store_data(pytplot_name, data={'x':kp['Time'], 'y':result})
        pytplot.options(pytplot_name, 'legend_names', legend_names)
        pytplot.tplot_options('title', title)
        pytplot.tplot_options('wsize', [1000,300])
        pytplot.tplot(pytplot_name, qt=qt)
        pytplot.del_data(pytplot_name)
    else:
        pytplot.tplot_options('title', title)
        pytplot.tplot_options('wsize', [1000,300*(iplot-1)])
        pytplot.tplot(obs, qt=qt)
        pytplot.del_data(obs)

    return
#--------------------------------------------------------------------------
