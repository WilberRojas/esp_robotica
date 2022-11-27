#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from gazebo_msgs.msg import ModelState
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Twist
import random
factor=1
models=['aruco_panel','cat_panel','elephant_panel']
pub = rospy.Publisher('gazebo/set_model_state', ModelState, queue_size=10)
panelS1_msg=ModelState()
panelS1_pose=Pose()
panelS1_msg.model_name=models[0]

def tfCallback(msg):
	for i in range(len(msg.transforms)):
		if(msg.transforms[i].child_frame_id=="tool0"):
			tx=msg.transforms[i].transform.translation.x
			ty=msg.transforms[i].transform.translation.y
			tz=msg.transforms[i].transform.translation.z
			panelS1_pose.position.y=tx
			panelS1_pose.position.x=ty
			panelS1_pose.position.z=tz
			panelS1_pose.orientation.z=0.707106
			panelS1_pose.orientation.w=0.707106
			panelS1_msg.pose=panelS1_pose
			pub.publish(panelS1_msg)
			
	


	
	count=0
	print("moving model randomly")
	while not rospy.is_shutdown() and count<10:

		panelS1_msg.pose=panelS1_pose



		pub.publish(panelS1_msg)
		rate.sleep()
		
		


		count+=1

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
