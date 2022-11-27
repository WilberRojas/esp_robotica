#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
import csv
import math
from tf.transformations import euler_from_quaternion

#def callback(data):
#    roll_x, pitch_y, yaw_z = euler_from_quaternion(data.pose.orientation.x, data.pose.orientation.y, data.pose.orientation.z, data.pose.orientation.w)
#    print("roll:", roll_x)
#    print("pitch:", pitch_y)
#    print("yaw:", yaw_z)

def callback(data):
    euler_angles = euler_from_quaternion ([data.pose.orientation.x, data.pose.orientation.y, data.pose.orientation.z, data.pose.orientation.w])
    print("roll:", euler_angles[0])
    print("pitch:", euler_angles[1])
    print("yaw:", euler_angles[2])

def track_marker():
    rospy.init_node('euler_pose', anonymous=True)
    rospy.Subscriber('/aruco_single/pose', PoseStamped, callback)
    rospy.spin()

# source: https://automaticaddison.com/how-to-convert-a-quaternion-into-euler-angles-in-python/
#def euler_from_quaternion(x, y, z, w):
#    """
#    Convert a quaternion into euler angles (roll, pitch, yaw)
#    roll is rotation around x in radians (counterclockwise)
#    pitch is rotation around y in radians (counterclockwise)
#    yaw is rotation around z in radians (counterclockwise)
#    """
#    t0 = +2.0 * (w * x + y * z)
#    t1 = +1.0 - 2.0 * (x * x + y * y)
#    roll_x = math.atan2(t0, t1)
     
#    t2 = +2.0 * (w * y - z * x)
#    t2 = +1.0 if t2 > +1.0 else t2
#    t2 = -1.0 if t2 < -1.0 else t2
#    pitch_y = math.asin(t2)
     
#    t3 = +2.0 * (w * z + x * y)
#    t4 = +1.0 - 2.0 * (y * y + z * z)
#    yaw_z = math.atan2(t3, t4)
     
#    return roll_x, pitch_y, yaw_z # in radians

if __name__ == '__main__':
    print('Orientation in euler angles format .......')
    track_marker()
