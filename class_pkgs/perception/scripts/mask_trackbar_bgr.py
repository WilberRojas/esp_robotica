#!/usr/bin/env python

import roslib
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

max_value = 255
low_B = 0
low_G = 0
low_R = 0
high_B = max_value
high_G = max_value
high_R = max_value
window_capture_name = 'Video Capture'
window_detection_name = 'Object Detection'
low_B_name = 'Low B'
low_G_name = 'Low G'
low_R_name = 'Low R'
high_B_name = 'High B'
high_G_name = 'High G'
high_R_name = 'High R'
def on_low_B_thresh_trackbar(val):
    global low_B
    global high_B
    low_B = val
    low_B = min(high_B-1, low_B)
    cv2.setTrackbarPos(low_B_name, window_detection_name, low_B)
def on_high_B_thresh_trackbar(val):
    global low_B
    global high_B
    high_B = val
    high_B = max(high_B, low_B+1)
    cv2.setTrackbarPos(high_B_name, window_detection_name, high_B)
def on_low_G_thresh_trackbar(val):
    global low_G
    global high_G
    low_G = val
    low_G = min(high_G-1, low_G)
    cv2.setTrackbarPos(low_G_name, window_detection_name, low_G)
def on_high_G_thresh_trackbar(val):
    global low_G
    global high_G
    high_G = val
    high_G = max(high_G, low_G+1)
    cv2.setTrackbarPos(high_G_name, window_detection_name, high_G)
def on_low_R_thresh_trackbar(val):
    global low_R
    global high_R
    low_R = val
    low_R = min(high_R-1, low_R)
    cv2.setTrackbarPos(low_R_name, window_detection_name, low_R)
def on_high_R_thresh_trackbar(val):
    global low_R
    global high_R
    high_R = val
    high_R = max(high_R, low_R+1)
    cv2.setTrackbarPos(high_R_name, window_detection_name, high_R)

cv2.namedWindow(window_capture_name)
cv2.namedWindow(window_detection_name)
cv2.createTrackbar(low_B_name, window_detection_name , low_B, max_value, on_low_B_thresh_trackbar)
cv2.createTrackbar(high_B_name, window_detection_name , high_B, max_value, on_high_B_thresh_trackbar)
cv2.createTrackbar(low_G_name, window_detection_name , low_G, max_value, on_low_G_thresh_trackbar)
cv2.createTrackbar(high_G_name, window_detection_name , high_G, max_value, on_high_G_thresh_trackbar)
cv2.createTrackbar(low_R_name, window_detection_name , low_R, max_value, on_low_R_thresh_trackbar)
cv2.createTrackbar(high_R_name, window_detection_name , high_R, max_value, on_high_R_thresh_trackbar)

class image_converter:

  def __init__(self):
    self.image_pub = rospy.Publisher("image_topic_2",Image)

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/diff_robot/camera/image_raw",Image,self.callback)

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    (rows,cols,channels) = cv_image.shape
    if cols > 60 and rows > 60 :
      cv2.circle(cv_image, (50,50), 10, 255)

    frame_threshold = cv2.inRange(cv_image, (low_B, low_G, low_R), (high_B, high_G, high_R))
    
    
    cv2.imshow(window_capture_name, cv_image)
    cv2.imshow(window_detection_name, frame_threshold)
    cv2.waitKey(3)

    try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
    except CvBridgeError as e:
      print(e)

def main(args):
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
