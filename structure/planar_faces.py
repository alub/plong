import bpy

MAX_ANGLE = .01
ALIGN_TOLERANCE = .1

class PlanarFacesSet(object):
    def __init__(self, obj, initial_face):
        self._obj = obj
        self._normal = initial_face.normal
        self._comp_face = initial_face
        self._proj_dist = initial_face.normal.dot(initial_face.center)
        self.total_area = initial_face.area
        self.faces = {initial_face}
    
    def test_face(self, face):
        """
        Checks if the given face should be in the set, and adds
        it if it the case.
        """
        
        
        if self._normal.angle(face.normal) <= MAX_ANGLE:
            if face not in self.faces:
                proj = self._normal.dot(face.center)
                if abs(self._proj_dist - proj) / abs(self._proj_dist) < ALIGN_TOLERANCE:
                    self.faces.add(face)
                    self.total_area += face.area
            
                    return True
        
        return False
    
    def select_all(self):
        """
        Select all faces from the plane.
        """
        
        for face in self.faces:
            face.select = True
    
    def get_plane(self):
        """
        Returns a vector and a point defining the plane containing
        the faces.
        """
        
        points = set()
        for face in self.faces:
            points.update(face.vertices)
        
        vertices = self._obj.data.vertices
        
        chosen_point = points.pop()
        best_distance = self._normal.dot(vertices[chosen_point].co)
        
        for point in points:
            distance = self._normal.dot(vertices[point].co)
            if distance > best_distance:
                chosen_point = point
                best_distance = distance
        
        return self._normal, point
    
    def __repr__(self):
        return "<PlanarFacesSet: %r>" % self.faces

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
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    
    obj = bpy.data.objects["Eggshape"]
    
    face_sets = cluster_planar_faces(obj)
    face_sets[9].select_all()
    #obj.data.vertices[point].select = True
    #print(vector)
    
    bpy.ops.object.mode_set(mode='EDIT')