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
		self.direction = "up"
		self.plan = []
		self.path = []
		self.reached_goal = False
		self.step_count = 0
		return

	def make_plan(self, o, height):
		# print "make_plan"
		order = list(o)
		# print order
		temp = {}
		for node in order:
			# temp[node] = str(order.index(node)/height) + '-' + str(order.index(node)%height)
			temp[node] = str(order.index(node)%height) + '-' + str(order.index(node)/height)
		for key in temp:
			self.path.append(temp[key])
		return self.path
		

	def path_to_plan(self):
		while self.path:
			currentNode = self.path.pop(0)
			if (not self.path):
				break
			curNode_dashIndex = currentNode.find('-')
			curNode_row = int(currentNode[:curNode_dashIndex])
			curNode_col = int(currentNode[curNode_dashIndex+1:])

			nextNode_dashIndex = self.path[0].find('-')
			nextNode_row = int(self.path[0][:nextNode_dashIndex])
			nextNode_col = int(self.path[0][nextNode_dashIndex+1:])
			#first dir is 2 spaces, second is 1
			#for ex, move_up_right means 2 spaces up and 1 right
			if (nextNode_row == curNode_row + 2 and nextNode_col == curNode_col + 1):
					self.plan.append("up_right")
			if (nextNode_row == curNode_row + 2 and nextNode_col == curNode_col - 1):
					self.plan.append("up_left")
			if (nextNode_row == curNode_row - 2 and nextNode_col == curNode_col + 1):
					self.plan.append("down_right")
			if (nextNode_row == curNode_row - 2 and nextNode_col == curNode_col - 1):
					self.plan.append("down_left")
			if (nextNode_row == curNode_row + 1 and nextNode_col == curNode_col + 2):
					self.plan.append("right_up")
			if (nextNode_row == curNode_row - 1 and nextNode_col == curNode_col + 2):
					self.plan.append("right_down")
			if (nextNode_row == curNode_row + 1 and nextNode_col == curNode_col - 2):
					self.plan.append("left_up")
			if (nextNode_row == curNode_row - 1 and nextNode_col == curNode_col - 2):
					self.plan.append("left_down")
		self.plan.append("stop")


	def run(self):
		while not self.done:
			if self.robot_list:
				self.robot = self.robot_list[0]
				while not self.done and self.go and self.plan:
					# self.go_forward()
					self.complete_step(self.plan.pop(0))
					if (self.done):
						break


	def complete_step(self, step):
		step_index = step.find('_')
		print step
		part1 = step[:step_index]
		part2 = step[step_index+1:]
		eval("self.orient_" + part1 + "()")
		self.go_forward()
		self.go_forward()
		eval("self.orient_" + part2 + "()")
		self.go_forward()
		self.direction = part2
		self.step_count += 1
		print self.step_count
		self.robot.set_wheel(0, 0)
		self.robot.set_wheel(1, 0)
		self.robot.set_musical_note(40)
		time.sleep(0.5)
		self.robot.set_musical_note(0)
		
	def go_forward(self):
		# print "go_forward"
		# time.sleep(0.5)
		# while (self.robot.get_floor(0) > 70 or self.robot.get_floor(1) > 70):
		# 	if (self.robot.get_floor(0) < 70):
		# 		self.robot.set_wheel(0, 60)
		# 		self.robot.set_wheel(1, 30)
		# 		# time.sleep(0.2)
		# 	elif (self.robot.get_floor(1) < 70):
		# 		self.robot.set_wheel(0, 30)
		# 		self.robot.set_wheel(1, 60)
		# 		# time.sleep(0.2)
		# 	else:
		# 		self.robot.set_wheel(0, 30)
		# 		self.robot.set_wheel(1, 30)
		# print "passed line"
		time.sleep(0.5)
		while (self.robot.get_floor(0) > 70 or self.robot.get_floor(1) > 70):
			if (self.robot.get_floor(0) < 70):
				self.robot.set_wheel(0, 50)
				self.robot.set_wheel(1, 100)
			elif (self.robot.get_floor(1) < 70):
				self.robot.set_wheel(0, 100)
				self.robot.set_wheel(1, 50)
			else:
				self.robot.set_wheel(0, 50)
				self.robot.set_wheel(1, 50)
		self.robot.set_wheel(0, 30)
		self.robot.set_wheel(1, 30)
		time.sleep(0.2)

	def orient_up(self):
		print "orient_up"
		if (self.direction == "right"):
			self.turn_left()
		elif (self.direction == "left"):
			self.turn_right()
		elif (self.direction == "down"):
			self.u_turn()
		self.direction = "up"

	def orient_down(self):
		if (self.direction == "right"):
			self.turn_right()
		elif (self.direction == "left"):
			self.turn_left()
		elif (self.direction == "up"):
			self.u_turn()
		self.direction = "down"

	def orient_left(self):
		if (self.direction == "up"):
			self.turn_left()
		elif (self.direction == "down"):
			self.turn_right()
		elif (self.direction == "right"):
			self.u_turn()
		self.direction = "left"

	def orient_right(self):
		print "orient_right"
		if (self.direction == "up"):
			self.turn_right()
		elif (self.direction == "down"):
			self.turn_left()
		elif (self.direction == "left"):
			self.u_turn()
		self.direction = "right"

	def turn_left(self):
		# self.robot.set_wheel(0, -30)
		# self.robot.set_wheel(1, -30)
		# time.sleep(0.2)
		self.robot.set_wheel(0, -30)
		self.robot.set_wheel(1, 30)
		time.sleep(0.16)
		# time.sleep(0.69)

	def turn_right(self):
		# self.robot.set_wheel(0, -30)
		# self.robot.set_wheel(1, -30)
		# time.sleep(0.2)
		self.robot.set_wheel(0, 30)
		self.robot.set_wheel(1, -30)
		time.sleep(0.16)
		# time.sleep(0.69)

	def u_turn(self):
		self.robot.set_wheel(0, 30)
		self.robot.set_wheel(1, -30)
		time.sleep(0.8)

	def stop(self):
		self.robot.set_wheel(0, 0)
		self.robot.set_wheel(1, 0)