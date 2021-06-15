#!/usr/bin/env python

# Software License Agreement (BSD License)
#
# Copyright (c) 2018, Delft University of Technology
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Delft University of Technology nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Authors: the Gerard Harkema

import rospy
import rostopic
import inspect


from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxySubscriberCached
from nist_gear.msg import Proximity
'''

Created on Jan 22, 2021

@author: Gerard Harkema

'''

class DetectBreakBeamState(EventState):
	'''
	State to detect the state of an Breakbeam sensor
  	># topic				string		the topic name for the break beam
	#> object_detected			bool		Detected object

	<= continue 				if the pose of the part has been succesfully obtained
	<= failed 				otherwise

	'''

	def __init__(self):
		# Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.
		super(DetectBreakBeamState, self).__init__(outcomes = ['continue', 'failed'], input_keys = ['topic'], output_keys = ['object_detected'])


	def execute(self, userdata):
		# This method is called periodically while the state is active.
		# Main purpose is to check state conditions and trigger a corresponding outcome.
		# If no outcome is returned, the state will stay active.

		if self._sub.has_msg(self._topic):
			message = self._sub.get_last_msg(self._topic)
			userdata.object_detected = message.object_detected
			return 'continue'

	def on_enter(self, userdata):
		# This method is called when the state becomes active, i.e. a transition from another state to this one is taken.
		# It is primarily used to start actions which are associated with this state.

		self._topic = userdata.topic

		# Subscribe to the topic for the logical camera
		(msg_path, msg_topic, fn) = rostopic.get_topic_type(self._topic)

		if msg_topic == self._topic:
			msg_type = self._get_msg_from_path(msg_path)
			self._sub = ProxySubscriberCached({self._topic: msg_type})
			self._connected = True
		else:
			Logger.logwarn('Topic %s for state %s not yet available.\nFound: %s\nWill try again when entering the state...' % (self._topic, self.name, str(msg_topic)))


	def on_exit(self, userdata):
		# This method is called when an outcome is returned and another state gets active.
		# It can be used to stop possibly running processes started by on_enter.

		pass # Nothing to do


	def on_start(self):
		# This method is called when the behavior is started.
		# If possible, it is generally better to initialize used resources in the constructor
		# because if anything failed, the behavior would not even be started.
		self._start_time = rospy.Time.now()

	def on_stop(self):
		# This method is called whenever the behavior stops execution, also if it is cancelled.
		# Use this event to clean up things like claimed resources.

		pass # Nothing to do


	def _get_msg_from_path(self, msg_path):
		'''
		Created on 11.06.2013

		@author: Philipp Schillinger
		'''
		msg_import = msg_path.split('/')
		msg_module = '%s.msg' % (msg_import[0])
		package = __import__(msg_module, fromlist=[msg_module])
		clsmembers = inspect.getmembers(package, lambda member: inspect.isclass(member) and member.__module__.endswith(msg_import[1]))
		return clsmembers[0][1]
