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
# Authors: the HRWROS mooc instructors
# Modified for using Ariac: Gerard Harkema

import rospy
import rostopic
import inspect

import tf2_ros
import tf2_geometry_msgs
import geometry_msgs.msg


from flexbe_core import EventState, Logger
from geometry_msgs.msg import Pose, PoseStamped
from nist_gear.msg import LogicalCameraImage, Model
from flexbe_core.proxy import ProxySubscriberCached

'''

Created on Sep 5 2018

@author: HRWROS mooc instructors

'''

class DetectPartCameraAndSideAriacState(EventState):
	'''
	State to detect the pose of the part with any of the cameras in the factory simulation of the Ariac
	-- time_out		float		Time in withs the camera to have detected the part
	># ref_frame		string		reference frame for the part pose output key
  	># camera_topic		string		the topic name for the camera to detect the part
	># camera_frame 	string		frame of the camera
	># part			string		Part to detect
	#> pose			PoseStamped	Pose of the detected part

	<= continue 				if the pose of the part has been succesfully obtained
	<= failed 				otherwise

	'''

	def __init__(self, time_out = 0.5):
		# Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.
		super(DetectPartCameraAndSideAriacState, self).__init__(outcomes = ['continue', 'failed', 'not_found'], input_keys = ['ref_frame', 'camera_topic', 'camera_frame', 'part'], output_keys = ['pose', 'side'])

		# Store state parameter for later use.
		self._wait = time_out

		# tf to transfor the object pose
		self._tf_buffer = tf2_ros.Buffer(rospy.Duration(10.0)) #tf buffer length
		self._tf_listener = tf2_ros.TransformListener(self._tf_buffer)


	def execute(self, userdata):
		# This method is called periodically while the state is active.
		# Main purpose is to check state conditions and trigger a corresponding outcome.
		# If no outcome is returned, the state will stay active.
		#rospy.logwarn(userdata.ref_frame)
		#rospy.logwarn(userdata.camera_topic)
		#rospy.logwarn(userdata.camera_frame)
		#rospy.logwarn(userdata.part)
		if not self._connected:
			userdata.pose = None
			return 'failed'

		if self._failed:
			userdata.pose = None
			return 'failed'

		elapsed = rospy.get_rostime() - self._start_time;
		if (elapsed.to_sec() > self._wait):
			return 'time_out'
		if self._sub.has_msg(self._topic):
			message = self._sub.get_last_msg(self._topic)
			#rospy.logwarn(message)
			for model in message.models:
				if model.type == userdata.part:
					part_pose = PoseStamped()
					#rospy.logwarn("model.pose")
					#rospy.logwarn(model.pose)
					part_pose.pose = model.pose
					part_pose.header.frame_id = self._camera_frame
					part_pose.header.stamp = rospy.Time.now()
					# Transform the pose to desired output frame
					part_pose = tf2_geometry_msgs.do_transform_pose(part_pose, self._transform)
					broadcaster = tf2_ros.StaticTransformBroadcaster()
					#rospy.logwarn("pose")
					#rospy.logwarn(part_pose)

					userdata.pose = part_pose
					if part_pose.pose.position.y < 0:
						self._side = False
					else:
						self._side = True
					userdata.side = self._side
					return 'continue'
			userdata.pose = None
			return 'not_found'

	def on_enter(self, userdata):
		# This method is called when the state becomes active, i.e. a transition from another state to this one is taken.
		# It is primarily used to start actions which are associated with this state.

		self.ref_frame = userdata.ref_frame
		self._topic = userdata.camera_topic
		self._camera_frame = userdata.camera_frame
		self._connected = False
		self._failed = False
		self._start_time = rospy.get_rostime()

		# Subscribe to the topic for the logical camera
		(msg_path, msg_topic, fn) = rostopic.get_topic_type(self._topic)

		if msg_topic == self._topic:
			msg_type = self._get_msg_from_path(msg_path)
			self._sub = ProxySubscriberCached({self._topic: msg_type})
			self._connected = True
		else:
			Logger.logwarn('Topic %s for state %s not yet available.\nFound: %s\nWill try again when entering the state...' % (self._topic, self.name, str(msg_topic)))

		# Get transform between camera and robot_base
		try:
			self._transform = self._tf_buffer.lookup_transform(self.ref_frame, self._camera_frame, rospy.Time(0), rospy.Duration(1.0))
		except Exception as e:
			Logger.logwarn('Could not transform pose: ' + str(e))
		 	self._failed = True


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
