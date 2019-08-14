'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.

   Name:          grid_graph_starter.py
   By:            Qin Chen
   Last Updated:  6/10/18
    
   Definition of class GridGraph. Description of all the methods is
   provided. Students are expected to implement the methods for Lab#6.
   ========================================================================*/
'''
import Tkinter as tk
from Knight_Tour_display import *
from Knight_Tour_searchv3 import *
from Knight_Tour_robot import *
from HamsterAPI.comm_ble import RobotComm

class GridGraph(object):
    def __init__(self):
        self.nodes = {} # {node_name: set(neighboring nodes), ...}
        self.startNode = None  # string
        self.goalNode = None    # string
        self.grid_rows = None
        self.grid_columns = None
        self.obs_list = []
        self.node_display_locations={}
        return

    # set number of rows in the grid
    def set_grid_rows(self, rows):
        self.grid_rows = rows

    # set number of columns in the grid
    def set_grid_cols(self, cols):
        self.grid_columns = cols

    # this method is used by make_grid() to create a key-value pair in self.nodes{},
    # where value is created as an empty set which is populated later while connecting
    # nodes.
    def add_node(self, name):
        self.nodes[name] = set()

    # set start node name
    def set_start(self, name):
        self.startNode = name

    # returns start node name
    def get_start_node(self):
        return self.startNode

    # set goal node name
    def set_goal(self, name):
        self.goalNode = name

    # return goal node name
    def get_goal_node(self):
        return self.goalNode

    # Given two neighboring nodes. Put them to each other's neighbors-set. This
    # method is called by self.connect_nodes() 
    def add_neighbor(self, node1, node2):
        self.nodes[node1].add(node2)
        self.nodes[node2].add(node1)

    # populate graph with all the nodes in the graph, excluding obstacle nodes
    def make_grid(self):
        for row in range(self.grid_rows):
            for col in range(self.grid_columns):
                if (str(row) + "-" + str(col) not in self.obs_list):
                    self.add_node(str(row) + "-" + str(col))

    # Based on node's name, this method identifies its neighbors and fills the 
    # set holding neighbors for every node in the graph.
    def connect_nodes(self):
        for key in self.nodes:
            dashIndex = key.find('-')
            row = key[:dashIndex]
            col = key[dashIndex+1:]
            row_plus_1 = str(int(row) + 1)
            row_minus_1 = str(int(row) - 1)
            col_plus_1 = str(int(col) + 1)
            col_minus_1 = str(int(col) - 1)
            if (row_plus_1 + "-" + col not in self.obs_list and int(row_plus_1) < self.grid_rows):
                self.add_neighbor(row + "-" + col, row_plus_1 + "-" + col)

            if (row_minus_1 + "-" + col not in self.obs_list and int(row_minus_1) >= 0):
                self.add_neighbor(row + "-" + col, row_minus_1 + "-" + col)

            if (row + "-" + col_plus_1 not in self.obs_list and int(col_plus_1) < self.grid_columns):
                self.add_neighbor(row + "-" + col, row + "-" + col_plus_1)

            if (row + "-" + col_minus_1 not in self.obs_list and int(col_minus_1) >= 0):
                self.add_neighbor(row + "-" + col, row + "-" + col_minus_1)

    # For display purpose, this function computes grid node location(i.e., offset from upper left corner where is (1,1)) 
    # of display area. based on node names.
    # Node '0-0' is displayed at bottom left corner 
    def compute_node_locations(self):
        for key in self.nodes:
            dashIndex = key.find('-')
            row = -int(key[:dashIndex])
            col = int(key[dashIndex+1:])
            self.node_display_locations[key] = [col*40 + 100, row * 40 + 400]

###########################################################
#  A testing program of your implementaion of GridGraph class.
###########################################################
def main():

    width = input("Enter graph width, from 1-10: ")
    height = input("Enter graph height, from 1-10: ")
    start_col = input("Enter starting column, from 0-" + str(width - 1) +": ")
    start_row = input("Enter starting row, from 0-" + str(height - 1) + ": ")
    if (width > 10 or height > 10 or start_row >= height or start_col >= width):
        print "Out of bounds"
        return


    graph = GridGraph()
    # grid dimension
    graph.set_grid_rows(width)
    graph.set_grid_cols(height)

    # origin of grid is (0, 0) lower left corner
    # graph.obs_list = ([1,1],)    # in case of one obs. COMMA
    
    # graph.set_start('0-0')
    # graph.obs_list = ("2-3", "1-1", "2-1", "2-2")
    # graph.set_goal('1-2')
    
    # graph.set_start('0-0')   
    # graph.obs_list = ("2-1", "1-2")
    # graph.set_goal('2-2')

    graph.make_grid()
    graph.connect_nodes()
    graph.compute_node_locations()

    

    search = KnightSearch(start_row, start_col, width, height)
    order = search.solve_tour()

    # kt = KnightSearch(8, 8)
    # kt.tour(1, [], (0,0))
    # kt.print_board()

    gMaxRobotNum = 1 # max number of robots to control
    comm = RobotComm(gMaxRobotNum)
    comm.start()
    print 'Bluetooth starts'
    robotList = comm.robotList

    behaviors = RobotBehaviorThread(robotList)
    path = list(behaviors.make_plan(order, width))
    behaviors.path_to_plan()
    behaviors.start()

    root = tk.Tk()
    graph_display = GridGraphDisplay(root, graph, path, behaviors)
    graph_display.display_graph()
    root.mainloop()
    
    comm.stop()
    comm.join()
    return

if __name__ == "__main__":
    main()