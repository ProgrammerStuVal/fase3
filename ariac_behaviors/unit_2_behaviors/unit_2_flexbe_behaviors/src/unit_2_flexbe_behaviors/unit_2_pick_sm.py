#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.determine_position import DetectPartCameraAriacState
from ariac_flexbe_states.lookup_from_table import LookupFromTableState
from ariac_logistics_flexbe_states.get_part_from_products_state import GetPartFromProductsState
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
		# x:1326 y:420, x:542 y:251
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['assembly_products', 'station_id'])
		_state_machine.userdata.ref_frame = 'world'
		_state_machine.userdata.camera_topic = ''
		_state_machine.userdata.camera_frame = ''
		_state_machine.userdata.assembly_part = ''
		_state_machine.userdata.assembly_products = []
		_state_machine.userdata.current_assembly_product = 0
		_state_machine.userdata.station_id = ''
		_state_machine.userdata.offset = []

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

			# x:647 y:47
			OperatableStateMachine.add('get part',
										GetPartFromProductsState(),
										transitions={'continue': 'find product on agv', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'products': 'assembly_products', 'index': 'current_assembly_product', 'type': 'assembly_part', 'pose': 'offset'})

			# x:395 y:31
			OperatableStateMachine.add('lookup camera frame',
										LookupFromTableState(parameter_name='ariac_tables_unit1', table_name='assembly_stations', index_title='as', column_title='as_camera_frame'),
										transitions={'found': 'get part', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'assembly_part', 'column_value': 'camera_frame'})

			# x:880 y:49
			OperatableStateMachine.add('find product on agv',
										DetectPartCameraAriacState(time_out=0.5),
										transitions={'continue': 'finished', 'failed': 'failed', 'not_found': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'assembly_part', 'pose': 'pose', 'side': 'side'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
