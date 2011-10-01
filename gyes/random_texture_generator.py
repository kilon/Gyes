# -*- coding: UTF-8 -*-
# first we import all the required modules

import bpy ,random , copy 
from bpy.props import *
import textwrap

class random_texture_class:
    """ this class contains all fuctions and variables concerning generation of random material """
    
    def __init__(self):
        """ several fuctions can be found here . All options for random generation . The History dictionary and several others."""
                   
        # various gui modes (simple, template etc)
        bpy.types.Scene.rtexture_gui_mode = EnumProperty(attr='mode', name='Mode', items=(
('simple', 'Simple', 'The first item'),
('simple_percentage', 'Simple percentage' , 'here you define individual percentage'),
('templates', 'Templates', 'The second item'),
('help', 'Help', 'The third item')), default='simple')

        # Here I define the selective areas that the user can enable or disable for randomisation in simple mode               
        bpy.types.Scene.rtexture_type = EnumProperty(attr='type', name='type', items=(
('RANDOM','RANDOM','RANDOM'),
('BLEND','BLEND','BLEND'),
('CLOUDS','CLOUDS','CLOUDS'),
('DISTORTED_NOISE','DISTORTED_NOISE','DISTORTED_NOISE'),
('ENVIRONMENT_MAP','ENVIRONMENT_MAP','ENVIRONMENT_MAP'),
('IMAGE','IMAGE','IMAGE'),
('MAGIC','MAGIC','MAGIC'),
('MARBLE','MARBLE','MARBLE'),
('MUSGRAVE','MUSGRAVE','MUSGRAVE'),
('NOISE','NOISE','NOISE'),
('POINT_DENSITY','POINT_DENSITY','POINT_DENSITY'),
('STUCCI','STUCCI','STUCCI'),
('VORONOI','VORONOI','VORONOI'),
('VOXEL_DATA','VOXEL_DATA','VOXEL_DATA'),
('WOOD','WOOD','WOOD')), default='RANDOM')

        bpy.types.Scene.rtexture_color = BoolProperty(name= "Color Factor" ,description = "Color factor of the texture" , default = True)    
        bpy.types.Scene.rtexture_intensity = BoolProperty(name= "Intensity" ,description = "Intensity of the texture" , default = True)
        bpy.types.Scene.rtexture_contrast = BoolProperty(name= "Contrast" ,description = "Contrast of the texture" , default = True)
        bpy.types.Scene.rtexture_saturation = BoolProperty(name= "Saturation" ,description = "Saturation of the texture" , default = True)
        bpy.types.Scene.rtexture_progression = BoolProperty(name= "Progression" ,description = "Progression of the texture" , default = True)
        bpy.types.Scene.rtexture_axis = BoolProperty(name= "Progr. Axis" ,description = "Progression of the texture" , default = True)
        
        # Percentage randomisation
        bpy.types.Scene.rtexture_general_percentage = IntProperty(name="General percentage", description = " General percentage of randomisation" , min = 0 , max = 100 , default = 100, subtype = 'PERCENTAGE')
        bpy.types.Scene.rtexture_color_percentage = IntProperty(name="Color Factor", description = " Color factor percentage of randomisation" , min = 0 , max = 100 , default = 100, subtype = 'PERCENTAGE')
        bpy.types.Scene.rtexture_intensity_percentage = IntProperty(name="Intensity", description = " Intensity of the texture" , min = 0 , max = 100 , default = 0, subtype = 'PERCENTAGE')
        bpy.types.Scene.rtexture_contrast_percentage = IntProperty(name="Contrast", description = " Contrast of the texture" , min = 0 , max = 100 , default = 0, subtype = 'PERCENTAGE')
        bpy.types.Scene.rtexture_saturation_percentage = IntProperty(name="Saturation", description = " Saturation of the texture" , min = 0 , max = 100 , default = 0, subtype = 'PERCENTAGE')
        bpy.types.Scene.rtexture_progression_percentage = IntProperty(name="Saturation", description = " Saturation of the texture" , min = 0 , max = 100 , default = 0, subtype = 'PERCENTAGE')
       
        # this is the dictionary that stores history
        bpy.types.Scene.rtexture_history_index = IntProperty(name= "History Index" ,description = "The eumber of Random Material Assigned to the Active MAterial of the Selected Object from the history" , default = 1, min = 1 )
        self.history={}
        self.delete_start_index=1
        
        # the prop that controls the text wrap in help menu
        bpy.types.Scene.text_width = IntProperty(name = "Text Width" , description = "The width above which the text wraps" , default = 20 , max = 180 , min = 1)
        
        # here is where history dictionary is saved with the blend file
        # if the backup is already saved with the blend file it is used 
        # to restory the history dictionary , if not it is created
        
        if hasattr(bpy.context.scene , "texture_historybak")==False:
            bpy.types.Scene.texture_historybak = StringProperty()
            print("created history backup")
            
         # non read only material properties where keyframes can be inserted or removed
        self.animated_properties=["alpha",
        "use_vertex_color_paint"]
            
        
    # compute randomisation based on the general or specific percentage chosen
    # if the specific percentage is zero then the general percentage is used
    def compute_percentage(self,min,max,value,percentage):
        range = max-min
        general_percentage = bpy.context.scene.rtexture_general_percentage
        
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
        
        length = len(self.history)
        index = bpy.context.scene.texture_history_index
        for x in range(index , length):
            if index != length :
                self.history[x]= self.history[x+1] 
        del self.history[length]
        length = len(self.history) 
        if index <= length:
            self.activate()
            
        bpy.context.scene.texture_historybak = str(self.rm_history)
    
    # the fuction that randomises the material 
    def random_texture(self,material):
        scn = bpy.context.scene
        
        # if the texture exists use that for randomisation if not then create a new one
        if material.texture_slots[material.active_texture_index] and material.texture_slots[material.active_texture_index].texture:
            texture = material.texture_slots[material.active_texture_index].texture
            if not scn.rtexture_type=='Random':
               texture.type = scn.rtexture_type
            else:
               texture.type = 'NOISE'
            material.texture_slots[material.active_texture_index].texture = texture 
        else:
            material.texture_slots.create(material.active_texture_index)           
            if not scn.rtexture_type=='Random':
               texture = bpy.data.textures.new('Rand_tex_',scn.rtexture_type)
            else:
               texture = bpy.data.textures.new('Rand_tex_','NOISE')
            material.texture_slots[material.active_texture_index].texture = texture
        
        # randomise parameters depending on the type of the texture
        
        if scn.rtexture_type == 'BLEND':
            
            if scn.rtexture_color:
                texture.factor_red = self.compute_percentage(0,2,texture.factor_red,scn.rtexture_color_percentage)
                texture.factor_green = self.compute_percentage(0,2,texture.factor_green,scn.rtexture_color_percentage)
                texture.factor_blue = self.compute_percentage(0,2,texture.factor_blue,scn.rtexture_color_percentage)
            if scn.rtexture_intensity:
                texture.intensity = self.compute_percentage(0,2,texture.intensity,scn.rtexture_intensity_percentage)
            if scn.rtexture_contrast:
                texture.contrast = self.compute_percentage(0,5,texture.contrast,scn.rtexture_contrast_percentage)
            if scn.rtexture_saturation:
                texture.saturation = self.compute_percentage(0,2,texture.saturation,scn.rtexture_saturation_percentage)
            if scn.rtexture_progression:
                texture.progression = random.choice(['LINEAR', 'QUADRATIC', 'EASING', 'DIAGONAL', 'SPHERICAL', 'QUADRATIC_SPHERE', 'RADIAL'])
            if scn.rtexture_axis and not (texture.progression=='DIAGONAL' or texture.progression=='SPHERICAL' or texture.progression=='QUADRATIC_SPHERE'):
                texture.use_flip_axis = random.choice(['HORIZONTAL', 'VERTICAL'])
          
        if scn.rtexture_type == 'NOISE':
            
            if scn.rtexture_intensity:
                texture.intensity = self.compute_percentage(0,2,texture.intensity,scn.rtexture_intensity_percentage)
          
        #self.store_to_history(texture)
          
        return texture

    #store active material to history
    def store_to_history(self, texture):
        scn = bpy.context.scene
        history_index = scn.texture_history_index
        self.history[history_index]= {"name" : texture.name} 
        print("text stored : "+self.history[history_index]["name"])
        texture.use_fake_user = True
                 
        bpy.context.scene.texture_historybak = str(self.history)
    """    
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
                
            material_slots_backup =[]    
            material_slots_len = len(i.material_slots)
            
            for x in range(0,material_slots_len):
                print("x = ",x)
                if x==0:
                    print("appending stored material")
                    i.active_material_index=material_slots_len-1
                    i.data.materials.append(bpy.data.materials[self.rm_history[index]["name"]])
                    i.active_material_index=0
                    bpy.ops.object.material_slot_remove()
                
                else:
                    print("deleting materials")
                    i.active_material_index=0
                    material_slots_backup.append(i.material_slots[0].material.name)
                    print("backup : "+i.material_slots[0].material.name)
                    bpy.ops.object.material_slot_remove()
                    
            
            i.active_material_index=0
            for y in range(0,len(material_slots_backup)):
                i.active_material_index=y
                i.data.materials.append(bpy.data.materials[material_slots_backup[y]])
            i.active_material_index=0
                  
 """
    # a nice multi label                        
    def multi_label(self, text, ui,text_width):
        
        for x in range(0,len(text)):
            el = textwrap.wrap(text[x], width = text_width)
            
            for y in range(0,len(el)):
                ui.label(text=el[y])
                
    def draw_gui(self ,context,panel):
        layout = panel.layout
        row = layout.row()
        row.prop(context.scene , "rtexture_gui_mode" )
        
        # check which Gui mode the user has selected (Simple is the default one and display the appropriate gui
        
        if context.scene.rtexture_gui_mode == 'simple' :
            box = layout.box()
            box.prop(context.scene,"rtexture_type")
            
            if context.scene.rtexture_type=='BLEND':
               box.prop(context.scene,"rtexture_color", toggle = True)
               box.prop(context.scene,"rtexture_intensity", toggle = True)
               box.prop(context.scene,"rtexture_contrast", toggle = True)
               box.prop(context.scene,"rtexture_saturation", toggle = True)
               box.prop(context.scene,"rtexture_progression", toggle = True)
               box.prop(context.scene,"rtexture_axis", toggle = True)
            
            if context.scene.rtexture_type=='NOISE':
               box.prop(context.scene,"rtexture_intensity", toggle = True)
            
            box.prop(context.scene,"rtexture_general_percentage", slider = True)
            layout.operator("gyes.random_texture")
            
        if context.scene.rtexture_gui_mode == 'simple_percentage' :
            box = layout.box()
            
            if context.scene.rtexture_type=='BLEND':
            
                if context.scene.rtexture_color:
                    box.prop(context.scene,"rtexture_color_percentage", slider = True)
                else:
                    box.label(text="Texture Intensity disabled ")
                    
                if context.scene.rtexture_intensity:
                    box.prop(context.scene,"rtexture_intensity_percentage", slider = True)
                else:
                    box.label(text="Texture Intensity disabled ")
                
                if context.scene.rtexture_intensity: 
                    box.prop(context.scene,"rtexture_contrast_percentage", slider = True)
                else:
                    box.label(text="Texture Contrast disabled ")
                
                if context.scene.rtexture_saturation: 
                    box.prop(context.scene,"rtexture_saturation_percentage", slider = True)
                else:
                    box.label(text="Texture Saturation disabled ")
            
            if context.scene.rtexture_type=='NOISE':
            
                if context.scene.rtexture_intensity:
                    box.prop(context.scene,"rtexture_intensity_percentage", slider = True)
                else:
                    box.label(text="Texture Intensity disabled ")
               
            box.prop(context.scene,"rtexture_general_percentage", slider = True)
            layout.operator("gyes.random_texture")
        
        if context.scene.rtexture_gui_mode== 'templates' : 
            box = layout.box()
            box.label(text="Not yet implemented")
                    
        if context.scene.rtexture_gui_mode== 'help' :
            box = layout.box()
            help_text=["","Copyright 2011 Kilon  ",
            "GYES - RGM",    
            "Random Material  Generator",
            "A tool that generates random materials.",
            "",
            "Simple Mode",
            "--------------------------",
            "In this mode you can do basic randomisation. Choose parameters you want to randomise by turning them on or off with clicking on them. Hit the random button when you are ready. Each time you hit the button the new random material is stored in a history index",
            "",
            "History",
            "--------------------------",
            "History index -> choose index",
            "( < ) -> Previous index (activate)",
            "( > ) -> Next index (activate)",
            "( |< ) -> First history index",
            "( >| ) -> Last history index",
            "Activate -> use this index as active material",
            "Animate -> Insert a keyframe in the current frame for every singly non read only material property",
            "X -> Remove a keyframe in the current frame for every singly non read only material property",
            "R -> works just like activate but instead of using the current selected index use a randomly selected one",
            "Delete -> delete this index",
            "Del start -> start deletion from here",
            "Del end -> end deletion here",
            "Restore -> restores history from the saved blend file",
            "",
            "Percentage",
            "--------------------------",
            "Percentage randomisation means that the parameter is randomised inside a range of percentage of the full range of the value. When a specific percentage is zero, the general percentage is used instead for that area. When a specific percentage is not zero then general percentage is ignored and specific percentage is used instead. If you dont want to randomise that area at all, in Simple Mode use the corresponding button to completely disable that area , the percentage slider will also be disable in the percentage mode. Randomisation takes always the current value as starting point so the next randomisation will use the current randomised value. Randomisation is always 50% of the specific percentage bellow the current value and 50% above . If the percentage exceeed minimum and maximum values of the full range, then it will default to minimum and maximum accordingly. "]
            w=bpy.context.scene.text_width
            box.prop(context.scene,"text_width", slider =True)
            self.multi_label(help_text,box,w) 
                                
rt =random_texture_class()

            
        
# Generate the random material button
class gyes_random_texture(bpy.types.Operator):
    
    bl_idname = "gyes.random_texture"
    bl_label = "Random Texture"
    label = bpy.props.StringProperty()
    bl_description = "Generate the random texture"
    
    def execute(self, context):
        for i in context.selected_objects :
            if i.type == 'MESH' :

                rt.random_texture(i.active_material)

        return{'FINISHED'}

#registration is necessary for the script to appear in the GUI
def register():
    bpy.utils.register_class(gyes_random_texture)
def unregister():
    bpy.utils.unregister_class(gyes_random_material)
if __name__ == '__main__':
    register()
