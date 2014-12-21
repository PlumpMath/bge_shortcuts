import os
import math
import ntpath

import bpy

class TestArea1Operator(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "bge_shortcuts.test_area_1"
	bl_label = "Test Area 1"
	bl_description = "Adds a simple test area for testing in the Game Engine"

	@classmethod
	def poll(cls, context):
		return True
		#return context.active_object is not None

	def execute(self, context):

		if 'bge_shortcuts_floor' not in bpy.data.objects:

			dir = os.path.join(ntpath.dirname(__file__), 'templates/blends/test_area_1.blend/Group/')
			bpy.ops.wm.append(filename="test_area_1",directory=dir)

		else:
			print('Looks like this has already been added. Are you sure you want to add it again?')

		return {'FINISHED'}
