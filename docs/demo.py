"""
TO RUN THESE COMMANDS

1) Have the anaconda distribution of python installed

2) In command prompt, type "pip install pydivide"

3) After that, type "conda install -c bokeh nodejs"

4) After that, type "ipython"

5) IPython should start up.  Type "import pydivide" and to use these commands
"""

import pydivide
import pytplot
import numpy as np

# MVN_KP_DOWNLOAD_FILES
pydivide.download_files(insitu=True, list_files=True)
pydivide.download_files(start_date='2015-12-25', end_date='2015-12-31', insitu=True, list_files=True)
pydivide.download_files(start_date='2015-12-25', end_date='2015-12-31', insitu=True, list_files=True, new_files=True)


# MVN_KP_DOWNLOAD_L2_FILES
# (Note the different name, that is because you can select data levels here)
pydivide.download_files(start_date='2015-12-25', end_date='2015-12-31', instruments=['swi', 'sta', 'ngi'],
                        list_files=True, new_files=True)

# MVN_KP_READ
insitu, iuvs = pydivide.read('2015-12-25')
insitu2, iuvs2 = pydivide.read([2404, 2406])

# MVN_KP_PLOT
pydivide.plot(insitu, parameter='SWIA.HPLUS_DENSITY')
pydivide.plot(insitu, list=True)
pydivide.plot(insitu, parameter=[192, 193, 194])

# MVN_KP_STANDARDS
# pydivide.standards(insitu, all_plots=True)  # Using all_plots seems to do bad things on some machines
pydivide.standards(insitu, mag_mso=True, ngims_ions=True, wave=True)

# MVN_KP_ALTPLOT
pydivide.altplot(insitu, parameter='MAG.MSO_X')

# MVN_KP_MAP2D
pydivide.map2d(insitu, parameter=100)
pydivide.map2d(insitu, parameter=100, basemap='mdim', subsolar=True)

# MVN_KP_INSITU_SEARCH
insitu_out = pydivide.insitu_search(insitu, parameter='SPACECRAFT.ALTITUDE', min=1000, max=2000)
pydivide.plot(insitu_out, parameter='SPACECRAFT.ALTITUDE')

# MVN_KP_BIN
insitu_out = pydivide.bin(insitu, 'SWIA.HPLUS_DENSITY', 'SPACECRAFT.ALTITUDE', binsize=10, avg=True, std=True)
pytplot.store_data('testing123', data={'x': np.arange(len(insitu_out[0])), 'y': insitu_out[0]})
pytplot.tplot('testing123')

# MVN_KP_ADD_DATA
mag_total = np.sqrt(insitu['MAG']['MSO_X'].apply(lambda x: x ** 2) + insitu['MAG']['MSO_Y'].apply(lambda x: x ** 2) +
                    insitu['MAG']['MSO_Z'].apply(lambda x: x ** 2))
insitu['MAG']['MAG_TOTAL'] = mag_total
pydivide.plot(insitu, parameter='MAG.MAG_TOTAL')

# MVN_KP_RESAMPLE
insitu_resampled = pydivide.resample(insitu, insitu['Time'])

# MVN_KP_INTERPOL_MODEL
# To download and use MAVEN models, see https://lasp.colorado.edu/maven/sdc/team/pages/models.html
dataout = pydivide.interpol_model(insitu, file='/Users/juba8233/Desktop/MGITM_LS270_F200_150615.nc')

# MVN_KP_CREATE_MODEL_MAP
pydivide.create_model_maps(200, file='/Users/juba8233/Desktop/MGITM_LS270_F200_150615.nc', fill=True)
# For the 'basemap' keyword arg below, you can choose between mola, mola_bw, mdim, elevation, mag,
# or you can put the full pathname to a basemap created by pydivide.create_model_maps (e.g., like in the above example)
pydivide.map2d(insitu, parameter='SWIA.HPLUS_TEMPERATURE', basemap='mola_bw', mso=True)
