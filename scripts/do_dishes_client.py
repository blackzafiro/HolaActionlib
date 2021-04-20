#! /usr/bin/python3

import roslib
roslib.load_manifest('hola_actionlib')
import rospy
import actionlib

from actionlib_msgs.msg import GoalStatus
from hola_actionlib.msg import DoDishesAction, DoDishesGoal

import random


ya_termino = False

    
def terminamos(state, total_dishes_cleaned):
    """
    Called when process transits to Done.
    
    The client decides here what to do once the server is done.
    state: integer code
    total_dishes_cleaned: from DoDishesResult
    """
    if state == GoalStatus.SUCCEEDED:
        #     The work of the client continues from here once the goal is accomplished.
        print("SUCCEEDED")
        print("[From server] ", total_dishes_cleaned)
        print("    Server washed the dishes")
    elif state == GoalStatus.PREEMPTED:
        print("PREEMPTED")
        print("    Whashig was canceled, canceling is complete.")
    elif state == GoalStatus.ABORTED:
        print("ABORTED")
        print("[From server] Washing failed: ", total_dishes_cleaned)
    elif state == GoalStatus.REJECTED:
        print("REJECTED")
        print("    Couldn't wash.")
    elif state == GoalStatus.RECALLED:
        print("RECALLED")
        print("    Washing was canceled before beginning.")
    else:
        print("Something else: ", state)
    global ya_termino
    ya_termino = True
    
def meta_activa():
    """
    Called whenever the goal transits to Active
    """
    print("Server says it is washing our dishes...")

def recibe_reporte(feeback_msg):
    """
    Called everytime the server wants to send feedback.
    feeback_msg: DoDishesFeedback
    """
    print("[From server] ", feeback_msg)
    rospy.sleep(1)


if __name__ == '__main__':
    rospy.init_node('do_dishes_client')
    
    print("Requesting dishwashing...")
    client = actionlib.SimpleActionClient('do_dishes', DoDishesAction)
    client.wait_for_server()
    rospy.sleep(1)
    print("Server received request...")

    # User randomdishwasher with ID = ?
    dishwasher_id = random.randint(1,10)
    goal = DoDishesGoal(dishwasher_id)
    # Fill in the goal here
    client.send_goal(goal, done_cb=terminamos,
                           active_cb=meta_activa,
                           feedback_cb=recibe_reporte)
    
    print("Goal sent to server ...")
    #client.wait_for_result(rospy.Duration.from_sec(15.0))
    
    rate = rospy.Rate(10) # 10hz
    while not ya_termino:
        rate.sleep()
    # O intentar con esto otro:
    # rospy.spin()

    #print("No dejemos al servidor lavando solo.")
    #while not ya_termino:
    #    rospy.sleep(1)
    #rospy.sleep(1)
    #print("Termina la ejecución del cliente")
    
