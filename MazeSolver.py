'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.
   This is a program that is provided to students in Robot AI class.
   Students use this it to build different Hamster behaviors.

   Name:          tk_behaviors_starter.py
   By:            Qin Chen
   Last Updated:  5/10/18

   PROPRIETARY and CONFIDENTIAL
   ========================================================================*/
'''
import sys
import time
import threading
import Tkinter as tk
from HamsterAPI.comm_ble import RobotComm	# no dongle
#from HamsterAPI.comm_usb import RobotComm	# yes dongle

################################
# Hamster control
################################
class RobotBehaviorThread(threading.Thread):
	def __init__(self, robotList):
		super(RobotBehaviorThread, self).__init__()
		self.maze = False
		self.done = False
		self.robotList = robotList
		return

	def run(self):
		robot=None
		while not self.done:
			for robot in self.robotList:
				if robot and self.maze:
					# print "motion handler start"
					print (str(robot.get_proximity(0)) + " " + str(robot.get_proximity(1)))
					if (robot.get_proximity(1) < 3):
						robot.set_wheel(0, 30)
						robot.set_wheel(1, -30)
					elif (robot.get_proximity(1) > 3 and robot.get_proximity(0) > 70):
						robot.set_wheel(0, -30)
						robot.set_wheel(1, 30)
					# elif(currentEvent.type == "straight"):
					else:
						robot.set_wheel(0, 30)
						robot.set_wheel(1, 30)


				

		# stop robot activities, such as motion, LEDs and sound
		# clean up after exit button pressed
		if robot:
			robot.reset()
			time.sleep(0.1)
		return

class GUI(object):
	def __init__(self, root, robot_control):
		self.root = root
		self.robot_control = robot_control
		root.geometry('500x30')
		root.title('Hamster Control')

		b1 = tk.Button(root, text='Maze Solver')
		b1.pack(side='left')
		b1.bind('<Button-1>', self.mazeProg)

		
		exitButton = tk.Button(root, text='Exit')
		exitButton.pack(side='right')
		exitButton.bind('<Button-1>', self.stopProg)	
		return

	def mazeProg(self, event=None):
		self.robot_control.maze = True
		return

	
	def stopProg(self, event=None):
		self.robot_control.done = True		
		self.root.quit() 	# close window
		return


#################################
# Don't change any code below!! #
#################################

def main():
    # instantiate COMM object
    gMaxRobotNum = 1; # max number of robots to control
    comm = RobotComm(gMaxRobotNum)
    comm.start()
    print 'Bluetooth starts'  
    robotList = comm.robotList

    behaviors = RobotBehaviorThread(robotList)
    behaviors.start()

    frame = tk.Tk()
    GUI(frame, behaviors)
    frame.mainloop()

    comm.stop()
    comm.join()
    print("terminated!")

if __name__ == "__main__":
    sys.exit(main())