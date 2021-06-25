#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.add_offset_to_pose_state import AddOffsetToPoseState
from ariac_flexbe_states.compute_grasp_ariac_state import ComputeGraspAriacState
from ariac_flexbe_states.get_object_pose import GetObjectPoseState
from ariac_flexbe_states.lookup_from_table import LookupFromTableState
from ariac_flexbe_states.message_state import MessageState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.vacuum_gripper_control_state import VacuumGripperControlState
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
from ariac_support_flexbe_states.equal_state import EqualState
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Jun 16 2021
@author: Nick
'''
class putproductonavgSM(Behavior):
	'''
	puts products down on corresponding agv
	'''


	def __init__(self):
		super(putproductonavgSM, self).__init__()
		self.name = 'put product on avg'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1414 y:635, x:746 y:323, x:1047 y:608
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'Next_product'], input_keys=['agv_id', 'current_kitting_product', 'number_of_kitting_products', 'part_height', 'offset'], output_keys=['current_kitting_product'])
		_state_machine.userdata.agv_id = ''
		_state_machine.userdata.number_of_kitting_products = 0
		_state_machine.userdata.current_kitting_product = 0
		_state_machine.userdata.one_value = 1
		_state_machine.userdata.part_height = ''
		_state_machine.userdata.ref_frame = 'world'
		_state_machine.userdata.agv_frame = ''
		_state_machine.userdata.move_group = 'kitting_arm'
		_state_machine.userdata.namespace = '/ariac/kitting'
		_state_machine.userdata.tool_link = 'ee_link'
		_state_machine.userdata.offset = []
		_state_machine.userdata.rotation = 0.0
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.agv_pregrasp = ''
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.offset_drop = 0.12

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:30 y:121
			OperatableStateMachine.add('agv_id',
										MessageState(),
										transitions={'continue': 'lookup agv_frame'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'agv_id'})

			# x:1120 y:43
			OperatableStateMachine.add('compute agv drop',
										ComputeGraspAriacState(joint_names=['elbow_joint', 'linear_arm_actuator_joint', 'shoulder_lift_joint', 'shoulder_pan_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']),
										transitions={'continue': 'move to agv', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group', 'namespace': 'namespace', 'tool_link': 'tool_link', 'pose': 'agv_frame', 'offset': 'offset_drop', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:429 y:55
			OperatableStateMachine.add('get agv pose',
										GetObjectPoseState(),
										transitions={'continue': 'move to agv pregrasp', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'frame': 'agv_frame', 'pose': 'agv_pose'})

			# x:1267 y:218
			OperatableStateMachine.add('gripper off',
										VacuumGripperControlState(enable=False, service_name='/ariac/kitting/arm/gripper/control'),
										transitions={'continue': 'wait for part to be dropped', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off})

			# x:1271 y:383
			OperatableStateMachine.add('iterate',
										AddNumericState(),
										transitions={'done': 'last product if'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'current_kitting_product', 'value_b': 'one_value', 'result': 'current_kitting_product'})

			# x:1251 y:467
			OperatableStateMachine.add('last product if',
										EqualState(),
										transitions={'true': 'finished', 'false': 'Next_product'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'number_of_kitting_products', 'value_b': 'current_kitting_product'})

			# x:273 y:56
			OperatableStateMachine.add('lookup agv pregrasp',
										LookupFromTableState(parameter_name='ariac_tables_unit1', table_name='agv_table', index_title='agv', column_title='agv_prepose'),
										transitions={'found': 'get agv pose', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'agv_id', 'column_value': 'agv_pregrasp'})

			# x:113 y:59
			OperatableStateMachine.add('lookup agv_frame',
										LookupFromTableState(parameter_name='ariac_tables_unit1', table_name='agv_table', index_title='agv', column_title='agv_kit'),
										transitions={'found': 'lookup agv pregrasp', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'agv_id', 'column_value': 'agv_frame'})

			# x:1270 y:41
			OperatableStateMachine.add('move to agv',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'gripper off', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'namespace': 'namespace', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:573 y:58
			OperatableStateMachine.add('move to agv pregrasp',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'add ofset to pose', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'agv_pregrasp', 'move_group': 'move_group', 'namespace': 'namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1263 y:285
			OperatableStateMachine.add('wait for part to be dropped',
										WaitState(wait_time=1),
										transitions={'done': 'iterate'},
										autonomy={'done': Autonomy.Off})

			# x:803 y:47
			OperatableStateMachine.add('add ofset to pose',
										AddOffsetToPoseState(),
										transitions={'continue': 'compute agv drop'},
										autonomy={'continue': Autonomy.Off},
										remapping={'input_pose': 'agv_pose', 'offset_pose': 'offset', 'output_pose': 'agv_frame'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
