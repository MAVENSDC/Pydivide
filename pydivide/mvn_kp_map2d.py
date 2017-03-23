from .mvn_kp_utilities import get_inst_obs_labels, param_list, range_select, orbit_time
import pytplot
import numpy as np
from datetime import datetime
import builtins
import math
import os

def mvn_kp_map2d( kp, 
                  parameter=None, 
                  time=None, 
                  list=False, 
                  color_table=None,
                  subsolar=False,
                  mso=False,
                  map_limit=None,
                  basemap=None,
                  alpha=None,
                  **kwargs ):
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


    # Check the time variable
    if time != None:
        kp = range_select(kp,time)

    # Generate the altitude array
    if mso:
        x = kp['SPACECRAFT']['MSO X'].as_matrix()
        y = kp['SPACECRAFT']['MSO Y'].as_matrix()
        z = kp['SPACECRAFT']['MSO Z'].as_matrix()
        r = np.sqrt((x**2) + (y**2) + (z**2))
        lat = (90 - np.arccos(z/r)*(180/math.pi))
        lon = (np.arctan2(y,x)*(180/math.pi)) + 180
    else:
        lon = kp['SPACECRAFT']['GEO Longitude']
        lat = kp['SPACECRAFT']['GEO Latitude']
    
    alt = kp['SPACECRAFT']['Altitude Aeroid']
    # Cycle through the parameters, plotting each according to
    #  the given keywords
    #
    names_to_plot=[]
    iplot = 0 # subplot indexes on 1
    for inst,obs in inst_obs:
        #
        # First, generate the dependent array from data
        y = kp[inst][obs]
        
        if subsolar and mso==False:
            pytplot.store_data('%s.%s'%(inst,obs), 
                               data={'x':[lon, 
                                          lat], 
                                     'y':y})
            pytplot.options('%s.%s'%(inst,obs), 'map', 1)
            pytplot.store_data('subsolar', 
                               data={'x':[kp['SPACECRAFT']['Subsolar Point GEO Longitude'],
                                          kp['SPACECRAFT']['Subsolar Point GEO Latitude']], 
                                    'y':alt})
            pytplot.options('subsolar', 'map', 1)
            names_to_plot.append('%s.%s.%s'%(inst,obs,'subsolar'))
            pytplot.store_data(names_to_plot[iplot], data=['%s.%s'%(inst,obs),'subsolar'])
            pytplot.options(names_to_plot[iplot], 'map', 1)
            pytplot.options(names_to_plot[iplot], 'colormap', ['magma', 'yellow'])
        else:
            names_to_plot.append('%s.%s'%(inst,obs))
            pytplot.store_data(names_to_plot[iplot], data={'x':[lon, lat], 'y':y})
            pytplot.options(names_to_plot[iplot], 'map', 1)
        
        if basemap and mso==False:
            if basemap=='mola':
                map_file='MOLA_color_2500x1250.jpg'
            elif basemap=='mola_bw':
                map_file='MOLA_BW_2500x1250.jpg'
            elif basemap=='mdim':
                map_file='MDIM_2500x1250.jpg'
            elif basemap=='elevation':
                map_file='MarsElevation_2500x1250.jpg'
            elif basemap=='mag':
                map_file='MAG_Connerny_2005.jpg'
            else:
                break    
            pytplot.options(names_to_plot[iplot], 
                            'basemap', 
                            os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                         'basemaps', 
                                         map_file))
            if alpha:
                pytplot.options(names_to_plot[iplot], 'alpha', alpha)
            
        iplot = iplot + 1
    
    
        
    pytplot.tplot_options('wsize', [1000,300*(iplot)])
    pytplot.tplot(names_to_plot)
        
