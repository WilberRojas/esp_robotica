#!/usr/bin/env python
import rospy #importing python support
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
import tf

pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
vel = Twist()
state=0
for_dist=10000
def forward(x):
	vel.linear.x = x
	vel.angular.z = 0
	pub.publish(vel)

def turn_right(z):
	vel.linear.x = 0
	vel.angular.z = z
	pub.publish(vel)

def turn_left(z):
	vel.linear.x = 0
	vel.angular.z = -z
	pub.publish(vel)

def stop():
	vel.linear.x = 0
	vel.angular.z = 0
	pub.publish(vel)
def laser_callback(message):
	global for_dist 
	for_dist=message.ranges[360]
	if for_dist < 0.5:
		stop()

def callback(data): #callback function
	global state
	dist_x = data.pose.pose.position.x
	dist_y = data.pose.pose.position.y

	euler = tf.transformations.euler_from_quaternion((data.pose.pose.orientation.x,data.pose.pose.orientation.y,data.pose.pose.orientation.z,data.pose.pose.orientation.w))
	yaw = euler[2]
	print("yaw: ",yaw)
	print ("dist_x: ",dist_x)
	print ("state: ",state)
	print ("dist_y: ",dist_y)
	if(state==0):
		if dist_x < 3:
			forward(0.2)
		else:	 
			stop()
			state=1

	if(state==1):
		if yaw > -1.5707:
			turn_right()
		else:	 
			stop()
			state=2
	if(state==2):
		if dist_y > -3:
			forward()
		else:	 
			stop()
			state=3
	if(state==3):
		if abs(yaw) < 3.14:
			turn_right()
		else:	 
			stop()
			state=4
	if(state==4):
		if dist_x > 0:
			forward()
		else:	 
			stop()
			state=5
	if(state==5):
		if yaw > 1.5707:
			turn_right()
		else:	 
			stop()
			state=6
	if(state==6):
		if dist_y <0:
			forward()
		else:	 
			stop()
			state=7
	if(state==7):
		if yaw > 0:
			turn_right()
		else:	 
			stop()
			state=0
def publisher():
	rospy.init_node('move_robot', anonymous=True) #Initialize the node, Node name -> point_publisher 
	rate = rospy.Rate(0.2) # 5hz 5 messages per second
	""" rospy.Subscriber("odom", Odometry, callback)
	rospy.Subscriber("scan", LaserScan, laser_callback) """
	rospy.spin()
if __name__ == '__main__':
	try:
		publisher()
	except rospy.ROSInterruptException:
		pass
