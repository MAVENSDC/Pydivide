'''
Created on Mar 3, 2015

@author: bharter
'''
import sys
sys.path.append('..')
import unittest
import os
from mvn_kp_download_files import mvn_kp_download_files
from mvn_kp_download_files_utilities import get_root_data_dir
from mvn_kp_download_sci_files import mvn_kp_download_sci_files
from mvn_kp_read import mvn_kp_read
from mvn_kp_bin import mvn_kp_bin
import math
import numpy

class TestPythonDivide(unittest.TestCase):
    '''
    Unit tests for the make_pds_bundles.make_pds_bundles package.  Tests will cover
    the ability to find files to archive, archive and zip the archived files.  Tests
    will also cover the generation of the PDS manifest file
    '''

    def setUp(self):
        self.x = 5

    def tearDown(self):
        for f in os.listdir(os.path.join(get_root_data_dir(),'maven','data','sci','kp','insitu','2015','01')):
            os.remove(os.path.join(get_root_data_dir(),'maven','data','sci','kp','insitu','2015','01',f))
        for f in os.listdir(os.path.join(get_root_data_dir(),'maven','data','sci','euv','l3','2015','01')):
            os.remove(os.path.join(get_root_data_dir(),'maven','data','sci','euv','l3','2015','01',f))

    def test_download_kp_files(self):
        mvn_kp_download_files(start_date='2015-01-05', end_date='2015-01-10', unittest=True)
        x = os.listdir(os.path.join(get_root_data_dir(),'maven','data','sci','kp','insitu','2015','01'))
        self.assertEqual(len(x),6)
        
    def test_download_sci_files(self):
        mvn_kp_download_sci_files(start_date='2015-01-05', end_date='2015-01-10', instrument='euv', level='l3', unittest=True)
        x = os.listdir(os.path.join(get_root_data_dir(),'maven','data','sci','euv','l3','2015','01'))
        self.assertEqual(len(x),6)
        
    def test_read_in_kp_files(self):
        mvn_kp_download_files(start_date='2015-01-05', end_date='2015-01-10', unittest=True)
        insitu = mvn_kp_read(['2015-01-05', '2015-01-08T05:15:00'], instruments=['SWEA','NGIMS','MAG'])
        self.assertEqual(len(insitu['MAG']['Magnetic Field MSO X']),37715)
        
    def test_bin_kp_data(self):
        #Basically just here to make sure bin is runing properly, really hard to actually check answers
        mvn_kp_download_files(start_date='2015-01-15', end_date='2015-01-16', unittest=True)   
        insitu = mvn_kp_read('2015-01-15')
        x,y,z,q = mvn_kp_bin(insitu, parameter='SEP.Ion Flux FOV 1 F', bin_by=['SWEA.Solar Wind Electron Density', 'SWEA.Solar Wind Electron Temperature', 'SPACECRAFT.Altitude Aeroid'], binsizes=[1,1,1000], median=True, avg=True, std=True, density=True)
        self.assertEqual(int(math.floor(numpy.nansum(z))), 108921)

