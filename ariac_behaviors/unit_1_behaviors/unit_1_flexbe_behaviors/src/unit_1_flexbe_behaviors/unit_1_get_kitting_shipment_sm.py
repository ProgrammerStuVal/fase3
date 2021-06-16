#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
from ariac_support_flexbe_states.equal_state import EqualState
from unit_1_flexbe_behaviors.unit_1_get_products_sm import unit_1_get_productsSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jun 14 2021
@author: Nick
'''
class unit_1_get_kitting_shipmentSM(Behavior):
	'''
	cycles through  shipments
	'''


	def __init__(self):
		super(unit_1_get_kitting_shipmentSM, self).__init__()
		self.name = 'unit_1_get_kitting_shipment'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(unit_1_get_productsSM, 'unit_1_get_products')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:636 y:502, x:614 y:279, x:376 y:346
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'false'], input_keys=['kitting_products', 'agv_id', 'station_id', 'number_of_kitting_products', 'shipment_type'])
		_state_machine.userdata.current_shipment = 0
		_state_machine.userdata.increment = 1
		_state_machine.userdata.number_of_kitting_shipments = []
		_state_machine.userdata.shipment_type = ''
		_state_machine.userdata.kitting_shipments = []
		_state_machine.userdata.kitting_products = []
		_state_machine.userdata.agv_id = ''
		_state_machine.userdata.station_id = ''
		_state_machine.userdata.number_of_kitting_products = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:552 y:49
			OperatableStateMachine.add('unit_1_get_products',
										self.use_behavior(unit_1_get_productsSM, 'unit_1_get_products'),
										transitions={'finished': 'increment shipment', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'kitting_products': 'kitting_products', 'number_of_kitting_products': 'number_of_kitting_products'})

			# x:576 y:327
			OperatableStateMachine.add('shipments done if',
										EqualState(),
										transitions={'true': 'finished', 'false': 'false'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'number_of_kitting_shipments', 'value_b': 'current_shipment'})

			# x:1016 y:50
			OperatableStateMachine.add('increment shipment',
										AddNumericState(),
										transitions={'done': 'shipments done if'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'current_shipment', 'value_b': 'increment', 'result': 'current_shipment'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
