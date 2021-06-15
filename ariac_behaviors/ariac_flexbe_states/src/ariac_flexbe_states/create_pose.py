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
# Authors: Gerard Harkema

import rospy
import rostopic
import inspect

import tf2_ros
import tf2_geometry_msgs
import geometry_msgs.msg
from tf.transformations import *


from flexbe_core import EventState, Logger
from geometry_msgs.msg import Pose, Point, Vector3, Quaternion
from flexbe_core.proxy import ProxySubscriberCached

'''

Created on March 21, 2021

@author: Gerard Harkema

'''

class CreatePoseState(EventState):
	'''
	Creats a pose
	-- xyz			Point		Position
	-- rpy			Vector3		Twist
	#> pose			Pose		Output of the pose

	<= continue 				if the pose of the part has been succesfully obtained
	<= failed 				otherwise

	'''

	def __init__(self, xyz, rpy):
		# Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.
		super(CreatePoseState, self).__init__(outcomes = ['continue', 'failed'], output_keys = ['pose'])

		self._pose = Pose()
		self._pose.position.x = xyz[0]
		self._pose.position.y = xyz[1]
		self._pose.position.z = xyz[2]
		q = quaternion_from_euler(rpy[0], rpy[1], rpy[2])	
		self._pose.orientation = Quaternion(*q)
		#rospy.logerr(self._pose)	



	def execute(self, userdata):
		userdata.pose = self._pose
		return 'continue'

	def on_enter(self, userdata):
		# This method is called when the state becomes active, i.e. a transition from another state to this one is taken.
		# It is primarily used to start actions which are associated with this state.
		pass # Nothing to do



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



