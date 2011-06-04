""" Copyright notice """

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
    

import bpy ,random
from bpy.props import *


    


#function for randomising the material properties
class random_material:
    
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
    
     
    def random_material(self,ob,name):
        #mat = bpy.data.materials.new(name)
        mat = ob
        scn = bpy.context.scene
    
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
        return mat

rm = random_material()
    
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
        
        #box.prop(context.scene,"rp")
        layout.operator("gyes.random_material")

#this is the random material button
class gyes_random_material(bpy.types.Operator):
    bl_idname = "gyes.random_material"
    bl_label = "Random Material"
    label = bpy.props.StringProperty()
    
    def execute(self, context):
        main_loop((0,0,0))
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