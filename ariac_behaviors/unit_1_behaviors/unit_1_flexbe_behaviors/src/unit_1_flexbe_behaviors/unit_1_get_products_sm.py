#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_logistics_flexbe_states.get_part_from_products_state import GetPartFromProductsState
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
from ariac_support_flexbe_states.equal_state import EqualState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jun 15 2021
@author: Nick
'''
class unit_1_get_productsSM(Behavior):
	'''
	program for getting the products
	'''


	def __init__(self):
		super(unit_1_get_productsSM, self).__init__()
		self.name = 'unit_1_get_products'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:607 y:471, x:615 y:295
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['kitting_products', 'number_of_kitting_products'])
		_state_machine.userdata.kitting_products = []
		_state_machine.userdata.current_product = 0
		_state_machine.userdata.product_type = ''
		_state_machine.userdata.product_pose = []
		_state_machine.userdata.iterator = 1
		_state_machine.userdata.number_of_kitting_products = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:208 y:48
			OperatableStateMachine.add('get parts',
										GetPartFromProductsState(),
										transitions={'continue': 'increment product iterator', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'products': 'kitting_products', 'index': 'current_product', 'type': 'product_type', 'pose': 'product_pose'})

			# x:839 y:58
			OperatableStateMachine.add('increment product iterator',
										AddNumericState(),
										transitions={'done': 'products done if'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'current_product', 'value_b': 'iterator', 'result': 'current_product'})

			# x:557 y:342
			OperatableStateMachine.add('products done if',
										EqualState(),
										transitions={'true': 'finished', 'false': 'get parts'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'current_product', 'value_b': 'number_of_kitting_products'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
