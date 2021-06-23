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
from ariac_flexbe_states.start_assignment_state import StartAssignment
from ariac_logistics_flexbe_states.get_assembly_shipment_from_order_state import GetAssemblyShipmentFromOrderState
from ariac_logistics_flexbe_states.get_order_state import GetOrderState
from ariac_logistics_flexbe_states.get_part_from_products_state import GetPartFromProductsState
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
from ariac_support_flexbe_states.equal_state import EqualState
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

			# x:1276 y:544
			OperatableStateMachine.add('end',
										EndAssignment(),
										transitions={'continue': 'increment shipment'},
										autonomy={'continue': Autonomy.Off})

			# x:656 y:53
			OperatableStateMachine.add('get assembly shipment',
										GetAssemblyShipmentFromOrderState(),
										transitions={'continue': 'get parts', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'assembly_shipments': 'assembly_shipments', 'assembly_index': 'current_assembly', 'shipment_type': 'shipment_type', 'products': 'assembly_products', 'shipment_type': 'shipment_type', 'station_id': 'station_id', 'number_of_products': 'number_of_products'})

			# x:367 y:58
			OperatableStateMachine.add('get order',
										GetOrderState(),
										transitions={'order_found': 'get assembly shipment', 'no_order_found': 'failed'},
										autonomy={'order_found': Autonomy.Off, 'no_order_found': Autonomy.Off},
										remapping={'order_id': 'order_id', 'kitting_shipments': 'kitting_shipments', 'number_of_kitting_shipments': 'number_of_kitting_shipments', 'assembly_shipments': 'assembly_shipments', 'number_of_assembly_shipments': 'number_of_assembly_shipments'})

			# x:1026 y:55
			OperatableStateMachine.add('get parts',
										GetPartFromProductsState(),
										transitions={'continue': 'uniti_2_gantry_motion', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'products': 'assembly_products', 'index': 'current_product', 'type': 'type', 'pose': 'pose'})

			# x:1025 y:542
			OperatableStateMachine.add('increment shipment',
										AddNumericState(),
										transitions={'done': 'last shipment if'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'current_product', 'value_b': 'onevalue', 'result': 'current_assembly'})

			# x:1248 y:416
			OperatableStateMachine.add('last product',
										EqualState(),
										transitions={'true': 'end', 'false': 'get parts'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'current_product', 'value_b': 'assembly_products'})

			# x:721 y:533
			OperatableStateMachine.add('last shipment if',
										EqualState(),
										transitions={'true': 'finished', 'false': 'get assembly shipment'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'current_assembly', 'value_b': 'assembly_shipments'})

			# x:1029 y:320
			OperatableStateMachine.add('unit_2_place',
										self.use_behavior(unit_2_placeSM, 'unit_2_place'),
										transitions={'finished': 'add part iterator', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'station_id': 'station_id', 'offset': 'pose'})

			# x:1022 y:156
			OperatableStateMachine.add('uniti_2_gantry_motion',
										self.use_behavior(uniti_2_gantry_motionSM, 'uniti_2_gantry_motion'),
										transitions={'finished': 'Unit_2_pick', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'station_id': 'station_id'})

			# x:1019 y:235
			OperatableStateMachine.add('Unit_2_pick',
										self.use_behavior(Unit_2_pickSM, 'Unit_2_pick'),
										transitions={'finished': 'unit_2_place', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'assembly_products': 'assembly_products', 'station_id': 'station_id'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
