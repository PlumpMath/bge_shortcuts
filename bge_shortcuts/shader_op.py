#----------------------------------------------------------
# File shader_op.py
#----------------------------------------------------------
from string import Template
import os
import ntpath
 
import bpy
from bpy.props import *

from .shader_settings import ShaderSettings


'''
 _  _  ____   __   __     __   ____   __   ____  ____ 
/ )( \(_  _) (  ) (  )   (  ) (_  _) (  ) (  __)/ ___)
) \/ (  )(    )(  / (_/\  )(    )(    )(   ) _) \___ \
\____/ (__)  (__) \____/ (__)  (__)  (__) (____)(____/
'''

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

def add_filter(context, script_name, filter_name, pass_index, options):


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

	update_shader(options, context, script_name)

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



def shader_props(cls):

	return [attr for attr in dir(cls) if not callable(attr) and not attr.startswith("__") and attr.startswith("shader")]

def set_shader_properties(cls, context):

	settings = context.scene.glsl_shader_settings
	properties = shader_props(cls)

	for prop in properties:
		value = getattr(cls, prop)
		setattr(settings,prop,value)

def prepare_shader_properties(cls, context):

	settings = context.scene.glsl_shader_settings
	properties = shader_props(cls)

	for prop in properties:
		value = getattr(settings, prop)
		setattr(cls,prop,value)



def update_shader(cls, context, shader_name):

	settings = context.scene.glsl_shader_settings
	dict = {}

	properties = shader_props(cls)
	for prop in properties:

		value = getattr(settings, prop)
		print(value)

		# GLSL needs lower case booleans
		if value == True:
			value = 'true'
		if value == False:
			value = 'false'

		dict[prop] = value

	shader_location = os.path.join(ntpath.dirname(__file__), 'templates/shaders/' + shader_name)
	shader_file = open(shader_location, 'r')
	text = shader_file.read()

	template = Template(text)
	shader = template.substitute(**dict)

	text_block = bpy.data.texts[shader_name]
	text_block.from_string(shader)

	return



'''
  __   ____  ____  ____   __   ____   __   ____  ____ 
 /  \ (  _ \(  __)(  _ \ / _\ (_  _) /  \ (  _ \/ ___)
(  O ) ) __/ ) _)  )   //    \  )(  (  O ) )   /\___ \
 \__/ (__)  (____)(__\_)\_/\_/ (__)  \__/ (__\_)(____/
 '''


# ---------------------------------------------------------------
# Depth of Field
# ---------------------------------------------------------------
class DOFFilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.dof_filter"
	bl_label = "Depth of Field"
	bl_description = "Adds a simple " + bl_label + " filter"


	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):

		options = DOFFilterOptionsOperator
		add_filter(context, 'fast_dof.glsl', 'dof', 10, options)

		return {'FINISHED'}


class DOFFilterOptionsOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.dof_filter_options"
	bl_label = "Depth of Field"
	bl_description = "Options for the " + bl_label + " Shader"

	shader_dof_blur_clamp = ShaderSettings.shader_dof_blur_clamp	
	shader_dof_bias = ShaderSettings.shader_dof_bias
	shader_dof_kernel_size = ShaderSettings.shader_dof_kernel_size
 
	def execute(self, context):
		set_shader_properties(self, context)
		update_shader(self, context, 'fast_dof.glsl')

		return {'FINISHED'}
 
	def invoke(self, context, event):
		prepare_shader_properties(self, context)
		return context.window_manager.invoke_props_dialog(self)


# ---------------------------------------------------------------
# Screen Space Ambient Occlusion
# ---------------------------------------------------------------
class SSAOFilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.ssao_filter"
	bl_label = "SSAO"
	bl_description = "Adds a simple " + bl_label + " filter"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):

		options = SSAOFilterOptionsOperator
		add_filter(context, 'ssao.glsl', 'ssao', 1, options)
		return {'FINISHED'}


class SSAOFilterOptionsOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.ssao_filter_options"
	bl_label = "SSAO"
	bl_description = "Options for the " + bl_label + " Shader"

	shader_ssao_samples = ShaderSettings.shader_ssao_samples
	shader_ssao_radius = ShaderSettings.shader_ssao_radius

	shader_ssao_diffarea = ShaderSettings.shader_ssao_diffarea
	shader_ssao_gdisplace = ShaderSettings.shader_ssao_gdisplace

	shader_ssao_lum_influence = ShaderSettings.shader_ssao_lum_influence

	shader_ssao_znear = ShaderSettings.shader_ssao_znear
	shader_ssao_zfar = ShaderSettings.shader_ssao_zfar

	shader_ssao_only_ao = ShaderSettings.shader_ssao_only_ao


	def execute(self, context):
		set_shader_properties(self, context)
		update_shader(self, context, 'ssao.glsl')

		return {'FINISHED'}
 
	def invoke(self, context, event):
		prepare_shader_properties(self, context)
		return context.window_manager.invoke_props_dialog(self)


