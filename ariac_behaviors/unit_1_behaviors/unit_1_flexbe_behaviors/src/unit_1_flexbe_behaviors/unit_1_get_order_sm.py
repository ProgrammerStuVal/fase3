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
from ariac_logistics_flexbe_states.get_kitting_shipment_from_order_state import GetKittingShipmentFromOrderState
from ariac_logistics_flexbe_states.get_order_state import GetOrderState
from ariac_logistics_flexbe_states.get_part_from_products_state import GetPartFromProductsState
from unit_1_flexbe_behaviors.put_product_on_avg_sm import putproductonavgSM
from unit_1_flexbe_behaviors.unit_1_get_products_from_bin_sm import unit_1_get_products_from_binSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jun 14 2021
@author: Nick
'''
class unit_1_get_orderSM(Behavior):
	'''
	Base program for unit 1
	'''


	def __init__(self):
		super(unit_1_get_orderSM, self).__init__()
		self.name = 'unit_1_get_order'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(putproductonavgSM, 'put product on avg')
		self.add_behavior(unit_1_get_products_from_binSM, 'unit_1_get_products_from_bin')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1155 y:557, x:558 y:361
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.shipments = []
		_state_machine.userdata.number_of_shipments = 0
		_state_machine.userdata.current_kitting = 0
		_state_machine.userdata.current_kitting_product = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:78 y:37
			OperatableStateMachine.add('start assignment',
										StartAssignment(),
										transitions={'continue': 'get order'},
										autonomy={'continue': Autonomy.Off})

			# x:531 y:25
			OperatableStateMachine.add('get kitting shipment',
										GetKittingShipmentFromOrderState(),
										transitions={'continue': 'get parts', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'kitting_shipments': 'kitting_shipments', 'kitting_index': 'current_kitting', 'shipment_type': 'shipment_type', 'products': 'kitting_products', 'agv_id': 'agv_id', 'station_id': 'station_id', 'number_of_products': 'number_of_kitting_products'})

			# x:279 y:49
			OperatableStateMachine.add('get order',
										GetOrderState(),
										transitions={'order_found': 'get kitting shipment', 'no_order_found': 'failed'},
										autonomy={'order_found': Autonomy.Off, 'no_order_found': Autonomy.Off},
										remapping={'order_id': 'order_id', 'kitting_shipments': 'kitting_shipments', 'number_of_kitting_shipments': 'number_of_kitting_shipments', 'assembly_shipments': 'shipments', 'number_of_assembly_shipments': 'number_of_shipments'})

			# x:916 y:29
			OperatableStateMachine.add('get parts',
										GetPartFromProductsState(),
										transitions={'continue': 'unit_1_get_products_from_bin', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'products': 'kitting_products', 'index': 'current_kitting_product', 'type': 'product_type', 'pose': 'product_pose'})

			# x:1418 y:41
			OperatableStateMachine.add('put product on avg',
										self.use_behavior(putproductonavgSM, 'put product on avg'),
										transitions={'finished': 'end', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'agv_id': 'agv_id', 'current_kitting_product': 'current_kitting_product', 'number_of_kitting_products': 'number_of_kitting_products', 'part_height': 'part_height', 'offset': 'product_pose'})

			# x:1150 y:37
			OperatableStateMachine.add('unit_1_get_products_from_bin',
										self.use_behavior(unit_1_get_products_from_binSM, 'unit_1_get_products_from_bin'),
										transitions={'finished': 'put product on avg', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'kitting_part': 'product_type', 'part_height': 'part_height'})

			# x:1402 y:550
			OperatableStateMachine.add('end',
										EndAssignment(),
										transitions={'continue': 'finished'},
										autonomy={'continue': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
