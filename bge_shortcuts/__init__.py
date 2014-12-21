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

bl_info = {
	"name": "Game Engine Shortcuts",
	"description": "Tools to make game development slightly easier",
	"author": "Nick Polet (klauser)",
	"version": (0, 0, 1),
	"blender": (2, 61, 0),
	"location": "View3D > Game Engine Tab",
	"warning": "", # used for warning icon and text in addons panel
	"wiki_url": "http://wiki.blender.org/index.php/Extensions:2.5/Py/"
				"Scripts/My_Script",
	"category": "Game Engine"}


if "bpy" in locals():
	import imp
	imp.reload(shader_op)
	imp.reload(test_areas)

else:
	from .shader_settings import *
	from . import shader_op
	from . import test_areas

	
import bpy
import math

from bpy.props import *



from bge_shortcuts.cameras import FlyCameraOperator, FirstPersonRigOperator, ThirdPersonRigOperator




def draw_toggle_button(panel, operator_name, icon, filter_name):

	options_operator = operator_name + '_options'

	if 'shortcuts_filters' in bpy.data.objects:
		object = bpy.data.objects['shortcuts_filters']
	else:
		object = None

	row = panel.layout.row(align=True)
	row.alignment = 'EXPAND'

	if object != None:
		if filter_name in object.game.actuators:
			# Button to remove the filter
			column = row.column()
			column.scale_x = 0.88
			column.operator(operator_name, icon='X')

			# Options button
			column = row.column()
			column.scale_x = 0.12
			column.operator(options_operator, text=' ', icon='SCRIPTWIN')
		else:
			row.operator(operator_name, icon=icon)

	else:
		row.operator(operator_name, icon=icon)




#
#    Menu in tools region
#
class ShortcutsPanel(bpy.types.Panel):
	bl_category = "Game Engine"
	bl_label = "Game Engine Shortcuts"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
 
	def draw(self, context):



		self.layout.label("Navigation", icon='ZOOMIN')
		self.layout.operator("bge_shortcuts.fly_camera_operator", icon='OUTLINER_OB_CAMERA')
		#self.layout.operator("bge_shortcuts.orbit_camera_operator", icon='CAMERA_DATA')
		
		self.layout.separator()
		self.layout.operator("bge_shortcuts.first_person_rig", icon='ARMATURE_DATA')
		self.layout.operator("bge_shortcuts.third_person_rig", icon='POSE_DATA')
 
		self.layout.separator()
		self.layout.label("Shaders", icon='COLOR')

		# Filters
		draw_toggle_button(self, "bge_shortcuts.dof_filter", "VISIBLE_IPO_ON", "dof")
		draw_toggle_button(self, "bge_shortcuts.ssao_filter", "SMOOTH", "ssao")
		draw_toggle_button(self, "bge_shortcuts.ssgi_filter", "MOD_SUBSURF", "ssgi")
		draw_toggle_button(self, "bge_shortcuts.bloom_filter", "LAMP_SUN", "bloom")
		draw_toggle_button(self, "bge_shortcuts.bleach_filter", "PROP_OFF", "bleach")
		draw_toggle_button(self, "bge_shortcuts.vignette_filter", "BBOX", "vignette")
		draw_toggle_button(self, "bge_shortcuts.retinex_filter", "SEQ_HISTOGRAM", "retinex")
		draw_toggle_button(self, "bge_shortcuts.chromatic_filter", "FORCE_FORCE", "chromatic")
		draw_toggle_button(self, "bge_shortcuts.saturate_filter", "MESH_CUBE", "saturate")
		draw_toggle_button(self, "bge_shortcuts.warm_sepia_filter", "MARKER_HLT", "warm_sepia")
		draw_toggle_button(self, "bge_shortcuts.technicolor_1_filter", "COLOR_RED", "technicolor_1")
		draw_toggle_button(self, "bge_shortcuts.technicolor_2_filter", "COLOR_BLUE", "technicolor_2")
		draw_toggle_button(self, "bge_shortcuts.movie_noise_filter", "CLIP", "movie_noise")
		draw_toggle_button(self, "bge_shortcuts.pixelate_filter", "MOD_BUILD", "pixelate")
		draw_toggle_button(self, "bge_shortcuts.edge_detect_filter", "VIEW3D_VEC", "edge_detect")
		draw_toggle_button(self, "bge_shortcuts.harsh_colors_filter", "SEQ_CHROMA_SCOPE", "harsh_colors")
		draw_toggle_button(self, "bge_shortcuts.depth_filter", "MOD_ARRAY", "depth")

		self.layout.separator()

		#self.layout.label("Test Areas", icon='COLOR')
		#self.layout.operator("bge_shortcuts.test_area_1", icon='POSE_DATA')


class OrbitCameraOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.orbit_camera_operator"
	bl_label = "Orbit Camera"
	bl_description = "Creates an orbit camera for rotating around an object"

	@classmethod
	def poll(cls, context):
		return True
		#return context.active_object is not None

	def execute(self, context):
		return {'FINISHED'}


def register():
	bpy.utils.register_module(__name__)

def unregister():
	bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
	register()
