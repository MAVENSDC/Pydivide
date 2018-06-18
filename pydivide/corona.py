# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pydivide

import pytplot
import numpy as np
import builtins

def corona(iuvs,
           sameplot=True,
           density=True,
           radiance=True,
           orbit_num=None,
           species=None,
           log=False,
           title='IUVS Corona Observations',
           qt=True):
    
    density_names_to_plot=[]
    density_legend_names = []
    dplot=0
    
    radiance_names_to_plot=[]
    radiance_legend_names = []
    rplot=0
    
    if not isinstance(species, builtins.list):
        species = [species]
    
    if not isinstance(orbit_num, builtins.list):
        orbit_num = [orbit_num]
        
    if orbit_num != [None]:
        restrict_orbit = True
    else:
        restrict_orbit = False
        
    if species != [None]:
        restrict_species = True
    else:
        restrict_species = False
    
    xmin = []
    xmax = []
    
    for orbit in iuvs:
        for obs in orbit:
            if obs.lower() == 'corona_lores_high':
                if restrict_orbit and int(orbit[obs]['orbit_number']) not in orbit_num:
                    continue
                if density:
                    x = np.array(orbit[obs]['density']['ALTITUDE'])
                    for var in orbit[obs]['density']:
                        if var.lower() != "altitude":
                            if restrict_species and var not in species:
                                continue
                            if not np.isnan(orbit[obs]['density'][var]).all():
                                xmin.append(np.min(x))
                                xmax.append(np.max(x))
                                density_names_to_plot.append(obs+'_density_'+var+'_'+str(orbit[obs]['orbit_number']))
                                density_legend_names.append('Orbit '+ str(orbit[obs]['orbit_number']) + ' ' + var+' density')
                                data = np.array(orbit[obs]['density'][var])
                                alts = x[~np.isnan(data)]
                                data = data[~np.isnan(data)]
                                fake_times = np.arange(len(alts))
                                pytplot.store_data(density_names_to_plot[dplot], data={'x':fake_times, 'y':data})
                                pytplot.store_data(density_names_to_plot[dplot]+"_alt", data={'x':fake_times, 'y':alts})
                                pytplot.options(density_names_to_plot[dplot], "link", ['alt', density_names_to_plot[dplot]+"_alt"])
                                pytplot.options(density_names_to_plot[dplot], 'alt', 1)
                                pytplot.options(density_names_to_plot[dplot], 'alt', 1)
                                dplot+=1
                if radiance:
                    x = np.array(orbit[obs]['radiance']['ALTITUDE'])
                    for var in orbit[obs]['radiance']:
                        if var.lower() != "altitude":
                            if restrict_species and var not in species:
                                continue
                            if not np.isnan(orbit[obs]['radiance'][var]).all():
                                xmin.append(np.min(x))
                                xmax.append(np.max(x))
                                radiance_names_to_plot.append(obs+'_radiance_'+var+'_'+str(orbit['corona_lores_high']['orbit_number']))
                                radiance_legend_names.append('Orbit '+ str(orbit[obs]['orbit_number']) + ' ' + var+' radiance')
                                data = np.array(orbit[obs]['radiance'][var])
                                alts = x[~np.isnan(data)]
                                data = data[~np.isnan(data)]
                                fake_times = np.arange(len(alts))
                                pytplot.store_data(radiance_names_to_plot[rplot], data={'x':fake_times, 'y':data})
                                pytplot.store_data(radiance_names_to_plot[rplot]+"_alt", data={'x':fake_times, 'y':alts})
                                pytplot.options(radiance_names_to_plot[rplot], "link", ['alt', radiance_names_to_plot[rplot]+"_alt"])
                                pytplot.options(radiance_names_to_plot[rplot], 'alt', 1)
                                rplot+=1
                                    
    if radiance and rplot == 0:
        print("There is no corona radiance data in the given IUVS variable")
        radiance = False
    if density and dplot == 0:
        print("There is no corona density data in the given IUVS variable")
        density = False
    
    list_of_plots = []
    if sameplot:
        if density:
            pytplot.store_data('corona_lores_high_density', data=density_names_to_plot)
            list_of_plots.append('corona_lores_high_density')
            pytplot.options('corona_lores_high_density', 'alt', 1)
            if log:
                pytplot.options('corona_lores_high_density', 'ylog', 1)
            pytplot.options('corona_lores_high_density', 'legend_names', density_legend_names)
            
        if radiance:
            pytplot.store_data('corona_lores_high_radiance', data=radiance_names_to_plot)
            list_of_plots.append('corona_lores_high_radiance')
            pytplot.options('corona_lores_high_radiance', 'alt', 1)
            if log:
                pytplot.options('corona_lores_high_radiance', 'ylog', 1)
            pytplot.options('corona_lores_high_radiance', 'legend_names', radiance_legend_names)
    else:
        i=0
        for d in density_names_to_plot:
            list_of_plots.append(d)
            pytplot.options(d, 'ytitle', density_legend_names[i])
            if log:
                pytplot.options(d, 'ylog', 1)
            i+=1
        i=0
        for r in radiance_names_to_plot:
            list_of_plots.append(r)
            pytplot.options(r, 'ytitle', radiance_legend_names[i])
            if log:
                pytplot.options(r, 'ylog', 1)
            i+=1
    pytplot.tplot_options('alt_range', [np.min(xmin), np.max(xmax)])
    pytplot.tplot_options('title', title)
    pytplot.tplot_options('wsize', [1000,400*len(list_of_plots)])
    pytplot.tplot(list_of_plots, bokeh=not qt)
    pytplot.del_data(list_of_plots)
    
    return