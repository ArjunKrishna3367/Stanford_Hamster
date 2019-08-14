'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.

   PROPRIETARY and CONFIDENTIAL

   This file contains source code that constitutes proprietary and
   confidential information created by David Zhu

   Kre8 Technology retains the title, ownership and intellectual property rights
   in and to the Software and all subsequent copies regardless of the
   form or media.  Copying or distributing any portion of this file
   without the written permission of Kre8 Technology is prohibited.

   Use of this code is governed by the license agreement,
   confidentiality agreement, and/or other agreement under which it
   was distributed. When conflicts or ambiguities exist between this
   header and the written agreement, the agreement supersedes this file.
   ========================================================================*/
'''

import Tkinter as tk  
import time  
import math
import pdb
import numpy as np

class virtual_robot:
	def __init__(self):
		#self.robot = None
		self.l = 20*math.sqrt(2) # half diagonal - robot is 40 mm square
		self.x = 0 # x coordinate
		self.y = 0 # y coordinate
		self.a = 0 # angle of the robot, 0 when aligned with verticle axis
		self.dist_l = False
		self.dist_r = False #distance
		self.floor_l = False 
		self.floor_r = False 
		self.sl = 0 # speed of left wheel
		self.sr = 0 # speed of right wheel
		self.t = 0 # last update time

	def reset_robot(self):
		self.x = 0 # x coordinate
		self.y = 0 # y coordinate
		self.a = 0 # angle of the robot, 0 when aligned with verticle axis
		self.dist_l = False
		self.dist_r = False #
		self.floor_l = False 
		self.floor_r = False     
		self.sl = 0 # speed of left wheel
		self.sr = 0 # speed of right wheel
		self.t = 0 # last update time

	def set_robot_speed(self, w_l, w_r):
		self.sl = w_l
		self.sr = w_r

	def set_robot_pose(self, a, x, y):
		self.a = a
		self.x = x
		self.y = y

	def set_robot_prox_dist(self, dist_l, dist_r):
		self.dist_l = dist_l
		self.dist_r = dist_r

	def set_robot_floor (self, floor_l, floor_r):
		self.floor_l = floor_l
		self.floor_r = floor_r

class virtual_world:
	def __init__(self):
		self.real_robot = False
		self.go = False # activate robot behavior
		self.vrobot = virtual_robot()
		self.canvas = None
		self.canvas_width = 0
		self.canvas_height = 0
		self.area = []
		self.map = []
		#self.cobs = []
		self.f_cell_list = []
		self.goal_list = []
		self.goal_list_index = 0
		self.goal_t = "None"
		self.goal_x = 0
		self.goal_y = 0
		self.goal_a = 0
		self.goal_achieved = True
		self.trace = False #leave trace of robot
		self.prox_dots = False # draw obstacles detected as dots on map
		self.floor_dots = False
		self.localize = False
		self.glocalize = False
		self.robot_coords = []
		
	def add_obstacle(self,rect):
		self.map.append(rect)
		return

	def draw_map(self):
		canvas_width = self.canvas_width
		canvas_height = self.canvas_height
		for rect in self.map:
			x1 = canvas_width + rect[0]
			y1= canvas_height - rect[1]
			x2= canvas_width + rect[2]
			y2 = canvas_height - rect[3]
			self.canvas.create_rectangle([x1,y1,x2,y2], outline="grey", fill="grey")
		# for cobs in self.cobs:
		#     x1 = canvas_width + cobs[0]
		#     y1= canvas_height - cobs[1]
		#     x2= canvas_width + cobs[2]
		#     y2 = canvas_height - cobs[3]
			#self.canvas.create_rectangle([x1,y1,x2,y2], fill=None)

	def draw_robot(self):
		canvas_width = self.canvas_width
		canvas_height = self.canvas_height
		pi4 = 3.1415 / 4 # quarter pi
		vrobot = self.vrobot
		a1 = vrobot.a + pi4
		a2 = vrobot.a + 3*pi4
		a3 = vrobot.a + 5*pi4
		a4 = vrobot.a + 7*pi4

		x1 = canvas_width + vrobot.l * math.sin(a1) + vrobot.x
		x2 = canvas_width + vrobot.l * math.sin(a2) + vrobot.x
		x3 = canvas_width + vrobot.l * math.sin(a3) + vrobot.x        
		x4 = canvas_width + vrobot.l * math.sin(a4) + vrobot.x

		y1 = canvas_height - vrobot.l * math.cos(a1) - vrobot.y
		y2 = canvas_height - vrobot.l * math.cos(a2) - vrobot.y
		y3 = canvas_height - vrobot.l * math.cos(a3) - vrobot.y
		y4 = canvas_height - vrobot.l * math.cos(a4) - vrobot.y

		self.robot_coords = [x1,y1,x2,y2,x3,y3,x4,y4]
		points = (x1,y1,x2,y2,x3,y3,x4,y4)
		poly_id = vrobot.poly_id
		self.canvas.itemconfig(poly_id, tags="robot")
		self.canvas.coords(poly_id, points)    

		if (self.trace):
			pi3 = 3.1415/3
			a1 = vrobot.a
			a2 = a1 + 2*pi3
			a3 = a1 + 4*pi3
			x1 = canvas_width + 3 * math.sin(a1) + vrobot.x
			x2 = canvas_width + 3 * math.sin(a2) + vrobot.x
			x3 = canvas_width + 3 * math.sin(a3) + vrobot.x 
			y1 = canvas_height - 3 * math.cos(a1) - vrobot.y
			y2 = canvas_height - 3 * math.cos(a2) - vrobot.y
			y3 = canvas_height - 3 * math.cos(a3) - vrobot.y
			self.canvas.create_polygon([x1,y1,x2,y2,x3,y3], outline="blue")

	def radial_intersect (self, a_r, x_e, y_e):
		shortest = False
		p_intersect = False
		p_new = False

		for obs in self.map:
			x1 = obs[0]
			y1 = obs[1]
			x2 = obs[2]
			y2 = obs[3]
			# first quadron
			if (a_r >= 0) and (a_r < 3.1415/2): 
				#print "radial intersect: ", x_e, y_e
				if (y_e < y1):
					x_i = x_e + math.tan(a_r) * (y1 - y_e)
					y_i = y1
					if (x_i > x1 and x_i < x2):
						p_new = [x_i, y_i, 1] # 1 indicating intersecting a bottom edge of obs
				if (x_e < x1):
					x_i = x1
					y_i = y_e + math.tan(3.1415/2 - a_r) * (x1 - x_e)
					if (y_i > y1 and y_i < y2):
						p_new = [x_i, y_i, 2] # left edge of obs
			# second quadron
			if (a_r >= 3.1415/2) and (a_r < 3.1415): 
				if (y_e > y2):
					x_i = x_e + math.tan(a_r) * (y2 - y_e)
					y_i = y2
					if (x_i > x1 and x_i < x2):
						p_new = [x_i, y_i, 3] # top edge
				if (x_e < x1):
					x_i = x1
					y_i = y_e + math.tan(3.1415/2 - a_r) * (x1 - x_e)
					if (y_i > y1 and y_i < y2):
						p_new = [x_i, y_i, 2] #left edge
			# third quadron
			if (a_r >= 3.1415) and (a_r < 1.5*3.1415): 
				if (y_e > y2):
					x_i = x_e + math.tan(a_r) * (y2 - y_e)
					y_i = y2
					if (x_i > x1 and x_i < x2):
						p_new = [x_i, y_i, 3] #top edge
				if (x_e > x2):
					x_i = x2
					y_i = y_e + math.tan(3.1415/2 - a_r) * (x2 - x_e)
					if (y_i > y1 and y_i < y2):
						p_new = [x_i, y_i, 4] # right edge
			# fourth quadron
			if (a_r >= 1.5*3.1415) and (a_r < 6.283): 
				if (y_e < y1):
					x_i = x_e + math.tan(a_r) * (y1 - y_e)
					y_i = y1
					if (x_i > x1 and x_i < x2):
						p_new = [x_i, y_i, 1] # bottom edge
				if (x_e > x2):
					x_i = x2
					y_i = y_e + math.tan(3.1415/2 - a_r) * (x2 - x_e)
					if (y_i > y1 and y_i < y2):
						p_new = [x_i, y_i, 4] # right edge
			if p_new:
				dist = abs(p_new[0]-x_e) + abs(p_new[1]-y_e) 
				if shortest:
					if dist < shortest:
						shortest = dist
						p_intersect = p_new
				else:
					shortest = dist
					p_intersect = p_new
			p_new = False

		if p_intersect: 
			return p_intersect
		else:
			return False

	def get_vrobot_prox(self, side):
		vrobot = self.vrobot

		a_r = vrobot.a # robot is orientation, same as sensor orientation
		if (a_r < 0):
			a_r += 6.283
		if (side == "left"):
			a_e = vrobot.a - 3.1415/4.5 #emitter location
		else:
			a_e = vrobot.a + 3.1415/4.5 #emitter location
		x_e = (vrobot.l-2) * math.sin(a_e) + vrobot.x #emiter pos of left sensor
		y_e = (vrobot.l-2) * math.cos(a_e) + vrobot.y #emiter pos of right sensor

		intersection = self.radial_intersect(a_r, x_e, y_e)

		if intersection:
			x_i = intersection[0]
			y_i = intersection[1]
			if (side == "left"):
				vrobot.dist_l = math.sqrt((y_i-y_e)*(y_i-y_e) + (x_i-x_e)*(x_i-x_e))
				if vrobot.dist_l > 120:
					vrobot.dist_l = False
				return vrobot.dist_l
			else:
				vrobot.dist_r = math.sqrt((y_i-y_e)*(y_i-y_e) + (x_i-x_e)*(x_i-x_e))
				if vrobot.dist_r > 120:
					vrobot.dist_r = False
				return vrobot.dist_r
		else:
			if (side == "left"):
				vrobot.dist_l = False
				return False
			else:
				vrobot.dist_r = False
				return False

	def draw_prox(self, side):
		canvas_width = self.canvas_width
		canvas_height = self.canvas_height
		vrobot = self.vrobot
		if (side == "left"):
			a_e = vrobot.a - 3.1415/5 #emitter location
			prox_dis = vrobot.dist_l
			prox_l_id = vrobot.prox_l_id
		else:
			a_e = vrobot.a + 3.1415/5 #emitter location
			prox_dis = vrobot.dist_r
			prox_l_id = vrobot.prox_r_id
		if (prox_dis):
			x_e = (vrobot.l-4) * math.sin(a_e) + vrobot.x #emiter pos of left sensor
			y_e = (vrobot.l-4) * math.cos(a_e) + vrobot.y #emiter pos of right sensor
			x_p = prox_dis * math.sin(vrobot.a) + x_e
			y_p = prox_dis * math.cos(vrobot.a) + y_e
			if (self.prox_dots):
				self.canvas.create_oval(canvas_width+x_p-1, canvas_height-y_p-1, canvas_width+x_p+1, canvas_height-y_p+1, outline='red')
			point_list = (canvas_width+x_e, canvas_height-y_e, canvas_width+x_p, canvas_height-y_p)
			self.canvas.coords(prox_l_id, point_list)
		else:
			point_list = (0,0,0,0)
			self.canvas.coords(prox_l_id, point_list)

	def draw_floor(self, side):
		canvas_width = self.canvas_width
		canvas_height = self.canvas_height
		vrobot = self.vrobot
		if (side == "left"):
			border = vrobot.floor_l
			floor_id = vrobot.floor_l_id
			a = vrobot.a - 3.1415/7 #rough position of the left floor sensor
		else:
			border = vrobot.floor_r
			floor_id = vrobot.floor_r_id
			a = vrobot.a + 3.1415/7 #rough position of the left floor sensor         
		x_f = (vrobot.l - 12) * math.sin(a) + vrobot.x
		y_f = (vrobot.l - 12) * math.cos(a) + vrobot.y
		points = (canvas_width+x_f-2, canvas_height-y_f-2, canvas_width+x_f+2, canvas_height-y_f+2)
		self.canvas.coords(floor_id, points)
		if (border): 
			self.canvas.itemconfig(floor_id, outline = "black", fill="black")
			if (self.floor_dots):
				self.canvas.create_oval(canvas_width+x_f-2, canvas_height-y_f-2, canvas_width+x_f+2, canvas_height-y_f+2, fill='black')
		else:
			self.canvas.itemconfig(floor_id, outline = "white", fill="white")

	######################################################################
	# This function returns True when simulated robot would collide with 
	# one of the obstacles at given pose(a,x,y)
	######################################################################
	def in_collision(self, a, x, y):
		if (self.robot_coords):
			collided = False
			p1 = [self.robot_coords[0] - self.canvas_width, self.canvas_height - self.robot_coords[1]]
			p2 = [self.robot_coords[2] - self.canvas_width, self.canvas_height - self.robot_coords[3]]
			p3 = [self.robot_coords[4] - self.canvas_width, self.canvas_height - self.robot_coords[5]]
			p4 = [self.robot_coords[6] - self.canvas_width, self.canvas_height - self.robot_coords[7]]

			# p1v2 = [x + (self.vrobot.l * math.cos(math.pi/4 - a)), y - (self.vrobot.l * math.cos(math.pi/4 - a))]
			# print p1v2
			# print str(x) + " " + str(y)

			for rect in self.map:
				x1 = self.canvas_width + rect[0]
				y1= self.canvas_height - rect[1]
				x2= self.canvas_width + rect[2]
				y2 = self.canvas_height - rect[3]

				for item in self.canvas.find_overlapping(x1, y1, x2, y2):
					print self.canvas.gettags(item)
					if self.canvas.gettags(item) and self.canvas.gettags(item)[0] == "robot":
						return True
					time.sleep(0.01)
				return False
				time.sleep(0.01)

			# for rect in self.map:
			# 	if (p1[0] > rect[0] and p1[0] < rect[2] and p1[1] > rect[1] and p1[1] < rect[3]):
			# 		print "True p1"
			# 		return True	
			# 	elif (p2[0] > rect[0] and p2[0] < rect[2] and p2[1] > rect[1] and p2[1] < rect[3]):
			# 		print "True p2"
			# 		return True	
			# 	elif (p3[0] > rect[0] and p3[0] < rect[2] and p3[1] > rect[1] and p3[1] < rect[3]):
			# 		print "True p3"
			# 		return True	
			# 	elif (p4[0] > rect[0] and p4[0] < rect[2] and p4[1] > rect[1] and p4[1] < rect[3]):
			# 		print "True p4"
			# 		return True			
			# 	else:
			# 		print "False"
			# 		return False

			# p1_to_p2 = []
			# p2_to_p3 = []
			# p3_to_p4 = []
			# p4_to_p1 = []

			# for x_coord in np.arange(p1[0], p2[0], 0.1):
			# 	m = (p1[1]-p2[1])/(p1[0]-p2[0]) #(y2-y1)/(x2-x1)
			# 	b = p1[1] - m*p1[0]
			# 	p1_to_p2.append([x_coord, m * x_coord + b])

			# for x_coord in np.arange(p2[0], p3[0], 0.1):
			# 	m = (p2[1]-p3[1])/(p2[0]-p3[0]) 
			# 	b = p2[1] - m*p2[0]
			# 	p2_to_p3.append([x_coord, m * x_coord + b])

			# for x_coord in np.arange(p3[0], p4[0], 0.1):
			# 	m = (p3[1]-p4[1])/(p3[0]-p4[0])
			# 	b = p3[1] - m*p3[0]
			# 	p3_to_p4.append([x_coord, m * x_coord + b])

			# for x_coord in np.arange(p4[0], p1[0], 0.1):
			# 	m = (p4[1]-p1[1])/(p4[0]-p1[0])
			# 	b = p4[1] - m*p4[0] 
			# 	p4_to_p1.append([x_coord, m * x_coord + b])

			# for rect in self.map:
			# 	for point in p1_to_p2:
			# 		# print point
			# 		if (point[0] > rect[0] and point[0] < rect[2] and point[1] > rect[1] and point[1] < rect[3]):
			# 			print "True p1"
			# 			collided = True	
			# 			break	
			# 	for point in p2_to_p3:
			# 		# print point
			# 		if (point[0] > rect[0] and point[0] < rect[2] and point[1] > rect[1] and point[1] < rect[3]):
			# 			print "True p2"
			# 			collided = True
			# 			break
			# 	for point in p3_to_p4:
			# 		# print point
			# 		if (point[0] > rect[0] and point[0] < rect[2] and point[1] > rect[1] and point[1] < rect[3]):
			# 			print "True p3"
			# 			collided = True
			# 			break
			# 	for point in p4_to_p1:
			# 		# print point
			# 		if (point[0] > rect[0] and point[0] < rect[2] and point[1] > rect[1] and point[1] < rect[3]):
			# 			print "True p4"
			# 			collided = True
			# 			break
			# 	if collided:
			# 		return True
			# 	else:
			# 		return False



