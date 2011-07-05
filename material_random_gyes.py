# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


""" Copyright  Kilon 2011 GPL licence applies"""

bl_info = {
    "name": "Material_Gyes",
    "description": "Random Material Generator",
    "author": "Kilon",
    "version": (0,1),
    "blender": (2, 5, 7),
    "api": 36147,
    "location": "View3D > Left panel ",
    "warning": '', # used for warning icon and text in addons panel
    "wiki_url": "http://blenderartists.org/forum/showthread.php?218110-Gyes-%28Random-Material-Generator%29",
    "tracker_url": "http://projects.blender.org/tracker/index.php?func=detail&aid=27470&group_id=153&atid=467",
    "category": "Other"}
    
# first we import all the required modules
import bpy ,random , copy 
from bpy.props import *


class random_material_class:
    """ this class contains all fuctions and variables concerning generation of random material """
    
    def __init__(self):
        """ several fuctions can be found here . All options for random generation . The History dictionary and several others."""
        
        # have not used this one yet, its suppose to control randomisation percentage
              
        
        # various gui modes (simple, template etc)
        bpy.types.Scene.gui_mode = EnumProperty(attr='mode', name='Mode', items=(
('simple', 'Simple', 'The first item'),
('simple_percentage', 'Simple percentage' , 'here you define individual percentage'),
('templates', 'Templates', 'The second item'),
('help', 'Help', 'The third item')), default='simple')
       
        # Here I define the selective areas that the user can enable or disable for randomisation in simple mode               
                     
        bpy.types.Scene.rdiffuse_shader = BoolProperty(name= "Diffuse Shader" ,description = "Randomise Diffuse Shader" , default = True)
        
        bpy.types.Scene.rdiffuse_color = BoolProperty(name= "Diffuse Color" ,description = "Randomise Diffuse Color", default = True  )
        
        bpy.types.Scene.rdiffuse_intensity = BoolProperty(name= "Diffuse Intensity" ,description = "Randomise Diffuse Intensity" , default = True )    
        bpy.types.Scene.rspecular_color = BoolProperty(name= "Specular Color" ,description = "Randomise Specular Color" , default = True)
        
        bpy.types.Scene.rspecular_shader = BoolProperty(name= "Specular Shader" ,description = "Randomise Specular Shader" , default = True)
        
        bpy.types.Scene.rspecular_intensity = BoolProperty(name= "Specular Intensity" ,description = "Randomise Specular Intensity" , default = True)
        
        bpy.types.Scene.rspecular_hardness = BoolProperty(name= "Specular Hardness" ,description = "Randomise Specular Hardness" , default = True)
        
        bpy.types.Scene.rtransparency = BoolProperty(name= "Transparency" ,description = "Use and Randomise Transparency" , default = True)
        
        # Percentage randomisation
        bpy.types.Scene.general_percentage = IntProperty(name="General percentage", description = " General percentage of randomisation" , min = 0 , max = 100 , default = 100)
        
        bpy.types.Scene.rdiffuse_shader_percentage =  IntProperty(name="Diffuse shader", description = " Diffuse shader percentage of randomisation" , min = 0 , max = 100 , default = 0)
        
        
        bpy.types.Scene.rdiffuse_color_percentage =  IntProperty(name="Diffuse Color", description = " Diffuse Color percentage of randomisation" , min = 0 , max = 100 , default = 0)
        
        
        bpy.types.Scene.rdiffuse_intensity_percentage =  IntProperty(name="Diffuse Intensity", description = " Diffuse Intensity percentage of randomisation" , min = 0 , max = 100 , default = 0)
           
        bpy.types.Scene.rspecular_color_percentage =  IntProperty(name="Specular Color", description = " Specular Color percentage of randomisation" , min = 0 , max = 100 , default = 0)
        
        
        bpy.types.Scene.rspecular_shader_percentage =  IntProperty(name="Specular Shader", description = " Specular Shader percentage of randomisation" , min = 0 , max = 100 , default = 0)
        
        
        bpy.types.Scene.rspecular_intensity_percentage =  IntProperty(name="Specular Intensity", description = " Specular Intensity percentage of randomisation" , min = 0 , max = 100 , default = 0)
        
        
        bpy.types.Scene.rspecular_hardness_percentage =  IntProperty(name="Specular Hardness", description = " Specular Hardness percentage of randomisation" , min = 0 , max = 100 , default = 0)
        
        
        bpy.types.Scene.rtransparency_percentage =  IntProperty(name="Transparency", description = " Transparency percentage of randomisation" , min = 0 , max = 100 , default = 0)
        
        
        # this is the dictionary that stores history
        bpy.types.Scene.history_index = IntProperty(name= "History Index" ,description = "The Number of Random Material Assigned to the Active MAterial of the Selected Object from the history" , default = 1, min = 1 , )
        bpy.context.scene.history_index=1
        self.rm_history={}
        self.delete_start_index=1
    
    #deletes from history an index but without leaving empty spaces, everythings is pushed back    
    def delete_from_history(self):
        
        length = len(self.rm_history)
        index = bpy.context.scene.history_index
        for x in range(index , length):
            if index != length :
                self.rm_history[x]= self.rm_history[x+1] 
        del self.rm_history[length]
        length = len(self.rm_history) 
        if index <= length:
            self.activate()
    
    #store active material to history
    def store_to_history(self, mat):
        scn = bpy.context.scene
        history_index = scn.history_index
        self.rm_history[history_index]= {"diffuse_color" : tuple(mat.diffuse_color),
          "diffuse_shader" : mat.diffuse_shader , 
          "diffuse_intensity" : mat.diffuse_intensity ,
          "specular_color" : tuple(mat.specular_color) , 
          "specular_shader" : mat.specular_shader ,
          "specular_intensity" : mat.specular_intensity , 
          "specular_hardness" : mat.specular_hardness , 
          "use_transparency" : mat.use_transparency , 
          "transparency_method" : mat.transparency_method , 
          "alpha" : mat.alpha , 
          "specular_alpha" : mat.specular_alpha , 
          "ambient" : mat.ambient }    
        
    # the fuction that randomises the material 
    def random_material(self,active_material,name):
        
        mat = active_material
                
        scn = bpy.context.scene
                  
        scn.history_index =len(self.rm_history)+1
        
        #checks that the user has allowed the randomisation of that specific parameter            
        if scn.rdiffuse_color:
            mat.diffuse_color = (random.random(),random.random(),random.random())
            
    
        if scn.rdiffuse_shader:
            mat.diffuse_shader = random.choice(['LAMBERT','FRESNEL','TOON','MINNAERT'])
            
            
    
        if scn.rdiffuse_intensity:
            mat.diffuse_intensity = random.random()  
            
    
        if scn.rspecular_color:
            mat.specular_color = (random.random(),random.random(),random.random())
            
    
        if scn.rspecular_shader:
            mat.specular_shader = random.choice(['COOKTORR','WARDISO','TOON','BLINN','PHONG'])
            
    
        if scn.rspecular_intensity:
            mat.specular_intensity = random.random()
            
    
        if scn.rspecular_hardness:
            mat.specular_hardness = random.randrange(1,511,1)
            
    
        mat.use_transparency = scn.rtransparency 
        
    
        if mat.use_transparency == True :
            mat.transparency_method == random.choice(['MASK', 'Z_TRANSPARENCY', 'RAYTRACE'])
            
            if mat.transparency_method == 'MASK' :
                mat.alpha = random.random()
                
            if mat.transparency_method == 'Z_TRANSPARENCY' :
                mat.alpha = random.random()
                
                mat.specular_alpha= random.random()
                
               
      
        mat.ambient = random.random()
        
        # after you finishes randomisation store the random material to history
        self.store_to_history(mat)
          
        return mat
    
    # Activate. Make active material the particular history index the user has chosen
    def activate(self):
        
        for i in bpy.context.selected_objects :
            if i.type == 'MESH' :
            
                
                scn = bpy.context.scene
                mat = i.active_material
        
                mat.diffuse_color = self.rm_history[scn.history_index]["diffuse_color"]
                mat.diffuse_shader = self.rm_history[scn.history_index]["diffuse_shader"]
                mat.diffuse_intensity = self.rm_history[scn.history_index]["diffuse_intensity"]
                mat.specular_color = self.rm_history[scn.history_index]["specular_color"]
                mat.specular_shader = self.rm_history[scn.history_index]["specular_shader"]
                mat.specular_intensity = self.rm_history[scn.history_index]["specular_intensity"]
                mat.specular_hardness = self.rm_history[scn.history_index]["specular_hardness"]
                mat.use_transparency = self.rm_history[scn.history_index]["use_transparency"]
                mat.transparency_method = self.rm_history[scn.history_index]["transparency_method"]
                mat.alpha = self.rm_history[scn.history_index]["alpha"]
                mat.specular_alpha = self.rm_history[scn.history_index]["specular_alpha"]
                mat.ambient = self.rm_history[scn.history_index]["ambient"]
       
    
    
