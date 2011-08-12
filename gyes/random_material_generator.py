# -*- coding: UTF-8 -*-
# first we import all the required modules
from code import InteractiveConsole
import bpy ,random , copy 
from bpy.props import *

class random_material_class:
    """ this class contains all fuctions and variables concerning generation of random material """
    
    def __init__(self):
        """ several fuctions can be found here . All options for random generation . The History dictionary and several others."""
                   
        # various gui modes (simple, template etc)
        bpy.types.Scene.gui_mode = EnumProperty(attr='mode', name='Mode', items=(
('simple', 'Simple', 'The first item'),
('simple_percentage', 'Simple percentage' , 'here you define individual percentage'),
('templates', 'Templates', 'The second item'),
('help', 'Help', 'The third item')), default='simple')
        self.weirdprop = EnumProperty(attr='mode', name='Mode', items=(
('simple', 'Simple', 'The first item'),
('simple_percentage', 'Simple percentage' , 'here you define individual percentage'),
('templates', 'Templates', 'The second item'),
('help', 'Help', 'The third item')), default='simple')
       
        # Here I define the selective areas that the user can enable or disable for randomisation in simple mode               
                     
        bpy.types.Scene.rdiffuse_shader = BoolProperty(name= "Diffuse Shader" ,description = "Enable/Disable Randomisation for the  Diffuse Shader " , default = True)
        bpy.types.Scene.rdiffuse_color = BoolProperty(name= "Diffuse Color" ,description = "Enable/Disable Randomisation for the Diffuse Color", default = True  )
        bpy.types.Scene.rdiffuse_intensity = BoolProperty(name= "Diffuse Intensity" ,description = "Enable/Disable Randomisation for the Diffuse Intensity" , default = True )    
        bpy.types.Scene.rspecular_color = BoolProperty(name= "Specular Color" ,description = "Enable/Disable Randomisation for the Specular Color" , default = True)
        bpy.types.Scene.rspecular_shader = BoolProperty(name= "Specular Shader" ,description = "Enable/Disable Randomisation for the Specular Shader" , default = True)
        bpy.types.Scene.rspecular_intensity = BoolProperty(name= "Specular Intensity" ,description = "Enable/Disable Randomisation for the Specular Intensity" , default = True)
        bpy.types.Scene.rspecular_hardness = BoolProperty(name= "Specular Hardness" ,description = "Enable/Disable Randomisation for the Specular Hardness" , default = True)
        bpy.types.Scene.rtransparency = BoolProperty(name= "Transparency" ,description = "Use and Randomise Transparency" , default = True)
        
        # Percentage randomisation
        bpy.types.Scene.general_percentage = IntProperty(name="General percentage", description = " General percentage of randomisation" , min = 0 , max = 100 , default = 100, subtype = 'PERCENTAGE')
        bpy.types.Scene.rdiffuse_shader_percentage =  IntProperty(name="Diffuse shader", description = " Diffuse shader percentage of randomisation" , min = 0 , max = 100 , default = 0, subtype = 'PERCENTAGE')
        bpy.types.Scene.rdiffuse_color_percentage =  IntProperty(name="Diffuse Color", description = " Diffuse Color percentage of randomisation" , min = 0 , max = 100 , default = 0, subtype = 'PERCENTAGE')
        bpy.types.Scene.rdiffuse_intensity_percentage =  IntProperty(name="Diffuse Intensity", description = " Diffuse Intensity percentage of randomisation" , min = 0 , max = 100 , default = 0, subtype = 'PERCENTAGE')
        bpy.types.Scene.rspecular_color_percentage =  IntProperty(name="Specular Color", description = " Specular Color percentage of randomisation" , min = 0 , max = 100 , default = 0 , subtype = 'PERCENTAGE')
        bpy.types.Scene.rspecular_shader_percentage =  IntProperty(name="Specular Shader", description = " Specular Shader percentage of randomisation" , min = 0 , max = 100 , default = 0, subtype = 'PERCENTAGE')
        bpy.types.Scene.rspecular_intensity_percentage =  IntProperty(name="Specular Intensity", description = " Specular Intensity percentage of randomisation" , min = 0 , max = 100 , default = 0, subtype = 'PERCENTAGE')
        bpy.types.Scene.rspecular_hardness_percentage =  IntProperty(name="Specular Hardness", description = " Specular Hardness percentage of randomisation" , min = 0 , max = 100 , default = 0, subtype = 'PERCENTAGE')
        bpy.types.Scene.rtransparency_percentage =  IntProperty(name="Transparency", description = " Transparency percentage of randomisation" , min = 0 , max = 100 , default = 0, subtype = 'PERCENTAGE')
        
        # this is the dictionary that stores history
        bpy.types.Scene.history_index = IntProperty(name= "History Index" ,description = "The Number of Random Material Assigned to the Active MAterial of the Selected Object from the history" , default = 1, min = 1 )
        self.rm_history={}
        self.delete_start_index=1
        
        # here is where history dictionary is saved with the blend file
        # if the backup is already saved with the blend file it is used 
        # to restory the history dictionary , if not it is created
        
        if hasattr(bpy.context.scene , "historybak")==False:
            bpy.types.Scene.historybak = StringProperty()
            print("created history backup")
        
    # compute randomisation based on the general or specific percentage chosen
    # if the specific percentage is zero then the general percentage is used
    def compute_percentage(self,min,max,value,percentage):
        range = max-min
        general_percentage = bpy.context.scene.general_percentage
        
        if percentage == 0:
            percentage_random = ( value -((range*(general_percentage/100))/2) )+ (range * (general_percentage / 100) * random.random())
        else:
            percentage_random = ( value - ((range*(percentage/100))/2)) + (range * (percentage / 100) * random.random())
             
        if percentage_random > max:
            percentage_random = max
        if percentage_random < min:
            percentage_random = min
        
        return percentage_random 
    
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
            
        bpy.context.scene.historybak = str(self.rm_history)
    
    # the fuction that randomises the material 
    def random_material(self,active_material,name):
        mat = active_material
        scn = bpy.context.scene
        scn.history_index =len(self.rm_history)+1
        
        #checks that the user has allowed the randomisation of that specific parameter            
        if scn.rdiffuse_color:
            rand_perc = scn.rdiffuse_color_percentage
            mat.diffuse_color = (self.compute_percentage(0,1,mat.diffuse_color[0],rand_perc),
            self.compute_percentage(0,1,mat.diffuse_color[1],rand_perc),
            self.compute_percentage(0,1,mat.diffuse_color[2],rand_perc))
            
 
        if scn.rdiffuse_shader:
            mat.diffuse_shader = random.choice(['LAMBERT','FRESNEL','TOON','MINNAERT'])
    
        if scn.rdiffuse_intensity:
            mat.diffuse_intensity = self.compute_percentage(0,1, mat.diffuse_intensity , scn.rdiffuse_intensity_percentage) 
    
        if scn.rspecular_color:
            rand_perc = scn.rspecular_color_percentage
            mat.specular_color = (self.compute_percentage(0,1,mat.specular_color[0],rand_perc),
            self.compute_percentage(0,1,mat.specular_color[1],rand_perc),
            self.compute_percentage(0,1,mat.specular_color[2],rand_perc))
    
        if scn.rspecular_shader:
            mat.specular_shader = random.choice(['COOKTORR','WARDISO','TOON','BLINN','PHONG'])
    
        if scn.rspecular_intensity:
            mat.specular_intensity =  self.compute_percentage(0,1, mat.specular_intensity , scn.rspecular_intensity_percentage)
    
        if scn.rspecular_hardness:
            mat.specular_hardness =  round(self.compute_percentage(1,511, mat.specular_hardness, scn.rspecular_shader_percentage))
            
        mat.use_transparency = scn.rtransparency 
        
        if mat.use_transparency == True :
            mat.transparency_method == random.choice(['MASK', 'Z_TRANSPARENCY', 'RAYTRACE'])
            mat.alpha = self.compute_percentage(0,1, mat.alpha, scn.rtransparency_percentage)
  
            if mat.transparency_method == 'MASK' :
                bing =0     # dummy code
                
            if mat.transparency_method == 'Z_TRANSPARENCY' :
                bing =0     # dummy code
                mat.specular_alpha= random.random()
     
        mat.ambient = self.compute_percentage(0,1, mat.ambient, scn.general_percentage)
        
        # after you finishes randomisation store the random material to history
        self.store_to_history(mat)
          
        return mat
    
    #store active material to history
    def store_to_history(self, mat):
        scn = bpy.context.scene
        history_index = scn.history_index
        self.rm_history[history_index]= {"diffuse_color" : tuple(mat.diffuse_color),
          "alpha" : mat.alpha ,
          "ambient" : mat.ambient ,
          "darkness": mat.darkness,
          "diffuse_color": tuple(mat.diffuse_color),
          "diffuse_fresnel" : mat.diffuse_fresnel,
          "diffuse_fresnel_factor" : mat.diffuse_fresnel_factor, 
          "diffuse_intensity" : mat.diffuse_intensity ,
          "diffuse_ramp_blend" : mat.diffuse_ramp_blend,
          "diffuse_ramp_factor": mat.diffuse_ramp_factor,
          "diffuse_ramp_input" : mat.diffuse_ramp_input,
          "diffuse_shader" : mat.diffuse_shader , 
          "diffuse_toon_size" : mat.diffuse_toon_size,
          "diffuse_toon_smooth" : mat.diffuse_toon_smooth,
          "emit" : mat.emit,
          "invert_z" : mat.invert_z,
          "mirror_color" : tuple(mat.mirror_color),
          "offset_z" : mat.offset_z ,
          "preview_render_type" : mat.preview_render_type,
          "roughness" : mat.roughness,
          "shadow_buffer_bias" : mat.shadow_buffer_bias,
          "shadow_cast_alpha" : mat.shadow_cast_alpha , 
          "shadow_only_type" : mat.shadow_only_type ,
          "shadow_ray_bias" : mat.shadow_ray_bias ,
          "specular_alpha" : mat.specular_alpha ,
          "specular_color" : tuple(mat.specular_color) , 
          "specular_hardness" : mat.specular_hardness , 
          "specular_intensity" : mat.specular_intensity , 
          "specular_ior" : mat.specular_ior,
          "specular_ramp_blend" : mat.specular_ramp_blend, 
          "specular_ramp_factor" : mat.specular_ramp_factor,
          "specular_ramp_input" :  mat.specular_ramp_input,
          "specular_shader" : mat.specular_shader ,
          "specular_slope" : mat.specular_slope,
          "specular_toon_size" : mat.specular_toon_size , 
          "specular_toon_smooth" : mat.specular_toon_smooth,
          "translucency" : mat.translucency , 
          "transparency_method" : mat.transparency_method,
          "type" : mat.type, 
          "use_cast_approximate" : mat.use_cast_approximate,
          "use_cast_buffer_shadows" : mat.use_cast_buffer_shadows,
          "use_cast_shadows_only" : mat.use_cast_shadows_only,
          "use_cubic" : mat.use_cubic,
          "use_diffuse_ramp" : mat.use_diffuse_ramp,
          "use_face_texture" : mat.use_face_texture,
          "use_face_texture_alpha" : mat.use_face_texture_alpha,
          "use_full_oversampling" : mat.use_full_oversampling,
          "use_light_group_exclusive" : mat.use_light_group_exclusive,
          "use_mist" : mat.use_mist,
          "use_nodes" : mat.use_nodes,
          "use_object_color" : mat.use_object_color,
          "use_only_shadow" : mat.use_only_shadow,
          "use_ray_shadow_bias" : mat.use_ray_shadow_bias,
          "use_raytrace" : mat.use_raytrace,
          "use_shadeless" :mat.use_shadeless,
          "use_shadows" : mat.use_shadows,
          "use_sky" : mat.use_sky,
          "use_specular_ramp" : mat.use_specular_ramp,
          "use_tangent_shading" : mat.use_tangent_shading,
          "use_textures" : mat.use_textures,
          "use_transparency" : mat.use_transparency , 
          "use_transparent_shadows" : mat.use_transparent_shadows,
          "use_vertex_color_paint" : mat.use_transparent_shadows} 
          
        # diffuse ramp
        if self.rm_history[history_index]["use_diffuse_ramp"]:
            self.rm_history[history_index]["diffuse_ramp"]={}
            for el in range(0,len(mat.diffuse_ramp.elements)):
                self.rm_history[history_index]["diffuse_ramp"].update({el:{"color":{0: mat.diffuse_ramp.elements[el].color[0] ,
                1: mat.diffuse_ramp.elements[el].color[1],
                2: mat.diffuse_ramp.elements[el].color[2],
                3: mat.diffuse_ramp.elements[el].color[3]},"position": mat.diffuse_ramp.elements[el].position}})
           
        # node_tree
        
        nt = mat.node_tree
        self.rm_history[history_index].update({"node_tree":{}})
            
        #store each node of the node tree to history 
        if self.rm_history[history_index]["use_nodes"]:
            
            self.rm_history[history_index]["node_tree"].update({"nodes":{}})
            for x in range(0,len(nt.nodes)):
                self.rm_history[history_index]["node_tree"]["nodes"].update({x:{"name": nt.nodes[x].name , 
                "pos_x": nt.nodes[x].location[0] ,
                "pos_y": nt.nodes[x].location[1] ,
                "type" : nt.nodes[x].type }})
                
                
            #store each node link to history
            self.rm_history[history_index]["node_tree"].update({"links":{}})
            for x in range(0,len(nt.links)):     
                self.rm_history[history_index]["node_tree"]["links"].update({x:{"from_node": nt.links[x].from_node.name , 
                "to_node": nt.links[x].to_node.name ,
                "from_socket": nt.links[x].from_socket.name ,
                "to_socket" : nt.links[x].to_socket.name }}) 
           
        print("node_tree : ",self.rm_history[history_index]["node_tree"])            
        bpy.context.scene.historybak = str(self.rm_history)
        
    # Activate. Make active material the particular history index the user has chosen
    def activate(self, random_assign = False):
        
        for i in bpy.context.selected_objects :
            if random_assign == False and i.type == 'MESH' and ( bpy.context.scene.history_index in rm.rm_history ) and rm.rm_history[bpy.context.scene.history_index]:                
                scn = bpy.context.scene
                mat = i.active_material
                index = scn.history_index
                
            if random_assign == True and i.type == 'MESH' :
            
                index = round(len(self.rm_history) * random.random())
                
                if index == 0 :
                    index = 1
                    
                scn = bpy.context.scene
                mat = i.active_material
                scn.history_index=index    
                         
            mat.alpha = self.rm_history[index]["alpha"]
            mat.ambient = self.rm_history[index]["ambient"]
            mat.darkness = self.rm_history[index]["darkness"]
            mat.diffuse_color = self.rm_history[index]["diffuse_color"]
            mat.diffuse_fresnel = self.rm_history[index]["diffuse_fresnel"]
            mat.diffuse_fresnel_factor = self.rm_history[index]["diffuse_fresnel_factor"]
            mat.diffuse_intensity = self.rm_history[index]["diffuse_intensity"]
            mat.diffuse_ramp_blend = self.rm_history[index]["diffuse_ramp_blend"]
            mat.diffuse_ramp_factor = self.rm_history[index]["diffuse_ramp_factor"]
            mat.diffuse_ramp_input = self.rm_history[index]["diffuse_ramp_input"]
            mat.diffuse_shader = self.rm_history[index]["diffuse_shader"]
            mat.diffuse_toon_size = self.rm_history[index]["diffuse_toon_size"]
            mat.diffuse_toon_smooth = self.rm_history[index]["diffuse_toon_smooth"]
            mat.emit = self.rm_history[index]["emit"]
            mat.invert_z = self.rm_history[index]["invert_z"]
            mat.mirror_color = self.rm_history[index]["mirror_color"]
            mat.offset_z = self.rm_history[index]["offset_z"]
            mat.preview_render_type = self.rm_history[index]["preview_render_type"]
            mat.roughness = self.rm_history[index]["roughness"]
            mat.shadow_buffer_bias = self.rm_history[index]["shadow_buffer_bias"]
            mat.shadow_cast_alpha = self.rm_history[index]["shadow_cast_alpha"]
            mat.shadow_only_type = self.rm_history[index]["shadow_only_type"]
            mat.shadow_ray_bias = self.rm_history[index]["shadow_ray_bias"]
            mat.specular_alpha = self.rm_history[index]["specular_alpha"]
            mat.specular_color = self.rm_history[index]["specular_color"]
            mat.specular_hardness = self.rm_history[index]["specular_hardness"]
            mat.specular_intensity = self.rm_history[index]["specular_intensity"]
            mat.specular_ior = self.rm_history[index]["specular_ior"]
            mat.specular_ramp_blend = self.rm_history[index]["specular_ramp_blend"]
            mat.specular_ramp_factor = self.rm_history[index]["specular_ramp_factor"]
            mat.specular_ramp_input = self.rm_history[index]["specular_ramp_input"]
            mat.specular_shader = self.rm_history[index]["specular_shader"]
            mat.specular_slope = self.rm_history[index]["specular_slope"]
            mat.specular_toon_size = self.rm_history[index]["specular_toon_size"]
            mat.specular_toon_smooth = self.rm_history[index]["specular_toon_smooth"]
            mat.translucency = self.rm_history[index]["translucency"] 
            mat.transparency_method = self.rm_history[index]["transparency_method"]
            mat.type = self.rm_history[index]["type"] 
            mat.use_cast_approximate = self.rm_history[index]["use_cast_approximate"]
            mat.use_cast_buffer_shadows = self.rm_history[index]["use_cast_buffer_shadows"]          
            mat.use_cast_shadows_only = self.rm_history[index]["use_cast_shadows_only"]
            mat.use_cubic = self.rm_history[index]["use_cubic"] 
            mat.use_diffuse_ramp = self.rm_history[index]["use_diffuse_ramp"]
            mat.use_face_texture = self.rm_history[index]["use_face_texture"]
            mat.use_face_texture_alpha = self.rm_history[index]["use_face_texture_alpha"]
            mat.use_full_oversampling = self.rm_history[index]["use_full_oversampling"] 
            mat.use_light_group_exclusive = self.rm_history[index]["use_light_group_exclusive"]
            mat.use_mist = self.rm_history[index]["use_mist"] 
            mat.use_nodes = self.rm_history[index]["use_nodes"]
            mat.use_object_color = self.rm_history[index]["use_object_color"]
            mat.use_only_shadow = self.rm_history[index]["use_only_shadow"]
            mat.use_ray_shadow_bias = self.rm_history[index]["use_ray_shadow_bias"]
            mat.use_raytrace = self.rm_history[index]["use_raytrace"]
            mat.use_shadeless = self.rm_history[index]["use_shadeless"]
            mat.use_shadows = self.rm_history[index]["use_shadows"] 
            mat.use_sky = self.rm_history[index]["use_sky"]
            mat.use_specular_ramp = self.rm_history[index]["use_specular_ramp"]
            mat.use_tangent_shading = self.rm_history[index]["use_tangent_shading"]
            mat.use_textures = self.rm_history[index]["use_textures"]
            mat.use_transparency = self.rm_history[index]["use_transparency"]
            mat.use_transparent_shadows = self.rm_history[index]["use_transparent_shadows"]
            mat.use_transparent_shadows = self.rm_history[index]["use_vertex_color_paint"]
            
            # activate the diffuse ramp
            if self.rm_history[index]["use_diffuse_ramp"]:
                
                while len(mat.diffuse_ramp.elements)>1:
                    ele = mat.diffuse_ramp.elements[-1]
                    mat.diffuse_ramp.elements.remove(ele)
                for el in range(0, len(self.rm_history[index]["diffuse_ramp"])):
                     
                    if el==0 :
                        
                        mat.diffuse_ramp.elements[el].color[0] = self.rm_history[index]["diffuse_ramp"][el]["color"][0]
                        mat.diffuse_ramp.elements[el].color[1] = self.rm_history[index]["diffuse_ramp"][el]["color"][1]
                        mat.diffuse_ramp.elements[el].color[2] = self.rm_history[index]["diffuse_ramp"][el]["color"][2]
                        mat.diffuse_ramp.elements[el].color[3] = self.rm_history[index]["diffuse_ramp"][el]["color"][3]
                        mat.diffuse_ramp.elements[el].position = self.rm_history[index]["diffuse_ramp"][el]["position"]
                    else :
                        mat.diffuse_ramp.elements.new(el)
                        mat.diffuse_ramp.elements[el].color[0] = self.rm_history[index]["diffuse_ramp"][el]["color"][0]
                        mat.diffuse_ramp.elements[el].color[1] = self.rm_history[index]["diffuse_ramp"][el]["color"][1]
                        mat.diffuse_ramp.elements[el].color[2] = self.rm_history[index]["diffuse_ramp"][el]["color"][2]
                        mat.diffuse_ramp.elements[el].color[3] = self.rm_history[index]["diffuse_ramp"][el]["color"][3]
                        mat.diffuse_ramp.elements[el].position = self.rm_history[index]["diffuse_ramp"][el]["position"]
                    
                    if self.rm_history[history_index]["use_nodes"]:
                        # activate node tree nodes
                        
                        nt = mat.node_tree
                        
                        #first remove any existent nodes to replace them with new ones
                        for x in range(0,len(nt.nodes)):
                            nt.nodes.remove(nt.nodes[-1])
                            
                        # now set the new nodes
                        
                        for x in range(0, len(self.rm_history[index]["node_tree"]["nodes"])):
                            
                            nt.nodes.new(self.rm_history[index]["node_tree"]["nodes"][x]["type"])
                            nt.nodes[x].name = self.rm_history[index]["node_tree"]["nodes"][x]["name"]
                            nt.nodes[x].location[0] = self.rm_history[index]["node_tree"]["nodes"][x]["pos_x"]
                            nt.nodes[x].location[1] = self.rm_history[index]["node_tree"]["nodes"][x]["pos_y"]
                            print(nt.nodes[x].name)
                        
                        for x in range(0, len(self.rm_history[index]["node_tree"]["links"])):
                            
                            node_name_source = self.rm_history[index]["node_tree"]["links"][x]["from_node"]
                            node_name_destination = self.rm_history[index]["node_tree"]["links"][x]["to_node"]
                            socket_name_source = self.rm_history[index]["node_tree"]["links"][x]["from_socket"]
                            socket_name_destination = self.rm_history[index]["node_tree"]["links"][x]["to_socket"]
                            
                            print("trying to connect node["+node_name_source+"] socket ["+socket_name_source+"] with node["+node_name_destination+"] socket["+socket_name_destination+"]")
                            nt.links.new(nt.nodes[node_name_source].outputs[socket_name_source],nt.nodes[node_name_destination].inputs[socket_name_destination])
                            
                        
                        
                        
     
