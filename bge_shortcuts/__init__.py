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
	
import bpy
import math



def create_filter_holder(context):

	bpy.ops.object.select_all(action='DESELECT')
	bpy.ops.object.text_add(view_align=False, enter_editmode=False, location=(0, 0, 2))
	bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
	bpy.ops.object.editmode_toggle()
	bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
	bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
	bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
	bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION')
	bpy.ops.font.text_insert(text="GLSL Filters")
	bpy.ops.object.editmode_toggle()
	bpy.context.object.hide_render = True
	bpy.context.object.name = "shortcuts_filters"
	bpy.context.object.data.align = 'CENTER'
	bpy.ops.object.game_property_new(name="timer", type='TIMER')

	return bpy.context.selected_objects[0]

def add_filter(context, filter_holder, script_name, filter_name, pass_index):


	# Object for adding the glsl filters to
	if 'shortcuts_filters' in bpy.data.objects:
		object = bpy.data.objects['shortcuts_filters']
	else:
		object = create_filter_holder(context)

	# Check to see if the filter has already been added
	if filter_name in object.game.actuators:
		bpy.ops.logic.actuator_remove(actuator=filter_name, object=object.name)
		bpy.ops.logic.controller_remove(controller=filter_name, object=object.name)
		bpy.ops.logic.sensor_remove(sensor=filter_name, object=object.name)
		return

	# Text block for the script
	if script_name in bpy.data.texts:
		text = bpy.data.texts[script_name]
	else:
		bpy.ops.text.new()
		text = bpy.data.texts[-1]
		text.name = script_name

		text.from_string(filter_holder.script)

	# Add an 'always' sensor
	bpy.ops.logic.sensor_add(type='ALWAYS', object=object.name)
	sensor = object.game.sensors[-1]
	sensor.name = filter_name
	sensor.show_expanded = False

	bpy.ops.logic.actuator_add(type='FILTER_2D', object=object.name)
	actuator = object.game.actuators[-1]
	actuator.show_expanded = False
	actuator.name = filter_name
	actuator.mode = 'CUSTOMFILTER'
	actuator.filter_pass = pass_index
	actuator.glsl_shader = text


	# Add a controller to link up the sensor and actuator
	bpy.ops.logic.controller_add(type='LOGIC_AND', object=object.name)        
	cont = object.game.controllers[-1]
	cont.show_expanded = False
	cont.name = filter_name
	cont.link(sensor, actuator)


def draw_toggle_button(panel, operator_name, icon, filter_name):


	if 'shortcuts_filters' in bpy.data.objects:
		object = bpy.data.objects['shortcuts_filters']
	else:
		object = None


	if object != None:
		if filter_name in object.game.actuators:
			panel.layout.operator(operator_name, icon='X')
		else:
			panel.layout.operator(operator_name, icon=icon)

	else:
		panel.layout.operator(operator_name, icon=icon)




