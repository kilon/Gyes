import bpy ,random

#function for randomising the material properties 
def random_material(name):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (random.random(),random.random(),random.random())
    mat.diffuse_shader = random.choice(['LAMBERT','FRESNEL','TOON','MINNAERT']) 
    mat.diffuse_intensity = random.random()
    mat.specular_color = (random.random(),random.random(),random.random())
    mat.specular_shader = 'COOKTORR'
    mat.specular_intensity = random.random()
    mat.alpha = random.random()
    mat.ambient = random.random()
    return mat

#fuction for assinging the random material to an object 
def setMaterial(ob, mat):
    me = ob.data
    me.materials.append(mat)
    

#this is the script's main loop 
def main_loop(origin):
    
    # Create the two random materials
    rm = random_material('Random1')
    setMaterial(bpy.context.object, rm)
    
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
bpy.utils.register_module(__name__)
