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
	def __init__(self, robot_list):
		super(RobotBehaviorThread, self).__init__()
		self.done = False   # set by GUI button
		self.go = False     # set by GUI button
		self.robot_list = robot_list
		# self.robot = None
		self.angle = 90
		self.direction = "north"
		self.plan = []
		self.reached_goal = False
		return

	def make_plan(self, p):
		print "make_plan"
		path = list(p)
		while path:
			currentNode = path.pop(0)
			if (not path):
				break
			curNode_dashIndex = currentNode.find('-')
			curNode_row = int(currentNode[:curNode_dashIndex])
			curNode_col = int(currentNode[curNode_dashIndex+1:])

			nextNode_dashIndex = path[0].find('-')
			nextNode_row = int(path[0][:nextNode_dashIndex])
			nextNode_col = int(path[0][nextNode_dashIndex+1:])

			if (nextNode_row == curNode_row + 1):
					self.plan.append("move_north")
			if (nextNode_row == curNode_row - 1):
				self.plan.append("move_south")
			if (nextNode_col == curNode_col + 1):
				self.plan.append("move_east")
			if (nextNode_col == curNode_col - 1):
				self.plan.append("move_west")
		self.plan.append("stop")

	def run(self):
		while not self.done:
			if self.robot_list:
				self.robot = self.robot_list[0]
				self.go_forward
				while not self.reached_goal and self.go and self.plan:
					step = "self." + self.plan.pop(0) + "()"
					eval(step)

	def move_north(self):
		if (self.direction == "east"):
			self.turn_left()
		elif (self.direction == "west"):
			self.turn_right()
		elif (self.direction == "south"):
			self.turn_right()
			self.turn_right()
		self.go_forward()
		self.direction = "north"

	def move_south(self):
		if (self.direction == "east"):
			self.turn_right()
		elif (self.direction == "west"):
			self.turn_left()
		elif (self.direction == "north"):
			self.turn_right()
			self.turn_right()
		self.go_forward()
		self.direction = "south"

	def move_east(self):
		if (self.direction == "north"):
			self.turn_right()
		elif (self.direction == "south"):
			self.turn_left()
		elif (self.direction == "west"):
			self.turn_right()
			self.turn_right()
		self.go_forward()
		self.direction = "east"

	def move_west(self):
		if (self.direction == "north"):
			self.turn_left()
		elif (self.direction == "south"):
			self.turn_right()
		elif (self.direction == "east"):
			self.turn_right()
			self.turn_right()
		self.go_forward()
		self.direction = "west"

	def go_forward(self):
		time.sleep(0.5)
		while (self.robot.get_floor(0) > 70 or self.robot.get_floor(1) > 70):
			if (self.robot.get_floor(0) < 70):
				self.robot.set_wheel(0, 30)
				self.robot.set_wheel(1, 60)
			elif (self.robot.get_floor(1) < 70):
				self.robot.set_wheel(0, 60)
				self.robot.set_wheel(1, 30)
			else:
				self.robot.set_wheel(0, 30)
				self.robot.set_wheel(1, 30)
		self.robot.set_wheel(0, 30)
		self.robot.set_wheel(1, 30)
		time.sleep(0.2)


	def turn_left(self):
		self.robot.set_wheel(0, -30)
		self.robot.set_wheel(1, 30)
		time.sleep(0.25)

	def turn_right(self):
		self.robot.set_wheel(0, 30)
		self.robot.set_wheel(1, -30)
		time.sleep(0.2)

	def stop(self):
		self.robot.set_wheel(0, 0)
		self.robot.set_wheel(1, 0)