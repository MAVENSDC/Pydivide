# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pydivide

# INSITU_SEARCH'
#   Searches input in situ KP data structure based on min and/or max search parameters.'
# '
# x = insitu_search(insitu_in, parameter=parameter, min=min_value, max=max_value)
# '
# REQUIRED FIELDS'
# ***************'
#   insitu_in: in situ KP data structure (data structure output from read)'
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

from .utilities import get_inst_obs_labels
from .utilities import param_list
import builtins 

def mvn_kp_insitu_search(kp,
                         parameter,
                         min=None,
                         max=None,
                         list=False):

    print("This procedure was renamed, just use insitu_search")
    x = insitu_search(kp=kp, 
                      parameter=parameter, 
                      min=min, 
                      max=max, 
                      list=list)
    return x

def insitu_search(kp,
                  parameter,
                  min=None,
                  max=None,
                  list=False):
    
    if list:
        x = param_list(kp)
        for param in x:
            print(param)
        return
    
    if parameter is 'inbound':
        inbound_data = kp[kp['IOFlag'] == 'I']
        kp_temp = {}
        for df in kp:
            if kp[df] is not None:
                kp_temp[df] = kp[df][inbound_data]
        return kp_temp
        
    if parameter in 'outbound':
        outbound_data = kp[kp['IOFlag'] == 'O']
        kp_temp = {}
        for df in kp:
            if kp[df] is not None:
                kp_temp[df] = kp[df][outbound_data]
        return kp_temp
    
    if max is None:
        max = [float("inf")]*len(parameter)
    if min is None:
        min = [float("-inf")]*len(parameter)
    if not isinstance(min, builtins.list):
        min = [min]
    if not isinstance(max, builtins.list):
        max = [max]
    if not isinstance(parameter, builtins.list):
        parameter = [parameter]
    
    if len(parameter) == len(min) == len(max):
        inst = []
        obs = []
        for param in parameter:
            a,b = get_inst_obs_labels(kp,param)
            inst.append(a)
            obs.append(b)
        parameter_inst_obs = builtins.list(zip( inst, obs ))
        
        
        i=0
        bool_index = (kp['SPACECRAFT']['ALTITUDE'] > 0)
        for inst, obs in parameter_inst_obs:
            bool_index = bool_index & (kp[inst][obs] > min[i]) & (kp[inst][obs] < max[i])
            i+=1
            
        kp_temp = {}
        for df in kp:
            if kp[df] is not None:
                kp_temp[df] = kp[df][bool_index]
            
            
        return kp_temp
    else:
        print("Min/Max do not match the length of given parameters")
        return kp