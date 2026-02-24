"""
Create a Sudoku class to easily represent the strings of numbers read in from the csv
"""
POSSIBLE_VALUES = {1,2,3,4,5,6,7,8,9}
class Square:
    def __init__(self, row:int, col:int, number: int, editable: bool):
        self.row = row
        self.col = col
        self.number = number
        self.editable = editable

    def set_number(self, num):
        self.number = num

    def __str__(self):
        return str(self.number)
    
class Sudoku:
    def __init__(self, board: str):
        self.initial_board = board
        self.board = []
        for i in range(9):
            self.board.append([])
            for j in range(9):
                number = int(board[(i * 9) + j])
                editable = True if number == 0 else False
                self.board[i].append(Square(i, j, number, editable))

    #update a sqaure (Assuming num is between 1-9) if it is editable
    def update(self, num, i, j):
        if self.is_valid_move(num, i, j):
            self.board[i][j].set_number(num)

    def is_valid_move(self, num, i, j):
        square = self.board[i][j]
        if square.editable:
            if num in self.get_possible_values(i, j):
                return True
        return False

    def get_row_values(self, row):
        values = []
        for i in self.board[row]:
            if i.number != 0:
                values.append(i.number)
        return values
    
    def get_col_values(self, col):
        values = []
        for row in self.board:
            if row[col].number != 0:
                values.append(row[col].number)
        return values
    
    def get_box_values(self, row, col):
        values = []
        #determine range from row and col
        row_range = ()
        if row % 3 == 0:
            row_range = (row, row + 1, row + 2)
        elif row % 3 == 1:
            row_range = (row - 1, row, row + 1)
        elif row % 3 == 2:
            row_range = (row - 2, row -1, row)

        col_range = ()
        if col % 3 == 0:
            col_range = (col, col + 1, col + 2)
        elif col % 3 == 1:
            col_range = (col - 1, col, col + 1)
        elif col % 3 == 2:
            col_range = (col - 2,col - 1, col)
        #add values to box
        for r in row_range:
            for c in col_range:
                if self.board[r][c].number != 0:
                    values.append(self.board[r][c].number)
        return values

    def get_possible_values(self, row, col):
        if self.board[row][col].editable:
            row_vals = self.get_row_values(row)
            col_vals = self.get_col_values(col)
            box_vals = self.get_box_values(row, col)

            possible = POSSIBLE_VALUES - set(row_vals)
            possible -= set(col_vals)
            possible -= set(box_vals)

            return list(possible)
        else:
            return []

    #to string
    def __str__(self):
        outstr = "-------------------------\n" #25 dashes
        for r in range(len(self.board)):
            outstr += f"| {self.board[r][0]} {self.board[r][1]} {self.board[r][2]} | "
            outstr += f"{self.board[r][3]} {self.board[r][4]} {self.board[r][5]} | "
            outstr += f"{self.board[r][6]} {self.board[r][7]} {self.board[r][8]} |\n"
            if r % 3 == 2:
                outstr += "-------------------------\n" #25 dashes
        return outstr 

#TESTING
s = Sudoku("004300209005009001070060043006002087190007400050083000600000105003508690042910300")
print(s)