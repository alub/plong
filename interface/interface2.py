###################################################################
# script for the addition of a mesh verification panel in Blender #
# author : Caroline Naud                                          #
###################################################################

from bpy import *
import bpy
import random

step = 1

###############################
# MeshVerificationPanel class #
###############################

class MeshVerificationPanel(bpy.types.Panel) :

    bl_idname = 'types.mesh_verification_panel'
    bl_label = "Mesh verification"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"  

    def draw(self, context) :
        
        obj = context.object
	mesh = obj.data
        scn = context.scene
    
        layout = self.layout
        row = layout.row()
        row.label(text="Verify your mesh before printing it", icon='MESH_ICOSPHERE')
   
        row = layout.row()
        row.label(text="The active mesh is : " + mesh.name)

        row = layout.row()
        row.label(text="------------------------------------------------------------------------------------------------------------------------------------------")

	
        box1 = layout.box()

	if step != 1 :
		box1.enabled = False

	row1 = box1.row()
        row1.label(text="-> Step 1 : Make it watertight & manifold")
       
        row2 = box1.row()
        row2.prop(scn,"FastProcessing")
        
        row3 = box1.row()
        c1 = row3.column()
        c1.operator("ops.non_destructive_manifold_watertight")        
       
        c2 = row3.column()
        c2.operator("ops.destructive_manifold_watertight")
        
        row4 = box1.row()
        row4.label(text="------------------------------------------------------------------------------------------------------------------------------------------") 
      
	box2 = layout.box()

	if step != 2 :
		box2.enabled = False

        row1 = box2.row()
        row1.label(text="-> Step 2 : Generate several adequate supporting plans for printing")
        
        row2 = box2.row()
        row2.operator("ops.generate_plans")
        
        row3 = box2.row()
        row3.label(text="------------------------------------------------------------------------------------------------------------------------------------------") 
     
	box3 = layout.box()

	if step != 3 :
		box3.enabled = False


        row1 = box3.row()
        row1.label(text="-> Step 3 : Choose your object orientation for printing")
        
        row2 = box3.row()
        c1 = row2.column()
        c1.operator("ops.vizualize_previous_plan")        
       
        c2 = row2.column()
        c2.operator("ops.vizualize_next_plan")
        
        row3 = box3.row()
        row3.operator("ops.choose_current_plan")
        
        row4 = box4.row()
        row4.label(text="------------------------------------------------------------------------------------------------------------------------------------------") 
     
###################################################
#  NonDestructiveManifoldWatertightOperator class #
###################################################
              
class NonDestructiveManifoldWatertightOperator(bpy.types.Operator) :
    
    bl_idname = 'ops.non_destructive_manifold_watertight'
    bl_label = "Non destructive method"
    bl_description = "This method won't damage your mesh in any way but might leave some imperfections"
    
    def execute (self, context) :

	global step

        self.report("INFO", "The mesh is now correct")

	step = 2

        return {'FINISHED'}
    
###############################################
# DestructiveManifoldWatertightOperator class #
###############################################
              
class DestructiveManifoldWatertightOperator(bpy.types.Operator) :
    
    bl_idname = 'ops.destructive_manifold_watertight'
    bl_label = "Destructive method"
    bl_description = "This method might damage your mesh in some ways but will make it completely ok for printing"
    
    def execute (self, context) :

	global step
         
        self.report("INFO", "The mesh is now correct")

	step = 2
        
        return {'FINISHED'}
    

#########################################
# GenerateSupportingPlansOperator class #
#########################################

              
class GenerateSupportingPlansOperator(bpy.types.Operator) :
    
    bl_idname = 'ops.generate_plans'
    bl_label = "Generate supporting plans"
    bl_description = "This function will calculate several possible plans on which your object can be printed" 
    
    def __init__ (self) :
        
        self.value = 0
        bpy.types.Operator.__init__(self)
        
    def execute (self, context) :

	global step
        
        self.report("INFO", "Several supporting plans have been calculated for your object")

	step = 3

        return {'FINISHED'}
    
###################################
# VizualizeNextPlanOperator class #
###################################
              
class VizualizeNextPlanOperator(bpy.types.Operator) :
    
    bl_idname = 'ops.vizualize_next_plan'
    bl_label = "Next >"
    bl_description = "Vizualize your object on the next supporting plan"
    
    def execute (self, context) :

	global step 

        self.report("INFO", "This is the next possible orientation for your object")

	step = 1

        return {'FINISHED'}
    
    
#######################################
# VizualizePreviousPlanOperator class #
#############################"#########
              
class VizualizePreviousPlanOperator(bpy.types.Operator) :
    
    bl_idname = 'ops.vizualize_previous_plan'
    bl_label = "< Previous"
    bl_description = "Vizualize your object on the previous supporting plan"
    
    def execute (self, context) :
        self.report("INFO", "This is the previous possible orientation for your object")
        return {'FINISHED'}
    
###################################
# ChooseCurrentPlanOperator class #
###################################
              
class ChooseCurrentPlanOperator(bpy.types.Operator) :
    
    bl_idname = 'ops.choose_current_plan'
    bl_label = "Choose the current plan"
    bl_description = "Your object will be registered as vizualized now"
    
    def execute (self, context) :
        self.report("INFO", "You chose the current orientation for your object")
        return {'FINISHED'}
    
#################
# Main function #
#################

if __name__ == "__main__":
    
    scn = types.Scene
    
    bpy.utils.register_class(MeshVerificationPanel)

    bpy.utils.register_class(NonDestructiveManifoldWatertightOperator)
    
    bpy.utils.register_class(DestructiveManifoldWatertightOperator)

    bpy.utils.register_class(GenerateSupportingPlansOperator)
    
    bpy.utils.register_class(VizualizeNextPlanOperator)
    
    bpy.utils.register_class(VizualizePreviousPlanOperator)
    
    bpy.utils.register_class(ChooseCurrentPlanOperator)
    
    scn.FastProcessing = props.BoolProperty(name = "Fast processing", default = False)
   

    
