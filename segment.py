# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 2019

@author: student
"""

import rospy
import cv2
import numpy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import String



class image_converter:

    def __init__(self):

        cv2.startWindowThread()
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",
                                          Image, self.callback)                       

    def callback(self, data):
        pub = rospy.Publisher('hue', String, queue_size=10)
                
        cv2.namedWindow("Image window", 1)
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError, e:
            print e

        bgr_thresh = cv2.inRange(cv_image,
                                 numpy.array((200, 230, 230)),
                                 numpy.array((255, 255, 255)))

        hsv_img = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        hsv_thresh = cv2.inRange(hsv_img,
                                 numpy.array((90, 150, 0)),
                                 numpy.array((180, 255, 255)))
                                 
        lower_red = numpy.array([90,150,0])
        upper_red = numpy.array([180,255,255])

        print numpy.mean(hsv_img[:, :, 0])
        print numpy.mean(hsv_img[:, :, 1])
        print numpy.mean(hsv_img[:, :, 2])

        _, bgr_contours, hierachy = cv2.findContours(
            bgr_thresh.copy(),
            cv2.RETR_TREE,
            cv2.CHAIN_APPROX_SIMPLE)

        _, hsv_contours, hierachy = cv2.findContours(
            hsv_thresh.copy(),
            cv2.RETR_TREE,
            cv2.CHAIN_APPROX_SIMPLE)
        for c in hsv_contours:
            a = cv2.contourArea(c)
            if a > 100.0:
                cv2.drawContours(cv_image, c, -1, (255, 0, 0))
        print '===='
        cv2.imshow("Image window", cv_image)
        
        mask = cv2.inRange(hsv_img, lower_red, upper_red)
        res = cv2.bitwise_and(cv_image,cv_image, mask= mask) 
        
        cv2.imshow('mask',mask)
        cv2.imshow('res',res)
    
        cv2.waitKey(1)
        
        
        
        mean = "the intesity is b %s" % numpy.mean(hsv_img[:, :, 0])
        mean2 = "the intesity is g %s" % numpy.mean(hsv_img[:, :, 1])
        mean3 = "the intesity is r %s" % numpy.mean(hsv_img[:, :, 2])
        rospy.loginfo(mean)
        rospy.loginfo(mean2)
        rospy.loginfo(mean3)
        pub.publish(mean)
        pub.publish(mean2)
        pub.publish(mean3)
        

image_converter()
rospy.init_node('image_converter', anonymous=True)
rospy.spin()
cv2.destroyAllWindows()
