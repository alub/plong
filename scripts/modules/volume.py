"""
This module provides general purpose functions related to volumetric parameters
of the object. It is designed to provide a criterion for choosing a supporting
a supporting plane.
"""

import bpy
from mathutils.geometry import distance_point_to_plane, area_tri
from mathutils import Vector, Matrix

class OrientationException(Exception):
    """
    An exception to be raised in this module.
    """
    pass

def center_of_gravity(obj):
    """
    Return a Vector with the coordinates of the center of gravity of the object,
    relatively to the object location. It assumes a uniform distribution of mass.
    It can only work with triangular and quad meshes.
    """
    x = y = z = 0
    orig = Vector((0, 0, 0))
    for face in obj.data.faces:
        if face.normal.length == 0.0:
            continue
        distance = distance_point_to_plane(orig, face.center, face.normal)
        
        nb_edges = len(face.vertices)
        v = [obj.data.vertices[f].co for f in face.vertices]
        if nb_edges == 3:
            face_vol = - face.area * distance / 3        
            x += face_vol * (v[0][0] + v[1][0] + v[2][0]) / 4
            y += face_vol * (v[0][1] + v[1][1] + v[2][1]) / 4
            z += face_vol * (v[0][2] + v[1][2] + v[2][2]) / 4
        elif nb_edges == 4:
            # let's cut the quad in triangles!
            # triangle 1: vertices 0, 1, 2
            area1 = area_tri(v[0], v[1], v[2])
            face_vol1 = - area1 * distance / 3
            x += face_vol1 * (v[0][0] + v[1][0] + v[2][0]) / 4
            y += face_vol1 * (v[0][1] + v[1][1] + v[2][1]) / 4
            z += face_vol1 * (v[0][2] + v[1][2] + v[2][2]) / 4
            # triangle 2: vertices 2, 3, 0
            area2 = area_tri(v[2], v[3], v[0])
            face_vol2 = - area2 * distance / 3
            x += face_vol2 * (v[0][0] + v[2][0] + v[3][0]) / 4
            y += face_vol2 * (v[0][1] + v[2][1] + v[3][1]) / 4
            z += face_vol2 * (v[0][2] + v[2][2] + v[3][2]) / 4
        else:
            raise OrientationException
            
    return Vector((x, y, z))

def volume(obj):
    """
    Compute the volume of the object `obj`. The mesh has to be manifold, and
    face normals coherently oriented towards the outside.
    """
    bpy.ops.object.mode_set(mode='OBJECT')
    volume = 0
    orig = Vector((0, 0, 0))
    for face in obj.data.faces:
        if face.normal.length == 0.0:
            continue
        distance = distance_point_to_plane(orig, face.center, face.normal)
        # minus sign, assuming normals are directed towards the outside
        volume -= face.area * distance / 3
    return volume

def point_inside_object(point, obj):
    """
    Return True if the given `point` is inside the `object`, False otherwise.
    Point coordinates must be in the object referential.
    """
    # http://blenderartists.org/forum/showthread.php?195605-Detecting-if-a-point-is-inside-a-mesh-2.5-API
    intersections_count = 0
    axis = obj.data.faces[0].center # arbitrary choice, but *not* a face vertice
    while True:
        location, normal, index = ob.ray_cast(point, point + axis * 10000.0)
        if index == -1:
            break
        intersections_count += 1
        point = location + axis * 0.00001
    return (intersections_count % 2 == 1)

def supported_volume(obj, sp):
    """
    Compute the volume actually supported by the plane `sp`.
    The object meshes have to be manifold.
    """
    sp.select()
    sp_normal, sp_vertex = sp.get_plane()
    height = max(sp_normal.dot(obj.data.vertices[sp_vertex].co - vertex.co)
                 for vertex in obj.data.vertices)
    bpy.ops.mesh.duplicate()
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate =
        {'value': - height * sp_normal.normalized()})
    old_objects = [o.name for o in bpy.data.objects]
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.select_all(action='DESELECT')
    for o in bpy.data.objects:
        if o.name not in old_objects:
            dup = o
    bpy.ops.object.modifier_add(type='BOOLEAN')
    obj.modifiers['Boolean'].object = dup
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier='Boolean')
    sv = volume(obj)
    bpy.ops.object.delete(use_global=False)
    return sv

if __name__ == '__main__':
    for ob in bpy.context.selected_objects:
        print("### Object “%s”" % ob.name)
        print("Volume : %s" % volume(ob))
        cog = center_of_gravity(ob)
        print("Center of gravity : %s" % cog)
        if point_inside_object(cog, ob):
            print("Center of gravity is inside the object.\n")
        else:
            print("Center of gravity is outside the object.\n")
            
        import planar_faces
        sp = planar_faces.SupportPlanes(ob)[0]
        print("Supported volume: %s\n" % supported_volume(ob, sp))