# create the instance class for randomisation   
rm = random_material_class()
                
# this the main panel
class gyes_panel(bpy.types.Panel):
    bl_label = "Gyes"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    @classmethod    
    def poll(self, context):
        if context.object and context.object.type == 'MESH':                    
            return len(context.object.data.materials)
        
    def draw(self, context):
        
        layout = self.layout
        row = layout.row()
        row.prop(context.scene , "gui_mode" )
        
        # check which Gui mode the user has selected (Simple is the default one and display the appropriate gui
        
        if context.scene.gui_mode == 'simple' :
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
            
        if context.scene.gui_mode == 'simple_percentage' :
            box = layout.box()
            
            if context.scene.rdiffuse_shader :
                box.prop(context.scene,"rdiffuse_shader_percentage", slider = True)
            else:
                box.label(text="Diffuse Shader is disabled ")
                
            if context.scene.rdiffuse_color :
                box.prop(context.scene,"rdiffuse_color_percentage", slider = True)
            else:
                box.label(text="Diffuse Color is disabled ")
                
            if context.scene.rdiffuse_intensity :
                box.prop(context.scene,"rdiffuse_intensity_percentage", slider = True)
            else:
                box.label(text="Diffuse Intensity is disabled ")
                
            if context.scene.rspecular_shader :
                box.prop(context.scene,"rspecular_shader_percentage", slider = True)
            else:
                box.label(text="Specular Shader is disabled ")
                
            if context.scene.rspecular_color :
                box.prop(context.scene,"rspecular_color_percentage", slider = True)
            else:
                box.label(text="Specular Color is disabled ")
                
            if context.scene.rspecular_intensity :
                box.prop(context.scene,"rspecular_intensity_percentage", slider = True)
            else:
                box.label(text="Specular Intensity is disabled ")
                
            if context.scene.rspecular_hardness :
                box.prop(context.scene,"rspecular_hardness_percentage", slider = True)
            else:
                box.label(text="Specular Hardness is disabled ")
            
            if context.scene.rtransparency :
                box.prop(context.scene,"rtransparency_percentage", slider = True)
            else:
                box.label(text="Transparency is disabled ")
                
            box.prop(context.scene,"general_percentage", slider = True)
            layout.operator("gyes.random_material")
        
        if context.scene.gui_mode== 'templates' : 
            box = layout.box()
                    
        if context.scene.gui_mode== 'help' :
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
            box.label(text="")
            box.label(text="Percentage")
            box.label(text="--------------------------")
            box.label(text="Percentage randomisation means that the parameter")
            box.label(text="is randomised inside a range of percentage of the")
            box.label(text=" full range of the value. When a specific percentage ")
            box.label(text="is zero, the general percentage is used instead for ")
            box.label(text="that area. When a specific percentage is not zero then ")
            box.label(text="general percentage is ignored and specific percentage ")
            box.label(text="is used instead. If you dont want to randomise that area ")
            box.label(text="at all, in Simple Mode use the corresponding button to")
            box.label(text="completely disable that area , the percentage slider")
            box.label(text="will also be disable in the percentage mode.")
            box.label(text="Randomisation takes always the current value as starting ")
            box.label(text="point so the next randomisation will use the current randomised ")
            box.label(text="value. Randomisation is always 50% of the specific percentage ")
            box.label(text="bellow the current value and 50% above . If the percentage exceeed")
            box.label(text="minimum and maximum values of the full range, then it will default")
            box.label(text="to minimum and maximum accordingly. ")
            box.label(text="")
            box.label(text="")
            box.label(text="")
            box.label(text="")
            box.label(text="")
                       
        # Display the History Gui for all modes
        
        layout.label(text="History")
        history_box= layout.box()
        history_box.prop(context.scene, "history_index")
        row = history_box.row()
        row.operator("gyes.first")
        row.operator("gyes.previous")
        row.operator("gyes.next")
        row.operator("gyes.last")
        rm_index = context.scene.history_index
        
        if rm_index in rm.rm_history and rm.rm_history[rm_index] :
            row = history_box.row()
            a = row.split(percentage = 0.2, align = True)
            a.operator("gyes.random_activate")
            a.operator("gyes.activate")
            
        else:
            history_box.label(text= "Empty Index ! ")
        
        if context.scene.history_index < len(rm.rm_history)+2:
            history_box.operator("gyes.store")
        else:
            history_box.label(text= "Not the first Empty Index")
        if rm_index in rm.rm_history and rm.rm_history[rm_index] :
            history_box.operator("gyes.delete")
            row2 = history_box.row()
            row2.operator("gyes.delete_start")
            row2.operator("gyes.delete_end")
        if hasattr(bpy.context.scene,"historybak") and bpy.context.scene.historybak!='':
            history_box.operator("gyes.restore")
        else:
            history_box.label(text="Backup not Found")    
        
