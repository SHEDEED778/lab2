#!/usr/bin/env python

import rospy
import actionlib
from birthday_cake.msg import CakeAction, CakeGoal
from MakeCakes.srv import CakeType, CakeTypeResponse

def make_cakes():
    client = actionlib.SimpleActionClient('cake_maker', CakeAction)
    client.wait_for_server()
    rospy.loginfo("Connected to cake_maker server")
    
    for i in range(3):
        goal = CakeGoal()
        goal.cake_type = i+1
        client.send_goal(goal)
        rospy.loginfo("Making Cake %d", i+1)
        client.wait_for_result()
        result = client.get_result()
        rospy.loginfo(result.message)
    
    rospy.loginfo("Cakes have been made. Enjoy!")

def handle_cake_type(req):
    month = rospy.get_param('/current_month')
    if month != 12:
        return CakeTypeResponse("It's not December yet. Please wait.")
    else:
        return CakeTypeResponse("Happy 25th birthday! Please make me some cakes.")

if _name_ == '_main_':
    rospy.init_node('app2')
    rospy.wait_for_param('/current_month')
    s = rospy.Service('cake_request', CakeType, handle_cake_type)
    rospy.loginfo("Waiting for cake request...")
    make_cakes()
