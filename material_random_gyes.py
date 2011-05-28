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

#function for randomising the material properties 
def random_material(ob,name):
    #mat = bpy.data.materials.new(name)
    mat = ob
    mat.diffuse_color = (random.random(),random.random(),random.random())
    mat.diffuse_shader = random.choice(['LAMBERT','FRESNEL','TOON','MINNAERT']) 
    mat.diffuse_intensity = random.random()
    mat.specular_color = (random.random(),random.random(),random.random())
    mat.specular_shader = random.choice(['COOKTORR','WARDISO','TOON','BLINN','PHONG'])
    mat.specular_intensity = random.random()
    mat.specular_hardness = random.randrange(1,511,1)
    mat.use_transparency = random.randrange(0,2)
    
    if mat.use_transparency == 1 :
        mat.transparency_method == random.choice(['MASK', 'Z_TRANSPARENCY', 'RAYTRACE'])
        if mat.transparency_method == 'MASK' :
            mat.alpha = random.random()
        if mat.transparency_method == 'Z_TRANSPARENCY' :
            mat.alpha = random.random()
            mat.specular_alpha= random.random()
      
    mat.ambient = random.random()
    return mat

#fuction for assinging the random material to an object 
def setMaterial(ob, mat):
    me = ob.data
    me.materials.append(mat)
    
#this is the script's main loop 
def main_loop(origin):
    
    # Create the two random materials
    for i in bpy.context.selected_objects :
        if i.type == 'MESH' :
            
            #setMaterial(i, i.active_material)
            
            rm = random_material(i.active_material,'Random')
            
           
# this the main panel
class gyes_panel(bpy.types.Panel):
    bl_label = "Gyes"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    @classmethod    
    def poll(self, context):
        if context.object and context.object.type == 'MESH':                    return len(context.object.data.materials)
        
    def draw(self, context):
        self.layout.operator("gyes.random_material")

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