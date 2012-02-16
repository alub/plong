import bpy
from mathutils.geometry import distance_point_to_plane, area_tri
from mathutils import Vector, Matrix

class OrientationException(Exception):
    pass

mesh = bpy.data.meshes['Cube']
ob = bpy.data.objects['Cube']
volume = 0
m100 = m010 = m001 = 0 # Geometric moments
orig = Vector((0,0,0))
eps = 1e-15

for face in mesh.faces:
    distance = distance_point_to_plane(orig, face.center, face.normal)
    # minus sign, assuming normals are directed towards the outside
    face_vol = - face.area * distance / 3
    volume += face_vol
    nb_edges = len(face.vertices)
    
    if nb_edges == 3:
        v = [mesh.vertices[face.vertices[i]].co for i in range(3)]
        m100 += face_vol * (v[0][0] + v[1][0] + v[2][0]) / 4
        m010 += face_vol * (v[0][1] + v[1][1] + v[2][1]) / 4
        m001 += face_vol * (v[0][2] + v[1][2] + v[2][2]) / 4
    elif nb_edges == 4:
        v = [mesh.vertices[face.vertices[i]].co for i in range(4)]
        # let's cut the quad in triangles!
        # triangle 1: vertices 0, 1, 2
        area1 = area_tri(mesh.vertices[face.vertices[0]].co,
                         mesh.vertices[face.vertices[1]].co,
                         mesh.vertices[face.vertices[2]].co)
        face_vol1 = - area1 * distance / 3
        m100 += face_vol1 * (v[0][0] + v[1][0] + v[2][0]) / 4
        m010 += face_vol1 * (v[0][1] + v[1][1] + v[2][1]) / 4
        m001 += face_vol1 * (v[0][2] + v[1][2] + v[2][2]) / 4
        # triangle 2: vertices 2, 3, 0
        area2 = area_tri(mesh.vertices[face.vertices[2]].co,
                         mesh.vertices[face.vertices[3]].co,
                         mesh.vertices[face.vertices[0]].co)
        face_vol2 = - area2 * distance / 3
        m100 += face_vol2 * (v[0][0] + v[2][0] + v[3][0]) / 4
        m010 += face_vol2 * (v[0][1] + v[2][1] + v[3][1]) / 4
        m001 += face_vol2 * (v[0][2] + v[2][2] + v[3][2]) / 4
    else:
         raise OrientationException
        
print("Volume: %s" % volume)
print("CoG: %s, %s, %s" % (m100, m010, m001))

center_of_gravity = Vector((m100, m010, m001))
point_a = mesh.faces[0].center # completely arbitrary

intersections_count = 0

# http://blenderartists.org/forum/showthread.php?195605-Detecting-if-a-point-is-inside-a-mesh-2.5-API
orig = center_of_gravity
axis = mesh.faces[0].center
while True:
    location, normal, index = ob.ray_cast(orig, orig + axis * 10000.0)
    if index == -1:
        break
    intersections_count += 1
    orig = location + axis * 0.00001

print("Number of intersections: %s" % intersections_count)

if intersections_count % 2 == 0:
    print("Center of gravity is outside the object.\n")
else:
    print("Center of gravity is inside the object.\n")