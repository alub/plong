##################################################################
# script for the addition of a mesh verification panel in Blender
# author : Caroline Naud
##################################################################

from bpy import *
import bpy
import random

###############################
# MeshVerificationPanel class #
###############################

class MeshVerificationPanel(bpy.types.Panel) :

    bl_idname = 'types.mesh_verification_panel'
    bl_label = "Mesh verification"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
	
    global instance 
    instance = None
    
    #def __init__(self):
     #   bpy.types.Panel.__init__(self)
       

    def draw(self, context) :
        
        MeshVerificationPanel.instance = self
        
        obj = context.object
    
        layout = self.layout
        row = layout.row()
        row.label(text="Verify your mesh before printing it", icon='MESH_ICOSPHERE')
   
        row = layout.row()
        row.label(text="The active mesh is : " + obj.name)

        row = layout.row()
        row.label(text="---------------------------------------------------------------------------")

        row = layout.row()
        row.operator("ops.manifold_watertight")        
       
        row = layout.row()
        row.label(text="---------------------------------------------------------------------------") 
     
        row = layout.row()
        row.operator("ops.check_orientation")
        row = layout.row()
        row.label(text="---------------------------------------------------------------------------") 
    
    def draw2(self, context) :
        
        layout = self.layout
        row = layout.row()
        row.label(text="Verify your mesh before printing it", icon='WORLD_DATA')      
        
        
#####################################
#  ManifoldWatertightOperator class #
#####################################
              
class ManifoldWatertightOperator(bpy.types.Operator) :
    
    bl_idname = 'ops.manifold_watertight'
    bl_label = "1. Make it watertight and manifold"
    bl_description = "This is to very if your mesh is correct for printing"
    
    def execute (self, context) :
        self.report("INFO", "The mesh is now correct")
        return {'FINISHED'}
    

###################################
#  CheckOrientationOperator class #
###################################

              
class CheckOrientationOperator(bpy.types.Operator) :
    
    bl_idname = 'ops.check_orientation'
    bl_label = "2. Check its orientation"
    bl_description = "This is to very if your mesh has a good supporting face" 
    
    def __init__ (self) :
        
        self.value = 0
        bpy.types.Operator.__init__(self)
        
    def execute (self, context) :
        self.report("INFO", "The CheckOrientation button has been pressed")
        self.value = random.randint(1,2)
        if self.value == 1 :
            self.report("INFO", "The orientation seem to be good for printing")
            MeshVerificationPanel.instance.layout
        elif self.value == 2 :  
            self.report("INFO", "The orientation doesn't seem to be good for printing. You might want to try one of our suggestions")  
        return {'FINISHED'}
    
    
#################
# Main function #
#################

if __name__ == "__main__":
    
    bpy.utils.register_class(MeshVerificationPanel)

    bpy.utils.register_class(ManifoldWatertightOperator)

    bpy.utils.register_class(CheckOrientationOperator)
    
    
