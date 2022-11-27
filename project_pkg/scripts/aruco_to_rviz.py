#!/usr/bin/env python3

# Nota: 
# Se suscribe a /aruco_single/position
# Despliega un rectangulo en RVIZ 
# Publica la posision real en /panel_position

import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg

from geometry_msgs.msg import Vector3Stamped
from geometry_msgs.msg import Point

class spawn_object_moveit(object):  
    def __init__(self):
        rospy.init_node("aruco_to_rviz", anonymous=True)
        # MOVEIT CONNECTION
        self.robot = moveit_commander.RobotCommander()
        self.scene = moveit_commander.PlanningSceneInterface()
        self.group_name = "kr6_group" #----------Change
        self.move_group = moveit_commander.MoveGroupCommander(self.group_name)
        self.display_trajectory_publisher = rospy.Publisher(
            "/move_group/display_planned_path",
            moveit_msgs.msg.DisplayTrajectory,
            queue_size=20,
        )
        
        self.planning_frame = self.move_group.get_planning_frame()
        self.eef_link = self.move_group.get_end_effector_link()
        self.group_names = self.robot.get_group_names()
        self.current_state = self.robot.get_current_state()
        # END MOVEIT CONNECTION

        self.test_world = "A"

        #variables
        self.aux_pose = geometry_msgs.msg.PoseStamped()
        self.aruco_pos = [1,1,1]
        
        #topics
        rospy.Subscriber("/aruco_single/position", Vector3Stamped, self.arucoCallback)
        self.pub1=rospy.Publisher("/panel_position", Point, queue_size=1)

    def arucoCallback(self, msg):
        
        x=msg.vector.x
        y=msg.vector.y
        z=msg.vector.z

        self.aruco_pos=[z/2,-x/2+0.15,-y+0.25]

        correction = [0.0, 0.0, 0.0]

        correctionA = [0.0, 0.15, 0.0]
        correctionB = [0.0, 0.1, -0.1]
        correctionD = [0.0, 0.0, 0.25]

        if self.test_world == 'A': correction = correctionA
        if self.test_world == 'B': correction = correctionB
        if self.test_world == 'C': correction = correctionA
        if self.test_world == 'D': correction = correctionD

        self.aruco_pos[0]=self.aruco_pos[0] + correction[0]
        self.aruco_pos[1]=self.aruco_pos[1] + correction[1] 
        self.aruco_pos[2]=self.aruco_pos[2] + correction[2] 
        
        #print(self.aruco_pos)

    def spawn_box(self):
        aux_pose = self.aux_pose
        aux_pose.header.frame_id = "base_link"
        aux_pose.pose.orientation.w = 1.0
        aux_pose.pose.position.x = self.aruco_pos[0]
        aux_pose.pose.position.y = self.aruco_pos[1]
        aux_pose.pose.position.z = self.aruco_pos[2]
        box_name = "panel"
        # <size>0.6 0.025 0.40</size>
        # size=(0.025, 0.6, 0.4)
        # size=(0.025, 0.25, 0.25)
        self.scene.add_box(box_name, aux_pose, size=(0.025, 0.6, 0.4))

    def run(self):
        self.test_world = rospy.get_param('/aruco_to_rviz/test') #str
        print("************************************ RUNNING: aruco_to_rviz ************************************")
        rate = rospy.Rate(10) # 1hz --> 1/1hz=1s
        while not rospy.is_shutdown():
            self.spawn_box()
            pointmessaje = Point(self.aruco_pos[0], self.aruco_pos[1], self.aruco_pos[2])
            self.pub1.publish(pointmessaje)
            rate.sleep() # delay de 1 segundo

app = spawn_object_moveit()
app.run()