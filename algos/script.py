import bpy

def voisin(edgeA, edgeB):
    va0 = edgeA.vertices[0]
    va1 = edgeA.vertices[1]
    vb0 = edgeB.vertices[0]
    vb1 = edgeB.vertices[1]
    return (va0 == vb0 or va0 == vb1 or va1 == vb1 or va1 == vb0)


sel_edges = []

bpy.ops.mesh.select_non_manifold()
cube = bpy.data.objects["Cube"]
for edge in cube.data.edges :
    if edge.select :
        sel_edges.append(edge)

holes = []
num_holes = 0
i = 0
edge_new = sel_edges.pop(0)
hole = [edge_new]
while sel_edges != []:
    n_e = len(sel_edges)
    i = 0
    while i<n_e and not(voisin(edge_new, sel_edges[i])) : #search for a neighbourind edge
        i = i + 1
    if i == n_e : #if none the hole is complete
        num_holes = num_holes + 1
        holes.append(hole);
        edge_new = sel_edges.pop(0)
        hole = [edge_new]
    else :
        hole.append(edge_new)
        edge_new = sel_edges.pop(i)

def select(edgeList) :
    for edge in edgeList :
        edge.select = True
        

bpy.ops.mesh.select_all(action='TOGGLE')
bpy.ops.object.mode_set(mode='OBJECT')
select(holes[0])