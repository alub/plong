"""
Planar faces test suite.
"""

import sys
from os.path import realpath
sys.path.append(realpath("."))

import unittest
from tests.utils import cleanup, import_model, select_object
from structure.planar_faces import SupportPlanes
from math import pi

def get_bounds(obj):
    """
    Returns the bounds (xmin, xmax, ymin, ymax, zmin, zmax) of
    an object.
    This method assumes that no transformations are applied to
    the object.
    """
    
    xmin, ymin, zmin = tuple(obj.data.vertices[0].co)
    xmax, ymax, zmax = xmin, ymin, zmin
    
    for point in obj.data.vertices:
        x, y, z = tuple(point.co)
        if x < xmin:
            xmin = x
        elif x > xmax:
            xmax = x
        
        if y < ymin:
            ymin = y
        elif y > ymax:
            ymax = y
        
        if z < zmin:
            zmin = z
        elif z > zmax:
            zmax = z
    
    return xmin, xmax, ymin, ymax, zmin, zmax

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
        self.assertAlmostEqual(xmin, -10.986856460571289)
        self.assertAlmostEqual(xmax, 10.986856460571289)
        self.assertAlmostEqual(ymin, -10.986852645874023)
        self.assertAlmostEqual(ymax, 10.986856460571289)
        self.assertAlmostEqual(zmin, -5.7220458984375e-06)
        self.assertAlmostEqual(zmax, 32.62044143676758)


if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(PlanarFacesTests)
	unittest.TextTestRunner(verbosity=2).run(suite)
