#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from unit_1_flexbe_behaviors.unit_1_get_order_sm import unit_1_get_orderSM
from unit_2_flexbe_behaviors.unit_2_get_order_sm import Unit_2_Get_orderSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Jun 24 2021
@author: Nick
'''
class Multi_ThreadingSM(Behavior):
	'''
	Multi threading programm that allows unit 1 and 2 to work at the same time
	'''


	def __init__(self):
		super(Multi_ThreadingSM, self).__init__()
		self.name = 'Multi_Threading'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Unit_2_Get_orderSM, 'Container/Unit_2_Get_order')
		self.add_behavior(unit_1_get_orderSM, 'Container/unit_1_get_order')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:30 y:365, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:30 y:365, x:130 y:365, x:230 y:365, x:330 y:365
		_sm_container_0 = ConcurrencyContainer(outcomes=['finished', 'failed'], conditions=[
										('finished', [('unit_1_get_order', 'finished'), ('Unit_2_Get_order', 'finished')]),
										('failed', [('unit_1_get_order', 'failed'), ('Unit_2_Get_order', 'failed')])
										])

		with _sm_container_0:
			# x:66 y:58
			OperatableStateMachine.add('unit_1_get_order',
										self.use_behavior(unit_1_get_orderSM, 'Container/unit_1_get_order'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:380 y:70
			OperatableStateMachine.add('Unit_2_Get_order',
										self.use_behavior(Unit_2_Get_orderSM, 'Container/Unit_2_Get_order'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})



		with _state_machine:
			# x:233 y:80
			OperatableStateMachine.add('Container',
										_sm_container_0,
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
