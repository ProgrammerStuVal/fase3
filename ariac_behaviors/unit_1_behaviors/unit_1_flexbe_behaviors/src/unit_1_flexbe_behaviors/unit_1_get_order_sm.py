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
from ariac_logistics_flexbe_states.get_order_state import GetOrderState
from unit_1_flexbe_behaviors.unit_1_get_kitting_shipment_sm import unit_1_get_kitting_shipmentSM
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
		self.add_behavior(unit_1_get_kitting_shipmentSM, 'unit_1_get_kitting_shipment')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1090 y:71, x:435 y:188
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.shipments = []
		_state_machine.userdata.number_of_shipments = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:115 y:35
			OperatableStateMachine.add('start assignment',
										StartAssignment(),
										transitions={'continue': 'get order'},
										autonomy={'continue': Autonomy.Off})

			# x:283 y:26
			OperatableStateMachine.add('get order',
										GetOrderState(),
										transitions={'order_found': 'unit_1_get_kitting_shipment', 'no_order_found': 'failed'},
										autonomy={'order_found': Autonomy.Off, 'no_order_found': Autonomy.Off},
										remapping={'order_id': 'order_id', 'kitting_shipments': 'kitting_shipments', 'number_of_kitting_shipments': 'number_of_kitting_shipments', 'assembly_shipments': 'shipments', 'number_of_assembly_shipments': 'number_of_shipments'})

			# x:533 y:32
			OperatableStateMachine.add('unit_1_get_kitting_shipment',
										self.use_behavior(unit_1_get_kitting_shipmentSM, 'unit_1_get_kitting_shipment'),
										transitions={'finished': 'end assignment', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'kitting_shipments': 'kitting_shipments', 'number_of_kitting_shipments': 'number_of_kitting_shipments'})

			# x:845 y:32
			OperatableStateMachine.add('end assignment',
										EndAssignment(),
										transitions={'continue': 'finished'},
										autonomy={'continue': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
