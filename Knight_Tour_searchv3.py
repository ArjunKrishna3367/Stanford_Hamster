from heapq import heappush, heappop # for priority queue
import random
import string

class KnightSearch(object):
    def __init__(self, row, col, width, height):
        self.x_start = col
        self.y_start = row
        self.x_dir = [2, 1, -1, -2, -2, -1,  1,  2];
        self.y_dir = [1, 2,  2,  1, -1, -2, -2, -1];
        self.width = width
        self.height = height # width and height of the chessboard
        self.solution = []
        return

    def solve_tour(self):
        
        # chessboard = [[0 for x in range(self.width)] for y in range(self.height)] # chessboard
        # # directions the Knight can move on the chessboard
        # # start the Knight from a random position
        # # x_start = random.randint(0, self.width - 1)
        # # y_start = random.randint(0, self.height - 1)
        # x_start = self.x_start
        # y_start = self.y_start

        # for k in range(self.width * self.height):
        #     chessboard[y_start][x_start] = k + 1
        #     pq = [] # priority queue of available neighbors
        #     for i in range(8):
        #         next_x = x_start + self.x_dir[i]; next_y = y_start + self.y_dir[i]
        #         if next_x >= 0 and next_x < self.width and next_y >= 0 and next_y < self.height:
        #             if chessboard[next_y][next_x] == 0:
        #                 # count the available neighbors of the neighbor
        #                 ctr = 0
        #                 for j in range(8):
        #                     ex = next_x + self.x_dir[j]; ey = next_y + self.y_dir[j]
        #                     if ex >= 0 and ex < self.width and ey >= 0 and ey < self.height:
        #                         if chessboard[ey][ex] == 0: ctr += 1
        #                 heappush(pq, (ctr, i))
        #     # move to the neighbor that has min number of available neighbors
        #     if len(pq) > 0:
        #         (p, m) = heappop(pq)
        #         x_start += self.x_dir[m]; y_start += self.y_dir[m]
        #     else: break

        # # print chessboard
        # for cy in range(self.height):
        #     for cx in range(self.width):
        #         self.solution.append(chessboard[cy][cx])
        #         print string.rjust(str(chessboard[cy][cx]), 2),
        #     # print
        # return self.solution

        cb = [[0 for x in range(self.width)] for y in range(self.height)] # chessboard
        # directions the Knight can move on the chessboard
        dx = [-2, -1, 1, 2, -2, -1, 1, 2]
        dy = [1, 2, 2, 1, -1, -2, -2, -1]
        # start the Knight from a random position
        kx = self.x_start
        ky = self.y_start

        for k in range(self.width * self.height):
            cb[ky][kx] = k + 1
            pq = [] # priority queue of available neighbors
            for i in range(8):
                nx = kx + dx[i]; ny = ky + dy[i]
                if nx >= 0 and nx < self.width and ny >= 0 and ny < self.height:
                    if cb[ny][nx] == 0:
                        # count the available neighbors of the neighbor
                        ctr = 0
                        for j in range(8):
                            ex = nx + dx[j]; ey = ny + dy[j]
                            if ex >= 0 and ex < self.width and ey >= 0 and ey < self.height:
                                if cb[ey][ex] == 0: ctr += 1
                        heappush(pq, (ctr, i))
            # move to the neighbor that has min number of available neighbors
            if len(pq) > 0:
                (p, m) = heappop(pq)
                kx += dx[m]; ky += dy[m]
            else: break

        # print cb
        zeroCount = 0
        for cy in range(self.height):
            for cx in range(self.width):
                if (cb[cy][cx] == 0):
                    zeroCount += 1
                    if (zeroCount > 1):
                        print "No Solution"
                        quit()
                self.solution.append(cb[cy][cx])
            #     print string.rjust(str(cb[cy][cx]), 2),
            # print
        return self.solution
