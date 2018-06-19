# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pydivide



## TO RUN THESE COMMANDS
#
# 1) Have the anaconda distribution of python installed
#
# 2) In command prompt, type "pip install pydivide"
#
# 3) After that, type "conda install -c bokeh nodejs"
#
# 4) After that, type "ipython"
#
# 5) IPython should start up.  Type "import pydivide" and to use these commands

import pydivide

#MVN_KP_DOWNLOAD_FILES
pydivide.mvn_kp_download_files(insitu=True, list_files=True)
pydivide.mvn_kp_download_files(start_date='2015-12-25', end_date='2015-12-31', insitu=True, list_files=True)
pydivide.mvn_kp_download_files(start_date='2015-12-25', end_date='2015-12-31', insitu=True, list_files=True, new_files=True)


#MVN_KP_DOWNLOAD_L2_FILES
#(Note the different name, that is because you can select data levels here)
pydivide.mvn_kp_download_sci_files(start_date='2015-12-25', end_date='2015-12-31', instruments=['swi','sta','ngi'], list_files=True, new_files=True)

#MVN_KP_READ
insitu, iuvs = pydivide.mvn_kp_read('2015-12-25')
insitu2, iuvs2 = pydivide.mvn_kp_read([2404, 2406])
#No new_files keyword implemented yet for mvn_kp_read
#insitu2, iuvs2 = pydivide.mvn_kp_read([2404, 2406], new_files=True)

#MVN_KP_3D
#Not a command yet

#MVN_KP_PLOT
pydivide.mvn_kp_plot(insitu, parameter='swia.hplus_density')
pydivide.mvn_kp_plot(insitu, list=True)
pydivide.mvn_kp_plot(insitu, parameter=[192,193,194])

#MVN_KP_TPLOT
#Not a command yet

#MVN_KP_STANDARDS
pydivide.mvn_kp_standards(insitu, all_plots=True) # Using all_plots seems to do bad things on some machines
pydivide.mvn_kp_standards(insitu, mag_mso=True, ngims_ions=True, wave=True)

#MVN_KP_ALTPLOT
pydivide.mvn_kp_altplot(insitu, parameter= 'MAG.MSO_X')

#MVN_KP_IUVS_LIMB
#Not a command yet

#MVN_KP_IUVS_CORONA
#Not a command yet

#MVN_KP_MAP2D
pydivide.mvn_kp_map2d(insitu, parameter=100)
pydivide.mvn_kp_map2d(insitu, parameter=100, basemap='mdim', subsolar=True)

#MVN_KP_INSITU_SEARCH
insitu_out = pydivide.mvn_kp_insitu_search(insitu, parameter='SPACECRAFT.ALTITUDE', min=1000, max=2000)
pydivide.mvn_kp_plot(insitu_out, parameter = 'spacecraft.altitude')

#MVN_KP_IUVS_SEARCH
#IUVS search is done in a similar way, no need for another example

#MVN_KP_BIN
import pytplot
import numpy as np
insitu_out = pydivide.mvn_kp_bin(insitu, 'SWIA.HPLUS_DENSITY', 'SPACECRAFT.ALTITUDE', binsize=10, avg=True, std=True)
pytplot.store_data('testing123', data={'x':np.arange(len(insitu_out[0])), 'y':insitu_out[0]})
pytplot.tplot('testing123')

#MVN_KP_ADD_DATA
import numpy as np
mag_total=np.sqrt(insitu['MAG']['MSO_X'].apply(lambda x: x**2) +insitu['MAG']['MSO_Y'].apply(lambda x: x**2)+insitu['MAG']['MSO_Z'].apply(lambda x: x**2))
insitu['MAG']['MAG_TOTAL'] = mag_total
pydivide.mvn_kp_plot(insitu, parameter = 'mag.mag_total')

#MVN_KP_RESAMPLE
insitu_resampled = pydivide.mvn_kp_resample(insitu, insitu['Time'])

#MVN_KP_INTERPOL_MODEL
dataout = pydivide.mvn_kp_interpol_model(insitu, file='C:/Mars Models/MGITM.nc')

#MVN_KP_CREATE_MODEL_MAP
pydivide.mvn_kp_create_model_maps(200, file='C:/Mars Models/MGITM.nc', fill=True)
pydivide.mvn_kp_map2d(insitu, basemap='C:/Mars Models/Model.png', mso=True)

