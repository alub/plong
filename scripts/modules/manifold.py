import bpy
import sys
import time
import holes
        
def clean_and_select(edges):
    """Remove reduntant faces and edges then select all non manifold edges
    returns :
        > is the resulting active object non manifold
    """
    edges = bpy.context.active_object.data.edges
    set_selectmode(mode='EDGE')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_non_manifold()
    set_selectmode(mode='VERTEX')
    bpy.ops.mesh.delete(type='FACE')
    bpy.ops.mesh.select_all(action='DESELECT')
    set_selectmode(mode='EDGE')
    bpy.ops.mesh.select_non_manifold()
    bpy.ops.object.mode_set(mode='OBJECT')
    not_manifold = False
    for e in edges:
        if e.select:
            not_manifold = True
    bpy.ops.object.mode_set(mode='EDIT')
    return not_manifold

def fill_and_check(edges, destructive, fast_processing, old_nb_edges):
    """Fill selected holes and purge the meshes according to the parameters
    parameters :
        > destructive : allow the method to supress some vertices in order to obtain a full manifold object
        > fast_processing : allow fast-processing which can result in bad accurate meshes
        > old_nb_edges : used for recursivity purposes
    returns :
        > 1 if the resulting object is still not manifold, 2 otherwise
    """
    if clean_and_select(edges):
        edges_holes, uho, nb_edges = get_holes(edges)
        if(nb_edges != old_nb_edges):
            set_selectmode(mode='EDGE')
            if fast_processing:
                print(nb_edges, "edges non manifold left")
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.object.mode_set(mode='OBJECT')
                for hole in edges_holes:
                   # sys.stdout.write('.%s' % len(hole))
                   # sys.stdout.flush()
                    select_hole(edges, hole)
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.fill()
                # sys.stdout.write('\n')
                return fill_and_check(edges, destructive, fast_processing, nb_edges)
            else:
                sys.stdout.write("%s edges non manifold left" % nb_edges)
                sys.stdout.flush()
                for hole in edges_holes:
                    #sys.stdout.write('.%s' % len(hole))
                    sys.stdout.write('.')
                    sys.stdout.flush()
                    bpy.ops.mesh.select_all(action='DESELECT')
                    bpy.ops.object.mode_set(mode='OBJECT')
                    select_hole(hole)
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.fill()
                sys.stdout.write('\n')
                return fill_and_check(edges, destructive, fast_processing, nb_edges)
        else:
            if destructive:
                print('Filling can\'t process further, removing broken vertices...')
                bpy.ops.mesh.delete(type='VERT')
                return fill_and_check(edges, destructive, fast_processing, 0)
            else:
                print('Filling can\'t process further, end of process')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.normals_make_consistent(inside=False)
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.object.mode_set(mode='OBJECT')
                return 1
    else:
        print('Repairing complete')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        return 2
        
def get_holes(edges):
    """
    returns :
        > a list of holes from the non-manifold selected edges
    """
    nb_edges = 0
    sel_edges = []
    bpy.ops.object.mode_set(mode='OBJECT')
    for e in edges :
        if e.select == True :
            nb_edges = nb_edges+1
            sel_edges.append(e.index)
    edges_holes, uho = holes.separate_holes(edges, sel_edges)
    bpy.ops.object.mode_set(mode='EDIT')
    return edges_holes, uho, nb_edges

def select_hole(edges, edgeList) :
    """visually select a hole from its edges list
    parameters :
        > edgeList : contains the indices of one hole's edges
    """
    for index in edgeList :
            edges[index].select = True
    
def set_selectmode(mode):
    """Change the selectMode
    parameters :
        > mode : one of the following: 'VERTEX', 'EDGE', 'FACE'
    """
    if mode == 'VERTEX':
       bpy.context.tool_settings.mesh_select_mode = [True, False, False]
    if mode == 'EDGE':
        bpy.context.tool_settings.mesh_select_mode = [False, True, False]
    if mode == 'FACE':
        bpy.context.tool_settings.mesh_select_mode = [False, False, True]


def correction(destructive, fast_processing):
    """Main function which try to correct the active-object
    parameters :
        > destructive : allow the method to supress some vertices in order to obtain a full manifold object
        > fast_processing : allow fast-processing which can result in bad accurate meshes
    returns :
        > 1 if the resulting object is still not manifold, 2 otherwise
    """
    bpy.ops.object.mode_set(mode='EDIT')
    edges = bpy.context.active_object.data.edges
    if destructive and fast_processing:
        print('Fast-processing and destructive repairing of object ', bpy.context.active_object.name)
    elif destructive and not fast_processing:
        print('Accurate and destructive repairing of object ', bpy.context.active_object.name)
    elif not destructive and fast_processing:
        print('Fast-processing simple cleaning of object ', bpy.context.active_object.name)
    else:
        print('Accurate simple cleaning of object ', bpy.context.active_object.name)
    step = fill_and_check(edges, destructive, fast_processing, 0)
    return step


def test(destructive, fast_processing):
    td = time.time()    
    step = correction(destructive, fast_processing)
    print('NEXT STEP : ', step)
    #bpy.ops.object.mode_set(mode='EDIT')
    #clean_and_select()
    #edges_holes, uho ,nbedges = get_holes()
    #bpy.ops.object.mode_set(mode='EDIT')
    #bpy.ops.mesh.select_all(action='DESELECT')
    #bpy.ops.object.mode_set(mode='OBJECT')
    #for hole in edges_holes:
    #    select_hole(hole)
    #bpy.ops.object.mode_set(mode='EDIT')
    tf = time.time()-td
    print('ELAPSED TIME: ', tf)
