import bpy

MAX_ANGLE = .01
ALIGN_TOLERANCE = .1

class PlanarFacesSet(object):
    def __init__(self, initial_face):
        self._comp_face = initial_face
        self._proj_dist = initial_face.normal.dot(initial_face.center)
        self.total_area = initial_face.area
        self.faces = {initial_face}
    
    def test_face(self, face):
        if self._comp_face.normal.angle(face.normal) <= MAX_ANGLE:
            if face not in self.faces:
                proj = self._comp_face.normal.dot(face.center)
                if abs(self._proj_dist - proj) / abs(self._proj_dist) < ALIGN_TOLERANCE:
                    self.faces.add(face)
                    self.total_area += face.area
            
                    return True
        
        return False
    
    def select_all(self):
        for face in self.faces:
            print(face)
            face.select = True
    
    def __repr__(self):
        return "<PlanarFacesSet: %r>" % self.faces

def cluster_planar_faces(obj):
    """
    Returns a list of set of faces sharing approximatively
    the same plane.
    """
    
    result = []
    remaining_faces = list(obj.data.faces)
    
    while remaining_faces:
        current_face = remaining_faces.pop()
        
        set_found = False
        for face_set in result:
            if face_set.test_face(current_face):
                set_found = True
                break
        
        if not set_found:
            result.append(PlanarFacesSet(current_face))

    return sorted(result, key=lambda face_set:
        face_set.total_area, reverse=True)

if __name__ == '__main__':
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    face_sets = cluster_planar_faces(bpy.data.objects["Cube.001"])
    face_sets[8].select_all()
    bpy.ops.object.mode_set(mode='EDIT')