#
#    Menu in tools region
#
class ShortcutsPanel(bpy.types.Panel):
	bl_category = "Game Engine"
	bl_label = "Game Engine Shortcuts"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
 
	def draw(self, context):



		self.layout.label("Add", icon='ZOOMIN')
		self.layout.operator("game_engine_shortcuts.fly_camera_operator", icon='OUTLINER_OB_CAMERA')
		self.layout.operator("game_engine_shortcuts.orbit_camera_operator", icon='CAMERA_DATA')
		
		self.layout.separator()
		self.layout.operator("game_engine_shortcuts.first_person_rig", icon='ARMATURE_DATA')
		self.layout.operator("game_engine_shortcuts.third_person_rig", icon='POSE_DATA')
 
		self.layout.separator()
		self.layout.label("Filters", icon='COLOR')

		# Filters
		draw_toggle_button(self, "game_engine_shortcuts.dof_filter", "VISIBLE_IPO_ON", "dof")
		draw_toggle_button(self, "game_engine_shortcuts.ssao_filter", "SMOOTH", "ssao")
		draw_toggle_button(self, "game_engine_shortcuts.ssgi_filter", "MOD_SUBSURF", "ssgi")
		draw_toggle_button(self, "game_engine_shortcuts.bloom_filter", "LAMP_SUN", "bloom")
		draw_toggle_button(self, "game_engine_shortcuts.bleach_filter", "PROP_OFF", "bleach")
		draw_toggle_button(self, "game_engine_shortcuts.vignette_filter", "BBOX", "vignette")
		draw_toggle_button(self, "game_engine_shortcuts.retinex_filter", "SEQ_HISTOGRAM", "retinex")
		draw_toggle_button(self, "game_engine_shortcuts.chromatic_filter", "FORCE_FORCE", "chromatic")
		draw_toggle_button(self, "game_engine_shortcuts.desaturate_filter", "MESH_CUBE", "desaturate")
		draw_toggle_button(self, "game_engine_shortcuts.warm_sepia_filter", "MARKER_HLT", "warm_sepia")
		draw_toggle_button(self, "game_engine_shortcuts.technicolor_1_filter", "COLOR_RED", "technicolor_1")
		draw_toggle_button(self, "game_engine_shortcuts.technicolor_2_filter", "COLOR_BLUE", "technicolor_2")
		draw_toggle_button(self, "game_engine_shortcuts.movie_noise_filter", "CLIP", "movie_noise")
		draw_toggle_button(self, "game_engine_shortcuts.pixelate_filter", "MOD_BUILD", "pixelate")
		draw_toggle_button(self, "game_engine_shortcuts.edge_detect_filter", "VIEW3D_VEC", "edge_detect")
		draw_toggle_button(self, "game_engine_shortcuts.harsh_colors_filter", "SEQ_CHROMA_SCOPE", "harsh_colors")
		draw_toggle_button(self, "game_engine_shortcuts.depth_filter", "MOD_ARRAY", "depth")



class FlyCameraOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "game_engine_shortcuts.fly_camera_operator"
	bl_label = "Fly Camera"
	bl_description = "Creates a fly camera for moving around the world"

	@classmethod
	def poll(cls, context):
		return True
		#return context.active_object is not None

	def execute(self, context):

		from game_engine_shortcuts.scripts import fly_camera

		
		# Add the camera
		bpy.ops.object.camera_add()
		camera = bpy.context.active_object
		camera.name = 'shortcuts_camera'

		# Set the cameras rotation to something useable
		camera.rotation_euler = [math.radians(90),0,0]

		# Text block for the script
		if 'fly_camera.py' in bpy.data.texts:
			text = bpy.data.texts['fly_camera.py']
		else:
			bpy.ops.text.new()
			text = bpy.data.texts[-1]
			text.name = 'fly_camera.py'

			text.from_string(fly_camera.script)
		
		# Add an 'always' sensor
		bpy.ops.logic.sensor_add(type='ALWAYS', object=camera.name)
		sensor = camera.game.sensors[-1]
		sensor.use_pulse_true_level = True
		sensor.show_expanded = False
		
		# Add a python controller to hold the scripts
		bpy.ops.logic.controller_add(type='PYTHON', object=camera.name)        
		cont = camera.game.controllers[-1]
		cont.name = 'fly_camera'
		cont.mode = 'MODULE'
		cont.module = 'fly_camera.main'
		cont.show_expanded = False
		cont.link(sensor)

		return {'FINISHED'}


class OrbitCameraOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "game_engine_shortcuts.orbit_camera_operator"
	bl_label = "Orbit Camera"
	bl_description = "Creates an orbit camera for rotating around an object"

	@classmethod
	def poll(cls, context):
		return True
		#return context.active_object is not None

	def execute(self, context):
		return {'FINISHED'}


class FirstPersonRigOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "game_engine_shortcuts.first_person_rig"
	bl_label = "First Person Rig"
	bl_description = "A simple First Person rig that allows you to move around the world"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):
		from game_engine_shortcuts.scripts import fps_rig

		# Create the parent
		bpy.ops.object.select_all(action='DESELECT')
		bpy.ops.mesh.primitive_cube_add(view_align=False, enter_editmode=False, location=(0, 0, 0))
		bpy.context.object.name = "shortcuts_fps_rig"
		bpy.ops.object.editmode_toggle()
		bpy.context.space_data.transform_manipulators = {'TRANSLATE', 'SCALE'}
		bpy.ops.transform.resize(value=(0.323522, 0.323522, 0.323522), constraint_axis=(True, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, release_confirm=True)
		bpy.ops.object.editmode_toggle()
		bpy.context.object.dimensions[2] = 2
		bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
		bpy.context.object.game.physics_type = 'DYNAMIC'
		bpy.context.object.game.use_collision_bounds = True
		bpy.context.object.game.collision_bounds_type = 'CAPSULE'
		bpy.context.object.hide_render = True
		bpy.context.object.draw_type = 'WIRE'



		holder = bpy.context.selected_objects[0]


		# Add the camera
		bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=(0, 0, 0), rotation=(1.1088, 1.34398e-07, -1.036))
		bpy.ops.object.rotation_clear()
		bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
		bpy.ops.transform.translate(value=(0, 0, 0.8), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, release_confirm=True)
		bpy.context.object.name = "shortcuts_fps_camera"

		camera = bpy.context.selected_objects[0]

		bpy.ops.object.select_all(action='DESELECT')

		# Make sure the camera is a child of the holder
		camera.parent = holder

		# Move everything to the 3d cursor
		holder.location = bpy.context.scene.cursor_location

		# Add the first person walking script


		# Text block for the script
		if 'fps_rig.py' in bpy.data.texts:
			text = bpy.data.texts['fps_rig.py']
		else:
			bpy.ops.text.new()
			text = bpy.data.texts[-1]
			text.name = 'fps_rig.py'

			text.from_string(fps_rig.script)
		
		# Add an 'always' sensor
		bpy.ops.logic.sensor_add(type='ALWAYS', object=holder.name)
		sensor = holder.game.sensors[-1]
		sensor.use_pulse_true_level = True
		sensor.show_expanded = False
		
		# Add a python controller to hold the scripts
		bpy.ops.logic.controller_add(type='PYTHON', object=holder.name)        
		cont = holder.game.controllers[-1]
		cont.name = 'fps_rig'
		cont.mode = 'MODULE'
		cont.module = 'fps_rig.main'
		cont.show_expanded = False
		cont.link(sensor)		


		return {'FINISHED'}


class ThirdPersonRigOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "game_engine_shortcuts.third_person_rig"
	bl_label = "Third Person Rig"
	bl_description = "A simple First Person rig that allows you to move around the world"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):
		return {'FINISHED'}


class DOFFilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "game_engine_shortcuts.dof_filter"
	bl_label = "Depth of Field"
	bl_description = "Adds a simple depth of field filter to the world"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):

		from game_engine_shortcuts.scripts.filters import fast_dof

		add_filter(context, fast_dof, 'fast_dof.glsl', 'dof', 10)

		return {'FINISHED'}


class SSAOFilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "game_engine_shortcuts.ssao_filter"
	bl_label = "SSAO"
	bl_description = "Adds a simple Screen Space Ambient Occlusion filter to the world"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):

		from game_engine_shortcuts.scripts.filters import ssao

		add_filter(context, ssao, 'ssao.glsl', 'ssao', 1)


		return {'FINISHED'}


class BloomFilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "game_engine_shortcuts.bloom_filter"
	bl_label = "Bloom"
	bl_description = "Adds a simple Bloom filter to the world"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):

		from game_engine_shortcuts.scripts.filters import bloom

		add_filter(context, bloom, 'bloom.glsl', 'bloom', 2)


		return {'FINISHED'}


class BleachFilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "game_engine_shortcuts.bleach_filter"
	bl_label = "Bleach"
	bl_description = "Adds a simple Bloom filter to the world"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):

		from game_engine_shortcuts.scripts.filters import bleach

		add_filter(context, bleach, 'bleach.glsl', 'bleach', 3)
		return {'FINISHED'}

class VignetteFilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "game_engine_shortcuts.vignette_filter"
	bl_label = "Vignette"
	bl_description = "Adds a simple Vignette filter to the world"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):

		from game_engine_shortcuts.scripts.filters import vignette

		add_filter(context, vignette, 'vignette.glsl', 'vignette', 20)

		return {'FINISHED'}


class RetinexFilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "game_engine_shortcuts.retinex_filter"
	bl_label = "Retinex"
	bl_description = "Adds a simple Retinex filter to the world"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):

		from game_engine_shortcuts.scripts.filters import retinex

		add_filter(context, retinex, 'retinex.glsl', 'retinex', 9)

		return {'FINISHED'}


class ChromaticFilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "game_engine_shortcuts.chromatic_filter"
	bl_label = "Chromatic Aberration"
	bl_description = "Adds a simple Chromatic Aberration filter to the world"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):

		from game_engine_shortcuts.scripts.filters import chromatic

		add_filter(context, chromatic, 'chromatic.glsl', 'chromatic', 8)

		return {'FINISHED'}


class DesaturateFilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "game_engine_shortcuts.desaturate_filter"
	bl_label = "Desaturate"
	bl_description = "Adds a simple Desaturate filter to the world"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):

		from game_engine_shortcuts.scripts.filters import desaturate

		add_filter(context, desaturate, 'desaturate.glsl', 'desaturate', 7)

		return {'FINISHED'}


class WarmSepiaFilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "game_engine_shortcuts.warm_sepia_filter"
	bl_label = "Warm Sepia"
	bl_description = "Adds a simple Desaturate filter to the world"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):

		from game_engine_shortcuts.scripts.filters import warm_sepia

		add_filter(context, warm_sepia, 'warm_sepia.glsl', 'warm_sepia', 6)

		return {'FINISHED'}


class Technicolor1FilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "game_engine_shortcuts.technicolor_1_filter"
	bl_label = "Technicolor 1"
	bl_description = "Adds a simple Technicolor 1 filter to the world"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):

		from game_engine_shortcuts.scripts.filters import technicolor_1

		add_filter(context, technicolor_1, 'technicolor_1.glsl', 'technicolor_1', 5)

		return {'FINISHED'}


class Technicolor2FilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "game_engine_shortcuts.technicolor_2_filter"
	bl_label = "Technicolor 2"
	bl_description = "Adds a simple Technicolor 2 filter to the world"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):

		from game_engine_shortcuts.scripts.filters import technicolor_2

		add_filter(context, technicolor_2, 'technicolor_2.glsl', 'technicolor_2', 4)

		return {'FINISHED'}


class SSGIFilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "game_engine_shortcuts.ssgi_filter"
	bl_label = "SSGI"
	bl_description = "Adds a simple Desaturate filter to the world"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):

		from game_engine_shortcuts.scripts.filters import ssgi

		add_filter(context, ssgi, 'ssgi.glsl', 'ssgi', 3)

		return {'FINISHED'}


class MovieNoiseFilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "game_engine_shortcuts.movie_noise_filter"
	bl_label = "Movie Noise"
	bl_description = "Adds a simple noise to the world that simulates movie noise"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):
		from game_engine_shortcuts.scripts.filters import movie_noise

		add_filter(context, movie_noise, 'movie_noise.glsl', 'movie_noise', 12)
		return {'FINISHED'}


class PixelateFilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "game_engine_shortcuts.pixelate_filter"
	bl_label = "Pixelate"
	bl_description = "Adds a simple pixelate to the world"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):
		from game_engine_shortcuts.scripts.filters import pixelate

		add_filter(context, pixelate, 'pixelate.glsl', 'pixelate', 12)
		return {'FINISHED'}


class EdgeDetectFilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "game_engine_shortcuts.edge_detect_filter"
	bl_label = "Edge Detect"
	bl_description = "Adds a simple edge detect to the world"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):
		from game_engine_shortcuts.scripts.filters import edge_detect

		add_filter(context, edge_detect, 'edge_detect.glsl', 'edge_detect', 12)
		return {'FINISHED'}

class HarshColorsFilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "game_engine_shortcuts.harsh_colors_filter"
	bl_label = "Harsh Colors"
	bl_description = "Makes all the colours very harsh"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):
		from game_engine_shortcuts.scripts.filters import harsh_colors

		add_filter(context, harsh_colors, 'harsh_colors.glsl', 'harsh_colors', 12)
		return {'FINISHED'}

class DepthFilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "game_engine_shortcuts.depth_filter"
	bl_label = "Depth"
	bl_description = "Depth filter"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):
		from game_engine_shortcuts.scripts.filters import depth

		add_filter(context, depth, 'depth.glsl', 'depth', 12)
		return {'FINISHED'}


def register():
	bpy.utils.register_module(__name__)

def unregister():
	bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
	register()
