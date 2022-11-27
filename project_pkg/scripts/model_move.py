#!/usr/bin/env python3

# Nota: 
# Se suscribe a /end_effector_position
# Mueve el gripper en Gazebo publicando en gazebo/set_model_state

import rospy
from gazebo_msgs.msg import ModelState
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Point

class move_gazebo_model(object): 
	def __init__(self):
		rospy.init_node('model_move', anonymous=True)
		self.pub = rospy.Publisher('gazebo/set_model_state', ModelState, queue_size=1)
		sub = rospy.Subscriber("/end_effector_position", Point, self.pos_callback)

		self.models=['gripper','person_faceB','unit_box']
		self.panelS1_msg = ModelState()
		self.init_position()
	
	def init_position(self):
		self.panelS1_msg.model_name = self.models[0]
		panelS1_pose = Pose()
		panelS1_pose.position.x = 1
		panelS1_pose.position.y = 1 
		panelS1_pose.position.z = 1
		self.panelS1_msg.pose = panelS1_pose
	
	def pos_callback(self,msg):
		self.panelS1_msg.model_name = self.models[0]
		panelS1_pose = Pose()
		panelS1_pose.position.x = msg.x
		panelS1_pose.position.y = msg.y
		panelS1_pose.position.z = msg.z
		self.panelS1_msg.pose = panelS1_pose
	
	def run(self):
		print(" ************************************ RUNNING: model_move ************************************")
		rate = rospy.Rate(10) # 10hz		
		while not rospy.is_shutdown():	
			self.pub.publish(self.panelS1_msg)
			rate.sleep()			


app = move_gazebo_model()
app.run()