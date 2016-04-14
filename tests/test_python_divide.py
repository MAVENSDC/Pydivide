'''
Created on Mar 3, 2015

@author: bharter
'''
import sys
sys.path.append('..')
import unittest
import shutil
import re
import os


class TestPythonDivide(unittest.TestCase):
    '''
    Unit tests for the make_pds_bundles.make_pds_bundles package.  Tests will cover
    the ability to find files to archive, archive and zip the archived files.  Tests
    will also cover the generation of the PDS manifest file
    '''

    def setUp(self):
        self.x = 5

    def tearDown(self):
        self.x = 2

    def test_result_generation(self):
        self.assertEqual(self.x, 5)