# Generate the random material button
class gyes_random_material(bpy.types.Operator):
    
    bl_idname = "gyes.random_material"
    bl_label = "Random Material"
    label = bpy.props.StringProperty()
    bl_description = "Generate the random material"
    
    def execute(self, context):
        for i in context.selected_objects :
            if i.type == 'MESH' :
            
                rm.random_material(i.active_material,'Random')
        return{'FINISHED'}

# Move to the first history index and activate it
class history_first(bpy.types.Operator):
    
    bl_label = "|<"
    bl_idname = "gyes.first"
    bl_description = "Move to the first history index and activate it"
    
    def execute(self, context):
        context.scene.history_index = 1 
        rm.activate()
        
        return{'FINISHED'}


# Move to the previous hisory index and activate it
class history_previous(bpy.types.Operator):
    
    bl_label = "<"
    bl_idname = "gyes.previous"
    bl_description = "Move to the previous history index and activate it"
    
    def execute(self, context):
        if context.scene.history_index > 1 :
            context.scene.history_index = context.scene.history_index -1
            rm_index = context.scene.history_index
            if rm_index in rm.rm_history and rm.rm_history[rm_index]:
                rm.activate()
        
        return{'FINISHED'}

# Move to the next hisory index and activate it
class history_next(bpy.types.Operator):
    
    bl_label = ">"
    bl_idname = "gyes.next"
    bl_description = "Move to the next history index and activate it"
    
    def execute(self, context):
        if context.scene.history_index > 0 :
            context.scene.history_index = context.scene.history_index +1
            rm_index = context.scene.history_index
            if rm_index in rm.rm_history and rm.rm_history[rm_index]:
                rm.activate()
        
        return{'FINISHED'}
    

