#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from unit_1_flexbe_behaviors.unit_1_get_products_from_bin_sm import unit_1_get_products_from_binSM
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
		self.add_behavior(unit_1_get_products_from_binSM, 'unit_1_get_products_from_bin')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:817 y:84, x:615 y:295
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['kitting_products', 'number_of_kitting_products', 'product_type', 'product_pose'])
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
			# x:501 y:24
			OperatableStateMachine.add('unit_1_get_products_from_bin',
										self.use_behavior(unit_1_get_products_from_binSM, 'unit_1_get_products_from_bin'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'kitting_part': 'product_type'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
