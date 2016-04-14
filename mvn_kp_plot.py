from mvn_kp_utilities import param_list_sav
from mvn_kp_utilities import param_list
from mvn_kp_utilities import param_range
from mvn_kp_utilities import range_select
from mvn_kp_utilities import insufficient_input_range_select
from mvn_kp_utilities import make_time_labels
from mvn_kp_utilities import get_inst_obs_labels
from mvn_kp_utilities import find_param_from_index
from mvn_kp_utilities import remove_inst_tag


def mvn_kp_plot( kp, parameter=None, time=None, errors=None, 
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
    plt.show()
#--------------------------------------------------------------------------
