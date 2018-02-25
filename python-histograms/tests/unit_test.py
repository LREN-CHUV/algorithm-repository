from nose.tools import assert_equal

import os

class TestHistograms:

    def __init__(self):
        self.db_conn = None

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_01_visit(self):
        """
        This is a basic use case.
        First, we want to visit a DICOM data-set after the 'ACQUISITION' process. Then, we want to visit a NIFTI
        data-set generated from the previous DICOM files after the 'DICOM2NIFTI' process.
        """


    def test_02_visit_again(self):
        """
        Here, run again the test_01_visit so we can check that there are no duplicates in the DB.
        """


    def test_03_visit_special(self):
        """
        This test tries to visit special files.
        These can be copies from already loaded files, DICOM with missing fields, etc.
        """
