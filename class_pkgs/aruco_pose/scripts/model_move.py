#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from gazebo_msgs.msg import ModelState
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Twist
import random
factor=1
models=['cow_panel','cat_panel','elephant_panel']
random.shuffle(models)
S1=2.5*random.random()+1.7


def talker():
	pub = rospy.Publisher('gazebo/set_model_state', ModelState, queue_size=10)
	rospy.init_node('move_model', anonymous=True)
	rate = rospy.Rate(100) # 10hz
	panelS1_msg=ModelState()
	panelS1_msg.model_name=models[0]

	
	panelS1_pose=Pose()


	panelS1_pose.position.y=0
	panelS1_pose.position.x=S1
	panelS1_pose.orientation.z=0.707106
	panelS1_pose.orientation.w=0.707106
	panelS1_msg.pose=panelS1_pose


	pub.publish(panelS1_msg)
	rate.sleep()
	


	
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
