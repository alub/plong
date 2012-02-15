import bpy
import py_holes

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
        
# return a list of holes from non-manifold selected edges
def getHoles():
    global edges
    sel_edges = []
    setSelectMode('EDGE')
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_non_manifold()
    bpy.ops.object.mode_set(mode='OBJECT')
    for e in edges :
        if e.select == True :
            sel_edges.append(e.index)
    holes = py_holes.separate_holes(sel_edges)
    bpy.ops.object.mode_set(mode='EDIT')
    return holes


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
    
# change the current select mode
def setSelectMode(mode):
    if mode == 'VERTEX':
       bpy.context.tool_settings.mesh_select_mode = [True, False, False]
    if mode == 'EDGE':
        bpy.context.tool_settings.mesh_select_mode = [False, True, False]
    if mode == 'FACE':
        bpy.context.tool_settings.mesh_select_mode = [False, False, True]

# main function
def main():
    global edges
    init()
    name = bpy.context.active_object.name
    print('Trying to repairs holes in object: ', name)
    edges = bpy.data.meshes[name].edges
    py_holes.init_script(edges)
    fillAndCheck()

        
# actual call
main()