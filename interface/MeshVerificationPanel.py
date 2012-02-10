import bpy
from bpy import *

class MeshVerificationPanel(bpy.types.Panel):
    bl_label = "Mesh Verification"
    bl_idname = "MeshVerification"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    def draw(self, context):

        layout = self.layout

        obj = context.object
 
        row = layout.row()
        row.label(text="Verify your mesh before printing it", icon='WORLD_DATA')
        
        row = layout.row()
        row.label(text="Active object is : " + obj.name)

        row = layout.row()
        row.label(text="---------------------------------------------------------------------------")
        

        row = layout.row()
        row.operator("ManifoldfWatertight")        
       
        row = layout.row()
        row.label(text="---------------------------------------------------------------------------") 
    
        row = layout.row()
        row.operator("CheckOrientation")
        

class ManifoldWatertight(bpy.types.Operator):
    bl_idname = "ManifoldfWatertight"
    bl_label = "Check the mesh"
    
    def execute(self, context) :
        print("Manifold and watertight characteristics checked")

class CheckOrientation(bpy.types.Operator):
    bl_idname = "CheckOrientation"
    bl_label = "Check the orientation"
    
    def execute(self, context) :
        print("Orientation checked")


def register():
    bpy.utils.register_class(MeshVerificationPanel)
    bpy.utils.register_class(ManifoldWatertight)
    bpy.utils.register_class(CheckOrientation)
    

def unregister():
    bpy.utils.unregister_class(MeshVerificationPanel)
    bpy.utils.unregister_class(ManifoldWatertight)
    bpy.utils.unregister_class(CheckOrientation)
        
       

if __name__ == "__main__":
    register()