# Move to the last hisory index and activate it
class history_last(bpy.types.Operator):
    
    bl_label = ">|"
    bl_idname = "gyes.last"
    bl_description = "Move to the last history index and activate it"
    
    def execute(self, context):
        index = rm.rm_history 
        context.scene.history_index = len(index) 
        rm.activate()
        
        return{'FINISHED'}

# The current history index becomes the active material 
class history_activate(bpy.types.Operator):
    
    bl_label = "Activate"
    bl_idname = "gyes.activate"
    bl_description = "The current history index becomes the active material"
    
    def execute(self, context):
        rm_index = context.scene.history_index
        if rm.rm_history[rm_index] != {}:
            rm.activate()
        
        return{'FINISHED'}

# A random history index becomes the active material 
class history_random_activate(bpy.types.Operator):
    
    bl_label = "R"
    bl_idname = "gyes.random_activate"
    bl_description = "A random history index becomes the active material"
    
    def execute(self, context):
        rm_index = context.scene.history_index
        if rm.rm_history[rm_index] != {}:
            rm.activate(random_assign = True)
        
        return{'FINISHED'}


# It stores current active material to the selected history index
class store_to_history(bpy.types.Operator):
    
    bl_label = "Store"
    bl_idname = "gyes.store"
    bl_description = " It stores current active material to the selected history index"
    
    def execute(self, context):
        mat = context.selected_objects[0].active_material
        rm.store_to_history(mat)
         
        
        return{'FINISHED'}

