#!/usr/bin/env python
import rospy
from sympy import*
import numpy as np
from std_msgs.msg import String
from geometry_msgs.msg import Point
from sensor_msgs.msg import JointState

t1=Symbol('t1')
t2=Symbol('t2')
t3=Symbol('t3')
t4=Symbol('t4')
t5=Symbol('t5')
t6=Symbol('t6')
pub = rospy.Publisher('/kuka_pos', Point, queue_size=10)
kuka_point=Point()
def dh_matrix (t,d,a,aph):

	T=Matrix([[cos(t), -sin(t)*cos(aph),sin(t)*sin(aph), a*cos(t)],[sin(t), cos(t)*cos(aph), -cos(t)*sin(aph), a*sin(t)],[0,sin(aph), cos(aph), d],[0, 0, 0, 1]])
	return T


T01=dh_matrix(pi,0,0,pi)
T12=dh_matrix(t1+pi,-0.4,0.025,pi/2)
T23=dh_matrix(t2,0,0.455,0)
T34=dh_matrix(t3-pi/2,0,0.035,pi/2)
T45=dh_matrix(t4+pi,-0.42,0,pi/2)
T5p=dh_matrix(t5+pi,0,0,pi/2)
T56=dh_matrix(0,-0.08,0,0)
T67=dh_matrix(t6,0,0,0)

T02=T01*T12
T03=T02*T23
T04=T03*T34
T05=T04*T45
T06=T05*T5p
T07=T06*T56
T08=T07*T67

print("x= ", T08[0,3])
print("y= ", T08[1,3])
print("z= ", T08[2,3])
print("---------------------------------")
def joint_callback(msg):
	angle1=msg.position[0]
	angle2=msg.position[1]
	angle3=msg.position[2]
	angle4=msg.position[3]
	angle5=msg.position[4]
	angle6=msg.position[5]
	T08n=T08.subs([(t1,angle1),(t2,angle2),(t3,angle3),(t4,angle4),(t5,angle5),(t6,angle6)])
	print("x= ", T08n[0,3])
	print("y= ", T08n[1,3])
	print("z= ", T08n[2,3])
	print("---------------------------------")
	kuka_point.x=T08n[0,3]
	kuka_point.y=T08n[1,3]
	kuka_point.z=T08n[2,3]
	pub.publish(kuka_point)
def subscriber():
    rospy.init_node('fk_kr6', anonymous=True)
    rospy.Subscriber("joint_states", JointState, joint_callback)
    rospy.spin()
if __name__ == '__main__':
    subscriber()
