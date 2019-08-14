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
    def __init__(self, frame, graph):
        self.node_dist = 60
        self.node_size = 20
        self.gui_root = frame
        self.canvas = tk.Canvas(self.gui_root, width = 500, height = 500)
        self.graph = graph
        self.nodes_location = graph.node_display_locations
        self.start_node = graph.startNode
        self.goal_node = graph.goalNode
        return

    # draws nodes and edges in a graph
    def display_graph(self, path, startNode, endNode):        
        self.canvas.pack()
        for key in self.nodes_location:
            for adj_node in self.graph.nodes[key]:
                    self.draw_edge(key, adj_node, "blue")
        for key in self.nodes_location:
            self.draw_node(key, "blue")
        self.highlight_path(path)
        self.highlight_start_and_end(startNode, endNode)
        self.gui_root.mainloop()

    # path is a list of nodes ordered from start to goal node
    def highlight_path(self, path):
        for node in path:
            location = self.nodes_location[node]
            self.canvas.create_oval(location[0] + self.node_size, location[1] + self.node_size, location[0] - self.node_size, location[1] - self.node_size, fill="gold")
            self.canvas.create_text(location[0], location[1], fill="white", text=node)

    def highlight_start_and_end(self, startNode, endNode):
        startLocation = self.nodes_location[startNode]
        endLocation = self.nodes_location[endNode]
        self.canvas.create_oval(startLocation[0] + self.node_size, startLocation[1] + self.node_size, startLocation[0] - self.node_size, startLocation[1] - self.node_size, fill="green")
        self.canvas.create_oval(endLocation[0] + self.node_size, endLocation[1] + self.node_size, endLocation[0] - self.node_size, endLocation[1] - self.node_size, fill="red")
        self.canvas.create_text(startLocation[0], startLocation[1], fill="white", text=startNode)
        self.canvas.create_text(endLocation[0], endLocation[1], fill="white", text=endNode)
  
    # draws a node in given color. The node location info is in passed-in node object
    def draw_node(self, node, n_color):
        location = self.nodes_location[node]
        self.canvas.create_oval(location[0] + self.node_size, location[1] + self.node_size, location[0] - self.node_size, location[1] - self.node_size, fill=n_color)
        self.canvas.create_text(location[0], location[1], fill="white", text=node)

    # draws an line segment, between two given nodes, in given color
    def draw_edge(self, node1, node2, e_color):
        location1 = self.nodes_location[node1]
        location2 = self.nodes_location[node2]
        self.canvas.create_line(location1[0], location1[1], location2[0], location2[1], fill=e_color)
          
