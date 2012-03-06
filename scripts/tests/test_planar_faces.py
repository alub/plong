"""
Planar faces test suite.
"""

import sys
from os.path import realpath
sys.path.append(realpath("."))

import unittest
from tests.utils import cleanup, import_model, select_object, get_bounds
from modules.planar_faces import SupportPlanes
from math import pi

class PlanarFacesTests(unittest.TestCase):
    def setUp(self):
        cleanup()
    
    def test_egg(self):
        chosen_faces = {32, 33, 34, 35, 36, 37, 38, 39, 40, 41,
            42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54,
            55, 56, 57, 58, 59, 60, 61, 62, 63}
        
        obj = import_model("egg_with_support.stl")
        select_object(obj)
        sp = SupportPlanes(obj)
        self.assertEqual(len(sp), 10)
        self.assertEqual(sp[0].faces, chosen_faces)
        sp[0].select()
        self.assertEqual(set(
            [face.index for face in obj.data.faces
                if face.select]), chosen_faces)
        
        
        sp[0].apply()
        xmin, xmax, ymin, ymax, zmin, zmax = get_bounds(obj)
        self.assertTrue(round(xmin - -10.986856460571289, 4) == 0)
        self.assertTrue(round(xmax - 10.986856460571289, 4) == 0)
        self.assertTrue(round(ymin - -10.986852645874023, 4) == 0)
        self.assertTrue(round(ymax - 10.986856460571289, 4) == 0)
        self.assertTrue(round(zmin - -5.7220458984375e-06, 4) == 0)
        self.assertTrue(round(zmax - 32.62044143676758, 4) == 0)


if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(PlanarFacesTests)
	unittest.TextTestRunner(verbosity=2).run(suite)
