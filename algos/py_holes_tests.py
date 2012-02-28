import bpy 

def is_neighbour(indA, indB):
    """
    This function determines if two edges in the active mesh are neighbours
    parameters : 
        > indA, indB : indexes of edges in the active object
    returns :
        > a boolean, true if and only if the two indicated edges are neihgbours in the active object
    """
    bpy.ops.object.mode_set(mode = 'OBJECT')
    obj = bpy.context.active_object
    edges = obj.data.edges
    va0 = edges[indA].vertices[0]
    va1 = edges[indA].vertices[1]
    vb0 = edges[indB].vertices[0]
    vb1 = edges[indB].vertices[1]
    return (va0 == vb0 or va0 == vb1 or va1 == vb1 or va1 == vb0)

def separate_holes(edgeIndexList) :
    """
    parameters : 
        > edgeIndexList : a list of edges of multiples holes in a 3D mesh
    returns :
        > a list of lists of edges where each list represents a hole 
    """
    holes = [] # a list of lists of edges...
    num_holes = 0
    i = 0
    if edgeIndexList != [] :
        edge_new = edgeIndexList.pop(0)
    hole = [] # first hole starts with first edge
    while edgeIndexList != []:
        n_e = len(edgeIndexList)
        i = 0
        while i<n_e and not(is_neighbour(edge_new, edgeIndexList[i])) : #search for a neighbourind edge
            i = i + 1
        if i == n_e : # if none the hole is complete
            num_holes = num_holes + 1
            hole.append(edge_new)
            holes.append(hole)
            edge_new = edgeIndexList.pop(0) # a new hole is started
            hole = []
        elif n_e == 1 :# this was the last edge
            hole.append(edge_new)
            hole.append(edgeIndexList.pop(i))
            holes.append(hole)
        else :
            hole.append(edge_new)
            edge_new = edgeIndexList.pop(i)
    return holes


def clean_zero_edges():
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    obj = bpy.context.active_object.data
    edges_copy = [edge.key for edge in obj.edges] # mapping from edge to adjacent faces
    for ThisFace in obj.faces :
        for ThisEdge in ThisFace.edge_keys :
            if ThisEdge in edges_copy:
                edges_copy.remove(ThisEdge)
    print(edges_copy)
    for edge in obj.edges:
        if edge.key in edges_copy:
            edge.select = True
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.delete(type='EDGE')


def select_to_list():
    sel_edges = []
    bpy.ops.object.mode_set(mode = 'OBJECT')
    obj = bpy.context.active_object
    for edge in obj.data.edges :
        if edge.select :
            sel_edges.append(edge.index)
    return sel_edges
    
def test3():
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_non_manifold()
    sel_edges =select_to_list()
    bpy.ops.object.mode_set(mode = 'OBJECT')
    obj = bpy.context.active_object.data
    ef = edgeToFaces()
    edgearite = {}
    for edge in sel_edges:
        edgearite[edge] = (len(ef.get(obj.edges[edge].key)))
    print(edgearite)     