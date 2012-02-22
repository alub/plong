from mathutils import Euler, Vector
from math import pi
import bpy
import heapq

MAX_FACES = 5000  # Maximum number of faces to consider
MAX_ANGLE = .01  # Maximum angle between face normals
ALIGN_TOLERANCE = .1  # Alignement tolerance between two faces
OUTSIDE_PROJ_TOLERANCE = .1  # Tolerance to ident. planes "outside" of the obj.
PROPOSAL_COUNT = 10  # Maximum number of face sets to propose

class PlanarFacesSet(object):
    __slots__ = ('_obj', '_normal', '_comp_face', '_proj_dist', 'total_area',
        'faces')

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
        
        
        all_vertices = set()
        for face in self.faces:
            all_vertices |= set(self._obj.data.faces[face].vertices)
        
        mean_x = 0.
        mean_y = 0.
        for vertex in all_vertices:
            mean_x += self._obj.data.vertices[vertex].co.x
            mean_y += self._obj.data.vertices[vertex].co.y
        
        mean_x /= len(all_vertices)
        mean_y /= len(all_vertices)
        
        # Set the location (given the applied rotation)
        self._obj.location = (-mean_x, -mean_y, -self._obj.data.vertices[point].co.z)
        
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
        face_sets = []
        
        # We take the MAX_FACES largest faces and the associated points.
        faces = heapq.nlargest(MAX_FACES, obj.data.faces,
            lambda face: face.area)
        points = set()
        for face in faces:
            points |= set(face.vertices)
        points = list(points)
        
        # Initial face clustering
        while faces:
            current_face = faces.pop()
            
            set_found = False
            for face_set in face_sets:
                if face_set.test_face(current_face):
                    set_found = True
                    break
            
            if not set_found:
                face_sets.append(PlanarFacesSet(obj, current_face))
        
        # We now take the PROPOSAL_COUNT largest face sets which are not
        # inside of the object.
        
        face_sets_heap = []
        for id, f_set in enumerate(face_sets):
            heapq.heappush(face_sets_heap, (-f_set.total_area, id, f_set))
        
        valid_face_sets = []
        
        while len(valid_face_sets) < PROPOSAL_COUNT and face_sets_heap:
            _, _, face_set = heapq.heappop(face_sets_heap)
            vector, point = face_set.get_plane()
            
            ref_proj = vector.dot(obj.data.vertices[point].co)
            is_valid = True
            
            for point_ident in points:
                proj = vector.dot(obj.data.vertices[point_ident].co)
                if proj > ref_proj:
                    error = abs(proj - ref_proj) / abs(proj) if proj else 1.0
                    if error > OUTSIDE_PROJ_TOLERANCE:
                        is_valid = False
                        break
            
            if is_valid:
                valid_face_sets.append(face_set)
        
        self.face_sets = valid_face_sets
    
    def __len__(self):
        return len(self.face_sets)
    
    def __repr__(self):
        return "<SupportPlanes: %r>" % self.face_sets
    
    def __getitem__(self, key):
        return self.face_sets[key]
    
    def __iter__(self):
        return iter(self.face_sets)

if __name__ == '__main__':
    obj = bpy.context.active_object
    
    sp = SupportPlanes(obj)
    sp[0].select()
