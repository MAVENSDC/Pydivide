# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pydivide

from .utilities import get_inst_obs_labels, param_list, orbit_time, range_select
import pytplot
import builtins


def altplot(kp, parameter=None, time=None, errors=None,
            sameplot=True, list=False, title='Altitude Plot',
            ylog=False, qt=True):
    '''
    Plot the provided data plotted against spacecraft altitude.
    If time is not provided plot entire data set.

    Required Parameters:
        kp : dict
            insitu kp data structure/dictionary read from file(s)
        parameter : list of str/int
            The parameter(s) to be plotted.  Can be provided as
            integers (by index) or strings (by name: inst.obs).  If a 
            single parameter is provided, it must be an int or str.  If
            several are provided it must be a list.  A list may contain
            a mixture of data types.

    Optional Parameters:
        time : list of str
            Two-element list of strings or integers indicating the
            range of Time to be plotted.  At present, there are no
            checks on whether provided Times are within provided data
        sameplot : bool
            if True, put all curves on same axes
            if False, generate new axes for each plot
        list : bool
            Lists all Key Parameters instead of plotting
        title : str
            The Title to give the plot
        ylog : bool
            Displays the log of the y axis
        qt : bool
            If true, plots with qt.  Else creates an HTML page with bokeh.

    Returns : None

    Examples:
        >>> # Plot LPW.ELECTRON_DENSITY against spacecraft altitude.
        >>> pydivide.altplot(insitu, parameter=['LPW.ELECTRON_DENSITY','MAG.MSO_Y'], qt=False, ylog=True)


    '''
    
    if list:
        x = param_list(kp)
        for param in x:
            print(param)
        return
    
    # Check for orbit num rather than time string
    if isinstance(time, builtins.list):
        if isinstance(time[0], int):
            time = orbit_time(time[0], time[1])
    elif isinstance(time, int):
        time = orbit_time(time)
        
    # Check existence of parameter
    if parameter is None:
        print("Must provide an index (or name) for param to be plotted.")
        return
    # Store instrument and observation of parameter(s) in lists
    inst = []
    obs = []
    if type(parameter) is int or type(parameter) is str:
        a, b = get_inst_obs_labels(kp, parameter)
        inst.append(a)
        obs.append(b)
    else:
        for param in parameter:
            a, b = get_inst_obs_labels(kp, param)
            inst.append(a)
            obs.append(b)
    inst_obs = builtins.list(zip(inst, obs))

    # Check the time variable
    if time is not None:
        kp = range_select(kp, time)

    # Generate the altitude array
    z = []
    index = 0
    for i in kp['TimeString']:
        z.append(kp['SPACECRAFT']['ALTITUDE'][index])
        index += 1
    
    pytplot.store_data('sc_alt', data={'x': kp['Time'], 'y': z})

    # Cycle through the parameters, plotting each according to
    #  the given keywords
    names_to_plot = []
    legend_names = []
    iplot = 0  # subplot indexes on 1
    for inst, obs in inst_obs:
        # First, generate the dependent array from data
        y = []
        index = 0
        for i in kp['TimeString']:
            y.append(kp[inst][obs][index])
            index += 1

        names_to_plot.append('%s.%s' % (inst, obs))
        legend_names.append(obs)
        
        pytplot.store_data(names_to_plot[iplot], data={'x': kp['Time'], 'y': y})
        pytplot.options(names_to_plot[iplot], 'link', ['alt', 'sc_alt'])
        pytplot.options(names_to_plot[iplot], 'alt', 1)
        pytplot.options(names_to_plot[iplot], 'ylog', ylog)

        iplot += 1

    if sameplot:
        pytplot_name = ','.join(legend_names)
        pytplot.store_data(pytplot_name, data=names_to_plot)
        pytplot.options(pytplot_name, 'alt', 1)
        pytplot.options(pytplot_name, 'ylog', ylog)
        pytplot.options(pytplot_name, 'legend_names', legend_names)
        pytplot.tplot_options('title', title)
        pytplot.tplot_options('wsize', [1000, 300])
        pytplot.tplot(pytplot_name, bokeh=not qt)
        pytplot.del_data(pytplot_name)
    else:
        pytplot.tplot_options('title', title)
        pytplot.tplot_options('wsize', [1000, 300 * (iplot - 1)])
        pytplot.tplot(names_to_plot, bokeh=not qt)
        pytplot.del_data(names_to_plot)
    return
