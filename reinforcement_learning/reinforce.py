import numpy as np
import matplotlib.pyplot as plt
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

"""

class SudokuEnv:
    def __init__(self, board:str):
        self.state = Sudoku(board)
        self.reward = 0
    def move(self):
        pass

class Agent:
    def __init__(self, env: SudokuEnv):
        self.env = env
    def value(self):
        pass #determines the desirability of a move
