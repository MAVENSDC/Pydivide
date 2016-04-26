from mvn_kp_utilities import get_inst_obs_labels
import math
import numpy



def set_elements_of_multi_array_to_list(the_array):
    index = 0
    for i in the_array:
        if  hasattr(i, "__len__"):
            the_array[index] = set_elements_of_multi_array_to_list(i)
        else:
            the_array[index] = []
        index = index + 1
    return the_array

def append_values_of_list_from_indexes(the_list, location, to_append):
    testing = the_list
    if hasattr(location, "__len__"):
        for i in range(len(location)):
            testing = testing[location[i]]
        testing.append(to_append)
    else:
        testing=testing[location]
        testing.append(to_append)

def get_values_of_list_from_indexes(the_list, location):
    testing = the_list
    if hasattr(location, "__len__"):
        for i in range(len(location)):
            testing = testing[location[i]]
        return testing
    else:
        testing=testing[location]
        return testing


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
    else:
        for param in parameter:
            a,b = get_inst_obs_labels(kp,param)
            inst.append(a)
            obs.append(b)
    parameter_inst_obs = zip( inst, obs )
    
    # Store instrument and observation of parameter(s) in lists
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
    
    total_fields = len(bin_by)

    if mins == None:
        mins = []
        for inst, obs in bin_by_inst_obs:
            mins.append(kp[inst][obs].min(skipna=True))
        
    ranges = []
    total_bins = []
        
    if maxs == None:
        maxs = []
        for inst, obs in bin_by_inst_obs:
            maxs.append(kp[inst][obs].max(skipna=True))
        
    for i in range(total_fields):        
        ranges.append(maxs[i]-mins[i])
        total_bins.append(int(math.ceil(ranges[i]/binsizes[i])))
    
    #Initialize the output and density arrays
    output_array = numpy.zeros(total_bins)
    density = numpy.zeros(total_bins)
    
    output_list = output_array.tolist()
    output_list  = set_elements_of_multi_array_to_list(output_list)
    
    
    
    for i in range(len(kp[parameter_inst_obs[0][0]][parameter_inst_obs[0][1]])):
        
        #Get the location in the output array to place the ith value of the parameter
        j=0
        data_value_indexes = []
        
        for bin_by_inst, bin_by_obs in bin_by_inst_obs:
            data_value = kp[bin_by_inst][bin_by_obs][i]
            dv = math.floor((data_value-mins[j])/binsizes[j])
            data_value_indexes.append(int(dv))
            j = j + 1
        
        
        data_value_indexes = tuple(data_value_indexes)
        append_values_of_list_from_indexes(output_list, data_value_indexes, kp[parameter_inst_obs[0][0]][parameter_inst_obs[0][1]][i])
        #output[data_value_indexes] = output[data_value_indexes] + kp[parameter_inst_obs[0][0]][parameter_inst_obs[0][1]][i]
        density[data_value_indexes] = density[data_value_indexes] + 1
        
    if median:
        median_array=numpy.zeros(total_bins)
        median_array.fill(numpy.nan)
    if avg == True:
        average_array=numpy.zeros(total_bins)
        average_array.fill(numpy.nan)
    if std == True:
        std_array=numpy.zeros(total_bins)
        std_array.fill(numpy.nan)
        
    for i in range(len(kp[parameter_inst_obs[0][0]][parameter_inst_obs[0][1]])):
        
        #Get the location in the output array to place the ith value of the parameter
        j=0
        data_value_indexes = []
        
        for bin_by_inst, bin_by_obs in bin_by_inst_obs:
            data_value = kp[bin_by_inst][bin_by_obs][i]
            dv = math.floor((data_value-mins[j])/binsizes[j])
            data_value_indexes.append(int(dv))
            j = j + 1
        
        
        data_value_indexes = tuple(data_value_indexes)
        if median:
            median_array[data_value_indexes] = numpy.median(get_values_of_list_from_indexes(output_list, data_value_indexes))
        if avg or std:
            average_array[data_value_indexes] = numpy.sum(get_values_of_list_from_indexes(output_list, data_value_indexes))/density[data_value_indexes]
        if std:
            squared_total = []
            for x in get_values_of_list_from_indexes(output_list, data_value_indexes):
                squared_total.append((x-avg[data_value_indexes])*(x-avg[data_value_indexes]))
            std_array[data_value_indexes] = numpy.sqrt((numpy.sum(squared_total)/density[data_value_indexes]))
            
    print 'Hello'
        

        
    