import bpy ,random
 
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
 
def setMaterial(ob, mat):
    me = ob.data
    me.materials.append(mat)
 
def run(origin):
    # Create two materials
    rm1 = random_material('Randome1')
    rm2 = random_material('Random2')
 
    # Create red cube
    bpy.ops.mesh.primitive_cube_add(location=origin)
    setMaterial(bpy.context.object, rm1)
    # and blue sphere
    bpy.ops.mesh.primitive_uv_sphere_add(location=origin)
    bpy.ops.transform.translate(value=(1,0,0))
    setMaterial(bpy.context.object, rm2)
 
if __name__ == "__main__":
    run((0,0,0))