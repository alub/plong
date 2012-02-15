import bpy

def init():
    global edges
    global nbHolesFilled
    global nbPassages
    edges = bpy.data.meshes[0].edges
    nbHolesFilled = 0
    nbPassages = 0
   
# purge non-manifold faces and select holes
def cleanAndSelect():
    global edges
    setSelectMode(mode='EDGE')
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_non_manifold()
    setSelectMode(mode='VERTEX')
    bpy.ops.mesh.delete(type='FACE')
    bpy.ops.mesh.select_all(action='DESELECT')
    setSelectMode(mode='EDGE')
    bpy.ops.mesh.select_non_manifold()
    bpy.ops.object.mode_set(mode='OBJECT')
    not_manifold = False
    for e in edges:
        if e.select:
            not_manifold = True
    return not_manifold

# fill selected holes and act recursively if there are still holes
def fillAndCheck():
    global edges
    global nbHolesFilled
    global nbPassages
    bpy.ops.object.mode_set(mode='EDIT')
    if nbPassages < 5 and cleanAndSelect() :
        nbPassages = nbPassages+1
        holes = getHoles()
        for hole in holes:
            selectHole(hole)
            bpy.ops.mesh.fill()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.mesh.select_all(action='DESELECT')
        fillAndCheck()
            
# change the current select mode
def setSelectMode(mode):
    if mode == 'VERTEX':
        bpy.context.tool_settings.mesh_select_mode = [True, False, False]
    if mode == 'EDGE':
        bpy.context.tool_settings.mesh_select_mode = [False, True, False]
    if mode == 'FACE':
        bpy.context.tool_settings.mesh_select_mode = [False, False, True]
        
def neighbour(indA, indB):
    """
    parameters : 
        > indA, indB : indexes of edges in the active object
    returns :
        > a boolean, true if and only if the two indicated edges are neihgbours in the active object
    """
    global edges
    va0 = edges[indA].vertices[0]
    va1 = edges[indA].vertices[1]
    vb0 = edges[indB].vertices[0]
    vb1 = edges[indB].vertices[1]
    return (va0 == vb0 or va0 == vb1 or va1 == vb1 or va1 == vb0)

# visually select a hole from its edges list
def selectHole(edgeList) :
    global edges
    bpy.ops.mesh.select_all(action='DESELECT')
    setSelectMode(mode='EDGE')
    bpy.ops.object.mode_set(mode='OBJECT')
    for e in edges :
        if e.index in edgeList :
            e.select = True
    bpy.ops.object.mode_set(mode='EDIT')
     
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
        if n_e == 1 :# this was the last edge
            hole.append(edge_new)
            hole.append(edgeIndexList.pop(i))
            holes.append(hole)
        elif i == n_e : # if none the hole is complete
            num_holes = num_holes + 1
            hole.append(edge_new)
            holes.append(hole)
            edge_new = edgeIndexList.pop(0) # a new hole is started
            hole = []
        else :
            hole.append(edge_new)
            edge_new = edgeIndexList.pop(i)
    return holes

# return a list of holes from non-manifold selected edges
def getHoles():
    global edges
    global holes
    sel_edges = []
    setSelectMode(mode='EDGE')
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_non_manifold()
    bpy.ops.object.mode_set(mode='OBJECT')
    for e in edges :
        if e.select == True :
            sel_edges.append(e.index)
    holes = separate_holes(sel_edges)
    bpy.ops.object.mode_set(mode='EDIT')
    return holes

# entry point to all subfunctions, clean one object
def fillOneObject(_edges):
    global edges
    global nbHolesFilled
    edges = _edges
    init()
    fillAndCheck()

# main function
def main():
    for mesh in bpy.data.meshes.values():
        fillOneObject(mesh.edges)


# actual call
main()