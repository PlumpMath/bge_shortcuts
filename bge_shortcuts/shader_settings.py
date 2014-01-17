#----------------------------------------------------------
# File shader_settings.py
#----------------------------------------------------------
 
import bpy
from bpy.props import *

from string import Template

# Settings for all the shaders to read from
class ShaderSettings(bpy.types.PropertyGroup):

	# -------------------------
	# DOF
	# -------------------------
	shader_dof_blur_clamp = bpy.props.FloatProperty(default=0.002, name='Blur Clamp', precision=4)
	shader_dof_bias = bpy.props.FloatProperty(default=0.05, name='Bias', min=0.0, max=1.0)
	shader_dof_kernel_size = bpy.props.FloatProperty(default=8.0, name='Kernel Size')

	# -------------------------
	# SSAO
	# -------------------------
	shader_ssao_samples = bpy.props.IntProperty(default=16, name='Samples')
	shader_ssao_radius = bpy.props.FloatProperty(default=3.0, name='Radius')

	shader_ssao_diffarea = bpy.props.FloatProperty(default=0.4, name='Self Shadowing Reduction')
	shader_ssao_gdisplace = bpy.props.FloatProperty(default=0.6, name='Gauss Bell Center')

	shader_ssao_lum_influence = bpy.props.FloatProperty(default=0.5, name='Luminance Influence')
	shader_ssao_only_ao = bpy.props.BoolProperty(default=False, name='Only AO')

	shader_ssao_znear = bpy.props.FloatProperty(default=0.3, name='Z-Near')
	shader_ssao_zfar = bpy.props.FloatProperty(default=100.0, name='Z-Far')


	# -------------------------
	# SSGI
	# -------------------------
	shader_ssgi_samples = bpy.props.IntProperty(default=16, name='Samples')	
	shader_ssgi_radius = bpy.props.FloatProperty(default=0.3, name='Radius')


	# -------------------------	
	# Bloom
	# -------------------------
	shader_bloom_strength = bpy.props.FloatProperty(default=0.8, name='Strength')	
	shader_bloom_shape = bpy.props.IntProperty(default=0, name='Shape', min=0, max=2)	
	shader_bloom_width = bpy.props.FloatProperty(default=3.0, name='Width')

	# -------------------------	
	# Bleach
	# -------------------------
	shader_bleach_strength = bpy.props.FloatProperty(default=1.0, name='Strength')

	# -------------------------	
	# Vignette
	# -------------------------
	shader_vignette_size = bpy.props.FloatProperty(default=0.5, name='Size')
	shader_vignette_tolerance = bpy.props.FloatProperty(default=0.6, name='Tolerance')


	# -------------------------	
	# Retinex
	# -------------------------
	shader_retinex_strength = bpy.props.FloatProperty(default=1.2, name='Strength')


	# -------------------------	
	# Chromatic Aberration
	# -------------------------
	shader_chromatic_strength = bpy.props.FloatProperty(default=1.5, name='Strength')

	# -------------------------	
	# Saturate
	# -------------------------
	shader_saturate_strength = bpy.props.FloatProperty(default=1.0, name='Strength')

	# -------------------------	
	# Warm Sepia
	# -------------------------
	shader_warm_sepia_strength = bpy.props.FloatProperty(default=1.0, name='Strength')


	# -------------------------	
	# Technicolor 1
	# -------------------------
	shader_technicolor_1_strength = bpy.props.FloatProperty(default=1.0, name='Strength')

	# -------------------------	
	# Technicolor 2
	# -------------------------
	shader_technicolor_2_strength = bpy.props.FloatProperty(default=1.0, name='Strength')


	# -------------------------	
	# Movie Noise
	# -------------------------
	shader_movie_noise_strength = bpy.props.FloatProperty(default=0.1, name='Strength')


	# -------------------------	
	# Pixelate
	# -------------------------
	shader_pixelate_cellw = bpy.props.FloatProperty(default=1.0, name='Cell Width')
	shader_pixelate_cellh = bpy.props.FloatProperty(default=1.0, name='Cell Height')

	# -------------------------	
	# Edge Detect
	# -------------------------
	shader_edge_detect_thickness = bpy.props.FloatProperty(default=2.0, name='Thickness')
	shader_edge_detect_edge = bpy.props.FloatProperty(default=3.0, name='Edge Threshold')



# Register the Shader Settings
bpy.utils.register_class(ShaderSettings)
bpy.types.Scene.glsl_shader_settings = bpy.props.PointerProperty(type=ShaderSettings, name='GLSL Shader Settings')


