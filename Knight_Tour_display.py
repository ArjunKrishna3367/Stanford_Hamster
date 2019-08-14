# Robot Programming
# breadth first search
# by Dr. Qin Chen
# May, 2016

import sys
import Tkinter as tk

##############
# This class supports display of a grid graph. The node location on canvas
# is included as a data field of the graph, graph.node_display_locations.
##############

class GridGraphDisplay(object):
    def __init__(self, frame, graph, path, behaviors):
        self.node_dist = 60
        self.node_size = 20
        self.behaviors = behaviors
        self.gui_root = frame
        self.canvas = tk.Canvas(self.gui_root, width = 500, height = 500)
        self.graph = graph
        self.nodes_location = graph.node_display_locations
        self.nodes = []
        self.path = path
        self.start_node = graph.startNode
        self.goal_node = graph.goalNode
        return

    # draws nodes and edges in a graph
    def display_graph(self):     
        self.canvas.pack()
        # for key in self.nodes_location:
        #     for adj_node in self.graph.nodes[key]:
        #             self.draw_edge(key, adj_node, "blue")

        for node in self.path:
            # print "node: " + str(node) + " location: " + str(self.nodes_location[node]) + " index: " + str(self.path.index(node))
            # self.nodes_location[node].append(self.path.index(node))
            self.nodes.append([node, self.nodes_location[node][0], self.nodes_location[node][1]])
        
        for node in self.nodes:
            self.draw_node(node, "blue")

        b1 = tk.Button(self.gui_root, text='Go')
        b1.pack()
        b1.bind('<Button-1>', self.startProg)

        b2 = tk.Button(self.gui_root, text='Exit')
        b2.pack()
        b2.bind('<Button-1>', self.stopProg)

        self.update_graph(self.behaviors.step_count)
        

    def update_graph(self, startIndex):
        if (startIndex >= 64):
            for node in self.nodes:
                self.draw_node(node, "gold")
            finishLabel = tk.Label(self.gui_root, text='Finished!')
            finishLabel.pack()

        startNode = self.nodes[startIndex]
        endNode = self.nodes[startIndex + 1]
        self.canvas.create_rectangle(startNode[1] + self.node_size, startNode[2] + self.node_size, startNode[1] - self.node_size, startNode[2] - self.node_size, fill="green")
        self.canvas.create_rectangle(endNode[1] + self.node_size, endNode[2] + self.node_size, endNode[1] - self.node_size, endNode[2] - self.node_size, fill="red")
        self.canvas.create_text(startNode[1], startNode[2], fill="white", text=startIndex + 1)
        self.canvas.create_text(endNode[1], endNode[2], fill="white", text=startIndex + 2)
        if (startIndex >= 1):
            prevNode = self.nodes[startIndex - 1]
            self.canvas.create_rectangle(prevNode[1] + self.node_size, prevNode[2] + self.node_size, prevNode[1] - self.node_size, prevNode[2] - self.node_size, fill="gold")
            self.canvas.create_text(prevNode[1], prevNode[2], fill="white", text=startIndex)
        self.gui_root.after(50, self.update_graph, self.behaviors.step_count)
  
    # draws a node in given color. The node location info is in passed-in node object
    def draw_node(self, node, n_color):
        self.canvas.create_rectangle(node[1] + self.node_size, node[2] + self.node_size, node[1] - self.node_size, node[2] - self.node_size, fill=n_color)
        self.canvas.create_text(node[1], node[2], fill="white", text=self.nodes.index(node) + 1)

    # draws an line segment, between two given nodes, in given color
    # def draw_edge(self, node1, node2, e_color):
    #     location1 = self.nodes_location[node1]
    #     location2 = self.nodes_location[node2]
    #     self.canvas.create_line(location1[0], location1[1], location2[0], location2[1], fill=e_color)

    def startProg(self, event=None):
        self.behaviors.go = True

    def stopProg(self, event=None):
        self.behaviors.done = True
        self.gui_root.quit()    # close window
        return
          