rm = random_material_class()
                  
# this the main panel
class gyes_panel(bpy.types.Panel):
    bl_label = "Gyes"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    @classmethod    
    def poll(self, context):
        if context.object and context.object.type == 'MESH':                    return len(context.object.data.materials)
        
    def draw(self, context):
        
        layout = self.layout
        row = layout.row()
        row.prop(context.scene , "gui_mode" )
        
        # check which Gui mode the user has selected (Simple is the default one and display the appropriate gui
        
        if bpy.context.scene.gui_mode == 'simple' :
            #bpy.context.scene.template_mode = False
            box = layout.box()
            box.prop(context.scene,"rdiffuse_shader", toggle = True)
            box.prop(context.scene,"rdiffuse_color", toggle = True)
            box.prop(context.scene,"rdiffuse_intensity", toggle = True)
            box.prop(context.scene,"rspecular_shader", toggle = True)
            box.prop(context.scene,"rspecular_color", toggle = True)
            box.prop(context.scene,"rspecular_intensity", toggle = True)
            box.prop(context.scene,"rspecular_hardness", toggle = True)
            box.prop(context.scene,"rtransparency", toggle = True)
            box.prop(context.scene,"general_percentage", slider = True)           
            layout.operator("gyes.random_material")
            
        if bpy.context.scene.gui_mode == 'simple_percentage' :
            #bpy.context.scene.template_mode = False
            box = layout.box()
            
            if bpy.context.scene.rdiffuse_shader :
                box.prop(context.scene,"rdiffuse_shader_percentage", slider = True)
            else:
                box.label(text="Diffuse Shader is disabled ")
                
            if bpy.context.scene.rdiffuse_color :
                box.prop(context.scene,"rdiffuse_color_percentage", slider = True)
            else:
                box.label(text="Diffuse Color is disabled ")
                
            if bpy.context.scene.rdiffuse_intensity :
                box.prop(context.scene,"rdiffuse_intensity_percentage", slider = True)
            else:
                box.label(text="Diffuse Intensity is disabled ")
                
            if bpy.context.scene.rspecular_shader :
                box.prop(context.scene,"rspecular_shader_percentage", slider = True)
            else:
                box.label(text="Specular Shader is disabled ")
                
            if bpy.context.scene.rspecular_color :
                box.prop(context.scene,"rspecular_color_percentage", slider = True)
            else:
                box.label(text="Specular Color is disabled ")
                
            if bpy.context.scene.rspecular_intensity :
                box.prop(context.scene,"rspecular_intensity_percentage", slider = True)
            else:
                box.label(text="Specular Intensity is disabled ")
                
            if bpy.context.scene.rspecular_hardness :
                box.prop(context.scene,"rspecular_hardness_percentage", slider = True)
            else:
                box.label(text="Specular Hardness is disabled ")
            
            if bpy.context.scene.rtransparency :
                box.prop(context.scene,"rtransparency_percentage", slider = True)
            else:
                box.label(text="Transparency is disabled ")
            
            layout.operator("gyes.random_material")
        
        if bpy.context.scene.gui_mode== 'templates' : 
            #bpy.context.scene.simple_mode = False
            print()
        
        if bpy.context.scene.gui_mode== 'help' :
            box = layout.box()
            box.label(text=" Copyright 2011 Kilon  ")
            box.label(text="Random Material  Generator Gyes ")
            box.label(text="A tool that generates random materials.")
            box.label(text="")
            box.label(text="Simple Mode")
            box.label(text="--------------------------")
            box.label(text="In this mode you can do basic randomisation.")
            box.label(text="Choose parameters you want to randomise by")
            box.label(text="turning them on or off with clicking on them")
            box.label(text="Hit the random button when you are ready")
            box.label(text="Each time you hit the button the new random")
            box.label(text="material is stored in a history index")
            box.label(text="")
            box.label(text="History")
            box.label(text="--------------------------")
            box.label(text="history index -> choose index")
            box.label(text="previous -> previous index (activate)")
            box.label(text="next -> next index (activate)")
            box.label(text="activate -> use this index as active material")
            box.label(text="delete -> delete this index")
            box.label(text="del start -> start deletion from here")
            box.label(text="del end -> end deletion here")
         
                  
                
        # Display the History Gui for all modes
        
        layout.label(text="History")
        history_box= layout.box()
        history_box.prop(context.scene, "history_index")
        row = history_box.row()
        row.operator("gyes.previous")
        row.operator("gyes.next")
        rm_index = bpy.context.scene.history_index
        
        if rm_index in rm.rm_history and rm.rm_history[rm_index] :
            history_box.operator("gyes.activate")
        else:
            history_box.label(text= "Empty Index ! ")
        
        if bpy.context.scene.history_index < len(rm.rm_history)+2:
            history_box.operator("gyes.store")
        else:
            history_box.label(text= "Not the first Empty Index")
        if rm_index in rm.rm_history and rm.rm_history[rm_index] :
            history_box.operator("gyes.delete")
            row2 = history_box.row()
            row2.operator("gyes.delete_start")
            row2.operator("gyes.delete_end")    
        
