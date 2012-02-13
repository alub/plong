import bpy

meshes = bpy.data.meshes[0]
edges = meshes.edges
testedEdges = []
nbPassages = 0
   
# purge non-manifold faces and select holes
def cleanAndSelect():
    setSelectMode(mode='EDGE')
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_non_manifold()
    setSelectMode(mode='VERTEX')
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.delete(type='FACE')
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
    global nbPassages
    if cleanAndSelect() :
        nbPassages = nbPassages + 1
        if nbPassages < 60:
            if nbPassages == 50:
                print('Too long...')
            i = 0
            while (i<len(edges)) and (edges[i].select == False or edges[i] in testedEdges):
                i = i+1 
            if i == len(edges):
                return
            print('new i tested is ',i)
            borderEdge = edges[i]
            testedEdges.append(borderEdge)
            for e in edges:
                if e != borderEdge:
                    e.select = False
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.loop_multi_select()
            bpy.ops.mesh.fill()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.normals_make_consistent(inside=False)
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode='OBJECT')
            fillAndCheck()
            
# change the current select mode
def setSelectMode(mode):
    if mode == 'VERTEX':
        bpy.context.tool_settings.mesh_select_mode[0] = True
        bpy.context.tool_settings.mesh_select_mode[1] = False
        bpy.context.tool_settings.mesh_select_mode[2] = False
    if mode == 'EDGE':
        bpy.context.tool_settings.mesh_select_mode[0] = False
        bpy.context.tool_settings.mesh_select_mode[1] = True
        bpy.context.tool_settings.mesh_select_mode[2] = False
    if mode == 'FACE':
        bpy.context.tool_settings.mesh_select_mode[0] = False
        bpy.context.tool_settings.mesh_select_mode[1] = False
        bpy.context.tool_settings.mesh_select_mode[2] = True
      
# main function
def main():
    fillAndCheck()        


# actual call
main()