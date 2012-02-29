###################################################################
# script for the addition of a mesh verification panel in Blender #
# author : Caroline Naud                                          #
###################################################################

from bpy import *
import bpy
import sys
from os.path import dirname, join
sys.path.insert(0, join(dirname(__file__), '../modules'))
import manifold
import planar_faces
   
step = 0 # step in the pre-processing of the mesh (3)
sp = [] # adequate supporting plans
plan = -1 # current supporting plan

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

        """
        Draws the additional panel containing the buttons to pre-process each mesh before printing in Blender's interface.
        """
        
        obj = context.active_object
        mesh = obj.data
        scn = context.scene
    
        layout = self.layout

	# Top of the panel
        row = layout.row()
        row.label(text="Verify your mesh before printing it", icon='MESH_ICOSPHERE')
   
        row = layout.row()
        row.label(text="The active mesh is : " + mesh.name)
        
        row = layout.row()
        row.operator("ops.check_mesh")
       	
	# First box of the panel (step 1) : correction of the mesh 
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
        
	# Second box of the panel (step 2) : generation of the supporting plans
        box2 = layout.box()

        if step != 2 :
            box2.enabled = False

        row1 = box2.row()
        row1.label(text="-> Step 2 : Generate adequate supporting plans for printing")
        
        row2 = box2.row()
        row2.operator("ops.generate_plans")
        
	# Third box of the panel (step 3) : Choice of the supporting plan
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
        
###################################################
#  NonDestructiveManifoldWatertightOperator class #
###################################################
              
class CheckMeshOperator(bpy.types.Operator) :
    
    bl_idname = 'ops.check_mesh'
    bl_label = "Check your mesh"
    bl_description = "This operator will check if your mesh is correct or not"
    
    def execute (self, context) :

        """
        Check if the mesh is correct.
        """

        global step
        
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.context.tool_settings.mesh_select_mode = [False, True, False]
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_non_manifold()
        bpy.ops.object.mode_set(mode='OBJECT')
        not_manifold = False
        for e in context.active_object.data.edges:
            if e.select:
                not_manifold = True
        bpy.ops.object.mode_set(mode='EDIT')
        if not_manifold :
            self.report({"INFO"}, "The mesh is not correct")
            step = 1
        else :
            step = 2
            self.report({"INFO"}, "The mesh is correct")
        return {'FINISHED'}
                
###################################################
#  NonDestructiveManifoldWatertightOperator class #
###################################################
              
class NonDestructiveManifoldWatertightOperator(bpy.types.Operator) :
    
    bl_idname = 'ops.non_destructive_manifold_watertight'
    bl_label = "Non destructive method"
    bl_description = "This method won't damage your mesh in any way but might leave some imperfections"
    
    def execute (self, context) :

        """
        Make the mesh watertight and often manifold but does not destroy it.
        """

        global step

        step = manifold.correction(False, context.scene.FastProcessing)
        self.report({"INFO"}, "The mesh is now correct")
        #step = 2 # Disable the first box and enable the second one
        return {'FINISHED'}
    
###############################################
# DestructiveManifoldWatertightOperator class #
###############################################
              
class DestructiveManifoldWatertightOperator(bpy.types.Operator) :
    
    bl_idname = 'ops.destructive_manifold_watertight'
    bl_label = "Destructive method"
    bl_description = "This method might damage your mesh in some ways but will make it completely ok for printing"
    
    def execute (self, context) :

        """
        Make the mesh watertight and manifold but might detroy some edges.
        """

        global step
        
        step = manifold.correction(True, context.scene.FastProcessing) 
        self.report({"INFO"}, "The mesh is now correct")
        step = 2 # Disable the first box and enable the second one    
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

        """
        Generate a list of supporting plans for the object on which it can be printed.
        """

        global step
        global sp
        
        obj = bpy.context.active_object
        sp = planar_faces.SupportPlanes(obj)
        self.report({"INFO"}, "Several supporting plans have been calculated for your object")
        step = 3 # Disable the second box and enable the third one
        return {'FINISHED'}
    
###################################
# VizualizeNextPlanOperator class #
###################################
              
class VizualizeNextPlanOperator(bpy.types.Operator) :
    
    bl_idname = 'ops.vizualize_next_plan'
    bl_label = "Next >"
    bl_description = "Vizualize your object on the next supporting plan"
    
    def execute (self, context) :

        """
        Allows to vizualize the object on the next supporting plan on the list.
        """
        
        global plan
        
        l = len(sp)
        if plan == l - 1 :
            plan = 0
        else :
            plan = plan + 1
        sp[plan].select()
        self.report({"INFO"}, "This is the next possible orientation for your object")
        return {'FINISHED'}
    
    
#######################################
# VizualizePreviousPlanOperator class #
#############################"#########
              
class VizualizePreviousPlanOperator(bpy.types.Operator) :
    
    bl_idname = 'ops.vizualize_previous_plan'
    bl_label = "< Previous"
    bl_description = "Vizualize your object on the previous supporting plan"
    
    def execute (self, context) :

        """
        Allows to vizualize the object on the previous supporting plan on the list.
        """
        global plan
        
        l = len(sp)
        if plan == 0 or plan == -1:
            plan = l - 1
        else :
            plan = plan - 1
        sp[plan].select()
        self.report({"INFO"}, "This is the previous possible orientation for your object")
        return {'FINISHED'}
    
###################################
# ChooseCurrentPlanOperator class #
###################################
              
class ChooseCurrentPlanOperator(bpy.types.Operator) :
    
    bl_idname = 'ops.choose_current_plan'
    bl_label = "Choose the current plan"
    bl_description = "Your object will be registered as vizualized now"
    
    def execute (self, context) :

        """
        Select the current supporting plan for printing.
        """
        
        global step
        global plan
        
        sp[plan].apply()
        self.report({"INFO"}, "You chose the current orientation for your object")      
        step = 0 # Disable the third box and enable the first button
        return {'FINISHED'}
    
#################
# Main function #
#################

def register():
    
    scn = types.Scene
    
    bpy.utils.register_class(MeshVerificationPanel)
    
    bpy.utils.register_class(CheckMeshOperator)

    bpy.utils.register_class(NonDestructiveManifoldWatertightOperator)
    
    bpy.utils.register_class(DestructiveManifoldWatertightOperator)

    bpy.utils.register_class(GenerateSupportingPlansOperator)
    
    bpy.utils.register_class(VizualizeNextPlanOperator)
    
    bpy.utils.register_class(VizualizePreviousPlanOperator)
    
    bpy.utils.register_class(ChooseCurrentPlanOperator)
    
    scn.FastProcessing = props.BoolProperty(name = "Fast processing", description = "Might not be as efficient as the normal processing", default = False)
