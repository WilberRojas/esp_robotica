#!/usr/bin/env python3

# Nota: Se sucribe a /panel_position, 
#       del cual, el robot obtiene su posicion objetivo
#       Se sucribe a /trigger, 
#       con el 1 se empieza a mover
#       Publica a /end_effector_position,
#       para que el modelo de gazebo lo siga


import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from moveit_commander.conversions import pose_to_list
from math import tau, dist, fabs, cos

from std_msgs.msg import Int32
from geometry_msgs.msg import Point
from detection_msgs.msg import BoundingBoxes


def all_close(goal, actual, tolerance):
    
    if type(goal) is list:
        for index in range(len(goal)):
            if abs(actual[index] - goal[index]) > tolerance:
                return False

    elif type(goal) is geometry_msgs.msg.PoseStamped:
        return all_close(goal.pose, actual.pose, tolerance)

    elif type(goal) is geometry_msgs.msg.Pose:
        x0, y0, z0, qx0, qy0, qz0, qw0 = pose_to_list(actual)
        x1, y1, z1, qx1, qy1, qz1, qw1 = pose_to_list(goal)
        # Euclidean distance
        d = dist((x1, y1, z1), (x0, y0, z0))
        # phi = angle between orientations
        cos_phi_half = fabs(qx0 * qx1 + qy0 * qy1 + qz0 * qz1 + qw0 * qw1)
        return d <= tolerance and cos_phi_half >= cos(tolerance / 2.0)

    return True


class MoveGroupPythonInterface(object):

    def __init__(self):
        super(MoveGroupPythonInterface, self).__init__()
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node("moveit_python", anonymous=True)
        robot = moveit_commander.RobotCommander()        
        scene = moveit_commander.PlanningSceneInterface()
        group_name = "kr6_group"
        move_group = moveit_commander.MoveGroupCommander(group_name)       
        display_trajectory_publisher = rospy.Publisher(
            "/move_group/display_planned_path",
            moveit_msgs.msg.DisplayTrajectory,
            queue_size=20,
        )
       
        planning_frame = move_group.get_planning_frame()       
        eef_link = move_group.get_end_effector_link()        
        group_names = robot.get_group_names()       
        current_state = robot.get_current_state()    

        # Misc variables
        self.box_name = ""
        self.robot = robot
        self.scene = scene
        self.move_group = move_group
        self.display_trajectory_publisher = display_trajectory_publisher
        self.planning_frame = planning_frame
        self.eef_link = eef_link
        self.group_names = group_names

    def get_position(self):
        move_group = self.move_group
        joint_goal = move_group.get_current_joint_values() #joints
        wpose = move_group.get_current_pose().pose #cartesian
        joint_list2 = []
        for index, data in enumerate(joint_goal):
            #print("joint_goal["+str(index)+"] = " + str(round(data,2)))  
            joint_list2.append(round(data,4))
        """ print("in list:", joint_list2)
        print("X:", wpose.position.x, "  Y:", wpose.position.y) """
        return [wpose.position.x, wpose.position.y, wpose.position.z]
   
    def cartesian_move(self, position):
        move_group = self.move_group
        waypoints = []

        wpose = move_group.get_current_pose().pose
        try:
            wpose.position.x = position[0]
            wpose.position.y = position[1]
            wpose.position.z = position[2]
        except:
            pass

        waypoints.append(copy.deepcopy(wpose))  
        
        (plan, fraction) = move_group.compute_cartesian_path(
            waypoints, 0.01, 0.0  # waypoints to follow  # eef_step
        )  # jump_threshold
        move_group.execute(plan, wait=True)
    
    
    
    def go_to_home(self):
        move_group = self.move_group
        joint_goal = move_group.get_current_joint_values()

        joint_goal[0] = 0
        joint_goal[1] = -tau/4
        joint_goal[2] = tau/4
        joint_goal[3] = 0
        joint_goal[4] = 0 #tau/4
        joint_goal[5] = 0

        move_group.go(joint_goal, wait=True)
        
        move_group.stop()

        # For testing:
        current_joints = move_group.get_current_joint_values()
        return all_close(joint_goal, current_joints, 0.01)
            
    #END CLASS

class class2(object):
    def __init__(self):
        rospy.Subscriber("/panel_position", Point, self.goal_Callback)
        rospy.Subscriber("/trigger", Int32, self.triggerCallback)
        rospy.Subscriber("/yolov5/detections", BoundingBoxes, self.yolo_Callback)
        self.pub1=rospy.Publisher("/end_effector_position", Point, queue_size=1)

        self.robot1 = MoveGroupPythonInterface()
        self.kuka_position = [0.25, 0.0, 0.6]
        self.yolo_detection = False
        self.aruco_detection = False

        self.arucoID = None
        self.detection_class = None
        self.test_world = None     

        self.aux_initial_aruco_pos = []
        self.aux_counter = 0

    def yolo_Callback(self, msg):
        rate = rospy.Rate(100)
        for bbox in msg.bounding_boxes:
            detection = bbox.Class
            if detection == self.detection_class:
                self.yolo_detection = True
        #print("DETECTION: ", detection)
        rate.sleep()

    def goal_Callback(self, msg):

        correction = [-0.1, 0.0, 0.0]

        x=msg.x + correction[0]
        y=msg.y + correction[1]
        z=msg.z + correction[2]

        self.kuka_position=[x,y,z]
        if self.aux_counter == 0:
            self.aux_initial_aruco_pos = self.kuka_position
            print(self.aux_initial_aruco_pos)
            self.aux_counter += 1

        if self.kuka_position != self.aux_initial_aruco_pos:
            self.aruco_detection = True

    def triggerCallback(self,msg):
        if(msg.data==1):
            #print("Detection: "+self.yolo_detection, "ArucoID: ")
            if self.yolo_detection and self.aruco_detection:
                self.robot1.go_to_home()
                self.robot1.cartesian_move(self.kuka_position)
                self.robot1.go_to_home()
                self.robot1.cartesian_move(self.kuka_position)
            else:
                self.robot1.cartesian_move([0.25, 0.0, 0.6])

    def run(self):
        print("************************************ RUNNING: moveit_python ************************************")
        rate = rospy.Rate(1) # 10hz --> 1/10hz=0.1s
        self.arucoID = rospy.get_param('/moveit_python/aruco') #int
        self.detection_class = rospy.get_param('/moveit_python/detection') #str
        self.test_world = rospy.get_param('/moveit_python/test') #str
        
        while not rospy.is_shutdown():           
            print(self.detection_class + " : " + str(self.yolo_detection), "| Aruco " + str(self.arucoID) + " : " + str(self.aruco_detection)) 
            positions_list = self.robot1.get_position()            
            pointmessaje = Point(positions_list[0], positions_list[1], positions_list[2])
            self.pub1.publish(pointmessaje)
            rate.sleep() # delay de 0.1 segundo

app = class2()
app.run()