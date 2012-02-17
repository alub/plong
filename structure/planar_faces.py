from mathutils import Euler, Vector
from math import pi
import bpy

MAX_ANGLE = .01
ALIGN_TOLERANCE = .1
MIN_AREA_RATIO = .001

class PlanarFacesSet(object):
    def __init__(self, obj, initial_face):
        self._obj = obj
        self._normal = initial_face.normal
        self._comp_face = initial_face.index
        self._proj_dist = initial_face.normal.dot(initial_face.center)
        self.total_area = initial_face.area
        self.faces = {initial_face.index}
    
    def test_face(self, face):
        """
        Checks if the given face should be in the set, and adds
        it if it the case.
        """
        
        divisor = abs(self._proj_dist) or 1.0
        if face.normal.length == 0.0 or self._normal.length == 0.0:
            return False
        elif self._normal.angle(face.normal) <= MAX_ANGLE:
            if face not in self.faces:
                proj = self._normal.dot(face.center)
                if abs(self._proj_dist - proj) / divisor < ALIGN_TOLERANCE:
                    self.faces.add(face.index)
                    self.total_area += face.area
            
                    return True
        
        return False
    
    def select(self):
        """
        Select all faces from the plane.
        """
        
        bpy.context.tool_settings.mesh_select_mode = (False, False, True)
        
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        
        for face in self.faces:
            self._obj.data.faces[face].select = True
        
        bpy.ops.object.mode_set(mode='EDIT')
   
    def apply(self):
        """
        Rotates and moves the object to place it over
        the plane.
        """
        
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        
        for ob in bpy.data.objects.values():
            ob.select = False
        bpy.context.scene.objects.active = self._obj
        self._obj.select = True
        
        
        # Apply pending tranformations to the object
        bpy.ops.object.transform_apply(location=True,
            rotation=True, scale=True)
        
        normal, point = self.get_plane()
        base_vec = Vector((0, 0, -1))
        
        diff = normal.rotation_difference(base_vec).to_euler('XYZ')
        new_normal = normal.normalized()
        new_normal.rotate(diff)
        if (new_normal - base_vec).length > .1:
            # new_normal and base_vec are not the same vector!
            # in fact, we have new_normal = -base_vec
            # so we need to rotate the whole object (on the
            # x axis, for instance)
            
            diff.x += pi
        
        self._obj.rotation_mode = 'XYZ'
        self._obj.rotation_euler = Euler((diff.x, diff.y, 0.0),
            'XYZ')
        
        # Apply the rotation
        bpy.ops.object.transform_apply(location=False,
            rotation=True, scale=False)
        
        
        # Set the location (given the applied rotation)
        pos = self._obj.data.vertices[point].co.xyz
        pos.negate()
        self._obj.location = tuple(pos)
        
        # Apply the rotation
        bpy.ops.object.transform_apply(location=True,
            rotation=False, scale=False)
    
    def get_plane(self):
        """
        Returns a vector and a point defining the plane containing
        the faces.
        """
        
        # Recalculate the initial face's normal in case it changed
        self._normal = self._obj.data.faces[self._comp_face].normal
        
        points = set()
        for face in self.faces:
            points.update(self._obj.data.faces[face].vertices)
        
        vertices = self._obj.data.vertices
        
        chosen_point = points.pop()
        best_distance = self._normal.dot(vertices[chosen_point].co)
        
        for point in points:
            distance = self._normal.dot(vertices[point].co)
            if distance > best_distance:
                chosen_point = point
                best_distance = distance
        
        return self._normal.xyz, point
    
    def __repr__(self):
        return "<PlanarFacesSet: %r>" % self.faces


class SupportPlanes(object):
    """
    This class calculates planes which may be used to
    support the object.
    """

    def __init__(self, obj):
        self.obj = obj
        self.face_sets = []

        it = iter(self.cluster_planar_faces(obj))
        largest_set = it.__next__()
        
        self.face_sets.append(largest_set)
        min_area = largest_set.total_area * MIN_AREA_RATIO
        
        for face_set in it:
            if face_set.total_area < min_area:
                break
            
            self.face_sets.append(face_set)
        
    
    def __len__(self):
        return len(self.face_sets)
    
    def __repr__(self):
        return "<SupportPlanes: %r>" % self.face_sets
    
    def __getitem__(self, key):
        return self.face_sets[key]
    
    def __iter__(self):
        return iter(self.face_sets)

    @staticmethod
    def cluster_planar_faces(obj):
        """
        Returns a list of set of faces sharing approximatively
        the same plane.
        """
        
        face_sets = []
        remaining_faces = list(obj.data.faces)
        
        while remaining_faces:
            current_face = remaining_faces.pop()
            
            set_found = False
            for face_set in face_sets:
                if face_set.test_face(current_face):
                    set_found = True
                    break
            
            if not set_found:
                face_sets.append(PlanarFacesSet(obj, current_face))
        
        valid_face_sets = []
        
        for face_set in face_sets:
            vector, point = face_set.get_plane()
            
            ref_proj = vector.dot(obj.data.vertices[point].co)
            is_valid = True
            
            for obj_point in obj.data.vertices:
                proj = vector.dot(obj_point.co)
                if proj > ref_proj:
                    if proj and abs(proj - ref_proj) / abs(proj) > .001:
                        is_valid = False
                        break
            
            if is_valid:
                valid_face_sets.append(face_set)
        
    
        return sorted(valid_face_sets, key=lambda face_set:
            face_set.total_area, reverse=True)

if __name__ == '__main__':
    obj = bpy.context.selected_objects[0]
    
    sp = SupportPlanes(obj)
    sp[0].select()
