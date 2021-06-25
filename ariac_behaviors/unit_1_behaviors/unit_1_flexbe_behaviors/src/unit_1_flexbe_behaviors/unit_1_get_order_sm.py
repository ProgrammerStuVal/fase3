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
from ariac_flexbe_states.notify_kitting_shipment_ready_state import NotifyKittingShipmentState
from ariac_flexbe_states.start_assignment_state import StartAssignment
from ariac_logistics_flexbe_states.get_kitting_shipment_from_order_state import GetKittingShipmentFromOrderState
from ariac_logistics_flexbe_states.get_order_state import GetOrderState
from ariac_logistics_flexbe_states.get_part_from_products_state import GetPartFromProductsState
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_support_flexbe_states.replace_state import ReplaceState
from flexbe_states.wait_state import WaitState
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
		# x:1185 y:631, x:558 y:361
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.shipments = []
		_state_machine.userdata.number_of_shipments = 0
		_state_machine.userdata.current_kitting = 0
		_state_machine.userdata.current_kitting_product = 0
		_state_machine.userdata.one_value = 1
		_state_machine.userdata.zero = 0

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

			# x:1305 y:514
			OperatableStateMachine.add('last kitting shipment if',
										EqualState(),
										transitions={'true': 'end', 'false': 'get kitting shipment'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'current_kitting', 'value_b': 'number_of_kitting_shipments'})

			# x:1206 y:131
			OperatableStateMachine.add('put product on avg',
										self.use_behavior(putproductonavgSM, 'put product on avg'),
										transitions={'finished': 'shipment ready', 'failed': 'failed', 'Next_product': 'get parts'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'Next_product': Autonomy.Inherit},
										remapping={'agv_id': 'agv_id', 'current_kitting_product': 'current_kitting_product', 'number_of_kitting_products': 'number_of_kitting_products', 'part_height': 'part_height', 'offset': 'product_pose'})

			# x:1319 y:429
			OperatableStateMachine.add('reset part iterator',
										ReplaceState(),
										transitions={'done': 'last kitting shipment if'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'zero', 'result': 'current_kitting_product'})

			# x:1339 y:354
			OperatableStateMachine.add('shipment iterator',
										AddNumericState(),
										transitions={'done': 'reset part iterator'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'current_kitting', 'value_b': 'one_value', 'result': 'current_kitting'})

			# x:1342 y:210
			OperatableStateMachine.add('shipment ready',
										NotifyKittingShipmentState(),
										transitions={'continue': 'wait for agv to move', 'fail': 'failed', 'service_timeout': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off, 'service_timeout': Autonomy.Off},
										remapping={'agv_id': 'agv_id', 'shipment_type': 'shipment_type', 'assembly_station_name': 'station_id', 'success': 'success', 'message': 'message'})

			# x:1183 y:25
			OperatableStateMachine.add('unit_1_get_products_from_bin',
										self.use_behavior(unit_1_get_products_from_binSM, 'unit_1_get_products_from_bin'),
										transitions={'finished': 'put product on avg', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'kitting_part': 'product_type', 'part_height': 'part_height'})

			# x:1360 y:288
			OperatableStateMachine.add('wait for agv to move',
										WaitState(wait_time=5),
										transitions={'done': 'shipment iterator'},
										autonomy={'done': Autonomy.Off})

			# x:1337 y:598
			OperatableStateMachine.add('end',
										EndAssignment(),
										transitions={'continue': 'finished'},
										autonomy={'continue': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
