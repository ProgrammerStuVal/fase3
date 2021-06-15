#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_logistics_flexbe_states.get_products_from_shipment_state import GetProductsFromShipmentState
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
from ariac_support_flexbe_states.equal_state import EqualState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jun 14 2021
@author: Nick
'''
class unit_1_get_shipmentSM(Behavior):
	'''
	cycles through  shipments
	'''


	def __init__(self):
		super(unit_1_get_shipmentSM, self).__init__()
		self.name = 'unit_1_get_shipment'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:440 y:436, x:429 y:187
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['shipments', 'shipmentIndex'])
		_state_machine.userdata.total_shipments = []
		_state_machine.userdata.current_shipment = [0]
		_state_machine.userdata.increment = [1]
		_state_machine.userdata.shipments = []
		_state_machine.userdata.shipmentIndex = []
		_state_machine.userdata.shipmentType = ''
		_state_machine.userdata.shipmentIterator = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:148 y:62
			OperatableStateMachine.add('Get products',
										GetProductsFromShipmentState(),
										transitions={'continue': 'increment shipment', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'shipments': 'shipments', 'index': 'shipmentIndex', 'shipment_type': 'shipment_type', 'agv_id': 'agv_id', 'products': 'products', 'number_of_products': 'number_of_products'})

			# x:642 y:48
			OperatableStateMachine.add('increment shipment',
										AddNumericState(),
										transitions={'done': 'shipments done if'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'current_shipment', 'value_b': 'increment', 'result': 'current_shipment'})

			# x:387 y:260
			OperatableStateMachine.add('shipments done if',
										EqualState(),
										transitions={'true': 'finished', 'false': 'Get products'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'total_shipments', 'value_b': 'current_shipment'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
