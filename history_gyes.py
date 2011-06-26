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

    
# first we import all the required modules
from bpy.props import *


class history:
    """ this class contains all fuctions and variables concerning history"""
    
    def __init__(self):
        """The History dictionary and several others."""
     
       
        bpy.types.Scene.history_index = IntProperty(name= "History Index" ,description = "The Number of Random Material Assigned to the Active MAterial of the Selected Object from the history" , default = 1, min = 1 , )
        bpy.context.scene.history_index=1
        self.history={}
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
    def store_to_history(self):
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
        #cheks that the user has allowed the randomisation of that specific parameter            
        if scn.rdiffuse_color:
            mat.diffuse_color = (random.random(),random.random(),random.random())
            
    
        if scn.rdiffuse_shader:
            mat.diffuse_shader = random.choice(['LAMBERT','FRESNEL','TOON','MINNAERT'])
            
            
    
        if scn.rdiffuse_intensity:
            mat.diffuse_intensity = random.random()  # *(0.01*scn["rp"])
            
    
        if scn.rspecular_color:
            mat.specular_color = (random.random(),random.random(),random.random())
            
    
        if scn.rspecular_shader:
            mat.specular_shader = random.choice(['COOKTORR','WARDISO','TOON','BLINN','PHONG'])
            
    
        if scn.rspecular_intensity:
            mat.specular_intensity = random.random()
            
    
        if scn.rspecular_hardness:
            mat.specular_hardness = random.randrange(1,511,1)
            
    
        mat.use_transparency = scn.rtransparency # random.randrange(0,2)
        
    
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
        layout.label(text="Options")
        box = layout.box()
        box.prop(context.scene,"rdiffuse_shader")
        box.prop(context.scene,"rdiffuse_color")
        box.prop(context.scene,"rdiffuse_intensity")
        box.prop(context.scene,"rspecular_shader")
        box.prop(context.scene,"rspecular_color")
        box.prop(context.scene,"rspecular_intensity")
        box.prop(context.scene,"rspecular_hardness")
        box.prop(context.scene,"rtransparency")
        
        layout.operator("gyes.random_material")
        
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

class delete_from_history(bpy.types.Operator):
    
    bl_label = "Delete"
    bl_idname = "gyes.delete"
    
    def execute(self, context):
        rm.delete_from_history()
        
        return{'FINISHED'}           

class delete_from_history_start(bpy.types.Operator):
    
    bl_label = "Del Start"
    bl_idname = "gyes.delete_start"
    
    def execute(self, context):
        rm_index = bpy.context.scene.history_index
        rm.delete_start_index = rm_index
        
        return{'FINISHED'}   

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