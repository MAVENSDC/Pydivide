###############################################################################
#
#Download Files Section
#
###############################################################################

from . import mvn_kp_download_files_utilities as utils

def mvn_kp_download_files(filenames=None, 
                          list_files=False, 
                          insitu=True, iuvs=False, 
                          text_files=True, 
                          cdf_files=False, 
                          new_files=False, 
                          start_date='2014-09-01', 
                          end_date='2015-11-15', 
                          update_prefs=False,
                          only_update_prefs=False, 
                          exclude_orbit_file=False,
                          local_dir=None,
                          help=False,
                          unittest=False):
    
    import os
    
    if (update_prefs==True or only_update_prefs==True):
        utils.set_root_data_dir()
        if (only_update_prefs==True):
            return
    
    public = utils.get_access()
    if (public==False):
        utils.get_uname_and_password()
    
    if text_files==True:
        extension='tab'
    if cdf_files==True:
        extension='cdf'
    if filenames==None:
        text_files=True
        extension='tab'

    if (filenames != None):
        if (insitu == True) and (iuvs == True):
            print("Can't request both INSITU and IUVS in one query.")
            return
        if not ((insitu == True) or (iuvs == True)):
            print("If not specifying filename(s) to download, Must specify either insitu=True or iuvs=True.")
            return
    
    instrument='kp'
    if (insitu==True):
        level='insitu'
    if (iuvs==True):
        level='iuvs'
    
    # Build the query to the website
    query_args=[]
    query_args.append("instrument="+instrument)
    query_args.append("level="+level)
    if (filenames!=None):
        query_args.append("file="+filenames)
    query_args.append("start_date="+start_date)
    query_args.append("end_date="+end_date)
    query_args.append("file_extension="+extension)
    
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
    
    if (insitu==True):
        if (text_files==True):
            estimated_size=len(s) * 38
        else:
            estimated_size=len(s) * 19
    else:
        if (text_files==True):
            estimated_size=len(s) * 1.0
        else:
            estimated_size=len(s) * .684
            
    if not unittest:
        print("Your request will download a total of: "+str(len(s))+" files with an approx total size of: "+str(estimated_size)+" MBs.")
        print('Would you like to procede with the download: ')
        valid_response=False
        while(valid_response==False):
            response = (input('(y/n) >'))
            if response=='y' or response=='Y':
                valid_response=True
            elif response=='n' or response=='N':
                print('Cancelled download. Returning...')
                valid_response=True
                return
            else:
                print('Invalid input.  Please answer with y or n.')
        
        
    print("Before downloading data files, checking for updated KP templates from the SDC")
    print("Not yet implemented, do we even need templates?")
    
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


    