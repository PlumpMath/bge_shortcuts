import os
import ntpath
import math

import bpy

class FlyCameraOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.fly_camera_operator"
	bl_label = "Fly Camera"
	bl_description = "Adds a Fly Camera at the 3D cursor"

	@classmethod
	def poll(cls, context):
		return True
		#return context.active_object is not None

	def execute(self, context):

		script_name = 'fly_camera.py'
		
		# Add the camera
		bpy.ops.object.camera_add()
		camera = bpy.context.active_object
		camera.name = 'shortcuts_camera'

		# Set the cameras rotation to something useable
		camera.rotation_euler = [math.radians(90),0,0]

		# Text block for the script
		if script_name in bpy.data.texts:
			text = bpy.data.texts[script_name]
		else:
			bpy.ops.text.new()
			text = bpy.data.texts[-1]
			text.name = script_name

			script_location = os.path.join(ntpath.dirname(__file__), 'templates/scripts/' + script_name)
			script_file = open(script_location, 'r')
			text.from_string(script_file.read())

			#text.from_string(fly_camera.script)
		
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


class FirstPersonRigOperator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.first_person_rig"
	bl_label = "First Person Rig"
	bl_description = "A simple First Person rig that allows you to move around the world"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):

		script_name = 'fps_rig.py'

		bpy.context.scene.game_settings.frame_type = 'EXTEND'


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
		if script_name in bpy.data.texts:
			text = bpy.data.texts[script_name]
		else:
			bpy.ops.text.new()
			text = bpy.data.texts[-1]
			text.name = script_name

			script_location = os.path.join(ntpath.dirname(__file__), 'templates/scripts/' + script_name)
			script_file = open(script_location, 'r')
			text.from_string(script_file.read())

		
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
	bl_idname = "bge_shortcuts.third_person_rig"
	bl_label = "Third Person Rig"
	bl_description = "Adds a simple third person controller at the 3D cursor"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):
		
		script_name = 'third_person_rig.py'

		bpy.context.scene.game_settings.frame_type = 'EXTEND'


		# Create the parent
		bpy.ops.object.select_all(action='DESELECT')
		bpy.ops.mesh.primitive_cube_add(view_align=False, enter_editmode=False, location=(0, 0, 0))
		bpy.context.object.name = "shortcuts_third_person_rig"
		bpy.ops.object.editmode_toggle()
		bpy.context.space_data.transform_manipulators = {'TRANSLATE', 'SCALE'}
		bpy.ops.transform.resize(value=(0.323522, 0.323522, 0.323522), constraint_axis=(True, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, release_confirm=True)
		bpy.ops.object.editmode_toggle()
		bpy.context.object.dimensions[2] = 2
		bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
		bpy.context.object.game.physics_type = 'DYNAMIC'
		bpy.context.object.game.use_collision_bounds = True
		bpy.context.object.game.collision_bounds_type = 'CAPSULE'

		holder = bpy.context.selected_objects[0]

		
		# Create the camera parent
		bpy.ops.object.select_all(action='DESELECT')
		bpy.ops.mesh.primitive_cube_add(view_align=False, enter_editmode=False, location=(0, 0, 0))
		bpy.context.object.name = "shortcuts_third_person_camera_parent"
		bpy.context.space_data.transform_manipulators = {'TRANSLATE', 'SCALE'}
		bpy.ops.object.editmode_toggle()
		bpy.ops.transform.resize(value=(0.257732, 0.257732, 0.257732), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
		bpy.ops.object.editmode_toggle()
		bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
		bpy.context.object.game.physics_type = 'NO_COLLISION'
		bpy.context.object.hide_render = True
		bpy.context.object.draw_type = 'WIRE'

		camera_parent = bpy.context.selected_objects[0]
		camera_parent.parent = holder



		# Add the camera
		bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=(0, 0, 0), rotation=(0.0, 0.0, 0.0))
		bpy.context.object.use_slow_parent = True
		#bpy.context.object.slow_parent_offset = 5.0
		bpy.ops.object.rotation_clear()
		bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
		bpy.ops.transform.rotate(value=-math.pi/8, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
		bpy.ops.transform.translate(value=(0, -4.5, 2.0), constraint_axis=(False, True, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, release_confirm=True)
		bpy.context.object.data.lens = 28.0

		bpy.context.object.name = "shortcuts_third_person_camera"

		camera = bpy.context.selected_objects[0]

		bpy.ops.object.select_all(action='DESELECT')

		# Make sure the camera is a child of the holder
		camera.parent = camera_parent

		# Move everything to the 3d cursor
		holder.location = bpy.context.scene.cursor_location

		# Add the first person walking script
		if script_name in bpy.data.texts:
			text = bpy.data.texts[script_name]
		else:
			bpy.ops.text.new()
			text = bpy.data.texts[-1]
			text.name = script_name

			script_location = os.path.join(ntpath.dirname(__file__), 'templates/scripts/' + script_name)
			script_file = open(script_location, 'r')
			text.from_string(script_file.read())
		
		# Add an 'always' sensor
		bpy.ops.logic.sensor_add(type='ALWAYS', object=holder.name)
		sensor = holder.game.sensors[-1]
		sensor.use_pulse_true_level = True
		sensor.show_expanded = False
		
		# Add a python controller to hold the scripts
		bpy.ops.logic.controller_add(type='PYTHON', object=holder.name)        
		cont = holder.game.controllers[-1]
		cont.name = 'third_person_rig'
		cont.mode = 'MODULE'
		cont.module = 'third_person_rig.main'
		cont.show_expanded = False
		cont.link(sensor)		


		return {'FINISHED'}