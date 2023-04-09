#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from birthday_cake.srv import Cake
from birthday_cake.msg import MakeCakesAction, MakeCakesResult, MakeCakesFeedback
import actionlib

rospy.init_node('app1')

# Create a service proxy to call the Cake service provided by app2
rospy.wait_for_service('/app2/cake_service')
cake_service = rospy.ServiceProxy('/app2/cake_service', Cake)

# Create an action client to call the MakeCakes action provided by app1
client = actionlib.SimpleActionClient('/app1/make_cakes', MakeCakesAction)
client.wait_for_server()

# Define the callback function to monitor the progress of the MakeCakes action
def feedback_cb(feedback):
    rospy.loginfo(feedback.status)

# Send a message to app2 for each month of the year
for month in range(1, 13):
    rospy.loginfo('Sending message for month %d', month)
    result = cake_service(month)
    rospy.loginfo('Received message from app2: %s', result.result)

# Send a message to app2 to wish a happy birthday on the 25th of December
if datetime.datetime.now().month == 12 and datetime.datetime.now().day == 25:
    rospy.loginfo('Sending happy birthday message')
    result = cake_service(0)
    rospy.loginfo('Received message from app2: %s', result.result)

# Call the MakeCakes action to request app2 to make 3 cakes
rospy.loginfo('Requesting app2 to make 3 cakes')
goal = MakeCakesAction(number_of_cakes=3)
client.send_goal(goal, feedback_cb=feedback_cb)

# Wait for the MakeCakes action to finish
client.wait_for_result()

# Log the result of the MakeCakes action
result = client.get_result()
if result.success_message:
    rospy.loginfo(result.success_message)
else:
    rospy.logerr(result.failure_message)
