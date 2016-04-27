from mvn_kp_utilities import get_inst_obs_labels
from mvn_kp_utilities import initialize_list
from mvn_kp_utilities import place_values_in_list
from mvn_kp_utilities import get_values_from_list
import math
import numpy

def mvn_kp_bin(kp,
               parameter=None,
               bin_by=None,
               mins=None,
               maxs=None,
               binsizes=None,
               std=False,
               avg=False,
               density=False,
               median=False):
    #
    #ERROR CHECKING
    #
    if parameter == None: 
        print "Must provide an index (or name) for param to be plotted."
        return
    
    if bin_by == None: 
        print "Must provide parameters to be binned by."
        return
    
    if avg==False and std==False and median==False and density==False:
        print "Must select array(s) to return (avg, std, median, density)."
        return
    #
    # Store instrument and observation of parameter in lists
    #
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
    parameter_inst_obs = zip( inst, obs )
    
    #
    # Store instrument and observation of "bin by" values in lists
    #
    inst = []
    obs = []
    if type(bin_by) is int or type(bin_by) is str:
        a,b = get_inst_obs_labels( kp, bin_by )
        inst.append(a)
        obs.append(b)
    else:
        for param in bin_by:
            a,b = get_inst_obs_labels(kp,param)
            inst.append(a)
            obs.append(b)       
    bin_by_inst_obs = zip( inst, obs )
    
    
    #
    #Calculate the dimensions of the binned array
    #Using the min/max values and the bin sizes
    #
    total_fields = len(bin_by)
    ranges = []
    total_bins = []
    if mins == None:
        mins = []
        for inst, obs in bin_by_inst_obs:
            mins.append(kp[inst][obs].min(skipna=True))
    if maxs == None:
        maxs = []
        for inst, obs in bin_by_inst_obs:
            maxs.append(kp[inst][obs].max(skipna=True))
        
    for i in range(total_fields):        
        ranges.append(maxs[i]-mins[i])
        total_bins.append(int(math.ceil(ranges[i]/binsizes[i])))
    
    #
    #Initialize the binned_list (a list of every value at a certain bin)
    #Initialize the density array (the number of values binned into a bin)
    #
    binned_array = numpy.zeros(total_bins)
    density = numpy.zeros(total_bins)
    binned_list = binned_array.tolist()
    binned_list  = initialize_list(binned_list)
    
    
    #
    #Loop through the KP to place the data into the correct bin
    #
    for i in range(len(kp[parameter_inst_obs[0][0]][parameter_inst_obs[0][1]])):
        #
        #Cannot do anything with NaNs.  Ignore them and continue.  
        #
        if math.isnan(kp[parameter_inst_obs[0][0]][parameter_inst_obs[0][1]][i]):
            continue
        #
        #Find out where to place i
        #
        j=0
        data_value_indexes = []
        for bin_by_inst, bin_by_obs in bin_by_inst_obs:
            data_value = kp[bin_by_inst][bin_by_obs][i]
            dv = math.floor((data_value-mins[j])/binsizes[j])
            data_value_indexes.append(int(dv))
            j = j + 1
        
        #
        #Populate binned_list in the proper spot, and add one to the density at that spot
        #
        data_value_indexes = tuple(data_value_indexes)
        place_values_in_list(binned_list, data_value_indexes, kp[parameter_inst_obs[0][0]][parameter_inst_obs[0][1]][i])
        density[data_value_indexes] = density[data_value_indexes] + 1
    
    #
    #Create arrays based on keywords
    #
    if median:
        median_array=numpy.zeros(total_bins)
        median_array.fill(numpy.nan)
    if avg == True:
        average_array=numpy.zeros(total_bins)
        average_array.fill(numpy.nan)
    if std == True:
        std_array=numpy.zeros(total_bins)
        std_array.fill(numpy.nan)
        
    #
    #Loop through the KP one more time to calculate median, avg, std.
    #This is necessary because we cannot calculate the median without knowing all the numbers 
    #in each bin first.
    #
    for i in range(len(kp[parameter_inst_obs[0][0]][parameter_inst_obs[0][1]])):
        #
        #Cannot do anything with NaNs.  Ignore them and continue.  
        #
        if math.isnan(kp[parameter_inst_obs[0][0]][parameter_inst_obs[0][1]][i]):
            continue
        #
        #Find out where to place i
        #
        j=0
        data_value_indexes = []
        
        for bin_by_inst, bin_by_obs in bin_by_inst_obs:
            data_value = kp[bin_by_inst][bin_by_obs][i]
            dv = math.floor((data_value-mins[j])/binsizes[j])
            data_value_indexes.append(int(dv))
            j = j + 1
        
        #
        #Calculate the mean/median/mode from the values in "output_list"
        #
        data_value_indexes = tuple(data_value_indexes)
        if median:
            median_array[data_value_indexes] = numpy.nanmedian(get_values_from_list(binned_list, data_value_indexes))
        if avg or std:
            average_array[data_value_indexes] = numpy.nansum(get_values_from_list(binned_list, data_value_indexes))/density[data_value_indexes]
        if std:
            squared_total = []
            for x in get_values_from_list(binned_list, data_value_indexes):
                squared_total.append((x-average_array[data_value_indexes])*(x-average_array[data_value_indexes]))
            std_array[data_value_indexes] = numpy.sqrt((numpy.sum(squared_total)/density[data_value_indexes]))
            
    #RETURN MEDIAN/AVERAGE/STANDARD DEVIATION
    return_list = []
    if median:
        return_list.append(median_array)
    if avg:
        return_list.append(average_array)
    if std:
        return_list.append(std_array)
    #
    #Print out a little cheat sheet so people know what is in the array they're getting
    #
    print 'Now returning binned data'
    dimension = 0
    for bin_by_inst, bin_by_obs in bin_by_inst_obs:
        print 'Dimension ' + str(dimension) + ' is ' + bin_by_obs
        print '    Range: ['+str(mins[dimension])+', '+str(mins[dimension] + binsizes[dimension])+', ... '+str(mins[dimension] + (binsizes[dimension]*(total_bins[dimension]-2)))+', '+str(mins[dimension] + (binsizes[dimension]*(total_bins[dimension]-1)))+']' 
        dimension = dimension+1
    
    
    return return_list
            

        

        
    