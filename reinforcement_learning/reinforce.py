import numpy as np
import pandas as pd
import os

from random import random

from sudoku import Sudoku

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
lr = 0.9 #learning rate
df = .95 #discount factor
epochs = 1000 # cycles
class Agent:
    def __init__(self, board: Sudoku):
        self.board = board
        self.q_table = np.zeros((n_states, n_actions))

    def reward(self, num, i, j):
        r = 0
        if not self.board.board[i][j].editable:
            r -= 10
        elif self.board.is_valid_move(num, i, j):
            r += 5
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
    #give a 2 pt penalty to every filled in board number when the solver gets stuck
    def penalty(self):
        for i in range(9):
            for j in range(9):
                num = self.board.board[i][j].number
                if self.board.board[i][j].editable and num != 0:
                    self.q_table[(i * 9) + j][num - 1] -= 1

    def update_q_table(self):
        for i in range(9):
            for j in range(9):
                for num in range(9):
                    self.q_table[(i * 9) + j][num] = self.reward(num + 1, i, j)

    def solve(self, row, col):
        self.update_q_table()
        # print(self.q_table)
        for _ in range(epochs):
            for i in range(row, 9):
                for j in range(col, 9):
                    #logic for using q_table to learn
                    max_action = np.argmax(self.q_table[(i * 9) + j])
                    r = self.q_table[(i * 9) + j][max_action]
                    if r >= 0:
                        # print(f"Reward {r} for placing {max_action + 1} at ({i}, {j})")                        
                        # TODO: add logic here to account for values that are in the q table but not in the board
                        discount_amount = 0
                        for r in range(9):
                            for c in range(9):
                                if r == i ^ c == j: #xor
                                    other_max_actions = np.argmax(self.q_table[(r * 9) + c])
                                    if other_max_actions == max_action:
                                        discount_amount += 1 * random()
                        #Bellmans equation
                        self.q_table[(i * 9) + j][max_action] += lr *(self.reward(max_action + 1, i, j) - (discount_amount))
                        if self.board.update(max_action + 1, i, j):
                            pass
                        else:
                            # print(f"Failed to update ({i}, {j}) to {max_action + 1}")
                            #penalty all of the previously placed numbers 
                            self.penalty()
                            # print(self.board)
                            self.board.reset_board()
                            if i < 8:
                                i += 1
                            if j < 8:
                                j += 1
                            if i == 8:
                                i = 0
                            if j == 8:
                                j = 0

        for i in range(9):
            for j in range(9):
                max_val = max(self.q_table[(i * 9) + j])
                max_idx = [i for i, x in enumerate(self.q_table[(i * 9) + j]) if x == max_val]
                trys = 0
                while trys < len(max_idx) and not self.board.update(max_idx[trys] + 1, i, j):
                    trys += 1
                    # print(f"Max at ({i}, {j}): {num + 1}")
                # if self.board.board[i][j].editable:
                #     self.board.board[i][j].set_number(num + 1)
        # print(self.board)
# TESTING 
s = Sudoku("503070190000006750047190600400038000950200300000010072000804001300001860086720005")
print("Start:")
print(s)
s.solve()
print("Solution:")
print(s)
        
s = Sudoku("503070190000006750047190600400038000950200300000010072000804001300001860086720005")
solver = Agent(s)
solver.solve(0, 0)
print("Reinforcement Learning:")
print(solver.board)



def runner():
    path = os.getcwd()
    df = pd.read_csv(path + "/training_data/train_sudoku1.csv", nrows=1, header=None, names=['quizzes', 'solutions'])

    correct = 0
    amt_off = []

    for i in range(len(df)):
        s = Sudoku(f"{df['quizzes'][i]:0>81}")
        solver = Agent(s)
        solver.solve(0, 0)
        solution = Sudoku(f"{df['solutions'][i]:0>81}")
        print("Solution:")
        print(solution)
        print("Learned Answer:")
        print(solver.board)
        if solver.board.board == solution.board:
            correct += 1
        else:
            num_wrong = 0
            for row in range(9):
                for col in range(9):
                    if solver.board.board[row][col].number != solution.board[row][col].number:
                        num_wrong += 1
            amt_off.append(num_wrong)
    print(correct, amt_off)

# runner()