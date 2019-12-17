# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pydivide

from .utilities import get_inst_obs_labels, param_list, range_select, orbit_time
import pytplot
import numpy as np
import builtins
import math
import os


def map2d(kp,
          parameter=None,
          time=None,
          list=False,
          subsolar=False,
          mso=False,
          basemap=None,
          alpha=None,
          title='MAVEN Mars',
          qt=True, exec_qt=True):
    '''
    Produces a 2D map of Mars, either in the planetocentric or MSO coordinate
    system, with the MAVEN orbital projection and a variety of basemaps.
    Spacecraft orbital path may be colored by a given insitu KP data value

    Parameters:
        kp : dict
            insitu kp data structure/dictionary read from file(s)
        parameter : list of str/int
            The parameter(s) to be plotted.  Can be provided as
            integers (by index) or strings (by name: inst.obs).  If a
            single parameter is provided, it must be an int or str.  If
            several are provided it must be a list.  A list may contain
            a mixture of data types.
        time : list of str
            Two-element list of strings or integers indicating the
            range of Time to be plotted.  At present, there are no
            checks on whether provided Times are within provided data
        color_table : str
            Specifies color table to use for plotting
        subsolar : bool
            Plot path of subsolar point
        mso : bool
            Plot using MSO map projection
        map_limit : list
            Set the bounding box on the map in lat/lon coordinates [x0,y0,x1,y1]
        basemap : str
            Name of the basemap on which the spacecraft data with be overlaid.  Choices are
            • ‘mdim’: Mars Digital Image Model
            • ‘mola’: Mars Topography (color)
            • ‘mola_bw’: Mars Topography (black and white)
            • ‘mag’: Mars Crustal Magnetism
            • ‘<dir_path>/file.png’: User-defined basemap
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
        exec_qt : bool
            If False, does not run the event loop for pyqtgraph.

    Returns :
        None

    Examples:
        >>> # Plot spacecraft altitude along MAVEN surface orbital track.
        >>> pydivide.map2d(insitu, 'spacecraft.altitude')

        >>> # Plot spacecraft altitude along MAVEN surface orbital track using MOLA altimetry basemap; plot subsolar point path.
        >>> pydivide.map2d(insitu, 'spacecraft.altitude', basemap='mola', subsolar=True)
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
        nparam = 1
    else:
        nparam = len(parameter)
        for param in parameter:
            a, b = get_inst_obs_labels(kp, param)
            inst.append(a)
            obs.append(b)
    inst_obs = builtins.list(zip(inst, obs))

    # Check the time variable
    if time is not None:
        kp = range_select(kp, time)

    # Generate the altitude array
    if mso:
        x = kp['SPACECRAFT']['MSO_X'].values
        y = kp['SPACECRAFT']['MSO_Y'].values
        z = kp['SPACECRAFT']['MSO_Z'].values
        r = np.sqrt((x**2) + (y**2) + (z**2))
        lat = (90 - np.arccos(z/r) * (180/math.pi))
        lon = (np.arctan2(y, x) * (180/math.pi)) + 180
    else:
        lon = kp['SPACECRAFT']['SUB_SC_LONGITUDE']
        lat = kp['SPACECRAFT']['SUB_SC_LATITUDE']
    
    alt = kp['SPACECRAFT']['ALTITUDE']

    # Cycle through the parameters, plotting each according to
    #  the given keywords
    names_to_plot = []
    iplot = 0  # subplot indexes on 1
    for inst, obs in inst_obs:
        #
        # First, generate the dependent array from data
        y = kp[inst][obs]
        
        if subsolar and not mso:
            pytplot.store_data('sc_lon', data={'x': kp['Time'], 'y': lon})
            pytplot.store_data('sc_lat', data={'x': kp['Time'], 'y': lat})
            pytplot.store_data('%s.%s' % (inst, obs), data={'x': kp['Time'], 'y': y})
            pytplot.options('%s.%s' % (inst, obs), 'link', ['lon', 'sc_lon'])
            pytplot.options('%s.%s' % (inst, obs), 'link', ['lat', 'sc_lat'])
            pytplot.options('%s.%s' % (inst, obs), 'map', 1)
            
            pytplot.store_data('ss_lon', data={'x': kp['Time'], 'y': kp['SPACECRAFT']['SUBSOLAR_POINT_GEO_LONGITUDE']})
            pytplot.store_data('ss_lat', data={'x': kp['Time'], 'y': kp['SPACECRAFT']['SUBSOLAR_POINT_GEO_LATITUDE']})
            pytplot.store_data('subsolar', data={'x': kp['Time'], 'y': alt})
            pytplot.options('subsolar', 'link', ['lon', 'ss_lon'])
            pytplot.options('subsolar', 'link', ['lat', 'ss_lat'])
            pytplot.options('subsolar', 'map', 1)
            names_to_plot.append('%s.%s.%s' % (inst, obs, 'subsolar'))
            pytplot.store_data(names_to_plot[iplot], data=['%s.%s' % (inst, obs), 'subsolar'])
            pytplot.options(names_to_plot[iplot], 'map', 1)
            pytplot.options(names_to_plot[iplot], 'colormap', ['magma', 'yellow'])
        else:
            names_to_plot.append('%s.%s' % (inst, obs))
            pytplot.store_data('sc_lon', data={'x': kp['Time'], 'y': lon})
            pytplot.store_data('sc_lat', data={'x': kp['Time'], 'y': lat})
            pytplot.store_data(names_to_plot[iplot], data={'x': kp['Time'], 'y': y})
            pytplot.options(names_to_plot[iplot], 'link', ['lon', 'sc_lon'])
            pytplot.options(names_to_plot[iplot], 'link', ['lat', 'sc_lat'])
            pytplot.options(names_to_plot[iplot], 'map', 1)
        
        if basemap:
            if basemap == 'mola':
                map_file = os.path.join(os.path.dirname(__file__), 'basemaps', 'MOLA_color_2500x1250.jpg')
            elif basemap == 'mola_bw':
                map_file = os.path.join(os.path.dirname(__file__), 'basemaps', 'MOLA_BW_2500x1250.jpg')
            elif basemap == 'mdim':
                map_file = os.path.join(os.path.dirname(__file__), 'basemaps', 'MDIM_2500x1250.jpg')
            elif basemap == 'elevation':
                map_file = os.path.join(os.path.dirname(__file__), 'basemaps', 'MarsElevation_2500x1250.jpg')
            elif basemap == 'mag':
                map_file = os.path.join(os.path.dirname(__file__), 'basemaps', 'MAG_Connerny_2005.jpg')
            else:
                map_file = basemap
            pytplot.options(names_to_plot[iplot], 
                            'basemap', 
                            map_file)
            if alpha:
                pytplot.options(names_to_plot[iplot], 'alpha', alpha)
            
        iplot += 1

    pytplot.tplot_options('title', title)
    pytplot.tplot_options('wsize', [1000, 500 * iplot])
    pytplot.tplot(names_to_plot, bokeh=not qt, exec_qt=exec_qt)
    pytplot.del_data('ss_lon')
    pytplot.del_data('ss_lat')
    pytplot.del_data('sc_lon')
    pytplot.del_data('sc_lat')
    pytplot.del_data(names_to_plot)

    return
