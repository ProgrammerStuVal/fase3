#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_logistics_flexbe_states.get_assembly_shipment_from_order_state import GetAssemblyShipmentFromOrderState
from ariac_logistics_flexbe_states.get_order_state import GetOrderState
from ariac_logistics_flexbe_states.get_part_from_products_state import GetPartFromProductsState
from unit_2_flexbe_behaviors.unit_2_pick_sm import Unit_2_pickSM
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

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1151 y:531, x:464 y:220
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.current_assembly = 0
		_state_machine.userdata.current_product = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:190 y:74
			OperatableStateMachine.add('get order',
										GetOrderState(),
										transitions={'order_found': 'get assembly shipment', 'no_order_found': 'failed'},
										autonomy={'order_found': Autonomy.Off, 'no_order_found': Autonomy.Off},
										remapping={'order_id': 'order_id', 'kitting_shipments': 'kitting_shipments', 'number_of_kitting_shipments': 'number_of_kitting_shipments', 'assembly_shipments': 'assembly_shipments', 'number_of_assembly_shipments': 'number_of_assembly_shipments'})

			# x:517 y:62
			OperatableStateMachine.add('get assembly shipment',
										GetAssemblyShipmentFromOrderState(),
										transitions={'continue': 'get parts', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'assembly_shipments': 'assembly_shipments', 'assembly_index': 'current_assembly', 'shipment_type': 'shipment_type', 'products': 'assembly_products', 'shipment_type': 'shipment_type', 'station_id': 'station_id', 'number_of_products': 'number_of_products'})

			# x:804 y:61
			OperatableStateMachine.add('get parts',
										GetPartFromProductsState(),
										transitions={'continue': 'Unit_2_pick', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'products': 'assembly_products', 'index': 'current_product', 'type': 'type', 'pose': 'pose'})

			# x:971 y:295
			OperatableStateMachine.add('Unit_2_pick',
										self.use_behavior(Unit_2_pickSM, 'Unit_2_pick'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'assembly_products': 'assembly_products'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]