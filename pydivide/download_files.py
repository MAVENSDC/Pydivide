# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pydivide

###############################################################################
#
# Download Files Section
#
###############################################################################

from . import download_files_utilities as utils
from .utilities import orbit_time
from dateutil.parser import parse

     
def download_files(filenames=None,
                   instruments=None, 
                   list_files=False,
                   level='l2', 
                   insitu=True, 
                   iuvs=False, 
                   new_files=False, 
                   start_date='2014-01-01', 
                   end_date='2020-01-01', 
                   update_prefs=False,
                   only_update_prefs=False, 
                   exclude_orbit_file=False,
                   local_dir=None,
                   unittest=False,
                   crustal_download=True):
    
    """
    This function creates a "Tplot Variable" based on the inputs, and
    stores this data in memory.  Tplot Variables store all of the information
    needed to generate a plot.  
    
    Parameters:
        name : str 
            Name of the tplot variable that will be created
        data : dict
            A python dictionary object.  
            
            'x' should be a 1-dimensional array that represents the data's x axis.  Typically this data is time,
            represented in seconds since epoch (January 1st 1970)
            
            'y' should be the data values. This can be 2 dimensions if multiple lines or a spectrogram are desired.
            
            'v' is optional, and is only used for spectrogram plots.  This will be a list of bins to be used.  If this
            is provided, then 'y' should have dimensions of x by z.
            
            'x' and 'y' can be any data format that can be read in by the pandas module.  Python lists, numpy arrays,
            or any pandas data type will all work.
        delete : bool, optional
            Deletes the tplot variable matching the "name" parameter
        newname: str
            Renames TVar to new name
        
    .. note::
        If you want to combine multiple tplot variables into one, simply supply the list of tplot variables to the
        "data" parameter.  This will cause the data to overlay when plotted.
        
    Returns:
        None
        
    Examples:
        >>> # Store a single line
        >>> import pytplot
        >>> x_data = [1,2,3,4,5]
        >>> y_data = [1,2,3,4,5]
        >>> pytplot.store_data("Variable1", data={'x':x_data, 'y':y_data})
    
        >>> # Store a two lines
        >>> x_data = [1,2,3,4,5]
        >>> y_data = [[1,5],[2,4],[3,3],[4,2],[5,1]]
        >>> pytplot.store_data("Variable2", data={'x':x_data, 'y':y_data})
        
        >>> # Store a spectrogram
        >>> x_data = [1,2,3]
        >>> y_data = [ [1,2,3] , [4,5,6], [7,8,9] ]
        >>> v_data = [1,2,3]
        >>> pytplot.store_data("Variable3", data={'x':x_data, 'y':y_data, 'v':v_data})
        
        >>> # Combine two different line plots
        >>> pytplot.store_data("Variable1and2", data=['Variable1', 'Variable2'])
        
        >>> #Rename TVar
        >>> pytplot.store_data('a', data={'x':[0,4,8,12,16], 'y':[1,2,3,4,5]})
        >>> pytplot.store_data('a',newname='f')
    
    import os

    # Check for orbit num rather than time string
    if isinstance(start_date, int) and isinstance(end_date, int):
        start_date, end_date = orbit_time(start_date, end_date)
        start_date = parse(start_date)
        end_date = parse(end_date)
        start_date = start_date.replace(hour=0, minute=0, second=0)
        end_date = end_date.replace(day=end_date.day + 1, hour=0, minute=0, second=0)
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')
        
    if update_prefs or only_update_prefs:
        utils.set_root_data_dir()
        if only_update_prefs:
            return
    
    public = utils.get_access()
    if not public:
        utils.get_uname_and_password()

    if filenames is None:
        if insitu and iuvs:
            print("Can't request both INSITU and IUVS in one query.")
            return
        if not insitu and not iuvs:
            print("If not specifying filename(s) to download, Must specify either insitu=True or iuvs=True.")
            return
        
    if instruments is None:
        instruments = ['kp']
        if insitu:
            level = 'insitu'
        if iuvs:
            level = 'iuvs'
            
    for instrument in instruments:
        # Build the query to the website
        query_args = []
        query_args.append("instrument=" + instrument)
        query_args.append("level=" + level)
        if filenames is not None:
            query_args.append("file=" + filenames)
        query_args.append("start_date=" + start_date)
        query_args.append("end_date=" + end_date)
        if level == 'iuvs':
            query_args.append("file_extension=tab")
        if local_dir is None:
            mvn_root_data_dir = utils.get_root_data_dir()
        else:
            mvn_root_data_dir = local_dir
        
        data_dir = os.path.join(mvn_root_data_dir, 'maven', 'data', 'sci', instrument, level)
        
        query = '&'.join(query_args)
        
        s = utils.get_filenames(query, public)
        
        if not s:
            print("No files found for {}.".format(instrument))

        if s:
            s = str(s)
            s = s.split(',')

            if not crustal_download:
                s = [f for f in s if 'crustal' not in f]
        
            if list_files:
                for f in s:
                    print(f)
                return
        
            if new_files:
                s = utils.get_new_files(s, data_dir, instrument, level)
                
            if not unittest:
                print("Your request will download a total of: " + str(len(s)) + " files for instrument " +
                      str(instrument))
                print('Would you like to proceed with the download? ')
                valid_response = False
                cancel = False
                while not valid_response:
                    response = (input('(y/n) >  '))
                    if response == 'y' or response == 'Y':
                        valid_response = True
                    elif response == 'n' or response == 'N':
                        print('Cancelled download. Returning...')
                        valid_response = True
                        cancel = True
                    else:
                        print('Invalid input.  Please answer with y or n.')

                if cancel:
                    continue

            if not exclude_orbit_file:
                print("Before downloading data files, checking for updated orbit # file from naif.jpl.nasa.gov")
                print("")
                utils.get_orbit_files()
        
            i = 0
            utils.display_progress(i, len(s))
            for f in s:
                i += 1
                full_path = utils.create_dir_if_needed(f, data_dir, level)
                utils.get_file_from_site(f, public, full_path)
                utils.display_progress(i, len(s))

    return
