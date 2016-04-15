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


