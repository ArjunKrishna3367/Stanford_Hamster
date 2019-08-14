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
		self.square = False
		self.shy = False
		self.follow = False
		self.dance = False
		self.lineFollow = False
		self.done = False
		self.robotList = robotList
		return

	def run(self):
		robot=None
		while not self.done:
			for robot in self.robotList:
				if robot and self.square:
					while(True):
						t0 = time.time()
						while(time.time() - t0 < 2.0):
							robot.set_wheel(0, 30)
							robot.set_wheel(1, 30)
								# print time.time() - t0
						while(time.time() - t0 > 2.0 and time.time() - t0 < 2.833):
							robot.set_wheel(0, -30)
							robot.set_wheel(1, 30)


				if robot and self.shy:
					#############################################
					# START OF YOUR WORKING AREA!!!
					#############################################
					while (robot.get_proximity(0) > 20 or robot.get_proximity(1) > 20):
						robot.set_wheel(0, -30)
						robot.set_wheel(1, -30)
					robot.set_wheel(0, 0)
					robot.set_wheel(1, 0)						
					#############################################
					# END OF YOUR WORKING AREA!!!
					#############################################	
				if robot and self.follow:
					while (robot.get_proximity(0) < 20 or robot.get_proximity(1) < 20):
						if (robot.get_proximity(0) < robot.get_proximity(1)):
							robot.set_wheel(0, 35)
							robot.set_wheel(1, 30)
						elif (robot.get_proximity(0) > robot.get_proximity(1)):
							robot.set_wheel(0, 30)
							robot.set_wheel(1, 35)
						else:
							robot.set_wheel(0, 0)
							robot.set_wheel(1, 0)

				if robot and self.dance:
					if (robot.get_proximity(0) > 20 or robot.get_proximity(1) > 20):
						robot.set_wheel(0, -30)
						robot.set_wheel(1, -30)
						time.sleep(0.5)
					elif (robot.get_proximity(0) < 20 or robot.get_proximity(1) < 20):
						robot.set_wheel(0, 30)
						robot.set_wheel(1, 30)

				if robot and self.lineFollow:
					print robot.get_floor(0)
					robot.set_wheel(0, 30)
					robot.set_wheel(1, 30)
					if(robot.get_floor(0) < 70):
						print "true"
						robot.set_wheel(0, -30)
						robot.set_wheel(1, 100)
					elif(robot.get_floor(1) < 70):
						robot.set_wheel(0, 100)
						robot.set_wheel(1, -30)
					else:
						robot.set_wheel(0, 30)
						robot.set_wheel(1, 30)
					# if(robot.get_floor(1) > 80):
					# 	robot.set_wheel(0, 60)
					# 	robot.set_wheel(1, 30)
					# if(robot.get_floor(0) > 80):
					# 	robot.set_wheel(0, 30)
					# 	robot.set_wheel(0, 60)
					# robot.set_line_tracer_mode_speed(0x11, 7)
					

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

		b1 = tk.Button(root, text='Square')
		b1.pack(side='left')
		b1.bind('<Button-1>', self.squareProg)

		b2 = tk.Button(root, text='Shy')
		b2.pack(side='left')
		b2.bind('<Button-1>', self.shyProg)

		b3 = tk.Button(root, text='Follow')
		b3.pack(side='left')
		b3.bind('<Button-1>', self.followProg)

		b4 = tk.Button(root, text='Dance')
		b4.pack(side='left')
		b4.bind('<Button-1>', self.danceProg)

		b5 = tk.Button(root, text='Line Follow')
		b5.pack(side='left')
		b5.bind('<Button-1>', self.lineFollowProg)

		exitButton = tk.Button(root, text='Exit')
		exitButton.pack(side='right')
		exitButton.bind('<Button-1>', self.stopProg)	
		return

	def squareProg(self, event=None):
		self.robot_control.square = True
		return

	def shyProg(self, event=None):
		self.robot_control.shy = True
		return

	def followProg(self, event=None):
		self.robot_control.follow = True
		return

	def danceProg(self, event=None):
		self.robot_control.dance = True
		return

	def lineFollowProg(self, event=None):
		self.robot_control.lineFollow = True
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
    gMaxRobotNum = 1 # max number of robots to control
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