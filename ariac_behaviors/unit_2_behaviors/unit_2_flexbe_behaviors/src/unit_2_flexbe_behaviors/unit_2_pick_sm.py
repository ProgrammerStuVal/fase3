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
from ariac_flexbe_states.detect_part_camera_and_side import DetectPartCameraAndSideAriacState
from ariac_flexbe_states.lookup_from_table import LookupFromTableState
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_logistics_flexbe_states.get_part_from_products_state import GetPartFromProductsState
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_support_flexbe_states.replace_state import ReplaceState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jun 21 2021
@author: Nick
'''
class Unit_2_pickSM(Behavior):
	'''
	picks up parts from agv
	'''


	def __init__(self):
		super(Unit_2_pickSM, self).__init__()
		self.name = 'Unit_2_pick'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:708 y:634, x:686 y:303
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['assembly_products', 'station_id'])
		_state_machine.userdata.ref_frame = 'world'
		_state_machine.userdata.camera_topic = ''
		_state_machine.userdata.camera_frame = ''
		_state_machine.userdata.assembly_part = ''
		_state_machine.userdata.assembly_products = []
		_state_machine.userdata.current_assembly_product = 0
		_state_machine.userdata.station_id = ''
		_state_machine.userdata.offset = []
		_state_machine.userdata.side = False
		_state_machine.userdata.true_value = True
		_state_machine.userdata.tool_link = 'ee_link'
		_state_machine.userdata.rotation = 0.0
		_state_machine.userdata.left_pick = 'as_left_pick'
		_state_machine.userdata.right_pick = 'as_right_pick'
		_state_machine.userdata.move_group = 'gantry_torso'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.namespace = '/ariac/gantry'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.column_title = ''

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:135 y:41
			OperatableStateMachine.add('lookup camera topic',
										LookupFromTableState(parameter_name='ariac_tables_unit1', table_name='assembly_stations', index_title='as', column_title='as_camera_topic'),
										transitions={'found': 'lookup camera frame', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'assembly_part', 'column_value': 'camera_topic'})

			# x:1414 y:144
			OperatableStateMachine.add('chosing right',
										ReplaceState(),
										transitions={'done': 'lookup robot pick position'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'right_pick', 'result': 'column_title'})

			# x:1203 y:627
			OperatableStateMachine.add('compute move to part',
										ComputeGraspAriacState(joint_names=['gantry_arm_elbow_joint', 'gantry_arm_shoulder_lift_joint', 'gantry_arm_shoulder_pan_joint', 'gantry_arm_wrist_1_joint', 'gantry_arm_wrist_2_joint', 'gantry_arm_wrist_3_joint']),
										transitions={'continue': 'finished', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group', 'namespace': 'namespace', 'tool_link': 'tool_link', 'pose': 'pose', 'offset': 'part_height', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:647 y:47
			OperatableStateMachine.add('get part',
										GetPartFromProductsState(),
										transitions={'continue': 'look what side part is', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'products': 'assembly_products', 'index': 'current_assembly_product', 'type': 'assembly_part', 'pose': 'assembly_offset'})

			# x:982 y:44
			OperatableStateMachine.add('look what side part is',
										DetectPartCameraAndSideAriacState(time_out=0.5),
										transitions={'continue': 'products left or right', 'failed': 'failed', 'not_found': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'assembly_part', 'pose': 'pose', 'side': 'side'})

			# x:395 y:31
			OperatableStateMachine.add('lookup camera frame',
										LookupFromTableState(parameter_name='ariac_tables_unit1', table_name='assembly_stations', index_title='as', column_title='as_camera_frame'),
										transitions={'found': 'get part', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'station_id', 'column_value': 'camera_frame'})

			# x:1336 y:486
			OperatableStateMachine.add('lookup camera frame_2',
										LookupFromTableState(parameter_name='ariac_tables_unit1', table_name='part_height_table', index_title='part_type', column_title='part_height'),
										transitions={'found': 'compute move to part', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'assembly_part', 'column_value': 'part_height'})

			# x:1286 y:273
			OperatableStateMachine.add('lookup robot pick position',
										LookupFromTableState(parameter_name='ariac_tables_unit1', table_name='assembly_stations', index_title='as', column_title=column_title),
										transitions={'found': 'move to pick', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'station_id', 'column_value': 'robot_pick_pos'})

			# x:1284 y:388
			OperatableStateMachine.add('move to pick',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'lookup camera frame_2', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'robot_pick_pos', 'move_group': 'move_group', 'namespace': 'namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1274 y:50
			OperatableStateMachine.add('products left or right',
										EqualState(),
										transitions={'true': 'chosing left', 'false': 'chosing right'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'side', 'value_b': 'true_value'})

			# x:1138 y:143
			OperatableStateMachine.add('chosing left',
										ReplaceState(),
										transitions={'done': 'lookup robot pick position'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'left_pick', 'result': 'column_title'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
