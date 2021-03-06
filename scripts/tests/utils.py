"""
Utility function to prepare a test scene, load objects, etc...
"""

import bpy
import mathutils

def mesh_objects():
    """
    Returns the list of mesh objects on the scene.
    """

    objects = []

    for obj in bpy.data.objects:
        if isinstance(obj.data, bpy.types.Mesh):
            objects.append(obj)
    
    return objects

def unselect_all():
    """
    Unselects every object.
    """
    
    if not mesh_objects():
        return
    
    for ob in bpy.data.objects.values():
        ob.select = False
    
    bpy.context.scene.objects.active = None
    


def select_object(obj):
    """
    Selects an object on the scene
    """

    unselect_all()
    
    bpy.context.scene.objects.active = obj
    obj.select = True


def cleanup():
    """
    Removes every mesh object from the scene.
    """
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    for obj in mesh_objects():
        select_object(obj)
        bpy.ops.object.delete(use_global=False)


def selected_object():
    return bpy.context.scene.objects.active


def import_model(name, scale=None, rotation_xyz=None):
    """
    Import a mesh model (from the models/ directory) into the scene, with
    optional scaling.
    imported_name must be the name of the imported object.
    Returns the imported object.
    """
    
    unselect_all()
    orig = set(bpy.data.objects)
    
    if name.endswith(".ply"):
        bpy.ops.import_mesh.ply(filepath="../models/" + name)
    else:
        bpy.ops.import_mesh.stl(filepath="../models/" + name)
    
    
    unselect_all()
    obj = (set(bpy.data.objects) - orig).pop()
    if scale:
        obj.scale = mathutils.Vector(scale)
        bpy.ops.object.transform_apply(scale=True)
    
    if rotation_xyz:
        obj.rotation_euler = mathutils.Euler(rotation_xyz, 'XYZ')
        bpy.ops.object.transform_apply(rotation=True)
    
    select_object(obj)
    
    return obj

def get_bounds(obj):
    """
    Returns the bounds (xmin, xmax, ymin, ymax, zmin, zmax) of
    an object.
    This method assumes that no transformations are applied to
    the object.
    """
    
    xmin, ymin, zmin = tuple(obj.data.vertices[0].co)
    xmax, ymax, zmax = xmin, ymin, zmin
    
    for point in obj.data.vertices:
        x, y, z = tuple(point.co)
        if x < xmin:
            xmin = x
        elif x > xmax:
            xmax = x
        
        if y < ymin:
            ymin = y
        elif y > ymax:
            ymax = y
        
        if z < zmin:
            zmin = z
        elif z > zmax:
            zmax = z
    
    return xmin, xmax, ymin, ymax, zmin, zmax

def get_selected_points():
    """
    Returns the selected points of the current object.
    """
    
    points = []
    
    for point in bpy.context.active_object.data.vertices:
        if point.select:
            points.append(point)
    
    return points

if __name__ == '__main__':
    cleanup()
    import_model("happy_vrip_res4.ply", scale=(200, 200, 200))
    
