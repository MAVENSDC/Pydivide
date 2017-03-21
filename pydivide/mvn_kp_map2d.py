from .mvn_kp_utilities import get_inst_obs_labels
import pytplot
import numpy as np
from datetime import datetime
import builtins
import math
from .mvn_kp_utilities import range_select

def mvn_kp_map2d( kp, 
                  parameter=None, 
                  time=None, 
                  list=False, 
                  basemap=None,
                  color_table=None,
                  subsolar=False,
                  mso=False,
                  map_limit=None,
                  **kwargs ):



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
    if time == None:
        istart, iend = 0,np.count_nonzero(kp['Orbit'])-1
    else:
        istart,iend = range_select(kp,time)

    # Generate the altitude array
    if mso:
        x = kp['SPACECRAFT']['MSO X'][istart:iend].as_matrix()
        y = kp['SPACECRAFT']['MSO Y'][istart:iend].as_matrix()
        z = kp['SPACECRAFT']['MSO Z'][istart:iend].as_matrix()
        r = np.sqrt((x**2) + (y**2) + (z**2))
        lat = (90 - np.arccos(z/r)*(180/math.pi))
        lon = (np.arctan2(y,x)*(180/math.pi)) + 180
    else:
        lon = kp['SPACECRAFT']['GEO Longitude'][istart:iend]
        lat = kp['SPACECRAFT']['GEO Latitude'][istart:iend]
    
    alt = kp['SPACECRAFT']['Altitude Aeroid'][istart:iend]
    # Cycle through the parameters, plotting each according to
    #  the given keywords
    #
    names_to_plot=[]
    iplot = 0 # subplot indexes on 1
    for inst,obs in inst_obs:
        #
        # First, generate the dependent array from data
        y = kp[inst][obs][istart:iend]
        
        if subsolar and mso==False:
            pytplot.store_data('%s.%s'%(inst,obs), 
                               data={'x':[lon, 
                                          lat], 
                                     'y':y})
            pytplot.options('%s.%s'%(inst,obs), 'map', 1)
            pytplot.store_data('subsolar', 
                               data={'x':[kp['SPACECRAFT']['Subsolar Point GEO Longitude'][istart:iend],
                                          kp['SPACECRAFT']['Subsolar Point GEO Latitude'][istart:iend]], 
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
            
        iplot = iplot + 1
    
    
        
    pytplot.tplot_options('wsize', [1000,300*(iplot)])
    pytplot.tplot(names_to_plot)
        
