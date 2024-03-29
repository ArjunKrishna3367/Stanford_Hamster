'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.

   Name:          Robot Escape
   By:            Qin Chen
   Last Updated:  6/10/18

   PROPRIETARY and CONFIDENTIAL
   ========================================================================*/
'''
# This program shows how threads can be created using Thread class and your
# own functions. Another way of creating threads is subclass Thread and override
# run().
# 
import sys
import logging
sys.path.append('../')
import time  # sleep
import threading
import Tkinter as tk
import Queue
from HamsterAPI.comm_ble import RobotComm

logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s) %(message)s',)

class Event(object):
	def __init__(self, event_type, event_data):
	  self.type = event_type #string
	  self.data = event_data #list of number or character depending on type

class BehaviorThreads(object):
	Threshold_border = 20   # if floor sensor reading falls equal or below this value, border is detected
	Threshold_obstacle = 40   # if prox sensor reading is equal or higher than this, obstacle is detected
	
	def __init__(self, robot_list):
		self.robot_list = robot_list
		self.go = False
		self.quit = False
		# events queues for communication between threads
		self.alert_q = Queue.Queue()
		self.motion_q = Queue.Queue()
		self.t_robot_watcher = None     # thread handles
		self.t_motion_handler = None
		
		# start a watcher thread
		t_robot_watcher = threading.Thread(name='watcher thread', target=self.robot_event_watcher, args=(self.alert_q, self.motion_q))
		t_robot_watcher.daemon = True
		t_robot_watcher.start()
		self.t_robot_watcher = t_robot_watcher

		###################################
		# start a motion handler thread
		###################################
		# t_motion_handler = threading.Thread(name='motion handler thread', target=self.robot_motion_handler, args=(self.motion_q, ))
		# t_motion_handler.daemon = True
		# t_motion_handler.start()
		# self.t_motion_handler = t_motion_handler

		return

	###################################
	# This function is called when border is detected
	###################################
	def get_out (self, robot):
		for robot in self.robot_list:
			robot.set_wheel(0, 0)
			robot.set_wheel(1, 0)
		return



	# This function monitors the sensors
	def robot_event_watcher(self, q1, q2):
		count = 0

		logging.debug('starting...')
		while not self.quit:
			for robot in self.robot_list:
				if self.go and robot:
					prox_l = robot.get_proximity(0)
					prox_r = robot.get_proximity(1)
					line_l = robot.get_floor(0)
					line_r = robot.get_floor(1)
					
					if (prox_l > BehaviorThreads.Threshold_obstacle or prox_r > BehaviorThreads.Threshold_obstacle):
						alert_event = Event("alert", [prox_l,prox_r])
						q1.put(alert_event)
						# logging.debug("alert event %s, %s, %s, %s", prox_l, prox_r, line_l, line_r)
						#time.sleep(0.01)
						count += 1
						#update movement every 5 ticks
						if (count % 5 == 0):
							# logging.debug("obstacle detected, q2: %d %d" % (prox_l, prox_r))
							obs_event = Event("obstacle", [prox_l, prox_r])
							#q2.put(obs_event)
					else:
						if (count > 0):
							# free event is created when robot goes from obstacle to no obstacle
							# logging.debug("free of obstacle")
							free_event = Event("free",[])
							#q2.put(free_event)  # put event in motion queue
							q1.put(free_event)  # put event in alert queue
							count = 0
					if (line_l < BehaviorThreads.Threshold_border or line_r < BehaviorThreads.Threshold_border):
						#logging.debug("border detected: %d %d" % (line_l, line_r))
						border_event = Event("border", [line_l, line_r])
						q1.put(border_event)
						#q2.put(border_event)
				#else:
					#print 'waiting ...'
			time.sleep(0.01)	# delay to give alert thread more processing time. Otherwise, it doesn't seem to have a chance to serve 'free' event
		return

	##############################################################
	# Implement your motion handler. You need to get event using the passed-in queue handle and
	# decide what Hamster should do. Hamster needs to avoid obstacle while escaping. Hamster
	# stops moving after getting out of the border and remember to flush the motion queue after getting out.
	#############################################################
	def robot_motion_handler(self, q):
		# robot.set_wheel(0, 30)
		# robot.set_wheel(1, 30)

		while not self.quit:
			for robot in self.robot_list:
				currentEvent = q.get()
				# print "motion handler start"
				if (currentEvent.type == "obstacle"):
					# if (currentEvent.data[0] > currentEvent.data[1]):
					robot.set_wheel(0, 30)
					robot.set_wheel(1, -30)
					# else:
					# 	robot.set_wheel(0, -30)
					# 	robot.set_wheel(1, 40)
				elif(currentEvent.type == "free"):
					robot.set_wheel(0, 30)
					robot.set_wheel(1, 30)
				elif (currentEvent.type == "border"):
					self.get_out(robot)
					q.queue.clear()
					break
			time.sleep(0.05)
		return

			 


class GUI(object):
	def __init__(self, root, threads_handle):
		self.root = root
		self.t_handle = threads_handle
		self.event_q = threads_handle.alert_q
		self.prox_l_id = None
		self.prox_r_id = None
		self.initUI()

	##########################################################
	# 1. Create a canvas widget and three canvas items: a square, and two lines 
	# representing prox sensor readings.
	# 2. Create two button widgets, for start and exit.
	# 3. Create a thread for alert handler, which is responsible for displaying prox sensors.
	##########################################################
	def initUI(self):
		self.root.geometry('500x525')
		self.canvas = tk.Canvas(self.root, width=500, height=450, bg='white', borderwidth=2, relief="groove")
		self.canvas.pack()
		self.hamsterBody = self.canvas.create_rectangle(125, 175, 375, 425, fill='green')
		self.leftProxSensor = self.canvas.create_line(187.5, 175, 187.5, 175, fill='red')
		self.rightProxSensor = self.canvas.create_line(312.5, 175, 312.5, 175, fill='red')
		exitButton = tk.Button(self.root, text='Exit')
		exitButton.pack(side='bottom')
		exitButton.bind('<Button-1>', self.stopProg)
		startButton = tk.Button(self.root, text='Start')
		startButton.pack(side='bottom')
		startButton.bind('<Button-1>', self.startRobot)

		self.robot_alert_handler(self.event_q)
		# t_alert_handler = threading.Thread(name='alert handler thread', target=self.robot_alert_handler, args=(self.event_q, ))
		# t_alert_handler.daemon = True
		# t_alert_handler.start()
		#self.t_alert_handler = t_alert_handler


	def startRobot(self, event=None):
		self.t_handle.go = True
		for robot in self.t_handle.robot_list:
			robot.set_wheel(0, 30)
			robot.set_wheel(1, 30)
		return

	def stopProg(self, event=None):
		self.t_handle.quit = True
		for robot in self.t_handle.robot_list:
			robot.reset()
		
		#self.t_handle.t_motion_handler.join()
		self.t_handle.t_robot_watcher.join()
		#self.t_alert_handler.join()
		self.root.quit()	# close GUI window
		return

	###################################################
	# Handles prox sensor display and warning(sound).
	# Query event queue(using passed-in queue handle).
	# If there is an "alert" event, display red beams.
	# Erase the beams when "free" event is in queue.
	# This runs in the main GUI thread. Remember to schedule
	# a callback of itself after 50 milliseconds.
	###################################################
	def robot_alert_handler(self, q):
		print 'alert handler'
		for robot in self.t_handle.robot_list:
			if not q.empty():
			# while not self.t_handle.quit and not q.empty() and self.t_handle.go and robot:
				currentEvent = q.get()
				# print 'after pop q'
				if(currentEvent.type == "alert"):
					robot.set_musical_note(40)
					self.canvas.coords(self.leftProxSensor, 187.5, 175, 187.5, (currentEvent.data[0] * 2))
					self.canvas.coords(self.rightProxSensor, 312.5, 175, 312.5, (currentEvent.data[1] * 2))
				elif(currentEvent.type == "free"):
					robot.set_musical_note(0)
					self.canvas.coords(self.leftProxSensor, 187.5, 175, 187.5, 175)
					self.canvas.coords(self.rightProxSensor, 312.5, 175, 312.5, 175)
				elif(currentEvent.type == "border"):
					robot.set_musical_note(48)
		self.root.after(50, self.robot_alert_handler, (q))
		

def main():
	max_robot_num = 1   # max number of robots to control
	comm = RobotComm(max_robot_num)
	comm.start()
	print 'Bluetooth starts'
	robotList = comm.robotList

	root = tk.Tk()
	t_handle = BehaviorThreads(robotList)
	gui = GUI(root, t_handle)
  
	root.mainloop()

	comm.stop()
	comm.join()

if __name__== "__main__":
  sys.exit(main())
  