#this is the random material button
class gyes_random_material(bpy.types.Operator):
    bl_idname = "gyes.random_material"
    bl_label = "Random Material"
    label = bpy.props.StringProperty()
    
    def execute(self, context):
        for i in bpy.context.selected_objects :
            if i.type == 'MESH' :
            
                rm.random_material(i.active_material,'Random')
        return{'FINISHED'}
    
# Move to the previous hisory index and activate it
class history_previous(bpy.types.Operator):
    
    bl_label = "Previous"
    bl_idname = "gyes.previous"
    
    def execute(self, context):
        if bpy.context.scene.history_index > 1 :
            bpy.context.scene.history_index = bpy.context.scene.history_index -1
            rm_index = bpy.context.scene.history_index
            if rm_index in rm.rm_history and rm.rm_history[rm_index]:
                rm.activate()
        
        return{'FINISHED'}

# Move to the next hisory index and activate it
class history_next(bpy.types.Operator):
    
    bl_label = "Next"
    bl_idname = "gyes.next"
    
    def execute(self, context):
        if bpy.context.scene.history_index > 0 :
            bpy.context.scene.history_index = bpy.context.scene.history_index +1
            rm_index = bpy.context.scene.history_index
            if rm_index in rm.rm_history and rm.rm_history[rm_index]:
                rm.activate()
        
        return{'FINISHED'}

