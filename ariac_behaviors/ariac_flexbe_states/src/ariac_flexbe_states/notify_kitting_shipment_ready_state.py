#!/usr/bin/env python

import sys
import rospy

from flexbe_core import EventState, Logger
from nist_gear.srv import AGVToAssemblyStation, AGVToAssemblyStationRequest, AGVToAssemblyStationResponse


class NotifyKittingShipmentState(EventState):
	'''
	Notify the shipment is ready for transportation

	<# agv_id 		string 	agv_id: agv1, agv2, agv3 or agv4 to select the desired agv
	<# shipment_type	string	shepment type to transport
	<# assembly_station_name	string	assembly station te send order

	#> success		bool	Result of the inspection
	#> message		string

	<= continue 		Given time has passed.
	<= fail	
	<= service_timeout		

	'''

	def __init__(self):
		# Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.
		super(NotifyKittingShipmentState, self).__init__(outcomes = ['continue', 'fail', 'service_timeout'], input_keys = ['agv_id', 'shipment_type', 'assembly_station_name'], output_keys = ['success', 'message'])



	def execute(self, userdata):
		# This method is called periodically while the state is active.
		# Main purpose is to check state conditions and trigger a corresponding outcome.
		# If no outcome is returned, the state will stay active.

		# initialize service proxy
		self._service = '/ariac/' + userdata.agv_id + '/submit_shipment'
		#Logger.logwarn(self._service)
		server_up = rospy.wait_for_service(self._service)#, rospy.Duration(10.0))
		'''
		if not server_up:
			rospy.loginfo('Service not availeble')
			return 'service_timeout'
		# nog timeout op service
		'''
		NotifyShipmentReady = rospy.ServiceProxy(self._service, AGVToAssemblyStation)


		request = AGVToAssemblyStationRequest()
		request.shipment_type = userdata.shipment_type
		request.assembly_station_name = userdata.assembly_station_name
		try:
			srv_result = NotifyShipmentReady(request)
			userdata.success = srv_result.success
			userdata.message = srv_result.message
			return 'continue'

		except Exception as e:
			Logger.logwarn('Could not submet shipment, service call failed')
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
		
