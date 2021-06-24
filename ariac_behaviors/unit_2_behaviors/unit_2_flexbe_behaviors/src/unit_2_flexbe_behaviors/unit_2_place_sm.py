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
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.vacuum_gripper_control_state import VacuumGripperControlState
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Jun 23 2021
@author: Nick
'''
class unit_2_placeSM(Behavior):
	'''
	placing objects in box
	'''


	def __init__(self):
		super(unit_2_placeSM, self).__init__()
		self.name = 'unit_2_place'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:366 y:635, x:672 y:383
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['station_id', 'offset'])
		_state_machine.userdata.station_id = ''
		_state_machine.userdata.offset = []
		_state_machine.userdata.move_group = 'gantry_torso'
		_state_machine.userdata.namespace = '/ariac/gantry'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.ref_frame = 'world'
		_state_machine.userdata.tool_link = 'gantry_arm_ee_link'
		_state_machine.userdata.part_height = 0.03
		_state_machine.userdata.rotation = 0.0
		_state_machine.userdata.move_group_arm = 'gantry_arm'
		_state_machine.userdata.arm_up_pos = 'gantry_arm_up'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:62 y:126
			OperatableStateMachine.add('lookup preplace',
										LookupFromTableState(parameter_name='ariac_tables_unit1', table_name='assembly_stations', index_title='as', column_title='as_preplace'),
										transitions={'found': 'lookup direct position', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'station_id', 'column_value': 'preplace'})

			# x:1207 y:372
			OperatableStateMachine.add('compute move to briefcase',
										ComputeGraspAriacState(joint_names=['gantry_arm_elbow_joint', 'gantry_arm_shoulder_lift_joint', 'gantry_arm_shoulder_pan_joint', 'gantry_arm_wrist_1_joint', 'gantry_arm_wrist_2_joint', 'gantry_arm_wrist_3_joint']),
										transitions={'continue': 'move to briefcase', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group_arm', 'namespace': 'namespace', 'tool_link': 'tool_link', 'pose': 'pose', 'offset': 'part_height', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1212 y:130
			OperatableStateMachine.add('get location briefcase',
										GetObjectPoseState(),
										transitions={'continue': 'add offset to briefcase', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'frame': 'briefcase', 'pose': 'pose'})

			# x:1218 y:614
			OperatableStateMachine.add('gripper off',
										VacuumGripperControlState(enable=False, service_name='/ariac/gantry/arm/gripper/control'),
										transitions={'continue': 'move arm up', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off})

			# x:992 y:130
			OperatableStateMachine.add('lookup briefcase',
										LookupFromTableState(parameter_name='ariac_tables_unit1', table_name='assembly_stations', index_title='as', column_title='as_briefcase'),
										transitions={'found': 'get location briefcase', 'not_found': 'move to preplace'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'station_id', 'column_value': 'briefcase'})

			# x:278 y:126
			OperatableStateMachine.add('lookup direct position',
										LookupFromTableState(parameter_name='ariac_tables_unit1', table_name='assembly_stations', index_title='as', column_title='as_direct_pos'),
										transitions={'found': 'move to direct position', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'station_id', 'column_value': 'direct_pos'})

			# x:1016 y:615
			OperatableStateMachine.add('move arm up',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'move back to preplace', 'planning_failed': 'retry move direct position_2', 'control_failed': 'retry move direct position_2', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'arm_up_pos', 'move_group': 'move_group_arm', 'namespace': 'namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:575 y:618
			OperatableStateMachine.add('move back to direct position',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'retry move back  direct position', 'control_failed': 'retry move back  direct position', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'direct_pos', 'move_group': 'move_group', 'namespace': 'namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:788 y:616
			OperatableStateMachine.add('move back to preplace',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'move back to direct position', 'planning_failed': 'retry move arm up', 'control_failed': 'retry move arm up', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'preplace', 'move_group': 'move_group', 'namespace': 'namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1212 y:488
			OperatableStateMachine.add('move to briefcase',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'gripper off', 'planning_failed': 'retry move to briefcase', 'control_failed': 'retry move to briefcase'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'namespace': 'namespace', 'move_group': 'move_group_arm', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:514 y:127
			OperatableStateMachine.add('move to direct position',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'move to preplace', 'planning_failed': 'retry move direct position', 'control_failed': 'retry move direct position', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'direct_pos', 'move_group': 'move_group', 'namespace': 'namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:766 y:131
			OperatableStateMachine.add('move to preplace',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'lookup briefcase', 'planning_failed': 'retry move to preplace', 'control_failed': 'retry move to preplace', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'preplace', 'move_group': 'move_group', 'namespace': 'namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:785 y:710
			OperatableStateMachine.add('retry move arm up',
										WaitState(wait_time=0.5),
										transitions={'done': 'move back to preplace'},
										autonomy={'done': Autonomy.Off})

			# x:583 y:718
			OperatableStateMachine.add('retry move back  direct position',
										WaitState(wait_time=0.5),
										transitions={'done': 'move back to direct position'},
										autonomy={'done': Autonomy.Off})

			# x:514 y:9
			OperatableStateMachine.add('retry move direct position',
										WaitState(wait_time=0.5),
										transitions={'done': 'move to direct position'},
										autonomy={'done': Autonomy.Off})

			# x:1012 y:710
			OperatableStateMachine.add('retry move direct position_2',
										WaitState(wait_time=0.5),
										transitions={'done': 'move arm up'},
										autonomy={'done': Autonomy.Off})

			# x:1445 y:484
			OperatableStateMachine.add('retry move to briefcase',
										WaitState(wait_time=0.5),
										transitions={'done': 'move to briefcase'},
										autonomy={'done': Autonomy.Off})

			# x:748 y:2
			OperatableStateMachine.add('retry move to preplace',
										WaitState(wait_time=0.5),
										transitions={'done': 'move to preplace'},
										autonomy={'done': Autonomy.Off})

			# x:1214 y:253
			OperatableStateMachine.add('add offset to briefcase',
										AddOffsetToPoseState(),
										transitions={'continue': 'compute move to briefcase'},
										autonomy={'continue': Autonomy.Off},
										remapping={'input_pose': 'pose', 'offset_pose': 'offset', 'output_pose': 'pose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