# Delete selected history index from history
class delete_from_history(bpy.types.Operator):
    
    bl_label = "Delete"
    bl_idname = "gyes.delete"
    bl_description = "Delete selected history index from history"
    
    def execute(self, context):
        rm.delete_from_history()
        
        return{'FINISHED'}
               
# Start deletion from this index
class delete_from_history_start(bpy.types.Operator):
    
    bl_label = "Del Start"
    bl_idname = "gyes.delete_start"
    bl_description = "Start deletion from this index"
    
    def execute(self, context):
        rm_index = context.scene.history_index
        rm.delete_start_index = rm_index
        
        return{'FINISHED'}   

# End deletion here and delete all selected indices
class delete_from_history_end(bpy.types.Operator):
    
    bl_label = "Del End"
    bl_idname = "gyes.delete_end"
    bl_description = "End deletion here and delete all selected indices"
    
    def execute(self, context):
        delete_end_index = context.scene.history_index
        context.scene.history_index = rm.delete_start_index
        for x in range ( rm.delete_start_index , delete_end_index):
            rm.delete_from_history()
        
        return{'FINISHED'} 
    
# End deletion here and delete all selected indices
class restore_history(bpy.types.Operator):
    
    bl_label = "Restore"
    bl_idname = "gyes.restore"
    bl_description = "Restore history"
    
    def execute(self, context):
        
        s=""
        s = bpy.context.scene.historybak
        print(s)
        rm.rm_history=eval(s)
        
        print("restored history dictionary") 
        
        return{'FINISHED'} 
    
 
         
