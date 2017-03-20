
# MVN_KP_INSITU_SEARCH'
#   Searches input in situ KP data structure based on min and/or max search parameters.'
# '
# x = mvn_kp_insitu_search(insitu_in, parameter=parameter, min=min_value, max=max_value)
# '
# REQUIRED FIELDS'
# ***************'
#   insitu_in: in situ KP data structure (data structure output from mvn_kp_read)'
# '
# OPTIONAL FIELDS'
# ***************'
#   min: the minimum value of the parameter to be searched on (or array of values).'
#        One or more minimum values. If multiple parameters input & multiple min values input, each min'
#        value will correspond with each parameter (by array position). If multiple parameters & one min value,'
#        the min value is used for all parameters. Cannot enter more min values than parameters.'
#   max: the maximum value of the parameter to be searced on (or array of values)'
#        One or more maximum values. If multiple parameters input & multiple max values input, each max'
#        value will correspond with each parameter (by array position). If multiple parameters & one max value,'
#        the max value is used for all parameters. Cannot enter more max values than parameters.'

from .mvn_kp_utilities import get_inst_obs_labels

def mvn_kp_insitu_search(kp,
                         parameter,
                         min=None,
                         max=None):
    
    if max is None:
        max = [float("inf")]*len(parameter)
    if min is None:
        min = [float("-inf")]*len(parameter)
    if not isinstance(min, list):
        min = [min]
    if not isinstance(max, list):
        max = [max]
    if not isinstance(parameter, list):
        parameter = [parameter]
    
    if len(parameter) == len(min) == len(max):
        inst = []
        obs = []
        for param in parameter:
            a,b = get_inst_obs_labels(kp,param)
            inst.append(a)
            obs.append(b)
        parameter_inst_obs = list(zip( inst, obs ))
        
        
        i=0
        bool_index = (kp['SPACECRAFT']['Altitude Aeroid'] > 0)
        for inst, obs in parameter_inst_obs:
            bool_index = bool_index & (kp[inst][obs] > min[i]) & (kp[inst][obs] < max[i])
            i+=1
            
        kp_temp = {}
        for df in kp:
            kp_temp[df] = kp[df][bool_index]
            
            
        return kp_temp
    else:
        print("Min/Max do not match the length of given parameters")
        return kp