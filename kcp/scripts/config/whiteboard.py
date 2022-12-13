#!/usr/bin/env python3
import rospy
import moveit_commander
import moveit_msgs.msg

from sympy import*
import numpy as np 

import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError




rospy.init_node('whiteboard', anonymous=True)

class Main:
    def __init__(self):

        robot = moveit_commander.RobotCommander()        
        scene = moveit_commander.PlanningSceneInterface()
        group_name = "kuka6"
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
        dist_kuka_piso = 0.8
    
        self.bridge = CvBridge()
        self.image_pub = rospy.Publisher("/whiteboard",Image, queue_size=1)
    
        self.size_whiteboard = 500
        self.color_text = (10, 10, 10)
        #template
        self.template = np.zeros((int(self.size_whiteboard*0.75), self.size_whiteboard, 3), dtype=np.uint8)
        self.template.fill(255) #Fondo blanco
        cv2.putText(self.template, 'Pizarra', (190, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, self.color_text, 2, cv2.LINE_AA)
        hoja_p1 = (50, 55)
        hoja_p2 = (447, 338)
        cv2.rectangle(self.template, hoja_p1, hoja_p2, self.color_text, 3)
        #cv2.circle(self.template, (245, 196), 3, self.color_text, -1)
        #frame
        self.whiteboard = self.template.copy()
        #template 2
        self.template_number = np.zeros((int(self.size_whiteboard*0.1), self.size_whiteboard, 3), dtype=np.uint8)
        self.template_number.fill(255) #Fondo blanco

        #corrections
        self.previus_x_pix = 0
        self.previus_y_pix = 0
        self.previus_z = 0



    def joint_callback(self, msg):

        # se recibe las pocisiones en un mensaje JointState
        angle1=msg.position[0]
        angle2=msg.position[1] 
        angle3=msg.position[2]
        angle4=msg.position[3]
        angle5=msg.position[4]

        # se aplica la multiplicacion de matrice
        T03n=self.T0N.subs([(j1,angle1),
                        (j2,angle2),
                        (j3,angle3),
                        (j4,angle4),
                        (j5,angle5)])

        # se obtiene X,Y,Z
        x_point = T03n[0,3]
        y_point = T03n[1,3]
        z_point = T03n[2,3]

        # Se borra la imagen si:
        if angle1 > 10:
            self.whiteboard = self.template.copy()

        # Rango de Z en que puede rayar:
        max_z = 0.155 #metros, se puede ver el dato actual en RVIZ
        min_z = 0.15 #metros

        #-----------Numero en otro frame
        distance_frame = self.template_number.copy()
        if z_point >= min_z:
            if z_point <= max_z:
                self.color_text = (10, 200, 10)
            else:
                self.color_text = (200, 10, 10)
            diff_z_cm = (z_point - min_z)*100
            algo = "%.2f" % diff_z_cm
            #print (algo, type(algo))
            cv2.putText(distance_frame, 'Tool: +' + algo + "cm", (40, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.color_text, 1, cv2.LINE_AA)
        else: 
            self.color_text = (10, 10, 200)
            cv2.putText(distance_frame, "Tool: COLLISION!", (50, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.color_text, 1, cv2.LINE_AA)

        if(z_point > min_z and z_point < max_z):
            zoom=1
            # ------- va de [-y, +y]
            y1 = 0.3 # extremo positivo
            x_pix = ((y_point + y1)/(2*y1)) * self.size_whiteboard * zoom

            # ------- va de [+x1, +x2]
            x1 = 0.4 # punto inicio
            x2 = 0.8 # punto fin
            y_pix = ((x_point - x1)/(x2-x1)) * self.size_whiteboard*0.75 * zoom

            #cv2.circle(self.whiteboard, (int(x_pix), int(y_pix)), 5, (255, 20, 20), -1)
            
            if(self.previus_z > min_z and self.previus_z < max_z):
                #print("distance OK:", round(self.previus_z*100,2), round(z_point*100,2))
                if self.previus_x_pix!=0:
                    if self.previus_x_pix != x_pix and self.previus_y_pix != y_pix:
                        #print("Line OK", (self.previus_x_pix, self.previus_y_pix), (int(x_pix), int(y_pix)))
                        cv2.line(self.whiteboard, (int(x_pix), int(y_pix)), (self.previus_x_pix, self.previus_y_pix), (0, 255, 0), thickness=5)
                
            self.previus_z = z_point
            self.previus_x_pix = int(x_pix)
            self.previus_y_pix = int(y_pix)
        else:
            self.previus_z = 0
            self.previus_x_pix = 0
            self.previus_y_pix = 0

        output_frame = im_v = cv2.vconcat([distance_frame, self.whiteboard])        
        image_msg = self.bridge.cv2_to_imgmsg(output_frame,"bgr8")
        self.image_pub.publish(image_msg)
    
    def run(self):
        rospy.spin()        

app = Main()
app.run()