#registration is necessary for the script to appear in the GUI
def register():
    bpy.utils.register_class(gyes_panel)
    bpy.utils.register_class(gyes_random_material)
    bpy.utils.register_class(history_previous)
    bpy.utils.register_class(history_next)
    bpy.utils.register_class(history_activate)
    bpy.utils.register_class(history_random_activate)
    bpy.utils.register_class(store_to_history)
    bpy.utils.register_class(delete_from_history)
    bpy.utils.register_class(delete_from_history_start)
    bpy.utils.register_class(delete_from_history_end)
    bpy.utils.register_class(history_first)
    bpy.utils.register_class(history_last)
    bpy.utils.register_class(restore_history)
   
def unregister():
    bpy.utils.unregister_class(gyes_panel)
    bpy.utils.unregister_class(gyes_random_material)
    bpy.utils.unregister_class(history_previous)
    bpy.utils.unregister_class(history_next)
    bpy.utils.unregister_class(history_activate)
    bpy.utils.unregister_class(history_random_activate)
    bpy.utils.unregister_class(store_to_history)
    bpy.utils.unregister_class(delete_from_history)
    bpy.utils.unregister_class(delete_from_history_start)
    bpy.utils.unregister_class(delete_from_history_end)
    bpy.utils.unregister_class(history_first)
    bpy.utils.unregister_class(history_last)
    bpy.utils.unregister_class(restore_history)
    
if __name__ == '__main__':
    register()