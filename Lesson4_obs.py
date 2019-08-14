'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.
   Stater program of 3-state obstacle avoidance using FSM.

   Name:          starter_tk_3state_avoid.py
   By:            Qin Chen
   Last Updated:  6/10/18

   PROPRIETARY and CONFIDENTIAL
   ========================================================================*/
'''
import sys
import time
import threading
import Tkinter as tk
import Queue
from HamsterAPI.comm_ble import RobotComm	# no dongle
#from HamsterAPI.comm_usb import RobotComm	# yes dongle

class Event(object):
    def __init__(self, event_type, event_data):
        self.type = event_type #string
        self.data = event_data #list of number or character depending on type

##############################
# Finite state machine engine
##############################
class StateMachine(object):
	def __init__(self, name, eventQ_handle):
		self.name = name		# machine name
		self.states = []	# list of lists, [[state name, event, transition, next_state],...]
		self.start_state = None
		self.end_states = []	# list of name strings
		self.q = eventQ_handle
		return

	def set_start_state(self, state_name):
		self.start_state = state_name
		return

	def get_start_state(self):
		return self.start_state
		
	def add_end_state(self, state_name):
		self.end_states.append(state_name)
		return
			
	def add_state(self, state, event, callback, next_state):
		self.states.append([state, event, callback, next_state]) # append to list
		return
	
	# you must set start state before calling run()
	def run(self):
		current_state = self.start_state
		#while not self.q.empty(): # for a machine that has end states
		while True:
			if current_state in self.end_states:
				break
			if not self.q.empty():
				e = self.q.get()
				for c in self.states:
					if c[0] == current_state and c[1] == e.type:
						c[2]()	# invoke callback function
						current_state = c[3] 	# next state
						break	# get out of inner for-loop
		return

################################
# Hamster control
################################
class RobotBehavior(object):
	def __init__(self, robot_list):
		self.done = False	# set by GUI button
		self.go = False		# set by GUI button
		self.robot_list = robot_list
		self.robot = None
		self.q = Queue.Queue()	# event queue for FSM
		self.spawn_threads()
		return

	def spawn_threads(self):
		###########################################################
		# Two threads are created here.
		# 1. create a watcher thread that reads sensors and registers events: obstacle on left, right or no obstacle. This
		# 	thread runs the method event_watcher() you are going to implement below.
		# 2. Instantiate StateMachine and populate it with avoidance states, triggers, etc. Set start state.
		# 3. Create a thread to run FSM engine.
		# ('current state name', 'event/input', 'action/callback', 'new state')
		###########################################################	
		t_robot_watcher = threading.Thread(name='watcher thread', target=self.event_watcher, args=(self.q, ))
		t_robot_watcher.daemon = True
		t_robot_watcher.start()
		print "watcher started"

		self.sm = StateMachine('Parking Ticket FSM', self.q)
		self.sm.add_state('Forward', 'no_obs', self.moving_forward, 'Forward')
		self.sm.add_state('Forward', 'obs_right', self.turning_left, 'TurnLeft')
		self.sm.add_state('Forward', 'obs_left', self.turning_right, 'TurnRight')
		self.sm.add_state('TurnLeft', 'no_obs' , self.moving_forward, 'Forward')
		self.sm.add_state('TurnLeft', 'obs_left', self.turning_left, 'TurnLeft')
		self.sm.add_state('TurnLeft', 'obs_right', self.turning_left, 'TurnLeft')
		self.sm.add_state('TurnRight', 'no_obs' , self.moving_forward, 'Forward')
		self.sm.add_state('TurnRight', 'obs_left', self.turning_right, 'TurnRight')
		self.sm.add_state('TurnRight', 'obs_right' , self.turning_right, 'TurnRight')
		self.sm.set_start_state('Forward')	# this must be done before starting machine

		t_state_machine = threading.Thread(name='state machine', target=self.sm.run)
		t_state_machine.daemon = True
		t_state_machine.start()
		print "state machine started"


	def event_watcher(self, q):
		while not self.done:
			if self.robot_list and self.go:
				prox_l = self.robot_list[0].get_proximity(0)
				prox_r = self.robot_list[0].get_proximity(1)
				print str(prox_l) + " " + str(prox_r)
				if (prox_l < 50 and prox_r < 50):
					q.put(Event("no_obs", []))
					# print "no_obs"
				elif (prox_l > prox_r):
					q.put(Event("obs_left", []))
					# print "obs_left"
				elif (prox_r > prox_l):
					q.put(Event("obs_right", []))
					# print "obs_right"
				###########################################################
				# Implement event producer here. The events are obstacle on left, right or no obstacle. Design your
				# logic for what event gets created based on sensor readings.
				###########################################################
			
	        return

	#######################################
	# Implement Hamster movements to avoid obstacle
	#######################################
	def turning_left(self):
		self.robot_list[0].set_wheel(0, -30)
		self.robot_list[0].set_wheel(1, 30)

	def turning_right(self):
		self.robot_list[0].set_wheel(0, 30)
		self.robot_list[0].set_wheel(1, -30)

	def moving_forward(self):
		self.robot_list[0].set_wheel(0, 30)
		self.robot_list[0].set_wheel(1, 30)
		  
class GUI(object):
	def __init__(self, root, robot_control):
		self.root = root
		self.robot_control = robot_control
		
		canvas = tk.Canvas(root, bg="white", width=300, height=250)
		canvas.pack(expand=1, fill='both')
		canvas.create_rectangle(175, 175, 125, 125, fill="green")

		b1 = tk.Button(root, text='Go')
		b1.pack()
		b1.bind('<Button-1>', self.startProg)

		b2 = tk.Button(root, text='Exit')
		b2.pack()
		b2.bind('<Button-1>', self.stopProg)
		return
	
	def startProg(self, event=None):
		# self.robot_control.robot_list[0].set_wheel(0, 30)
		# self.robot_control.robot_list[0].set_wheel(1, 30)
		self.robot_control.go = True
		return

	def stopProg(self, event=None):
		self.robot_control.done = True		
		self.root.quit() 	# close window
		return

def main():
    gMaxRobotNum = 1 # max number of robots to control
    comm = RobotComm(gMaxRobotNum)
    comm.start()
    print 'Bluetooth starts'

    robot_list = comm.robotList
    behaviors = RobotBehavior(robot_list)

    frame = tk.Tk()
    GUI(frame, behaviors)
    frame.mainloop()

    comm.stop()
    comm.join()
    return

if __name__ == "__main__":
    sys.exit(main())