#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.compute_grasp_ariac_state import ComputeGraspAriacState
from ariac_flexbe_states.detect_part_camera_ariac_state import DetectPartCameraAriacState
from ariac_flexbe_states.lookup_from_table import LookupFromTableState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_logistics_flexbe_states.get_material_locations import GetMaterialLocationsState
from ariac_support_flexbe_states.get_item_from_list_state import GetItemFromListState
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

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:607 y:471, x:644 y:258
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.kitting_part = ''
		_state_machine.userdata.location_type = ''
		_state_machine.userdata.material_locations = []
		_state_machine.userdata.first = 0
		_state_machine.userdata.parameter_name = 'ariac_tables_unit1'
		_state_machine.userdata.table_name = 'unit1_table'
		_state_machine.userdata.index_title = 'bin'
		_state_machine.userdata.camera_topic = ''
		_state_machine.userdata.camera_frame = ''
		_state_machine.userdata.robot_pregrasp = ''
		_state_machine.userdata.ref_frame = 'world'
		_state_machine.userdata.move_group = 'manipulator'
		_state_machine.userdata.namespace = '/ariac/kitting'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = 'kitting'
		_state_machine.userdata.joint_values = []
		_state_machine.userdata.joint_names = []
		_state_machine.userdata.tool_link = 'ee_link'
		_state_machine.userdata.offset = 0.0
		_state_machine.userdata.rotation = 0.0

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

			# x:1165 y:38
			OperatableStateMachine.add('detect part with camera',
										DetectPartCameraAriacState(time_out=0.1),
										transitions={'continue': 'pre move to part', 'failed': 'failed', 'not_found': 'failed'},
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
										LookupFromTableState(parameter_name=parameter_name, table_name=table_name, index_title=index_title, column_title='camera_frame'),
										transitions={'found': 'lookup pre grasp', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'camera_frame'})

			# x:565 y:40
			OperatableStateMachine.add('lookup camera topic',
										LookupFromTableState(parameter_name=parameter_name, table_name=table_name, index_title=index_title, column_title='camera_topic'),
										transitions={'found': 'lookup camera  frame', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'camera_topic'})

			# x:938 y:41
			OperatableStateMachine.add('lookup pre grasp',
										LookupFromTableState(parameter_name=parameter_name, table_name=table_name, index_title=index_title, column_title='robot_config'),
										transitions={'found': 'detect part with camera', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'robot_pregrasp'})

			# x:1174 y:311
			OperatableStateMachine.add('move to bin',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'compute pick', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'namespace': 'namespace', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1176 y:155
			OperatableStateMachine.add('pre move to part',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'move to bin', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'robot_pregrasp', 'move_group': 'move_group', 'namespace': 'namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1178 y:448
			OperatableStateMachine.add('compute pick',
										ComputeGraspAriacState(joint_names=['linear_arm_actuator_joint', 'base_link', 'shoulder_link', 'upper_arm_link', 'forearm_link', 'wrist_1_link', 'wrist_2_link', 'wrist_3_link', 'ee_link']),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group', 'namespace': 'namespace', 'tool_link': 'tool_link', 'pose': 'part_pose', 'offset': 'offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
