'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.

   Name:          bfs_engine.py
   By:            Qin Chen
   Last Updated:  6/10/18

   PROPRIETARY and CONFIDENTIAL
   ========================================================================*/
'''
import sys

class BFS(object):
    def __init__(self, graph):
        self.graph = graph
        return

    ######################################################
    # this function returns the shortest path for given start and goal nodes
    ######################################################
    def bfs_shortest_path(self, start, goal):
        stack = [(start, [start])]
        while stack:
            (node, path) = stack.pop(0)
            # print '\nvisiting node', node, 'path=', path
            for next in self.graph[node] - set(path):
                # print 'next node', next
                if next == goal:
                    return path + [next]
                else:
                    stack.append((next, path + [next]))
                    # print "Stack push", next, path + [next]

                


    ######################################################
    # this function returns all paths for given start and goal nodes
    ######################################################
    def bfs_knight_path(self, start, goal):
        q = [(start, [start])]
        while q:
            (node, path) = q.pop(0)
            for next in self.graph[node] - set(path):
                if next == goal:
                    yield path + [next]
                else:
                    q.append((next, path+[next]))
        pass
                
    #########################################################
    # This function returns the shortest paths for given list of paths
    #########################################################
    def shortest(self, paths):
        pass

    #########################################################
    # THis function traverses the graph from given start node
    # return order of nodes visited
    #########################################################
    def bfs(self, start):
        print "bfs"
        visited_order = list()
        visited = set()
        q = list([start])

        while q:
            node = q.pop(0)
            if node not in visited:
                # print("visiting ", node)
                visited.add(node)
                visited_order.append(node)
                # print ("---visited_order", visited_order)
                q.extend(self.graph[node] - visited)
        return visited_order

def main():
    graph = {'A': set(['B', 'C']),
         'B': set(['A', 'E', 'D']),
         'C': set(['A', 'F', 'G']),
         'D': set(['B', 'H']),
         'E': set(['B','I', 'J']),
         'F': set(['C','K']),
         'G': set(['C']),
         'H': set(['D']),
         'I': set(['E']),
         'J': set(['E']),
         'K': set(['F'])}

    bfs = BFS(graph)

    start_node = 'A'
    end_node = 'E'

    order = bfs.bfs(start_node)
    print "\n##########traverse order:", order

    return

if __name__ == "__main__":
    sys.exit(main())