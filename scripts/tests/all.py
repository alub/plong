"""
Run all defined test suites.
"""

from os.path import realpath, dirname
import unittest

if __name__ == "__main__":
    my_dir = dirname(realpath(__file__))
    suite = unittest.defaultTestLoader.discover(my_dir)
    
    unittest.TextTestRunner(verbosity=2).run(suite)