# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pydivide

###############################################################################
#
#Download Files Section
#
###############################################################################

from . import download_files_utilities as utils
from .utilities import orbit_time
from dateutil.parser import parse

def mvn_kp_download_files(filenames=None, 
                          list_files=False, 
                          insitu=True, iuvs=False, 
                          text_files=True, 
                          cdf_files=False, 
                          new_files=False, 
                          start_date='2014-01-01', 
                          end_date='2020-01-01', 
                          update_prefs=False,
                          only_update_prefs=False, 
                          exclude_orbit_file=False,
                          local_dir=None,
                          unittest=False):
    print("This procedure was renamed, just use download_files")
    download_files(filenames=filenames,
                   list_files=list_files,
                   insitu=insitu,
                   iuvs=iuvs,
                   new_files=new_files,
                   start_date=start_date,
                   end_date=end_date,
                   update_prefs=update_prefs,
                   only_update_prefs=only_update_prefs,
                   exclude_orbit_file=exclude_orbit_file,
                   local_dir=local_dir,
                   unittest=unittest,
                   instruments=None)
    return

def mvn_kp_download_sci_files(filenames=None, 
                              instruments=None,
                              level='l2',
                              list_files=False, 
                              new_files=False, 
                              start_date='2014-01-01', 
                              end_date='2020-01-01', 
                              update_prefs=False,
                              only_update_prefs=False, 
                              exclude_orbit_file=False,
                              local_dir=None,
                              help=False,
                              unittest=False):
    print("This procedure was renamed, just use download_files")
    download_files(filenames=filenames,
                   instruments=instruments,
                   level=level,
                   list_files=list_files,
                   new_files=new_files,
                   start_date=start_date,
                   end_date=end_date,
                   update_prefs=update_prefs,
                   only_update_prefs=only_update_prefs,
                   exclude_orbit_file=exclude_orbit_file,
                   local_dir=local_dir,
                   unittest=unittest)
    return
     
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
                   unittest=False):
    
    import os
    
    #Check for orbit num rather than time string
    if isinstance(start_date, int) and isinstance(end_date, int):
        start_date, end_date = orbit_time(start_date, end_date)
        start_date = parse(start_date)
        end_date = parse(end_date)
        start_date = start_date.replace(hour=0, minute=0, second=0)
        end_date = end_date.replace(day=end_date.day+1, hour=0, minute=0, second=0)
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')
        
    if (update_prefs==True or only_update_prefs==True):
        utils.set_root_data_dir()
        if (only_update_prefs==True):
            return
    
    public = utils.get_access()
    if (public==False):
        utils.get_uname_and_password()

    if (filenames != None):
        if (insitu == True) and (iuvs == True):
            print("Can't request both INSITU and IUVS in one query.")
            return
        if not ((insitu == True) or (iuvs == True)):
            print("If not specifying filename(s) to download, Must specify either insitu=True or iuvs=True.")
            return
        
    if instruments==None:
        instruments=['kp']
        if (insitu==True):
            level='insitu'
        if (iuvs==True):
            level='iuvs'
            
    for instrument in instruments:
        # Build the query to the website
        query_args=[]
        query_args.append("instrument="+instrument)
        query_args.append("level="+level)
        if (filenames!=None):
            query_args.append("file="+filenames)
        query_args.append("start_date="+start_date)
        query_args.append("end_date="+end_date)
        if level == 'iuvs':
            query_args.append("file_extension=tab")
        if local_dir == None:
            mvn_root_data_dir = utils.get_root_data_dir()
        else:
            mvn_root_data_dir = local_dir
        
        data_dir = os.path.join(mvn_root_data_dir,'maven','data','sci',instrument,level)  
        
        query = '&'.join(query_args)
        
        s = utils.get_filenames(query, public)
        
        if (len(s)==0):
            print("No files found.")
            return
        
        s = str(s)
        s = s.split(',')
        
        if (list_files==True):
            for f in s:
                print(f)
            return
        
        if (new_files==True):
            s = utils.get_new_files(s, data_dir, instrument, level)
            
        if (len(s)==0):
            print("No files found.")
            return
                
        if not unittest:
            print("Your request will download a total of: "+str(len(s))+" files for instrument "+str(instrument))
            print('Would you like to proceed with the download? ')
            valid_response=False
            while(valid_response==False):
                response = (input('(y/n) >  '))
                if response=='y' or response=='Y':
                    valid_response=True
                    cancel=False
                elif response=='n' or response=='N':
                    print('Cancelled download. Returning...')
                    valid_response=True
                    cancel=True
                else:
                    print('Invalid input.  Please answer with y or n.')
                    
        if cancel:
            continue
        
        if exclude_orbit_file == False:
            print("Before downloading data files, checking for updated orbit # file from naif.jpl.nasa.gov")
            print("")
            utils.get_orbit_files()
        
        i=0
        utils.display_progress(i, len(s))
        for f in s:
            i = i+1
            full_path = utils.create_dir_if_needed(f, data_dir, level)
            utils.get_file_from_site(f, public, full_path)
            utils.display_progress(i, len(s))
    
     
    return


    