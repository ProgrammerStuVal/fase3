#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.detect_part_camera_ariac_state import DetectPartCameraAriacState
from ariac_flexbe_states.lookup_from_table import LookupFromTableState
from ariac_flexbe_states.message_state import MessageState
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_logistics_flexbe_states.get_material_locations import GetMaterialLocationsState
from ariac_support_flexbe_states.get_item_from_list_state import GetItemFromListState
from unit_1_flexbe_behaviors.gripper_correcting_sm import Gripper_correctingSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jun 15 2021
@author: Nick
'''
class unit_1_get_products_from_binSM(Behavior):
	'''
	program for getting the products
	'''


	def __init__(self):
		super(unit_1_get_products_from_binSM, self).__init__()
		self.name = 'unit_1_get_products_from_bin'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Gripper_correctingSM, 'Gripper_correcting')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		gripper_service = '/ariac/kitting/arm/gripper/control'
		gripper_topic = '/ariac/kitting/arm/gripper/state'
		# x:556 y:657, x:644 y:258
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['kitting_part'], output_keys=['part_height'])
		_state_machine.userdata.kitting_part = ''
		_state_machine.userdata.location_type = ''
		_state_machine.userdata.material_locations = []
		_state_machine.userdata.first = 0
		_state_machine.userdata.camera_topic = ''
		_state_machine.userdata.camera_frame = ''
		_state_machine.userdata.robot_pregrasp = ''
		_state_machine.userdata.ref_frame = 'world'
		_state_machine.userdata.move_group = 'kitting_arm'
		_state_machine.userdata.namespace = '/ariac/kitting'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.joint_values = []
		_state_machine.userdata.joint_names = []
		_state_machine.userdata.tool_link = 'ee_link'
		_state_machine.userdata.offset = 0.0
		_state_machine.userdata.rotation = 0.0
		_state_machine.userdata.gripper_service = '/ariac/kitting/arm/gripper/control'
		_state_machine.userdata.gripper_topic = '/ariac/kitting/arm/gripper/state'
		_state_machine.userdata.gripper_enabled = False
		_state_machine.userdata.gripper_attached = False
		_state_machine.userdata.true_var = True
		_state_machine.userdata.kitting_part_pose = []
		_state_machine.userdata.part_height = ''

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('get part location',
										GetMaterialLocationsState(),
										transitions={'continue': 'get bin'},
										autonomy={'continue': Autonomy.Off},
										remapping={'part': 'kitting_part', 'location_type': 'location_type', 'material_locations': 'material_locations'})

			# x:1099 y:22
			OperatableStateMachine.add('debug',
										MessageState(),
										transitions={'continue': 'detect part with camera'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'robot_pregrasp'})

			# x:1246 y:30
			OperatableStateMachine.add('detect part with camera',
										DetectPartCameraAriacState(time_out=0.5),
										transitions={'continue': 'pre move to bin', 'failed': 'failed', 'not_found': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'kitting_part', 'pose': 'part_pose'})

			# x:331 y:43
			OperatableStateMachine.add('get bin',
										GetItemFromListState(),
										transitions={'done': 'lookup camera topic', 'invalid_index': 'failed'},
										autonomy={'done': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'list': 'material_locations', 'index': 'first', 'item': 'bin'})

			# x:749 y:39
			OperatableStateMachine.add('lookup camera  frame',
										LookupFromTableState(parameter_name='ariac_tables_unit1', table_name='unit1_table', index_title='bin', column_title='camera_frame'),
										transitions={'found': 'lookup pre grasp', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'camera_frame'})

			# x:565 y:40
			OperatableStateMachine.add('lookup camera topic',
										LookupFromTableState(parameter_name='ariac_tables_unit1', table_name='unit1_table', index_title='bin', column_title='camera_topic'),
										transitions={'found': 'lookup camera  frame', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'camera_topic'})

			# x:1188 y:407
			OperatableStateMachine.add('lookup part_height',
										LookupFromTableState(parameter_name='ariac_tables_unit1', table_name='part_height_table', index_title='part_type', column_title='part_height'),
										transitions={'found': 'Gripper_correcting', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'kitting_part', 'column_value': 'part_height'})

			# x:938 y:41
			OperatableStateMachine.add('lookup pre grasp',
										LookupFromTableState(parameter_name='ariac_tables_unit1', table_name='unit1_table', index_title='bin', column_title='robot_config'),
										transitions={'found': 'debug', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'robot_pregrasp'})

			# x:1176 y:155
			OperatableStateMachine.add('pre move to bin',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'what part', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'robot_pregrasp', 'move_group': 'move_group', 'namespace': 'namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:932 y:645
			OperatableStateMachine.add('pre move to bin again',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'robot_pregrasp', 'move_group': 'move_group', 'namespace': 'namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1211 y:313
			OperatableStateMachine.add('what part',
										MessageState(),
										transitions={'continue': 'lookup part_height'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'kitting_part'})

			# x:1161 y:515
			OperatableStateMachine.add('Gripper_correcting',
										self.use_behavior(Gripper_correctingSM, 'Gripper_correcting'),
										transitions={'finished': 'pre move to bin again', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'part_pose': 'part_pose', 'part_height': 'part_height', 'move_group': 'move_group', 'namespace': 'namespace', 'tool_link': 'tool_link', 'action_topic': 'action_topic'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
