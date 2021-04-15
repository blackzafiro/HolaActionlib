#! /usr/bin/python3

import roslib
roslib.load_manifest('hola_actionlib')
import rospy
import actionlib

import random

from hola_actionlib.msg import DoDishesAction, DoDishesFeedback, DoDishesResult

class DoDishesServer:
  def __init__(self):
    self.server = actionlib.SimpleActionServer('do_dishes', DoDishesAction, self.execute, False)
    print("Preparing to wash the dishes...")
    
    self.server.start()
    print("Ready to wash dishes.")
    print()

  def execute(self, goal):
    """
    goal: dishwasher_id
    """
    print("Washing just began!")
    print("Using ", goal)
    
    # Do lots of awesome groundbreaking robot stuff here: wash the dishes
    for percentage in [0, 60, 100]:
        self.server.publish_feedback(DoDishesFeedback(percentage))
        rospy.sleep(1)            # Wait for the connection to complete
        
    num_dishes = random.randint(-10,10)
    
    if num_dishes > 0:
        # Everything was fine
        self.server.set_succeeded(result=DoDishesResult(num_dishes), text="Washed :)")
        print("Washing was possitive.")
    else:
        # It broke some dishes or washed none.
        result=DoDishesResult(num_dishes)
        self.server.set_aborted(result=result, text="Giving up :(")
        if num_dishes < 0:
            print("Ups! Broke some dishes.")
        else:
            print("Sort of useless.")
    print("Finished washing ", num_dishes, " dishes.")
    print()
    

if __name__ == '__main__':
  rospy.init_node('do_dishes_server')
  server = DoDishesServer()
  rospy.spin()

