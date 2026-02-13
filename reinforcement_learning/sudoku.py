"""
Create a Sudoku class to easily represent the strings of numbers read in from the csv
"""
import numpy as np
class Sudoku:
    def __init__(self):
        self.board = np.zeros(9,9)
    
