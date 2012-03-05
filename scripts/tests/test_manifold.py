"""
Manifold correction test suite.
"""

import sys
from os.path import realpath
sys.path.append(realpath("."))

import bpy
import unittest
from tests.utils import (cleanup, import_model, select_object, get_bounds,
    get_selected_points)
from modules.manifold import correction

class PlanarFacesTests(unittest.TestCase):
    def setUp(self):
        cleanup()
    
    def test_buddha(self):
        obj = import_model("happy_vrip_res4.ply")
        select_object(obj)
        prev_bounds = get_bounds(obj)
        correction(True, False)
        self.assertEqual(prev_bounds, get_bounds(obj))
        
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.context.tool_settings.mesh_select_mode = [False, True, False]
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_non_manifold()
        self.assertEqual(get_selected_points(), [])

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(PlanarFacesTests)
	unittest.TextTestRunner(verbosity=2).run(suite)
