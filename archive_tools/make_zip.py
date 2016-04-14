#!/usr/bin/python
'''
make_zip

Python script to create a zip file of the MAVEn DIViDE IDL Toolkit
for publication on the Team and Public websites.  Based on input, 
it *writes* the access.txt file that determines whether this is a
public or team version.  NB, we should probably *rewrite* it to 
indicate Team version after we are finished

Input: access: Team or Public.  Exit with error if other
       include_basemaps: boolean
       Debug: if true, do not overwrite access.txt file

Output: None: generates ZIP file, placed two directories above archive_tools/
                i.e., one level above maventoolkit/
              Updates the help files
              prints message to screen indicating name of generated file.

Author: McGouldrick (2015-Oct-01)
Version: 1.0
'''
import os
import re
import sys
import zipfile
import hashlib

def check_args():
    '''
    Definition to check the passed arguments and ensure
    that the desired actions can and will be performed.
    '''
    #
    # Define Default values
    #
    IncludeBasemaps = True
    Debug = False
    #
    # Process the arguments
    #
    total = len( sys.argv )   # get total number of args passed
    cmdargs = str( sys.argv ) # Get the args list
    if total <= 1:
        print '\nUSAGE:'
        print '%> python make_zip.py access=... ' \
              + '[IncludeBasemaps=...] [Debug=...]'
        print '  -- or --'
        print '%> ./make_zip.py access=... ' \
              + '[IncludeBasemaps=...] [Debug=...]'
        print ' '
        print 'Where values in [] are Optional arguments.\n'
        print 'Returning having done nothing.....\n'
        sys.exit(1)        
    #
    #  cycle through args and get info
    #
    for i in sys.argv[1:]: 
        token,value = re.split("=",i)
        if re.match('access',token): 
            if value == 'Team' or value == 'team':
                access='Team'
            elif value == 'Public' or value == 'public':
                access='Public'
            else:
                print "****ERROR****"
                print '"%s" is an invalid argument for <access>' % value
                print 'Only "Team" and "Public" are acceptable'
                print 'Returning having done nothing...'
                sys.exit(1)
        if re.match('[Ii]nclude[Bb]asemaps',token): 
            if value != 'True' and value != 'False':
                print '*****ERROR*****'
                print '<IncludeBasemaps> must be Boolean (True/False)'
                print 'Returning having done nothing...'
                sys.exit(1)
            else:
                IncludeBasemaps=(value=='True')
        if re.match('[Dd]ebug',token):
            if value != 'True' and value != 'False':
                print '*****ERROR*****'
                print '<Debug> must be Boolean (True/False)'
                print 'Returning having done nothing...'
                sys.exit(1)
            else:
                Debug=(value=='True')
    #
    #  Verify that access argument was provided
    #
    if 'access' not in locals():
        print '*****ERROR*****'
        print 'Access level must be provided as an argument'
        print '%> python make_zip.py access=<value>'
        print 'where <value> = "Team" or "Public"'
        print 'Returning having done nothing...'
        sys.exit(1)

    return Debug, IncludeBasemaps, access

#------------------------------------------------------------------------

def define_file_name(Debug, IncludeBasemaps, access):
    '''
    Based on input parameters, create a unique filename for 
    the ZIP file to be produced
    '''
    #
    # Move to relevant direcotry
    #
    os.chdir(os.environ['HOME']+'/DIVIDE/dev/maventoolkit/')
    #
    #  Create the new access.txt file
    #
    if Debug:
        access_file = open('access.txt.temp','wb')
    else:
        access_file = open('access.txt','wb')
        access_file.write('; IDL Toolkit Access Level (Public(=0) '+
                          'or Private(=1) website)\n')
    if access == 'Team': 
        access_file.write('access_level: 1\n')
    elif access == 'Public':
        access_file.write('access_level: 0\n')
    else:
        print '*****ERROR*****'
        print 'value of <access> must be either "Team" or "Public"'
        sys.exit(1)
    access_file.flush()
    access_file.close()
    #
    #  Read the Current Version of the Toolkit from Version_History.txt
    #
    for line in open('Version_History.txt'):
        if line.startswith('Current Version'):
            token,value = re.split(':',line)
            version = str(value)
            #
            #  Change slash to underscore; 
            # but should imrpove this to standards
            #  (i.e., YYYYMMDD<a>)
            #
            version = ''.join(version.replace("/","_").split())
    #
    # Define the ZIP file name
    #
    map_str = ('WithMaps' if IncludeBasemaps else 'NoMaps')
    zipout = '../Toolkit_V'+version+'_'+access+'_'+map_str+'.zip'
    print 'Preparing file: %s' % zipout[3:]

    return zipout

