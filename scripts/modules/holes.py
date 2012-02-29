import bpy 

def is_neighbour(edges, ind, vertex):
    """
    This function determines if an edge in the active mesh contains a vertex
    
    :param ind: indexes of edges in the active object
    :type ind: list
    :returns: a boolean, True if and only if the two indicated edges are neihgbours in the active object
    """
    obj = bpy.context.active_object
    vertices = obj.data.vertices
    vb0 = edges[ind].vertices[0]
    vb1 = edges[ind].vertices[1]
    if vertex == vb0:
        return vb1
    elif vertex == vb1:
        return vb0
    else:
        return False
    
def separate_holes(edges, edgeIndexList) :
    """
    :param edgeIndexList: a list of edges of multiples holes in a 3D mesh
    :type edgeIndexList: list
    :returns: a list of lists of edges where each list represents a hole 
    """
    holes = [] # a list of lists of edges...
    uho = [] # a list of unidentified hole objects
    i = 0
    if edgeIndexList != [] :
        edge_new = edgeIndexList.pop(0)
    hole = [] # first hole starts with first edge
    v_index = edges[edge_new].vertices[0]
    while edgeIndexList != []:
        n_e = len(edgeIndexList)
        i = 0
        while i<n_e and not(is_neighbour(edges, edgeIndexList[i], v_index)) : #search for a neighbouring edge
            i = i + 1
        if i == n_e : # if none the hole is complete
            hole.append(edge_new)
            if len(hole) <= 2:
                uho.append(hole)
            else:
                holes.append(hole)
            edge_new = edgeIndexList.pop(0) # a new hole is started
            v_index = edges[edge_new].vertices[0]
            hole = []
        elif n_e == 1 :# this was the last edge
            hole.append(edge_new)
            hole.append(edgeIndexList.pop(i))
            holes.append(hole)
        else :
            v_index = is_neighbour(edges, edgeIndexList[i], v_index)
            hole.append(edge_new)
            edge_new = edgeIndexList.pop(i)
    #print(holes)
    #print(uho)
    return holes, uho

def clean_zero_edges():
    """
    This functions checks the mesh for edges that are part of no face and deletes them.    
    """
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    obj = bpy.context.active_object.data
    edges_copy = [edge.key for edge in obj.edges] # mapping from edge to adjacent faces
    for ThisFace in obj.faces :
        for ThisEdge in ThisFace.edge_keys :
            if ThisEdge in edges_copy:
                edges_copy.remove(ThisEdge)
    #print(edges_copy)
    for edge in obj.edges:
        if edge.key in edges_copy:
            edge.select = True
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.delete(type='EDGE')
            
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
