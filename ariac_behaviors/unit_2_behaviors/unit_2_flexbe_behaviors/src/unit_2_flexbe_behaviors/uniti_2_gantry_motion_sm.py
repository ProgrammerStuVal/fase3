#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.lookup_from_table import LookupFromTableState
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jun 22 2021
@author: Nick
'''
class uniti_2_gantry_motionSM(Behavior):
	'''
	moving gantry to proper positions
	'''


	def __init__(self):
		super(uniti_2_gantry_motionSM, self).__init__()
		self.name = 'uniti_2_gantry_motion'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1087 y:227, x:613 y:297
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['station_id'])
		_state_machine.userdata.station_id = ''
		_state_machine.userdata.move_group = 'gantry_torso'
		_state_machine.userdata.namespace = '/ariac/gantry'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = ''

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:153 y:41
			OperatableStateMachine.add('lookup station area',
										LookupFromTableState(parameter_name='ariac_tables_unit1', table_name='assembly_stations', index_title='as', column_title='as_global_pos'),
										transitions={'found': 'move to station area', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'station_id', 'column_value': 'station_area'})

			# x:399 y:14
			OperatableStateMachine.add('move to station area',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'lookup station  specific', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'station_area', 'move_group': 'move_group', 'namespace': 'namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:954 y:59
			OperatableStateMachine.add('move to station specific',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'station_specific', 'move_group': 'move_group', 'namespace': 'namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:629 y:35
			OperatableStateMachine.add('lookup station  specific',
										LookupFromTableState(parameter_name='ariac_tables_unit1', table_name='assembly_stations', index_title='as', column_title='as_direct_pos'),
										transitions={'found': 'move to station specific', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'station_id', 'column_value': 'station_specific'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
