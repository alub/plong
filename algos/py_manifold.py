import bpy
import sys
import py_holes

def init():
    global nbHolesFilled
    global nbPassages
    nbHolesFilled = 0
    nbPassages = 0

        
# purge non-manifold faces and select holes
def cleanAndSelect():
    global edges
    setSelectMode(mode='EDGE')
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
    bpy.ops.object.mode_set(mode='EDIT')
    return not_manifold

# fill selected holes and act recursively if there are still holes
def fillAndCheck(destructive, fastProcessing, oldNbEdges):
    global edges
    global nbHolesFilled
    global nbPassages
    if cleanAndSelect():
        holes, nbEdges = getHoles()
        if(nbEdges != oldNbEdges):
            setSelectMode(mode='EDGE')
            if fastProcessing:
                print(nbEdges, "edges non manifold left")
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.object.mode_set(mode='OBJECT')
                for hole in holes:
                    selectHole(hole)
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.fill()
                fillAndCheck(destructive, fastProcessing, nbEdges)
            else:
                sys.stdout.write("%s edges non manifold left" % nbEdges)
                sys.stdout.flush()
                for hole in holes:
                    sys.stdout.write('.')
                    sys.stdout.flush()
                    bpy.ops.mesh.select_all(action='DESELECT')
                    selectHole(hole)
                    bpy.ops.mesh.fill()
                sys.stdout.write('\n')
                fillAndCheck(destructive, fastProcessing, nbEdges)
        else:
            if destructive:
                print('Filling can\'t process further, removing broken vertices...')
                bpy.ops.mesh.delete(type='VERT')
                fillAndCheck(destructive, fastProcessing, 0)
            else:
                print('Filling can\'t process further, end of process')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.normals_make_consistent(inside=False)
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.object.mode_set(mode='OBJECT')
    else:
        print('Repairing complete')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        
# return a list of holes from non-manifold selected edges
def getHoles():
    global edges
    nbEdges = 0
    sel_edges = []
    bpy.ops.object.mode_set(mode='OBJECT')
    for e in edges :
        if e.select == True :
            nbEdges = nbEdges+1
            sel_edges.append(e.index)
    holes = py_holes.separate_holes(edges, sel_edges)
    bpy.ops.object.mode_set(mode='EDIT')
    return holes, nbEdges

# visually select a hole from its edges list
def selectHole(edgeList) :
    global edges
    #bpy.ops.object.mode_set(mode='OBJECT')
    for index in edgeList :
            edges[index].select = True
    #bpy.ops.object.mode_set(mode='EDIT')
    
# change the current select mode
def setSelectMode(mode):
    if mode == 'VERTEX':
       bpy.context.tool_settings.mesh_select_mode = [True, False, False]
    if mode == 'EDGE':
        bpy.context.tool_settings.mesh_select_mode = [False, True, False]
    if mode == 'FACE':
        bpy.context.tool_settings.mesh_select_mode = [False, False, True]

# main function
def correction(destructive, fastProcessing):
    global edges
    if destructive and fastProcessing:
        print('Fast-processing and destructive repairing of object ', bpy.context.active_object.name)
    elif destructive and not fastProcessing:
        print('Accurate and destructive repairing of object ', bpy.context.active_object.name)
    elif not destructive and fastProcessing:
        print('Fast-processing simple cleaning of object ', bpy.context.active_object.name)
    else:
        print('Accurate simple cleaning of object ', bpy.context.active_object.name)
    init()
    edges = bpy.context.active_object.data.edges
    bpy.ops.object.mode_set(mode='EDIT')
    fillAndCheck(destructive, fastProcessing, 0)
        

correction(True, True)