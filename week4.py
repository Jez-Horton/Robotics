# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 12:44:14 2019
@author: student
"""
"""
Spyder Editor
This is a temporary script file.
"""

#!/usr/bin/env python


import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32

wheel_radius = 0.076
robot_radius = 0.025

# computing the forward kinematics for a differential drive
def forward_kinematics(w_l, w_r):
    c_l = wheel_radius * w_l
    c_r = wheel_radius * w_r
    v = (c_l + c_r) / 2
    a = (c_r - c_l) / (2 * robot_radius)
    return (v, a)


# computing the inverse kinematics for a differential drive
def inverse_kinematics(v, a):
    c_l = v - (robot_radius * a) 
    c_r = v + (robot_radius * a) 
    w_l = c_l / wheel_radius
    w_r = c_r / wheel_radius
    return (w_l, w_r)


# inverse kinematics from a Twist message (This is what a ROS robot has to do)
def inverse_kinematics_from_twist(t):
    return inverse_kinematics(t.linear.x, t.angular.z)


class robot_wheel_controller:
    
    def __init__(self):
        
        rospy.Rate(10)
        self.wheels_please_pub = rospy.Subscriber("/wheels_please", Float32, self.callback)
        #self.wheel_left_vel_sub = rospy.Publisher("/wheel_vel_left", Float32, queue_size=10)
        self.vel_pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)
        #self.vel_sub = rospy.Subscriber("/wheels_please", self.callback, Float32)
            
    
    def callback(self, data):
           print("hello")
           (v, a) = forward_kinematics(data.data, 0.0)
           print "\n\nForward Kinematics\nv = %f,\ta = %f" % (v, a)

           vel_data = Twist()
           vel_data.linear.x = v
           vel_data.angular.z = a
           self.vel_pub.publish(vel_data)
            
print('Hello')

rospy.init_node('robot_wheel_controller')
iv = robot_wheel_controller()
rospy.spin()