# ---------------------------------------------------------------
# Screen Space Global Illumination
# ---------------------------------------------------------------
class SSGIFilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.ssgi_filter"
	bl_label = "SSGI"
	bl_description = "Adds a simple " + bl_label + " filter"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):

		options = SSGIFilterOptionsOperator
		add_filter(context, 'ssgi.glsl', 'ssgi', 3, options)
		return {'FINISHED'}


class SSGIFilterOptionsOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.ssgi_filter_options"
	bl_label = "SSGI"
	bl_description = "Options for the " + bl_label + " Shader"

	shader_ssgi_samples = ShaderSettings.shader_ssgi_samples
	shader_ssgi_radius = ShaderSettings.shader_ssgi_radius

	def execute(self, context):
		set_shader_properties(self, context)
		update_shader(self, context, 'ssgi.glsl')

		return {'FINISHED'}
 
	def invoke(self, context, event):
		prepare_shader_properties(self, context)
		return context.window_manager.invoke_props_dialog(self)



# ---------------------------------------------------------------
# Bloom
# ---------------------------------------------------------------
class BloomFilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.bloom_filter"
	bl_label = "Bloom"
	bl_description = "Adds a simple " + bl_label + " filter"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):

		options = BloomFilterOptionsOperator
		add_filter(context, 'bloom.glsl', 'bloom', 4, options)
		return {'FINISHED'}


class BloomFilterOptionsOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.bloom_filter_options"
	bl_label = "Bloom"
	bl_description = "Options for the " + bl_label + " Shader"

	shader_bloom_strength = ShaderSettings.shader_bloom_strength
	shader_bloom_width = ShaderSettings.shader_bloom_width
	shader_bloom_shape = ShaderSettings.shader_bloom_shape

	def execute(self, context):
		set_shader_properties(self, context)
		update_shader(self, context, 'bloom.glsl')

		return {'FINISHED'}
 
	def invoke(self, context, event):
		prepare_shader_properties(self, context)
		return context.window_manager.invoke_props_dialog(self)


# ---------------------------------------------------------------
# Bleach
# ---------------------------------------------------------------
class BleachFilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.bleach_filter"
	bl_label = "Bleach"
	bl_description = "Adds a simple " + bl_label + " filter"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):

		options = BleachFilterOptionsOperator
		add_filter(context, 'bleach.glsl', 'bleach', 5, options)
		return {'FINISHED'}


class BleachFilterOptionsOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.bleach_filter_options"
	bl_label = "Bleach"
	bl_description = "Options for the " + bl_label + " Shader"

	shader_bleach_strength = ShaderSettings.shader_bleach_strength

	def execute(self, context):
		set_shader_properties(self, context)
		update_shader(self, context, 'bleach.glsl')

		return {'FINISHED'}
 
	def invoke(self, context, event):
		prepare_shader_properties(self, context)
		return context.window_manager.invoke_props_dialog(self)

# ---------------------------------------------------------------
# Vignette
# ---------------------------------------------------------------
class VignetteFilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.vignette_filter"
	bl_label = "Vignette"
	bl_description = "Adds a simple " + bl_label + " filter"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):

		options = VignetteFilterOptionsOperator
		add_filter(context, 'vignette.glsl', 'vignette', 5, options)
		return {'FINISHED'}


class VignetteFilterOptionsOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.vignette_filter_options"
	bl_label = "Vignette"
	bl_description = "Options for the " + bl_label + " Shader"

	shader_vignette_size = ShaderSettings.shader_vignette_size
	shader_vignette_tolerance = ShaderSettings.shader_vignette_tolerance

	def execute(self, context):
		set_shader_properties(self, context)
		update_shader(self, context, 'vignette.glsl')

		return {'FINISHED'}
 
	def invoke(self, context, event):
		prepare_shader_properties(self, context)
		return context.window_manager.invoke_props_dialog(self)


# ---------------------------------------------------------------
# Retinex
# ---------------------------------------------------------------
class RetinexFilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.retinex_filter"
	bl_label = "Retinex"
	bl_description = "Adds a simple " + bl_label + " filter"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):

		options = RetinexFilterOptionsOperator
		add_filter(context, 'retinex.glsl', 'retinex', 5, options)
		return {'FINISHED'}


class RetinexFilterOptionsOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.retinex_filter_options"
	bl_label = "Retinex"
	bl_description = "Options for the " + bl_label + " Shader"

	shader_retinex_strength = ShaderSettings.shader_retinex_strength

	def execute(self, context):
		set_shader_properties(self, context)
		update_shader(self, context, 'retinex.glsl')

		return {'FINISHED'}
 
	def invoke(self, context, event):
		prepare_shader_properties(self, context)
		return context.window_manager.invoke_props_dialog(self)

