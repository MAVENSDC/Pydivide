# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pydivide

import pytplot
import numpy as np
import builtins


def occultation(iuvs,
                sameplot=True,
                orbit_num=None,
                species=None,
                log=False,
                title='IUVS Occultation Observations',
                qt=True, exec_qt=True):
    '''
    Plot IUVS Stellar Occultation data against spacecraft altitude.

    Parameters:
        iuvs : dict
            iuvs kp data structure/dictionary read from file(s)
        orbit_num : list of int
            The orbit numbers to plot from the IUVS data structure
        species: list of str
            The species to plot.  Values can be "CO2", "O2", "O3", and "Temp."
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
        >>> # Plot CO2 density vs spacecraft altitude.
        >>> insitu, iuvs = pydivide.read(input_time=['2016-01-01', '2016-01-31'])
        >>> pydivide.occultation(iuvs, log=True, species=['CO2'], qt=False)
    '''
    
    retrieval_names_to_plot = []
    retrieval_legend_names = []
    dplot = 0
    
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
            if obs.lower()[0:-1] == 'occultation':
                if restrict_orbit and int(orbit[obs]['orbit_number']) not in orbit_num:
                    continue
                x = np.array(orbit[obs]['retrieval']['ALTITUDE'])
                for var in orbit[obs]['retrieval']:
                    if var.lower() != "altitude":
                        if restrict_species and var not in species:
                            continue
                        if not np.isnan(orbit[obs]['retrieval'][var]).all():
                            xmin.append(np.min(x))
                            xmax.append(np.max(x))
                            retrieval_names_to_plot.append(obs + '_retrieval_' + var + '_' +
                                                           str(orbit[obs]['orbit_number']))
                            retrieval_legend_names.append('Orbit ' + str(orbit[obs]['orbit_number']) + ' ' + var +
                                                          ' retrieval')
                            data = np.array(orbit[obs]['retrieval'][var])
                            alts = x[~np.isnan(data)]
                            data = data[~np.isnan(data)]
                            fake_times = np.arange(len(alts))
                            pytplot.store_data(retrieval_names_to_plot[dplot], data={'x': fake_times, 'y': data})
                            pytplot.store_data(retrieval_names_to_plot[dplot] + "_alt", data={'x': fake_times, 'y': alts})
                            pytplot.options(retrieval_names_to_plot[dplot], 'link',
                                            ['alt', retrieval_names_to_plot[dplot] + '_alt'])
                            pytplot.options(retrieval_names_to_plot[dplot], 'alt', 1)
                            dplot += 1
                                    
    if dplot == 0:
        print("There is no occultation retrieval data in the given IUVS variable")
        return
    
    list_of_plots = []
    if sameplot:
        pytplot.store_data('occultation_retrieval', data=retrieval_names_to_plot)
        list_of_plots.append('occultation_retrieval')
        pytplot.options('occultation_retrieval', 'alt', 1)
        if log:
            pytplot.options('occultation_retrieval', 'ylog', 1)
        pytplot.options('occultation_retrieval', 'legend_names', retrieval_legend_names)
    else:
        i = 0
        for d in retrieval_names_to_plot:
            list_of_plots.append(d)
            pytplot.options(d, 'ytitle', retrieval_legend_names[i])
            if log:
                pytplot.options(d, 'ylog', 1)
            i += 1
        i = 0
    pytplot.tplot_options('alt_range', [np.min(xmin), np.max(xmax)])
    pytplot.tplot_options('title', title)
    pytplot.tplot_options('wsize', [1000, 400 * len(list_of_plots)])
    pytplot.tplot(list_of_plots, bokeh=not qt, exec_qt=exec_qt, window_name='PYIDIVDE_Occultation_Plot')
    pytplot.del_data(list_of_plots)
    
    return
