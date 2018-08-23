import rospy
import actionlib

from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalStatus
from tf.transformations import quaternion_from_euler

def execute(self, inputs, outputs, gvm):
    x = inputs["goal_x"]
    y = inputs["goal_y"]
    phi = inputs["goal_phi"]
    frame = inputs["ref_frame"]
    self.logger.info("Setting goal: " + str(x) + " " + str(y) + " " + str(phi))
    
    # setup move_base client
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()
    rate = rospy.Rate(10)

    q = quaternion_from_euler(0, 0, phi)
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = frame
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.orientation.x = q[0]
    goal.target_pose.pose.orientation.y = q[1]
    goal.target_pose.pose.orientation.z = q[2]
    goal.target_pose.pose.orientation.w = q[3]

    client.send_goal(goal)
#    wait = client.wait_for_result()
    
    while client.get_state() == GoalStatus.PENDING:
       self.logger.info("Waiting for goal to be recieved")
    
    
    while client.get_state() == GoalStatus.ACTIVE:
       self.logger.info("Still navigating!")
       rate.sleep()

    
    return 0
