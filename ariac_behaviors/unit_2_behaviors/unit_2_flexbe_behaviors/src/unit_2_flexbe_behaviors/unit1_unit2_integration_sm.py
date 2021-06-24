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
from ariac_flexbe_states.notify_kitting_shipment_ready_state import NotifyKittingShipmentState
from ariac_flexbe_states.start_assignment_state import StartAssignment
from ariac_logistics_flexbe_states.get_assembly_shipment_from_order_state import GetAssemblyShipmentFromOrderState
from ariac_logistics_flexbe_states.get_kitting_shipment_from_order_state import GetKittingShipmentFromOrderState
from ariac_logistics_flexbe_states.get_order_state import GetOrderState
from ariac_logistics_flexbe_states.get_part_from_products_state import GetPartFromProductsState
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_support_flexbe_states.replace_state import ReplaceState
from unit_1_flexbe_behaviors.put_product_on_avg_sm import putproductonavgSM
from unit_1_flexbe_behaviors.unit_1_get_products_from_bin_sm import unit_1_get_products_from_binSM
from unit_2_flexbe_behaviors.unit_2_pick_sm import Unit_2_pickSM
from unit_2_flexbe_behaviors.unit_2_place_sm import unit_2_placeSM
from unit_2_flexbe_behaviors.uniti_2_gantry_motion_sm import uniti_2_gantry_motionSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Jun 24 2021
@author: Nick
'''
class unit1_unit2_integrationSM(Behavior):
	'''
	integration programm of unit 1 and 2
	'''


	def __init__(self):
		super(unit1_unit2_integrationSM, self).__init__()
		self.name = 'unit1_unit2_integration'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Unit_2_pickSM, 'Unit_2_pick')
		self.add_behavior(putproductonavgSM, 'put product on avg')
		self.add_behavior(unit_1_get_products_from_binSM, 'unit_1_get_products_from_bin')
		self.add_behavior(unit_2_placeSM, 'unit_2_place')
		self.add_behavior(uniti_2_gantry_motionSM, 'uniti_2_gantry_motion')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1040 y:837, x:892 y:410
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.current_assembly = 0
		_state_machine.userdata.current_kitting_product = 0
		_state_machine.userdata.current_kitting = 0
		_state_machine.userdata.part_height = 0.0
		_state_machine.userdata.current_product = 0
		_state_machine.userdata.onevalue = 1
		_state_machine.userdata.zero = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:153 y:50
			OperatableStateMachine.add('start',
										StartAssignment(),
										transitions={'continue': 'get order'},
										autonomy={'continue': Autonomy.Off})

			# x:248 y:517
			OperatableStateMachine.add('assembly ready_2',
										NotifyAssemblyReadyState(),
										transitions={'continue': 'last kitting shipment if_2', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'as_id': 'station_id_assembly', 'shipment_type': 'shipment_type_assembly', 'success': 'success', 'inspection_result': 'inspection_result'})

			# x:1171 y:815
			OperatableStateMachine.add('end',
										EndAssignment(),
										transitions={'continue': 'finished'},
										autonomy={'continue': Autonomy.Off})

			# x:623 y:42
			OperatableStateMachine.add('get assembly shipment',
										GetAssemblyShipmentFromOrderState(),
										transitions={'continue': 'uniti_2_gantry_motion', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'assembly_shipments': 'assembly_shipments', 'assembly_index': 'current_assembly', 'shipment_type': 'shipment_type_assembly', 'products': 'assembly_products', 'shipment_type': 'shipment_type_assembly', 'station_id': 'station_id_assembly', 'number_of_products': 'number_of_products'})

			# x:1214 y:31
			OperatableStateMachine.add('get kitting shipment',
										GetKittingShipmentFromOrderState(),
										transitions={'continue': 'get parts', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'kitting_shipments': 'kitting_shipments', 'kitting_index': 'current_kitting', 'shipment_type': 'shipment_type_kitting', 'products': 'kitting_products', 'agv_id': 'agv_id', 'station_id': 'station_id_kitting', 'number_of_products': 'number_of_kitting_products'})

			# x:367 y:58
			OperatableStateMachine.add('get order',
										GetOrderState(),
										transitions={'order_found': 'get assembly shipment', 'no_order_found': 'failed'},
										autonomy={'order_found': Autonomy.Off, 'no_order_found': Autonomy.Off},
										remapping={'order_id': 'order_id', 'kitting_shipments': 'kitting_shipments', 'number_of_kitting_shipments': 'number_of_kitting_shipments', 'assembly_shipments': 'assembly_shipments', 'number_of_assembly_shipments': 'number_of_assembly_shipments'})

			# x:1246 y:137
			OperatableStateMachine.add('get parts',
										GetPartFromProductsState(),
										transitions={'continue': 'unit_1_get_products_from_bin', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'products': 'kitting_products', 'index': 'current_kitting_product', 'type': 'product_type', 'pose': 'product_pose'})

			# x:1266 y:524
			OperatableStateMachine.add('get parts_2',
										GetPartFromProductsState(),
										transitions={'continue': 'Unit_2_pick', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'products': 'assembly_products', 'index': 'current_product', 'type': 'type', 'pose': 'offset'})

			# x:925 y:674
			OperatableStateMachine.add('increment part iterator',
										AddNumericState(),
										transitions={'done': 'last product unit 2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'current_product', 'value_b': 'onevalue', 'result': 'current_product'})

			# x:393 y:711
			OperatableStateMachine.add('increment shipment',
										AddNumericState(),
										transitions={'done': 'last shipment if'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'current_assembly', 'value_b': 'onevalue', 'result': 'current_assembly'})

			# x:1461 y:478
			OperatableStateMachine.add('kitting shipment iterator_2',
										AddNumericState(),
										transitions={'done': 'last kitting shipment if_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'current_kitting', 'value_b': 'onevalue', 'result': 'current_kitting'})

			# x:1665 y:463
			OperatableStateMachine.add('last kitting shipment if_2',
										EqualState(),
										transitions={'true': 'last shipment if_3', 'false': 'get kitting shipment'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'current_kitting', 'value_b': 'number_of_kitting_shipments'})

			# x:562 y:555
			OperatableStateMachine.add('last product unit 1',
										EqualState(),
										transitions={'true': 'get parts_2', 'false': 'get parts'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'current_kitting_product', 'value_b': 'number_of_kitting_products'})

			# x:703 y:679
			OperatableStateMachine.add('last product unit 2',
										EqualState(),
										transitions={'true': 'increment shipment', 'false': 'last product unit 1'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'current_product', 'value_b': 'number_of_products'})

			# x:101 y:695
			OperatableStateMachine.add('last shipment if',
										EqualState(),
										transitions={'true': 'assembly ready_2', 'false': 'reset part iterator'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'current_assembly', 'value_b': 'number_of_assembly_shipments'})

			# x:1503 y:311
			OperatableStateMachine.add('last shipment if_2',
										EqualState(),
										transitions={'true': 'get parts', 'false': 'get parts_2'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'current_assembly', 'value_b': 'number_of_assembly_shipments'})

			# x:1506 y:722
			OperatableStateMachine.add('last shipment if_3',
										EqualState(),
										transitions={'true': 'end', 'false': 'get parts_2'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'current_assembly', 'value_b': 'number_of_assembly_shipments'})

			# x:1248 y:313
			OperatableStateMachine.add('put product on avg',
										self.use_behavior(putproductonavgSM, 'put product on avg'),
										transitions={'finished': 'shipment ready', 'failed': 'failed', 'Next_product': 'last shipment if_2'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'Next_product': Autonomy.Inherit},
										remapping={'agv_id': 'agv_id', 'current_kitting_product': 'current_kitting_product', 'number_of_kitting_products': 'number_of_kitting_products', 'part_height': 'part_height', 'offset': 'product_pose'})

			# x:70 y:283
			OperatableStateMachine.add('reset part iterator',
										ReplaceState(),
										transitions={'done': 'get assembly shipment'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'zero', 'result': 'current_product'})

			# x:1264 y:412
			OperatableStateMachine.add('shipment ready',
										NotifyKittingShipmentState(),
										transitions={'continue': 'kitting shipment iterator_2', 'fail': 'failed', 'service_timeout': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off, 'service_timeout': Autonomy.Off},
										remapping={'agv_id': 'agv_id', 'shipment_type': 'shipment_type_kitting', 'assembly_station_name': 'station_id_kitting', 'success': 'success', 'message': 'message'})

			# x:1222 y:237
			OperatableStateMachine.add('unit_1_get_products_from_bin',
										self.use_behavior(unit_1_get_products_from_binSM, 'unit_1_get_products_from_bin'),
										transitions={'finished': 'put product on avg', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'kitting_part': 'product_type', 'part_height': 'part_height'})

			# x:1262 y:674
			OperatableStateMachine.add('unit_2_place',
										self.use_behavior(unit_2_placeSM, 'unit_2_place'),
										transitions={'finished': 'increment part iterator', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'station_id': 'station_id_assembly', 'offset': 'offset'})

			# x:937 y:29
			OperatableStateMachine.add('uniti_2_gantry_motion',
										self.use_behavior(uniti_2_gantry_motionSM, 'uniti_2_gantry_motion'),
										transitions={'finished': 'get kitting shipment', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'station_id': 'station_id_assembly'})

			# x:1257 y:597
			OperatableStateMachine.add('Unit_2_pick',
										self.use_behavior(Unit_2_pickSM, 'Unit_2_pick'),
										transitions={'finished': 'unit_2_place', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'station_id': 'station_id_assembly', 'assembly_part': 'type', 'assembly_offset': 'offset'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
