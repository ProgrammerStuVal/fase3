#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.end_assignment_state import EndAssignment
from ariac_flexbe_states.notify_assembly_ready_state import NotifyAssemblyReadyState
from ariac_flexbe_states.start_assignment_state import StartAssignment
from ariac_logistics_flexbe_states.get_assembly_shipment_from_order_state import GetAssemblyShipmentFromOrderState
from ariac_logistics_flexbe_states.get_order_state import GetOrderState
from ariac_logistics_flexbe_states.get_part_from_products_state import GetPartFromProductsState
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_support_flexbe_states.replace_state import ReplaceState
from unit_2_flexbe_behaviors.unit_2_pick_sm import Unit_2_pickSM
from unit_2_flexbe_behaviors.unit_2_place_sm import unit_2_placeSM
from unit_2_flexbe_behaviors.uniti_2_gantry_motion_sm import uniti_2_gantry_motionSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jun 21 2021
@author: Nick
'''
class Unit_2_Get_orderSM(Behavior):
	'''
	main program unit 2
	'''


	def __init__(self):
		super(Unit_2_Get_orderSM, self).__init__()
		self.name = 'Unit_2_Get_order'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Unit_2_pickSM, 'Unit_2_pick')
		self.add_behavior(unit_2_placeSM, 'unit_2_place')
		self.add_behavior(uniti_2_gantry_motionSM, 'uniti_2_gantry_motion')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:507 y:547, x:746 y:247
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.current_assembly = 0
		_state_machine.userdata.current_product = 0
		_state_machine.userdata.onevalue = 1
		_state_machine.userdata.zero = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:138 y:50
			OperatableStateMachine.add('start',
										StartAssignment(),
										transitions={'continue': 'get order'},
										autonomy={'continue': Autonomy.Off})

			# x:1030 y:416
			OperatableStateMachine.add('add part iterator',
										AddNumericState(),
										transitions={'done': 'last product'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'current_product', 'value_b': 'onevalue', 'result': 'current_product'})

			# x:1251 y:542
			OperatableStateMachine.add('assembly ready',
										NotifyAssemblyReadyState(),
										transitions={'continue': 'increment shipment', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'as_id': 'station_id', 'shipment_type': 'shipment_type', 'success': 'success', 'inspection_result': 'inspection_result'})

			# x:575 y:531
			OperatableStateMachine.add('end',
										EndAssignment(),
										transitions={'continue': 'finished'},
										autonomy={'continue': Autonomy.Off})

			# x:656 y:53
			OperatableStateMachine.add('get assembly shipment',
										GetAssemblyShipmentFromOrderState(),
										transitions={'continue': 'uniti_2_gantry_motion', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'assembly_shipments': 'assembly_shipments', 'assembly_index': 'current_assembly', 'shipment_type': 'shipment_type', 'products': 'assembly_products', 'shipment_type': 'shipment_type', 'station_id': 'station_id', 'number_of_products': 'number_of_products'})

			# x:367 y:58
			OperatableStateMachine.add('get order',
										GetOrderState(),
										transitions={'order_found': 'get assembly shipment', 'no_order_found': 'failed'},
										autonomy={'order_found': Autonomy.Off, 'no_order_found': Autonomy.Off},
										remapping={'order_id': 'order_id', 'kitting_shipments': 'kitting_shipments', 'number_of_kitting_shipments': 'number_of_kitting_shipments', 'assembly_shipments': 'assembly_shipments', 'number_of_assembly_shipments': 'number_of_assembly_shipments'})

			# x:1023 y:152
			OperatableStateMachine.add('get parts',
										GetPartFromProductsState(),
										transitions={'continue': 'Unit_2_pick', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'products': 'assembly_products', 'index': 'current_product', 'type': 'type', 'pose': 'offset'})

			# x:1025 y:542
			OperatableStateMachine.add('increment shipment',
										AddNumericState(),
										transitions={'done': 'last shipment if'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'current_assembly', 'value_b': 'onevalue', 'result': 'current_assembly'})

			# x:1248 y:416
			OperatableStateMachine.add('last product',
										EqualState(),
										transitions={'true': 'assembly ready', 'false': 'get parts'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'current_product', 'value_b': 'number_of_products'})

			# x:721 y:533
			OperatableStateMachine.add('last shipment if',
										EqualState(),
										transitions={'true': 'end', 'false': 'reset part iterator'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'current_assembly', 'value_b': 'number_of_assembly_shipments'})

			# x:719 y:440
			OperatableStateMachine.add('reset part iterator',
										ReplaceState(),
										transitions={'done': 'get assembly shipment'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'zero', 'result': 'current_product'})

			# x:1029 y:320
			OperatableStateMachine.add('unit_2_place',
										self.use_behavior(unit_2_placeSM, 'unit_2_place'),
										transitions={'finished': 'add part iterator', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'station_id': 'station_id', 'offset': 'offset'})

			# x:1021 y:80
			OperatableStateMachine.add('uniti_2_gantry_motion',
										self.use_behavior(uniti_2_gantry_motionSM, 'uniti_2_gantry_motion'),
										transitions={'finished': 'get parts', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'station_id': 'station_id'})

			# x:1019 y:235
			OperatableStateMachine.add('Unit_2_pick',
										self.use_behavior(Unit_2_pickSM, 'Unit_2_pick'),
										transitions={'finished': 'unit_2_place', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'station_id': 'station_id', 'assembly_part': 'type', 'assembly_offset': 'offset'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
