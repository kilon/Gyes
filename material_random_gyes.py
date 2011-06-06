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
    

import bpy ,random , copy 
from bpy.props import *


class random_material_class:
    
    def __init__(self):
     
        bpy.types.Scene.rp = IntProperty(name="percentage", description = "percentage of randomisation" , min = 0 , max = 100 , default = 50)
        bpy.types.Scene.rdiffuse_shader = BoolProperty(name= "Diffuse Shader" ,description = "Randomise Diffuse Shader" , default = True)
        bpy.types.Scene.rdiffuse_color = BoolProperty(name= "Diffuse Color" ,description = "Randomise Diffuse Color", default = True  )
        bpy.types.Scene.rdiffuse_intensity = BoolProperty(name= "Diffuse Intensity" ,description = "Randomise Diffuse Intensity" , default = True )    
        bpy.types.Scene.rspecular_color = BoolProperty(name= "Specular Color" ,description = "Randomise Specular Color" , default = True)
        bpy.types.Scene.rspecular_shader = BoolProperty(name= "Specular Shader" ,description = "Randomise Specular Shader" , default = True)
        bpy.types.Scene.rspecular_intensity = BoolProperty(name= "Specular Intensity" ,description = "Randomise Specular Intensity" , default = True)
        bpy.types.Scene.rspecular_hardness = BoolProperty(name= "Specular Hardness" ,description = "Randomise Specular Hardness" , default = True)
        bpy.types.Scene.rtransparency = BoolProperty(name= "Transparency" ,description = "Use and Randomise Transparency" , default = True)
        bpy.types.Scene.history_index = IntProperty(name= "History Index" ,description = "The Number of Random Material Assigned to the Active MAterial of the Selected Object from the history" , default = 0)
        self.rm_history={}
    
    def store_to_history(self, mat):
        scn = bpy.context.scene
        self.rm_history[scn.history_index]= {"diffuse_color" : tuple(mat.diffuse_color),
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
        #mat = bpy.data.materials.new(name)
        mat = active_material
        self.store_to_history(mat)
        scn = bpy.context.scene
        
        bpy.types.Scene.history_index = IntProperty(name= "History Index" ,description = "The Number of Random Material Assigned to the Active MAterial of the Selected Object from the history" , default = 0, min = 0,max = len(self.rm_history))
        
        #self.rm_history.append(mat)
        
              
        scn.history_index = len(self.rm_history)+1
    
        if scn.rdiffuse_color:#scn["rdiffuse_color"]==True:
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
        
        self.store_to_history(mat)
          
        return mat
    
    
    def set_material(self):
        
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
    
#this is the script's main loop 
def main_loop(origin):
    
    # Create the two random materials
    for i in bpy.context.selected_objects :
        if i.type == 'MESH' :
            
            rm.random_material(i.active_material,'Random')
                   
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
        history_box.operator("gyes.activate")

#this is the random material button
class gyes_random_material(bpy.types.Operator):
    bl_idname = "gyes.random_material"
    bl_label = "Random Material"
    label = bpy.props.StringProperty()
    
    def execute(self, context):
        main_loop((0,0,0))
        return{'FINISHED'}
    
class history_item(bpy.types.Operator):
    
    bl_label = "Activate"
    bl_idname = "gyes.activate"
    
    def execute(self, context):
        rm.set_material()
        
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