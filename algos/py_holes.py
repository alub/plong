import bpy 

def init_script(_edges):
    global edges
    edges = _edges

def neighbour(indA, indB):
    """
    parameters : 
        > indA, indB : indexes of edges in the active object
    returns :
        > a boolean, true if and only if the two indicated edges are neihgbours in the active object
    """
    global edges
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
        while i<n_e and not(neighbour(edge_new, edgeIndexList[i])) : #search for a neighbourind edge
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
        
#main
def test():
    sel_edges = []
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_non_manifold()
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.mode_set(mode = 'OBJECT')
    obj = bpy.context.active_object
    for edge in obj.data.edges :
        if edge.select :
            sel_edges.append(edge.index)
         
    holes = separate_holes(sel_edges)
    
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    
    if holes!=[]:
        for hole in holes :
            selectHole(hole)
            bpy.ops.object.mode_set(mode='EDIT')
    
    bpy.ops.object.mode_set(mode='OBJECT')       
    hole1 = holes[0]
    for edgeInd in hole1 :
        bpy.context.active_object.data.edges[edgeInd].select = True
    bpy.ops.object.mode_set(mode='EDIT')