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
    "description": "Gyes is a collection of scripts that simplify , automate and extend blender",
    "author": "Kilon",
    "version": (0,5),
    "blender": (2, 5, 8),
    "api": 38600,
    "location": "View3D > Left panel ",
    "warning": '', # used for warning icon and text in addons panel
    "wiki_url": "http://blenderartists.org/forum/showthread.php?218110-Gyes-%28Random-Material-Generator%29",
    "tracker_url": "http://projects.blender.org/tracker/index.php?func=detail&aid=27470&group_id=153&atid=467",
    "category": "Other"}
    
if "bpy" in locals():
    import imp
    imp.reload(random_material_generator)
    #imp.reload(random_landscape_generator)
else:
    from gyes import random_material_generator
    #from gyes import random_landscape_generator
    
import bpy
from bpy.props import *


# Choose the tool you want to use
bpy.types.Scene.tool = EnumProperty(attr='tool', name='Tool', items=(
('RGM', 'RGM', 'Random Material Generator'),
('RLG', 'RLG' , 'Random Landscape Generator'),
('TARTARA', 'TARTARA', 'An online Library for any kind of blender asset')), default='RGM')


rm = random_material_generator.rm                 
# this the main panel
class gyes_panel(bpy.types.Panel):
    bl_label = "Gyes - RGM "
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    @classmethod    
    def poll(self, context):
        if context.object and context.object.type == 'MESH':                    
            return len(context.object.data.materials)
        
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(context.scene , "tool" )
        
        # check which tool the user has selected (RGM is the default one) and display the appropriate gui
        
        if context.scene.tool == 'RGM' :
            rm.draw_gui(context,self)
        r = layout.row()
        if context.scene.tool == 'RLG' :
            r.label(text="WIP not finished yet")
        if context.scene.tool == 'TARTARA' :
            r.label(text="WIP not finished yet")


        
def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

 
if __name__ == "__main__":
    register()
