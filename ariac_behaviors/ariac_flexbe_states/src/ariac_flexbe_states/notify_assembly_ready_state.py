#!/usr/bin/env python

import sys
import rospy

from flexbe_core import EventState, Logger
from nist_gear.srv import AssemblyStationSubmitShipment, AssemblyStationSubmitShipmentRequest, AssemblyStationSubmitShipmentResponse


class NotifyAssemblyReadyState(EventState):
	'''
	Notify the shipment is ready for transportation

	<# as_id 		string 	as_id: as1, asv2, as3 or as4 to select the desired as
	<# shipment_type	string	shepment type to transport

	#> success		bool	Result of the inspection
	#> inspection_result	float

	<= continue 		Given time has passed.
	<= fail	
		

	'''

	def __init__(self):
		# Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.
		super(NotifyAssemblyReadyState, self).__init__(outcomes = ['continue', 'fail'], input_keys = ['as_id', 'shipment_type'], output_keys = ['success', 'inspection_result'])



	def execute(self, userdata):
		# This method is called periodically while the state is active.
		# Main purpose is to check state conditions and trigger a corresponding outcome.
		# If no outcome is returned, the state will stay active.

		# initialize service proxy
		self._service = '/ariac/' + userdata.as_id + '/submit_shipment'
		#Logger.logwarn(self._service)
		server_up = rospy.wait_for_service(self._service)#, rospy.Duration(10.0))
		'''
		if not server_up:
			rospy.loginfo('Service not availeble')
			return 'service_timeout'
		# nog timeout op service
		'''
		AssemblyStationSubmitShipment = rospy.ServiceProxy(self._service, AssemblyStationSubmitShipment)


		request = AssemblyStationSubmitShipmentRequest()
		request.shipment_type = userdata.shipment_type
		try:
			srv_result = AssemblyStationSubmitShipment(request)
			userdata.success = srv_result.success
			userdata.inspection_result = srv_result.inspection_result
			return 'continue'

		except Exception as e:
			Logger.logwarn('Could not submit assembly, service call failed')
			rospy.logwarn(str(e))
			userdata.message = None
			return 'fail'


	def on_enter(self, userdata):
		# This method is called when the state becomes active, i.e. a transition from 
		pass # Nothing to do in this example.

	def on_exit(self, userdata):
		# This method is called when an outcome is returned and another state gets active.
		# It can be used to stop possibly running processes started by on_enter.

		pass # Nothing to do in this example.


	def on_start(self):
		# This method is called when the behavior is started.
		# If possible, it is generally better to initialize used resources in the constructor
		# because if anything failed, the behavior would not even be started.

		# In this example, we use this event to set the correct start time.
		pass # Nothing to do in this example.


	def on_stop(self):
		# This method is called whenever the behavior stops execution, also if it is cancelled.
		# Use this event to clean up things like claimed resources.

		pass # Nothing to do in this example.
		
