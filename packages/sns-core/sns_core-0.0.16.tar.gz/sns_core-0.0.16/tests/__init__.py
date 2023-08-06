import unittest
import sys
sys.path.append('../')

def test_suite():
    loader = unittest.TestLoader()
    suite = loader.discover('.')
    return suite