# 
class history_activate(bpy.types.Operator):
    
    bl_label = "Activate"
    bl_idname = "gyes.activate"
    
    def execute(self, context):
        rm_index = bpy.context.scene.history_index
        if rm.rm_history[rm_index] != {}:
            rm.activate()
        
        return{'FINISHED'}

# It stores current active material to the selected history index
class store_to_history(bpy.types.Operator):
    
    bl_label = "Store"
    bl_idname = "gyes.store"
    
    def execute(self, context):
        mat = bpy.context.selected_objects[0].active_material
        rm.store_to_history(mat)
         
        
        return{'FINISHED'}

# delete from history
class delete_from_history(bpy.types.Operator):
    
    bl_label = "Delete"
    bl_idname = "gyes.delete"
    
    def execute(self, context):
        rm.delete_from_history()
        
        return{'FINISHED'}
               
# start deletion from here
class delete_from_history_start(bpy.types.Operator):
    
    bl_label = "Del Start"
    bl_idname = "gyes.delete_start"
    
    def execute(self, context):
        rm_index = bpy.context.scene.history_index
        rm.delete_start_index = rm_index
        
        return{'FINISHED'}   

#end deletion here
class delete_from_history_end(bpy.types.Operator):
    
    bl_label = "Del End"
    bl_idname = "gyes.delete_end"
    
    def execute(self, context):
        delete_end_index = bpy.context.scene.history_index
        bpy.context.scene.history_index = rm.delete_start_index
        for x in range ( rm.delete_start_index , delete_end_index):
            rm.delete_from_history()
        
        return{'FINISHED'}   
         
#registration is necessary for the script to appear in the GUI
def register():
    bpy.utils.register_module(__name__)
    pass

def unregister():
    bpy.utils.register_module(__name__)
    pass

if __name__ == '__main__':
    register()