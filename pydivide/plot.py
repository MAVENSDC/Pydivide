# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pydivide

from .utilities import get_inst_obs_labels, param_list, orbit_time
import pytplot
import pandas as pd
import builtins
import pydivide

def plot(kp,
         parameter=None,
         time=None,
         errors=None,
         sameplot=True,
         list=False, title='',
         qt=True, exec_qt=True,
         log=False):
    '''

    Plot time-series data from insitu data structure.

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
        qt : bool
            If true, plots with qt.  Else creates an HTML page with bokeh.
        exec_qt : bool
            If False, does not run the event loop for pyqtgraph.

    Returns : None

    Examples :
    >>> # Plot SWIA H+ density.
    >>> pydivide.plot(insitu,parameter='swia.hplus_density')
    >>> # Plot SWIA H+ density and altitude in the same window.
    >>> pydivide.plot(insitu,parameter=['swia.hplus_density', 'spacecraft.altitude'],sameplot=True)

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
        inst.append(a.upper())
        obs.append(b.upper())
        nparam = 1
    else:
        nparam = len(parameter)
        for param in parameter:
            a, b = get_inst_obs_labels(kp, param)
            inst.append(a.upper())
            obs.append(b.upper())
    inst_obs = builtins.list(zip(inst, obs))

    # Cycle through the parameters, plotting each according to
    #  the given keywords
    #
    iplot = 1  # subplot indexes on 1
    legend_names = []

    y_list = pydivide.tplot_varcreate(kp, instruments=inst, observations=obs)
    for inst_temp, obs_temp in inst_obs:
        legend_names.append(obs_temp)
        iplot += 1
    if time is not None:
        pytplot.xlim(time[0], time[1])

    if sameplot:
        pytplot_name = ''.join(legend_names)
        pytplot.store_data(pytplot_name, data=y_list)
        pytplot.options(pytplot_name, 'legend_names', legend_names)
        pytplot.options(pytplot_name, 'ylog', log)
        pytplot.link(pytplot_name, "mvn_kp::spacecraft::altitude", link_type='alt')
        pytplot.link(pytplot_name, "mvn_kp::spacecraft::mso_x", link_type='x')
        pytplot.link(pytplot_name, "mvn_kp::spacecraft::mso_y", link_type='y')
        pytplot.link(pytplot_name, "mvn_kp::spacecraft::mso_z", link_type='z')
        pytplot.link(pytplot_name, "mvn_kp::spacecraft::geo_x", link_type='geo_x')
        pytplot.link(pytplot_name, "mvn_kp::spacecraft::geo_y", link_type='geo_y')
        pytplot.link(pytplot_name, "mvn_kp::spacecraft::geo_z", link_type='geo_z')
        pytplot.link(pytplot_name, "mvn_kp::spacecraft::sub_sc_longitude", link_type='lon')
        pytplot.link(pytplot_name, "mvn_kp::spacecraft::sub_sc_latitude", link_type='lat')
        pytplot.tplot_options('title', title)
        pytplot.tplot_options('wsize', [1000, 300])
        pytplot.tplot(pytplot_name, bokeh=not qt, exec_qt=exec_qt, window_name='PYDIVIDE_PLOT')
    else:
        pytplot.tplot_options('title', title)
        pytplot.tplot_options('wsize', [1000, 300 * (iplot - 1)])
        pytplot.tplot(y_list, bokeh=not qt, exec_qt=exec_qt, window_name='PYDIVIDE_PLOT')

    return
