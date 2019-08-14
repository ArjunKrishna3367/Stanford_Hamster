import sys

class KnightSearch(object):
	def __init__(self, graph):
		self.graph = graph
		self.x_move = [2, 1, -1, -2, -2, -1,  1,  2];
		self.y_move = [1, 2,  2,  1, -1, -2, -2, -1];
		self.N = 6
		self.solution = []
		return
		

	"""Solution of Knight tour problem using backtracking."""

	def is_safe(self, board, x, y):
		return 0 <= x < self.N and 0 <= y < self.N and board[x][y] == -1


	def solve_tour(self):
		"""Function to find one of the feasible knight tours."""
		board = [[-1 for _ in range(self.N)]for _ in range(self.N)]
		board[0][0] = 0

		z = self.find_tour(board, 0, 0, 1)
		if z:
			for i in range(self.N):
				for j in range(self.N):
					self.solution.append(board[i][j])
			print board
			return self.solution
				
		else:
			print("No solution")


	def find_tour(self, board, x, y, move_k):
		"""Recursive function that return whether a solution exist from given position."""
		if move_k == self.N * self.N:
			return True

		for k in range(8):
			x_next = x + self.x_move[k]
			y_next = y + self.y_move[k]

			if self.is_safe(board, x_next, y_next):
				board[x_next][y_next] = move_k

				if self.find_tour(board, x_next, y_next, move_k + 1):
					return True
				else:
					board[x_next][y_next] = -1

		return False