# ---------------------------------------------------------------
# Chromatic Aberration
# ---------------------------------------------------------------
class ChromaticFilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.chromatic_filter"
	bl_label = "Chromatic"
	bl_description = "Adds a simple " + bl_label + " filter"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):

		options = ChromaticFilterOptionsOperator
		add_filter(context, 'chromatic.glsl', 'chromatic', 5, options)
		return {'FINISHED'}


class ChromaticFilterOptionsOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.chromatic_filter_options"
	bl_label = "Chromatic"
	bl_description = "Options for the " + bl_label + " Shader"

	shader_chromatic_strength = ShaderSettings.shader_chromatic_strength

	def execute(self, context):
		set_shader_properties(self, context)
		update_shader(self, context, 'chromatic.glsl')

		return {'FINISHED'}
 
	def invoke(self, context, event):
		prepare_shader_properties(self, context)
		return context.window_manager.invoke_props_dialog(self)


# ---------------------------------------------------------------
# Saturate
# ---------------------------------------------------------------
class SaturateFilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.saturate_filter"
	bl_label = "Saturate"
	bl_description = "Adds a simple " + bl_label + " filter"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):

		options = SaturateFilterOptionsOperator
		add_filter(context, 'saturate.glsl', 'saturate', 5, options)
		return {'FINISHED'}


class SaturateFilterOptionsOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.saturate_filter_options"
	bl_label = "Saturate"
	bl_description = "Options for the " + bl_label + " Shader"

	shader_saturate_strength = ShaderSettings.shader_saturate_strength

	def execute(self, context):
		set_shader_properties(self, context)
		update_shader(self, context, 'saturate.glsl')

		return {'FINISHED'}
 
	def invoke(self, context, event):
		prepare_shader_properties(self, context)
		return context.window_manager.invoke_props_dialog(self)


# ---------------------------------------------------------------
# Warm Sepia
# ---------------------------------------------------------------
class WarmSepiaFilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.warm_sepia_filter"
	bl_label = "WarmSepia"
	bl_description = "Adds a simple " + bl_label + " filter"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):

		options = WarmSepiaFilterOptionsOperator
		add_filter(context, 'warm_sepia.glsl', 'warm_sepia', 5, options)
		return {'FINISHED'}


class WarmSepiaFilterOptionsOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.warm_sepia_filter_options"
	bl_label = "WarmSepia"
	bl_description = "Options for the " + bl_label + " Shader"

	shader_warm_sepia_strength = ShaderSettings.shader_warm_sepia_strength

	def execute(self, context):
		set_shader_properties(self, context)
		update_shader(self, context, 'warm_sepia.glsl')

		return {'FINISHED'}
 
	def invoke(self, context, event):
		prepare_shader_properties(self, context)
		return context.window_manager.invoke_props_dialog(self)

# ---------------------------------------------------------------
# Technicolor 1
# ---------------------------------------------------------------
class Technicolor1FilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.technicolor_1_filter"
	bl_label = "Technicolor1"
	bl_description = "Adds a simple " + bl_label + " filter"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):

		options = Technicolor1FilterOptionsOperator
		add_filter(context, 'technicolor_1.glsl', 'technicolor_1', 5, options)
		return {'FINISHED'}


class Technicolor1FilterOptionsOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.technicolor_1_filter_options"
	bl_label = "Technicolor1"
	bl_description = "Options for the " + bl_label + " Shader"

	shader_technicolor_1_strength = ShaderSettings.shader_technicolor_1_strength

	def execute(self, context):
		set_shader_properties(self, context)
		update_shader(self, context, 'technicolor_1.glsl')

		return {'FINISHED'}
 
	def invoke(self, context, event):
		prepare_shader_properties(self, context)
		return context.window_manager.invoke_props_dialog(self)

# ---------------------------------------------------------------
# Technicolor 2
# ---------------------------------------------------------------
class Technicolor2FilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.technicolor_2_filter"
	bl_label = "Technicolor2"
	bl_description = "Adds a simple " + bl_label + " filter"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):

		options = Technicolor2FilterOptionsOperator
		add_filter(context, 'technicolor_2.glsl', 'technicolor_2', 5, options)
		return {'FINISHED'}


class Technicolor2FilterOptionsOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.technicolor_2_filter_options"
	bl_label = "Technicolor2"
	bl_description = "Options for the " + bl_label + " Shader"

	shader_technicolor_2_strength = ShaderSettings.shader_technicolor_2_strength

	def execute(self, context):
		set_shader_properties(self, context)
		update_shader(self, context, 'technicolor_2.glsl')

		return {'FINISHED'}
 
	def invoke(self, context, event):
		prepare_shader_properties(self, context)
		return context.window_manager.invoke_props_dialog(self)


