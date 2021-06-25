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
from ariac_flexbe_states.get_gripper_status_state import GetGripperStatusState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_states.vacuum_gripper_control_state import VacuumGripperControlState
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_support_flexbe_states.replace_state import ReplaceState
from ariac_support_flexbe_states.text_to_float_state import TextToFloatState
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Jun 16 2021
@author: Nick
'''
class Gripper_correctingSM(Behavior):
	'''
	lowers the robot to correct the  part_height mistake
	'''


	def __init__(self):
		super(Gripper_correctingSM, self).__init__()
		self.name = 'Gripper_correcting'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1369 y:630, x:608 y:211
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['part_pose', 'part_height', 'move_group', 'namespace', 'tool_link', 'action_topic'])
		_state_machine.userdata.part_pose = []
		_state_machine.userdata.part_height = ''
		_state_machine.userdata.part_height_float = 0.0
		_state_machine.userdata.rotation = 0
		_state_machine.userdata.move_group = ''
		_state_machine.userdata.namespace = ''
		_state_machine.userdata.tool_link = ''
		_state_machine.userdata.action_topic = ''
		_state_machine.userdata.gripper_enabled = False
		_state_machine.userdata.gripper_attached = False
		_state_machine.userdata.gripper_attach_iterator = 0
		_state_machine.userdata.one_value = 1
		_state_machine.userdata.three_value = 3
		_state_machine.userdata.True_value = True
		_state_machine.userdata.zero = 0
		_state_machine.userdata.down_move = -0.001

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:145 y:37
			OperatableStateMachine.add('trans_text_to_float',
										TextToFloatState(),
										transitions={'done': 'compute_move'},
										autonomy={'done': Autonomy.Off},
										remapping={'text_value': 'part_height', 'float_value': 'part_height_float'})

			# x:1116 y:493
			OperatableStateMachine.add('check_three_times',
										EqualState(),
										transitions={'true': 'reset_iterator', 'false': 'get_gripper_status'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'gripper_attach_iterator', 'value_b': 'three_value'})

			# x:391 y:36
			OperatableStateMachine.add('compute_move',
										ComputeGraspAriacState(joint_names=['elbow_joint', 'linear_arm_actuator_joint', 'shoulder_lift_joint', 'shoulder_pan_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']),
										transitions={'continue': 'move_to_part', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group', 'namespace': 'namespace', 'tool_link': 'tool_link', 'pose': 'part_pose', 'offset': 'part_height_float', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1108 y:165
			OperatableStateMachine.add('get_gripper_status',
										GetGripperStatusState(topic_name='/ariac/kitting/arm/gripper/state'),
										transitions={'continue': 'status_true_if', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'enabled': 'gripper_enabled', 'attached': 'gripper_attached'})

			# x:465 y:480
			OperatableStateMachine.add('gripper_off',
										VacuumGripperControlState(enable=False, service_name='/ariac/kitting/arm/gripper/control'),
										transitions={'continue': 'move_down_more', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off})

			# x:897 y:29
			OperatableStateMachine.add('gripper_on',
										VacuumGripperControlState(enable=True, service_name='/ariac/kitting/arm/gripper/control'),
										transitions={'continue': 'wait_for_gripper_to_attach', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off})

			# x:255 y:490
			OperatableStateMachine.add('move_down_more',
										AddNumericState(),
										transitions={'done': 'compute_move'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'part_height_float', 'value_b': 'down_move', 'result': 'part_height_float'})

			# x:664 y:30
			OperatableStateMachine.add('move_to_part',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'gripper_on', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'namespace': 'namespace', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:916 y:486
			OperatableStateMachine.add('reset_iterator',
										ReplaceState(),
										transitions={'done': 'status_true_if_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'zero', 'result': 'gripper_attach_iterator'})

			# x:1102 y:279
			OperatableStateMachine.add('status_true_if',
										EqualState(),
										transitions={'true': 'finished', 'false': 'add_iteration'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'gripper_attached', 'value_b': 'True_value'})

			# x:695 y:478
			OperatableStateMachine.add('status_true_if_2',
										EqualState(),
										transitions={'true': 'finished', 'false': 'gripper_off'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'gripper_attached', 'value_b': 'True_value'})

			# x:1100 y:31
			OperatableStateMachine.add('wait_for_gripper_to_attach',
										WaitState(wait_time=0.4),
										transitions={'done': 'get_gripper_status'},
										autonomy={'done': Autonomy.Off})

			# x:1112 y:403
			OperatableStateMachine.add('add_iteration',
										AddNumericState(),
										transitions={'done': 'check_three_times'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'gripper_attach_iterator', 'value_b': 'one_value', 'result': 'gripper_attach_iterator'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
