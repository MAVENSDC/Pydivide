# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pydivide

# CLEANUP_FILES
#     Searches code directory for .tab files, keeps latest versions/revisions, asks to delete old versions/revisions
# 
# FUNCTION CALL
#     cleanup_files()
# 
# REQUIREMENTS
#     All .tab files must be named with the following formats: 
#     "mvn_kp_insitu_YYYYMMDD_vXX_rXX.tab"
#     "mvn_kp_iuvs_ORBIT_YYYYMMDDTHHMMSS_VXX_rXX.tab"
#     Any extraneous characters or formatting changes will break the regexing for this function.
#     Will ignore files not ending in .tab and not starting with "mvn_kp_insitu" or "mvn_kp_iuvs".

from __future__ import division
import numpy
import glob
from pydivide.download_files_utilities import get_root_data_dir
import os

def cleanup_files():
    #pull directory path preferences from mvn_toolkit_prefs.txt
    dir_path = get_root_data_dir()
    print(" ")
    print("Looking for files in " + dir_path + "/* ...")

    print(" ")
    print(" ")
    print("Finding insitu files...")
    print(" ")
    
    ##### INSITU FILE CLEANUP #####
    files_del = []
    files_ver = []
    files_date = []
    files_rev = []
    #search for .tab insitu files in directory path
    for filename in glob.iglob(dir_path+ '/**/*.tab', recursive=True):
        if filename.endswith(".tab") and "mvn_kp_insitu" in filename:
            #pull version and date from filename
            fver = filename[-10:-8]
            fdate = filename[-20:-12]
            frev = filename[-6:-4]
            #append to arrays
            files_del = files_del + [filename]
            files_ver = files_ver + [fver]
            files_date = files_date + [fdate]
            files_rev = files_rev + [frev]

    #convert from strings to int arrays
    tot_files = len(files_del)
    files_date = list(map(int, files_date))
    files_ver = list(map(int, files_ver))
    files_rev = list(map(int, files_rev))
    datearray = numpy.array(files_date)
    verarray = numpy.array(files_ver)
    setdatearray = list(set(datearray))
    
    #group version numbers by date
    date_dict = dict()
    for date in setdatearray:
        index = [i for i, j in enumerate(datearray) if j == date]
        for i in index:
            if date in date_dict:
                # append the new number to the existing array at this slot
                date_dict[date].append(verarray[i])

            else:
                # create a new array in this slot
                date_dict[date] = [verarray[i]]

    #group filenames by date
    file_dict = dict()
    for date in setdatearray:
        index = [i for i, j in enumerate(datearray) if j == date]
        for i in index:
            if date in file_dict:
                # append the new number to the existing array at this slot
                file_dict[date].append(files_del[i])
            else:
                # create a new array in this slot
                file_dict[date] = [files_del[i]]
                
    #group revision numbers by date
    rev_dict = dict()
    for date in setdatearray:
        index = [i for i, j in enumerate(datearray) if j == date]
        for i in index:
            if date in rev_dict:
                # append the new number to the existing array at this slot
                rev_dict[date].append(files_rev[i])
            else:
                # create a new array in this slot
                rev_dict[date] = [files_rev[i]]
                
    
    frev = []
    tot_files_old = 0
    #output names of latest files
    print("Newest versions of .tab files are:")
    for key in date_dict:
            frev = []
            versions = date_dict[key]
            newest = max(versions)
            rep_ver = versions.count(newest)
            #if more than one of the same version
            if rep_ver > 1:
                for r in rev_dict[key]:
                    #if version associate with revision isn't the newest, convert to -1 placeholder
                    if date_dict[key][rev_dict[key].index(r)] != newest:
                        frev = frev + [-1]
                    else:
                        frev = frev + [r]
                #find latest revision, correllate with version
                newrev = max(frev)
                newest_ind = frev.index(newrev)
            else:
                newest_ind = versions.index(newest)
            
            #create string for printing    
            pr_ver_del = "    " + str(file_dict[key][newest_ind])[-34:]
            print(pr_ver_del)
            tot_files_old = tot_files_old + 1
            #remove newest from file dictionary
            file_dict[key].remove(file_dict[key][newest_ind])

    flag = 0
    #if file_dict entry still has entries, verify deletion
    for key in file_dict:
        if not file_dict[key]:
            pass
        else:
            flag = 1
    if flag == 0:
        print("All files up to date.")
    else:
        if tot_files - tot_files_old == 1:
            print(" ")
            print("You have " + str(tot_files - tot_files_old) + " out of date file.")
            del_verif = input("Would you like to remove it? (Y/N) >  ")
        else:
            print(" ")
            print("You have " + str(tot_files - tot_files_old) + " out of date files.")
            del_verif = input("Would you like to remove all older versions/revisions? (Y/N) > ")
        if del_verif == "Y" or del_verif == "y":
            print(" ")
            print("Removing:")
            #if nothing in date key, do nothing
            for key in file_dict:
                if not file_dict[key]:
                    pass
                else:
                    #reconstruct file path
                    for item in file_dict[key]:
                        del_path = '/'.join(str(item).split('\\'))
                        del_path = '/'.join((del_path).split('//'))
                        print("    " + del_path)
                        #remove file
                        os.remove(del_path)
            print("Old versions removed.")
        else:
            print("Old versions will not be removed.")
             
    ##### INSITU FILE CLEANUP #####   
        
    print(" ")
    print(" ")
    print("Finding iuvs files...")
    print(" ")
    
    ##### IUVS FILE CLEANUP #####
    files_del = []
    files_ver = []
    files_date = []
    files_rev = []
    for filename in glob.iglob(dir_path+ '/**/*.tab', recursive=True):
        if filename.endswith(".tab") and "mvn_kp_iuvs" in filename:
            #pull version and orbit from filename
            forbit = filename[-33:-28]
            fver = filename[-10:-8]
            frev = filename[-6:-4]
            
            files_date = files_date + [forbit]
            files_del = files_del + [filename]
            files_ver = files_ver + [fver]
            files_rev = files_rev + [frev]
    
    tot_files = len(files_del)
    files_date = list(map(int, files_date))
    files_ver = list(map(int, files_ver))
    files_rev = list(map(int, files_rev))
    datearray = numpy.array(files_date)
    verarray = numpy.array(files_ver)
    setdatearray = list(set(datearray))
    
    #group version numbers by date
    date_dict = dict()
    for date in setdatearray:
        index = [i for i, j in enumerate(datearray) if j == date]
        for i in index:
            if date in date_dict:
                # append the new number to the existing array at this slot
                date_dict[date].append(verarray[i])

            else:
                # create a new array in this slot
                date_dict[date] = [verarray[i]]

    #group filenames by date
    file_dict = dict()
    for date in setdatearray:
        index = [i for i, j in enumerate(datearray) if j == date]
        for i in index:
            if date in file_dict:
                # append the new number to the existing array at this slot
                file_dict[date].append(files_del[i])
            else:
                # create a new array in this slot
                file_dict[date] = [files_del[i]]
                
    #group revision numbers by date
    rev_dict = dict()
    for date in setdatearray:
        index = [i for i, j in enumerate(datearray) if j == date]
        for i in index:
            if date in rev_dict:
                # append the new number to the existing array at this slot
                rev_dict[date].append(files_rev[i])
            else:
                # create a new array in this slot
                rev_dict[date] = [files_rev[i]]
                
    
    frev = []
    tot_files_old = 0
    #output names of latest files
    print("Newest versions of .tab files are:")
    for key in date_dict:
            frev = []
            versions = date_dict[key]
            newest = max(versions)
            rep_ver = versions.count(newest)
            #if more than one of the same version
            if rep_ver > 1:
                for r in rev_dict[key]:
                    #if version associate with revision isn't the newest, convert to -1 placeholder
                    if date_dict[key][rev_dict[key].index(r)] != newest:
                        frev = frev + [-1]
                    else:
                        frev = frev + [r]
                #find latest revision, correllate with version
                newrev = max(frev)
                newest_ind = frev.index(newrev)
            else:
                newest_ind = versions.index(newest)
            
            #create string for printing    
            pr_ver_del = "    " + str(file_dict[key][newest_ind])[-45:]
            print(pr_ver_del)
            tot_files_old = tot_files_old + 1
            #remove newest from file dictionary
            file_dict[key].remove(file_dict[key][newest_ind])

    flag = 0
    #if file_dict entry still has entries, verify deletion
    for key in file_dict:
        if not file_dict[key]:
            pass
        else:
            flag = 1
    if flag == 0:
        print("All files up to date.")
    else:
        if tot_files - tot_files_old == 1:
            print(" ")
            print("You have " + str(tot_files - tot_files_old) + " out of date file.")
            del_verif = input("Would you like to remove it? (Y/N) >  ")
        else:
            print(" ")
            print("You have " + str(tot_files - tot_files_old) + " out of date files.")
            del_verif = input("Would you like to remove all older versions/revisions? (Y/N) > ")
        if del_verif == "Y" or del_verif == "y":
            print(" ")
            print("Removing:")
            #if nothing in date key, do nothing
            for key in file_dict:
                if not file_dict[key]:
                    pass
                else:
                    #reconstruct file path
                    for item in file_dict[key]:
                        del_path = '/'.join(str(item).split('\\'))
                        del_path = '/'.join((del_path).split('//'))
                        print("    " + del_path)
                        #remove file
                        os.remove(del_path)
            print("Old versions removed.")
        else:
            print("Old versions will not be removed.")
    
    ##### IUVS FILE CLEANUP #####       