# ---------------------------------------------------------------
# Movie Noise
# ---------------------------------------------------------------
class MovieNoiseFilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.movie_noise_filter"
	bl_label = "MovieNoise"
	bl_description = "Adds a simple " + bl_label + " filter"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):

		options = MovieNoiseFilterOptionsOperator
		add_filter(context, 'movie_noise.glsl', 'movie_noise', 5, options)
		return {'FINISHED'}


class MovieNoiseFilterOptionsOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.movie_noise_filter_options"
	bl_label = "MovieNoise"
	bl_description = "Options for the " + bl_label + " Shader"

	shader_movie_noise_strength = ShaderSettings.shader_movie_noise_strength

	def execute(self, context):
		set_shader_properties(self, context)
		update_shader(self, context, 'movie_noise.glsl')

		return {'FINISHED'}
 
	def invoke(self, context, event):
		prepare_shader_properties(self, context)
		return context.window_manager.invoke_props_dialog(self)


# ---------------------------------------------------------------
# Pixelate
# ---------------------------------------------------------------
class PixelateFilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.pixelate_filter"
	bl_label = "Pixelate"
	bl_description = "Adds a simple " + bl_label + " filter"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):

		options = PixelateFilterOptionsOperator
		add_filter(context, 'pixelate.glsl', 'pixelate', 5, options)
		return {'FINISHED'}


class PixelateFilterOptionsOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.pixelate_filter_options"
	bl_label = "Pixelate"
	bl_description = "Options for the " + bl_label + " Shader"

	shader_pixelate_cellw = ShaderSettings.shader_pixelate_cellw
	shader_pixelate_cellh = ShaderSettings.shader_pixelate_cellh

	def execute(self, context):
		set_shader_properties(self, context)
		update_shader(self, context, 'pixelate.glsl')

		return {'FINISHED'}
 
	def invoke(self, context, event):
		prepare_shader_properties(self, context)
		return context.window_manager.invoke_props_dialog(self)


# ---------------------------------------------------------------
# Edge Detect
# ---------------------------------------------------------------
class EdgeDetectFilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.edge_detect_filter"
	bl_label = "EdgeDetect"
	bl_description = "Adds a simple " + bl_label + " filter"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):

		options = EdgeDetectFilterOptionsOperator
		add_filter(context, 'edge_detect.glsl', 'edge_detect', 5, options)
		return {'FINISHED'}


class EdgeDetectFilterOptionsOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.edge_detect_filter_options"
	bl_label = "EdgeDetect"
	bl_description = "Options for the " + bl_label + " Shader"

	shader_edge_detect_thickness = ShaderSettings.shader_edge_detect_thickness
	shader_edge_detect_edge = ShaderSettings.shader_edge_detect_edge

	def execute(self, context):
		set_shader_properties(self, context)
		update_shader(self, context, 'edge_detect.glsl')

		return {'FINISHED'}
 
	def invoke(self, context, event):
		prepare_shader_properties(self, context)
		return context.window_manager.invoke_props_dialog(self)



# ---------------------------------------------------------------
# Harsh Colors
# ---------------------------------------------------------------
class HarshColorsFilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.harsh_colors_filter"
	bl_label = "HarshColors"
	bl_description = "Adds a simple " + bl_label + " filter"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):

		options = HarshColorsFilterOptionsOperator
		add_filter(context, 'harsh_colors.glsl', 'harsh_colors', 5, options)
		return {'FINISHED'}


class HarshColorsFilterOptionsOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.harsh_colors_filter_options"
	bl_label = "HarshColors"
	bl_description = "Options for the " + bl_label + " Shader"


	def execute(self, context):
		set_shader_properties(self, context)
		update_shader(self, context, 'harsh_colors.glsl')

		return {'FINISHED'}
 
	def invoke(self, context, event):
		prepare_shader_properties(self, context)
		return context.window_manager.invoke_props_dialog(self)


# ---------------------------------------------------------------
# Depth
# ---------------------------------------------------------------
class DepthFilterOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.depth_filter"
	bl_label = "Depth"
	bl_description = "Adds a simple " + bl_label + " filter"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):

		options = DepthFilterOptionsOperator
		add_filter(context, 'depth.glsl', 'depth', 5, options)
		return {'FINISHED'}


class DepthFilterOptionsOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.depth_filter_options"
	bl_label = "Depth"
	bl_description = "Options for the " + bl_label + " Shader"


	def execute(self, context):
		set_shader_properties(self, context)
		update_shader(self, context, 'depth.glsl')

		return {'FINISHED'}
 
	def invoke(self, context, event):
		prepare_shader_properties(self, context)
		return context.window_manager.invoke_props_dialog(self)


 
def register():
	bpy.utils.register_module(__name__)


def unregister():
	bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
	pass
	#register()
