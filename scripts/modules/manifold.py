import bpy
import sys
import time
from modules import holes
from modules.gui import ProgressText
        
def clean_and_select(edges):
    """
    Remove reduntant faces and edges then select all non manifold edges

    :returns: the resulting active object non manifold
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

def fill_and_check(edges, destructive, fast_processing, old_nb_edges, pt):
    """
    Fill selected holes and purge the meshes according to the parameters :

    :param destructive: allow the method to supress some vertices in order to obtain a full manifold object
    :type destructive: bool
    :param fast_processing: allow fast-processing which can result in bad accurate meshes
    :type fast_processing: bool
    :param old_nb_edges: used for recursivity purposes
    :type old_nb_edges: int
    :returns: 1 if the resulting object is still not manifold, 2 otherwise
    """
    if clean_and_select(edges):
        edges_holes, uho, nb_edges = get_holes(edges)
        if(nb_edges != old_nb_edges):
            set_selectmode(mode='EDGE')
            if fast_processing:
                pt.output("%d edges non manifold left\n" % nb_edges)
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.object.mode_set(mode='OBJECT')
                for hole in edges_holes:
                   # sys.stdout.write('.%s' % len(hole))
                   # sys.stdout.flush()
                    select_hole(edges, hole)
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.fill()
                # sys.stdout.write('\n')
                return fill_and_check(edges, destructive, fast_processing, nb_edges, pt)
            else:
                pt.output("%d edges non manifold left" % nb_edges)
                for hole in edges_holes:
                    #sys.stdout.write('.%s' % len(hole))
                    pt.output('.')
                    bpy.ops.mesh.select_all(action='DESELECT')
                    bpy.ops.object.mode_set(mode='OBJECT')
                    select_hole(edges, hole)
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.fill()
                pt.output("\n")
                return fill_and_check(edges, destructive, fast_processing, nb_edges, pt)
        else:
            if destructive:
                pt.output("Filling can\'t process further, removing broken vertices...\n")
                bpy.ops.mesh.delete(type='VERT')
                return fill_and_check(edges, destructive, fast_processing, 0, pt)
            else:
                pt.output("Filling can\'t process further, end of process\n")
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.normals_make_consistent(inside=False)
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.object.mode_set(mode='OBJECT')
                return 1
    else:
        pt.output("Repairing complete\n")
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        return 2
        
def get_holes(edges):
    """
    :returns: a list of holes from the non-manifold selected edges
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
    """
    Visually select a hole from its edges list
    :param edgeList: contains the indices of one hole's edges
    :type edgeList: list
    """
    for index in edgeList :
            edges[index].select = True
    
def set_selectmode(mode):
    """
    Change the selectMode

    :param mode: one of the following: 'VERTEX', 'EDGE', 'FACE'
    """
    if mode == 'VERTEX':
       bpy.context.tool_settings.mesh_select_mode = [True, False, False]
    if mode == 'EDGE':
        bpy.context.tool_settings.mesh_select_mode = [False, True, False]
    if mode == 'FACE':
        bpy.context.tool_settings.mesh_select_mode = [False, False, True]


def correction(destructive, fast_processing):
    """
    Main function which try to correct the active-object

    :param destructive: allow the method to supress some vertices in order to obtain a full manifold object
    :type destructive: bool
    :param fast_processing: allow fast-processing which can result in bad accurate meshes
    :type fast_processing: bool
    :returns: 1 if the resulting object is still not manifold, 2 otherwise
    """
    bpy.ops.object.mode_set(mode='EDIT')
    edges = bpy.context.active_object.data.edges
    with ProgressText("Manifold correction") as pt:

        if destructive and fast_processing:
            pt.output("Fast-processing and destructive repairing of object %s:\n" %
                bpy.context.active_object.name)
        elif destructive and not fast_processing:
            pt.output("Accurate and destructive repairing of object %s:\n" %
                bpy.context.active_object.name)
        elif not destructive and fast_processing:
            pt.output("Fast-processing simple cleaning of object %s:\n" %
                bpy.context.active_object.name)
        else:
            pt.output("Accurate simple cleaning of object %s:\n" %
                bpy.context.active_object.name)
        step = fill_and_check(edges, destructive, fast_processing, 0, pt)
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
