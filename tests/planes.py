import bpy
import pprint
from mathutils import Vector

def cluster_normals(mesh, max_angle=0.02):
    bpy.ops.object.mode_set(mode='OBJECT')
    clusters = [[mesh.faces[0]]]
    for face in mesh.faces[1:]:
        affected = False
        for cluster in clusters:
            if face.normal.angle(cluster[0].normal) < max_angle:
                cluster.append(face)
                affected = True
                break
        if not affected:
            clusters.append([face])
    return clusters

c = cluster_normals(bpy.data.meshes['Torus'])
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(c[0])

# Faces selection mode
bpy.context.tool_settings.mesh_select_mode[0] = False
bpy.context.tool_settings.mesh_select_mode[1] = False
bpy.context.tool_settings.mesh_select_mode[2] = True

bpy.ops.object.mode_set(mode='OBJECT')

for f in bpy.data.meshes['Torus'].faces:
    f.select = False

for f in c[3]:
    f.select = True
    
bpy.ops.object.mode_set(mode='EDIT')