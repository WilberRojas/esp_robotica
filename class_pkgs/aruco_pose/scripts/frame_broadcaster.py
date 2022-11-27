#!/usr/bin/env python3  
import roslib
import rospy
import tf
import math
import tf2_ros
import tf2_msgs.msg
import geometry_msgs.msg

br = tf.TransformBroadcaster()

def tfCallback(msg):
	for i in range(len(msg.transforms)):
		if (msg.transforms[i].child_frame_id=="marker_frame"):
			tx=msg.transforms[i].transform.translation.x
			ty=msg.transforms[i].transform.translation.y
			tz=msg.transforms[i].transform.translation.z
			rx=msg.transforms[i].transform.rotation.x
			ry=msg.transforms[i].transform.rotation.y
			rz=msg.transforms[i].transform.rotation.z
			#br.sendTransform((tz, ty, tx+0.4), (0, 0, 0, 1), rospy.Time.now(), "dynamic_frame", "base_link")
			br.sendTransform((tz, -tx, 0.4-ty), (0, 0, 0, 1), rospy.Time.now(), "dynamic_frame", "base_link")

if __name__ == '__main__':
	rospy.init_node('dynamic_tf')
	rospy.Subscriber("/tf",tf2_msgs.msg.TFMessage,tfCallback)
    	#br = tf.TransformBroadcaster()
	rospy.spin()
