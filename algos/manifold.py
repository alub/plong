import bpy

def init():
    global edges
    global testedEdges
    global nbPassages
    global nbHolesFilled
    edges = bpy.data.meshes[1].edges
    testedEdges = []
    nbPassages = 0
    nbHolesFilled = 0
   
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
    for i in edges:
        if i.select == True:
            not_manifold = True
    return not_manifold

# fill selected holes and act recursively if there are still holes
def fillAndCheck():
    global edges
    global testedEdges
    global nbPassages
    global nbHolesFilled
    if cleanAndSelect() :
        i = 0
        while (i<len(edges)) and (edges[i].select == False or edges[i] in testedEdges): i = i+1 
        if i == len(edges): return
        borderEdge = edges[i]
        testedEdges.append(borderEdge)
        bpy.ops.object.mode_set(mode='OBJECT')    
        for e in edges:
            if e != borderEdge:
                e.select = False
        bpy.ops.object.mode_set(mode='EDIT')  
        bpy.ops.mesh.loop_multi_select()
        bpy.ops.mesh.fill()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.mesh.select_all(action='DESELECT')
        nbHolesFilled = nbHolesFilled+1
        fillAndCheck()
            
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
    init()
    fillAndCheck()
    print('Number of holes filled: ', nbHolesFilled)    


# actual call
main()