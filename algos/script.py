import bpy 

def neighbour(indA, indB):
    bpy.ops.object.mode_set(mode = 'OBJECT')
    obj = bpy.context.active_object
    edges = obj.data.edges
    va0 = edges[indA].vertices[0]
    va1 = edges[indA].vertices[1]
    vb0 = edges[indB].vertices[0]
    vb1 = edges[indB].vertices[1]
    return (va0 == vb0 or va0 == vb1 or va1 == vb1 or va1 == vb0)

def separate_holes(edgeIndexList) :
    holes = [] # a list of lists of edges...
    num_holes = 0
    i = 0
    if edgeIndexList != [] :
        edge_new = edgeIndexList.pop(0)
    hole = [] # first hole starts with first edge
    while edgeIndexList != []:
        n_e = len(edgeIndexList)
        i = 0
        while i<n_e and not(neighbour(edge_new, edgeIndexList[i])) : #search for a neighbourind edge
            i = i + 1
        if n_e == 1 :# this was the last edge
            hole.append(edge_new)
            hole.append(edgeIndexList.pop(i))
            holes.append(hole)
        elif i == n_e : # if none the hole is complete
            num_holes = num_holes + 1
            holes.append(hole)
            edge_new = edgeIndexList.pop(0) # a new hole is started
            hole = []
        else :
            hole.append(edge_new)
            edge_new = edgeIndexList.pop(i)
    return holes

#main
sel_edges = []
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='DESELECT')
bpy.ops.mesh.select_non_manifold()
bpy.ops.object.editmode_toggle()
bpy.ops.object.editmode_toggle()
cube = bpy.data.objects["Cube"]
for edge in cube.data.edges :
    if edge.select :
        sel_edges.append(edge.index)
     
holes = separate_holes(sel_edges)


bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='DESELECT')

if holes!=[]:
    for hole in holes :
        print("hole number")
        print(holes.index(hole))
        print(hole)

bpy.ops.object.mode_set(mode='OBJECT')       
hole1 = holes[0]
for edgeInd in hole1 :
    bpy.context.active_object.data.edges[edgeInd].select = True
bpy.ops.object.mode_set(mode='EDIT')