'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.

   Name:          Joystick for Hamster
   By:            Qin Chen
   Last Updated:  5/10/18

   PROPRIETARY and CONFIDENTIAL
   ========================================================================*/
'''
import sys
import Tkinter as tk
from HamsterAPI.comm_ble import RobotComm
#for PC, need to import from commm_usb

class Robots(object):
    def __init__(self, robotList):
        self.robotList = robotList
        return

    def move_forward(self, event=None):
        if self.robotList:
            for robot in self.robotList:
                robot.set_wheel(0, 100)
                robot.set_wheel(1, 100)
        else:
            print "waiting for robot"

    def move_backward(self, event=None):
        if self.robotList:
            for robot in self.robotList:
                robot.set_wheel(0, -100)
                robot.set_wheel(1, -100)
        else:
            print "waiting for robot"

    def turn_left(self, event=None):
        if self.robotList:
            for robot in self.robotList:
                robot.set_wheel(0, -100)
                robot.set_wheel(1, 100)
        else:
            print "waiting for robot"

    def turn_right(self, event=None):
        if self.robotList:
            for robot in self.robotList:
                robot.set_wheel(0, 100)
                robot.set_wheel(1, -100)
        else:
            print "waiting for robot"

    def get_prox(self, event=None):
        if self.robotList:
            for robot in self.robotList:
                return [robot.get_proximity(0), robot.get_proximity(1)]

    def get_floor(self, event=None):
        if self.robotList:
            for robot in self.robotList:
                return [robot.get_floor(0), robot.get_floor(1)]

    def stop_move(self, event=None):
        if self.robotList:
            for robot in self.robotList:
                robot.set_wheel(0, 0)
                robot.set_wheel(1, 0)
        else:
            print "waiting for robot"

    def reset_robot(self, event=None): # use Hamster API reset()
        if self.robotList:
            for robot in self.robotList:
                robot.reset()

class UI(object):
    def __init__(self, root, robot_handle):
        self.root = root
        self.robot_handle = robot_handle  # handle to robot commands
        self.prox_l_id = None
        self.prox_r_id = None
        self.floor_l_id = None
        self.floor_r_id = None
        self.initUI()
        return

    def initUI(self):
        self.root.geometry('500x500')
        self.canvas = tk.Canvas(self.root, width=500, height=450, bg='white', borderwidth=2, relief="groove")
        self.canvas.pack()
        self.hamsterBody = self.canvas.create_rectangle(125, 175, 375, 425, fill='green')
        self.leftProxSensor = self.canvas.create_line(187.5, 175, 187.5, 175, fill='red')
        self.rightProxSensor = self.canvas.create_line(312.5, 175, 312.5, 175, fill='red')
        self.leftFloorSensor = self.canvas.create_rectangle(156.25, 206.25, 225, 250, fill='white')
        self.rightFloorSensor = self.canvas.create_rectangle(275, 206.25, 343.75, 250, fill='white')
        exitButton = tk.Button(self.root, text='Exit')
        exitButton.pack(side='bottom')
        exitButton.bind('<Button-1>', self.stopProg)
        self.root.bind('<KeyPress>', self.keydown)
        self.root.bind('<KeyRelease>', self.keyup)

        self.display_sensor()
        
        ###################################################################
        # Create a Hamster joystick window which contains
        # 1. a canvas widget where "sensor readings" are displayed
        # 2. a square representing Hamster
        # 3. 4 canvas items to display floor sensors and prox sensors
        # 4. a button for exit, i.e., a call to stopProg(), given in this class
        # 5. listen to key press and key release when focus is on this window
        ###################################################################
    
    ######################################################
    # This function refreshes floor and prox sensor display every 100 milliseconds.
    # Register callback using Tkinter's after method().
    ######################################################
    def display_sensor(self):
        if (self.robot_handle.get_floor() and self.canvas):
            if (self.robot_handle.get_floor()[0] > 50):
                self.canvas.itemconfig(self.leftFloorSensor, fill='white')
            else:
                self.canvas.itemconfig(self.leftFloorSensor, fill='black')

            if (self.robot_handle.get_floor()[1] > 50):
                self.canvas.itemconfig(self.rightFloorSensor, fill='white')
            else:
                self.canvas.itemconfig(self.rightFloorSensor, fill='black')

        if (self.robot_handle.get_prox() and self.canvas):

            self.canvas.coords(self.leftProxSensor, 187.5, 175, 187.5, (self.robot_handle.get_prox()[0] * 2))
            self.canvas.coords(self.rightProxSensor, 312.5, 175, 312.5, (self.robot_handle.get_prox()[1] * 2))

        self.root.after(100, self.display_sensor)

    ####################################################
    # Implement callback function when key press is detected
    ####################################################
    def keydown(self, event):
        if (event.char == 'w'):
            self.robot_handle.move_forward()
        elif (event.char == 's'):
            self.robot_handle.move_backward()
        elif (event.char == 'a'):
            self.robot_handle.turn_left()
        elif (event.char == 'd'):
            self.robot_handle.turn_right()

    #####################################################
    # Implement callback function when key release is detected
    #####################################################
    def keyup(self, event):
        self.robot_handle.stop_move()

    def stopProg(self, event=None):
        # print "hello" + str(self.robot_handle.get_prox())
        self.root.quit()    # close window
        self.robot_handle.reset_robot()
        return

def main(argv=None):
    gMaxRobotNum = 1 # max number of robots to control
    comm = RobotComm(gMaxRobotNum)
    comm.start()
    print 'Bluetooth starts'
    robotList = comm.robotList

    robot_handle = Robots(robotList)
    m = tk.Tk() #root
    gui = UI(m, robot_handle)

    m.mainloop()

    comm.stop()
    comm.join()

if __name__== "__main__":
    sys.exit(main())