#---------------------------------------------------------------------------

def create_zip_file(Debug,IncludeBasemaps,access,zipout):
    '''
    Do the heavy lifting to apply regex patterns to select the 
    files to be included in the generated ZIP file.  And then
    create that file.
    '''
    #
    #  Start with the pro files in the root directory
    #
    all_files = [each for each in os.listdir('./') if each.endswith('.pro')]
    #
    #  Add the access.txt and Version History files (hack)
    #
    all_files.append('access.txt')
    all_files.append('Version_History.txt')
    #
    #  Define the root dir regex whether getting basemaps or not
    #
    if IncludeBasemaps:
        root_regex = '.+(basemaps|help|orbitfiles|_lib)'
    else:
        root_regex = '.+(help|orbitfiles|_lib)'
    #
    #  Now, get a list of sub-directory files
    #
    for root, dirs, files in os.walk('./',topdown=False):
        if re.search(root_regex,root):
            if re.search('testing_lib',root):
                file_regex = '.+\.(pro|txt|tab|cdf)'
            else:
                file_regex = '.+\.(pro|sav|txt|jpg)'
            for each in files:
                if re.search(file_regex,each):
                    all_files.append(root+os.path.sep+each)
    #
    #  Now, cycle through those files, adding them to the ZIP file
    #
    
    os.remove('SourceList')
    f=open('SourceList', 'w')
    if os.path.isfile(zipout): os.remove(zipout)
    with zipfile.ZipFile(zipout,'a',zipfile.ZIP_DEFLATED) as myzip:
        for i in all_files:
            myzip.write(i)
            m = hashlib.md5(open(i, 'rb').read())
            f.write(m.hexdigest())
            f.write(' ')
            f.write(i)
            f.write('\n')
        f.close()
        myzip.write('SourceList')
        myzip.close()
    #
    #  Re-write the access.txt file to indicate Team member access
    #
    if Debug:
        access_file = open('access.txt.temp','wb')
    else:
        access_file = open('access.txt','wb')
    access_file.write('; IDL Toolkit Access Level (Public(=0) '+
                      'or Private(=1) website)\n')
    access_file.write('access_level: 1\n')
    access_file.flush()
    access_file.close()

#---------------------------------------------------------------------------

def make_help():
    '''
    Python script to parse the *.pro files in the MAVEn Toolkit main level
    directory, and make a txt help file out of the header information, located
    between bracket ;+ and ;- lines

    Author: McGouldrick (2015-Jul-21)
    '''

    os.chdir(os.environ['HOME']+'/DIVIDE/dev/maventoolkit/')
    pro_files = []
    pro_files += [each for each in os.listdir('./') if each.endswith('.pro')]

    for f in pro_files:
        fin = open(f,'rb')
        # create the output file
        fout = open('help/'+re.sub('\.pro','.txt',f), 'wb')
        # Initialize parse Boolean
        parse = False
        # Parse the pro file and write the header to txt file
        for line in fin:
            if parse:
                fout.write(re.sub(';','',line)) # strip the initial semicolon
            if line.startswith(';+'): 
                parse = True
            elif line.startswith(';-'):
                parse = False
        fout.flush()
        fout.close() # close files and then end
        fin.close()

#----------------------------------------------------------------------------

def main():
    '''
    The main program
    '''
    Debug, IncludeBasemaps, access = check_args()
    zipout = define_file_name( Debug, IncludeBasemaps, access )
    make_help()
    create_zip_file( Debug, IncludeBasemaps, access, zipout )

#---------------------------------------------------------------------------

if __name__ == "__main__":
    main()
