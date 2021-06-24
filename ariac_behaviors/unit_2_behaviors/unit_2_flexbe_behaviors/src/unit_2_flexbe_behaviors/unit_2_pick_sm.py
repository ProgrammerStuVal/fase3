#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.detect_part_camera_and_side import DetectPartCameraAndSideAriacState
from ariac_flexbe_states.detect_part_camera_ariac_state import DetectPartCameraAriacState
from ariac_flexbe_states.lookup_from_table import LookupFromTableState
from ariac_flexbe_states.lookup_from_table_special import LookupFromTableSpecialState
from ariac_flexbe_states.message_state import MessageState
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_support_flexbe_states.replace_state import ReplaceState
from flexbe_states.wait_state import WaitState
from unit_2_flexbe_behaviors.unit_2_gripper_correcting_sm import unit_2_Gripper_correctingSM
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
		self.add_behavior(unit_2_Gripper_correctingSM, 'unit_2_Gripper_correcting')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:201 y:567, x:686 y:303
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['station_id', 'assembly_part', 'assembly_offset'])
		_state_machine.userdata.ref_frame = 'torso_main'
		_state_machine.userdata.camera_topic = ''
		_state_machine.userdata.camera_frame = ''
		_state_machine.userdata.assembly_part = ''
		_state_machine.userdata.current_assembly_product = 0
		_state_machine.userdata.station_id = ''
		_state_machine.userdata.offset = []
		_state_machine.userdata.side = True
		_state_machine.userdata.true_value = True
		_state_machine.userdata.tool_link = 'gantry_arm_ee_link'
		_state_machine.userdata.rotation = 0.0
		_state_machine.userdata.left_pick = 'as_left_pick'
		_state_machine.userdata.right_pick = 'as_right_pick'
		_state_machine.userdata.move_group = 'gantry_torso'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.namespace = '/ariac/gantry'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.parameter_name = 'ariac_tables_unit1'
		_state_machine.userdata.table_name = 'assembly_stations'
		_state_machine.userdata.index_title = 'as'
		_state_machine.userdata.ref_frame2 = 'world'
		_state_machine.userdata.move_group_2 = 'gantry_arm'
		_state_machine.userdata.left_prepick = 'as_left_prepick'
		_state_machine.userdata.right_prepick = 'as_right_prepick'
		_state_machine.userdata.arm_up_pos = 'gantry_arm_up'
		_state_machine.userdata.assembly_offset = []

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:62 y:29
			OperatableStateMachine.add('what as',
										MessageState(),
										transitions={'continue': 'lookup camera topic'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'station_id'})

			# x:1142 y:256
			OperatableStateMachine.add('chosing left prepick',
										ReplaceState(),
										transitions={'done': 'lookup robot prepick position'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'left_prepick', 'result': 'column_title_2'})

			# x:1414 y:144
			OperatableStateMachine.add('chosing right pick',
										ReplaceState(),
										transitions={'done': 'chosing right prepick'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'right_pick', 'result': 'column_title_'})

			# x:1419 y:250
			OperatableStateMachine.add('chosing right prepick',
										ReplaceState(),
										transitions={'done': 'lookup robot prepick position'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'right_prepick', 'result': 'column_title_2'})

			# x:647 y:40
			OperatableStateMachine.add('look what side part is',
										DetectPartCameraAndSideAriacState(time_out=0.5),
										transitions={'continue': 'what pose', 'failed': 'failed', 'not_found': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'assembly_part', 'pose': 'pose', 'side': 'side'})

			# x:1089 y:752
			OperatableStateMachine.add('look where part is now',
										DetectPartCameraAriacState(time_out=0.5),
										transitions={'continue': 'unit_2_Gripper_correcting', 'failed': 'failed', 'not_found': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame2', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'assembly_part', 'pose': 'pose'})

			# x:395 y:31
			OperatableStateMachine.add('lookup camera frame',
										LookupFromTableState(parameter_name='ariac_tables_unit1', table_name='assembly_stations', index_title='as', column_title='as_camera_frame'),
										transitions={'found': 'look what side part is', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'station_id', 'column_value': 'camera_frame'})

			# x:1302 y:785
			OperatableStateMachine.add('lookup camera frame_2',
										LookupFromTableState(parameter_name='ariac_tables_unit1', table_name='part_height_table', index_title='part_type', column_title='part_height'),
										transitions={'found': 'look where part is now', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'assembly_part', 'column_value': 'part_height'})

			# x:217 y:31
			OperatableStateMachine.add('lookup camera topic',
										LookupFromTableState(parameter_name='ariac_tables_unit1', table_name='assembly_stations', index_title='as', column_title='as_camera_topic'),
										transitions={'found': 'lookup camera frame', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'station_id', 'column_value': 'camera_topic'})

			# x:1304 y:560
			OperatableStateMachine.add('lookup robot pick position',
										LookupFromTableSpecialState(),
										transitions={'found': 'move to pick', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'parameter_name': 'parameter_name', 'table_name': 'table_name', 'index_title': 'index_title', 'column_title': 'column_title_', 'index_value': 'station_id', 'column_value': 'robot_pick_pos'})

			# x:1258 y:329
			OperatableStateMachine.add('lookup robot prepick position',
										LookupFromTableSpecialState(),
										transitions={'found': 'move to prepick', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'parameter_name': 'parameter_name', 'table_name': 'table_name', 'index_title': 'index_title', 'column_title': 'column_title_2', 'index_value': 'station_id', 'column_value': 'robot_pick_pos'})

			# x:331 y:655
			OperatableStateMachine.add('lookup robot prepick position_2',
										LookupFromTableSpecialState(),
										transitions={'found': 'move to pick_2', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'parameter_name': 'parameter_name', 'table_name': 'table_name', 'index_title': 'index_title', 'column_title': 'column_title_2', 'index_value': 'station_id', 'column_value': 'robot_pick_pos'})

			# x:637 y:649
			OperatableStateMachine.add('move arm up',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'lookup robot prepick position_2', 'planning_failed': 'retry move arm up', 'control_failed': 'retry move arm up', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'arm_up_pos', 'move_group': 'move_group_2', 'namespace': 'namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1332 y:654
			OperatableStateMachine.add('move to pick',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'lookup camera frame_2', 'planning_failed': 'retry move to pick', 'control_failed': 'retry move to pick', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'robot_pick_pos', 'move_group': 'move_group', 'namespace': 'namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:157 y:657
			OperatableStateMachine.add('move to pick_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'retry move to prepick_2', 'control_failed': 'retry move to prepick_2', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'robot_pick_pos', 'move_group': 'move_group', 'namespace': 'namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1284 y:412
			OperatableStateMachine.add('move to prepick',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'lookup robot pick position', 'planning_failed': 'retry move to prepick', 'control_failed': 'retry move to prepick', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'robot_pick_pos', 'move_group': 'move_group', 'namespace': 'namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1274 y:50
			OperatableStateMachine.add('products left or right',
										EqualState(),
										transitions={'true': 'chosing left pick', 'false': 'chosing right pick'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'side', 'value_b': 'true_value'})

			# x:630 y:751
			OperatableStateMachine.add('retry move arm up',
										WaitState(wait_time=0.5),
										transitions={'done': 'move arm up'},
										autonomy={'done': Autonomy.Off})

			# x:1520 y:650
			OperatableStateMachine.add('retry move to pick',
										WaitState(wait_time=0.5),
										transitions={'done': 'move to pick'},
										autonomy={'done': Autonomy.Off})

			# x:1495 y:418
			OperatableStateMachine.add('retry move to prepick',
										WaitState(wait_time=0.5),
										transitions={'done': 'move to prepick'},
										autonomy={'done': Autonomy.Off})

			# x:177 y:762
			OperatableStateMachine.add('retry move to prepick_2',
										WaitState(wait_time=0.5),
										transitions={'done': 'move to pick_2'},
										autonomy={'done': Autonomy.Off})

			# x:889 y:636
			OperatableStateMachine.add('unit_2_Gripper_correcting',
										self.use_behavior(unit_2_Gripper_correctingSM, 'unit_2_Gripper_correcting'),
										transitions={'finished': 'move arm up', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'part_pose': 'pose', 'part_height': 'part_height', 'move_group': 'move_group_2', 'namespace': 'namespace', 'tool_link': 'tool_link', 'action_topic': 'action_topic'})

			# x:927 y:42
			OperatableStateMachine.add('what pose',
										MessageState(),
										transitions={'continue': 'what side'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'pose'})

			# x:1121 y:35
			OperatableStateMachine.add('what side',
										MessageState(),
										transitions={'continue': 'products left or right'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'side'})

			# x:1138 y:143
			OperatableStateMachine.add('chosing left pick',
										ReplaceState(),
										transitions={'done': 'chosing left prepick'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'left_pick', 'result': 'column_title_'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
