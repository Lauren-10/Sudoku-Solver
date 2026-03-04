import numpy as np
import matplotlib.pyplot as plt
from sudoku import Sudoku, POSSIBLE_VALUES

"""
Actions: Update a value to value 1-9
States: 81 row, col pairs (i,j) 
Rewards: -1 value is not editable
         -5 invalid value
         +1 valid value
         +10 solved row/column
         +100 solved board
Goal: 280 + 81 = 361
Bellmans Equation for Q-learning: Q(s, a) = R(s, a) + y max_a(Q(s', a))
For Q-learning there needs to be a Q-table with all the possible action and state pairs.

to get state in q_table use (i * 9) + j
"""
n_states = 81
n_actions = 9
lr = 0.8 #learning rate
df = .95 #discount factor
ep = 0.1 #exploration probability
epochs = 500 # cycles (TODO: replace while loop with epochs later)
class Agent:
    def __init__(self, board: Sudoku):
        self.board = board
        self.q_table = np.zeros((n_states, n_actions))

    def reward(self, num, i, j):
        r = 0
        if not self.board.board[i][j].editable:
            r -= 10
        elif self.board.is_valid_move(num, i, j):
            r += 1
        else:
            r -= 5
        if self.board.fills_row(num, i, j):
            r += 10
        if self.board.fills_col(num, i, j):
            r += 10
        if self.board.fills_cell(num, i, j):
            r += 10
        # if self.board.solves_board(num, i, j):
        #     r += 100
        return r 
    
    def update_q_table(self):
        for i in range(9):
            for j in range(9):
                for num in range(9):
                    self.q_table[(i * 9) + j][num] = self.reward(num + 1, i, j)

    def solve(self, row, col):
        not_solved = True
        self.update_q_table()
        for _ in range(epochs):
            for i in range(row, 9):
                for j in range(col, 9):
                    #logic for using q_table to learn
                    max_action = np.argmax(self.q_table[(i * 9) + j])
                    r = self.q_table[(i * 9) + j][max_action]
                    if r >= 0:
                        print(f"Reward {r} for ({i}, {j})")
                        next_state = (i * 9) + j + 1 if (i * 9) + j + 1 < 81 else 0
                        #Bellmans equation
                        self.q_table[(i * 9) + j][max_action] += lr *(self.reward(max_action + 1, i, j) + df * np.max(self.q_table[next_state]) - self.q_table[(i * 9) + j][max_action])
                        if self.board.update(max_action + 1, i, j):
                            pass
                            # print(f"Updated ({i}, {j}) to {max_action + 1}")
                            # if i == 8 and j == 8:
                            #     self.solve(0, 0)
                        else:
                            # print(f"Failed to update ({i}, {j}) to {max_action + 1}")
                            #TODO: penalty all of the previously placed numbers 
                            self.board.reset_board()
                            
                            # if j < 8 and i < 8:
                            #     j += 1
                            # elif i == 8 and j == 8:
                            #     j = 0
                            #     i = 0
                            # elif j == 8 and i < 8:
                            #     j = 0
                            #     i += 1
                            # self.solve(i, j)

                    if self.q_table[(i * 9) + j][max_action] >= 100:
                        not_solved = False

        for i in range(9):
            for j in range(9):
                num = np.argmax(self.q_table[(i * 9) + j])
                self.board.update(num + 1, i, j)
        print(self.board)
            
s = Sudoku("004300209005009001070060043006002087190007400050083000600000105003508690042910300")
solver = Agent(s)
solver.solve(0, 0)