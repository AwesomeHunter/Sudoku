from math import sqrt

class Sudoku:
    
    CORRECT       = 1
    WRONG         = 2
    NOT_COMPLETED = 3
    
    def __init__(self, size, init_board=None):
        self.size = size ** 2
        self.box_size = size
        if init_board is None:
            self.board = [[0] * self.size for i in range(self.size)]
        else:
            self.board = init_board
    
    def get_column(self, position):
        return [self.board[i][int(position.x)] for i in range(self.size)]

    def get_row(self, position):
        return self.board[int(position.y)]
    
    def get_box(self, position):
        box_pos = (position // self.box_size) * self.box_size
        numbers = []
        for y in range(self.box_size):
            for x in range(self.box_size):
                numbers.append(self.board[int(box_pos.y + y)][int(box_pos.x + x)])
        return numbers      
    
    def check_numbers(self, numbers):
        valid_numbers = [el for el in numbers if el != 0]
        unique = list(set(valid_numbers))
        if len(unique) > 0 and (max(unique) > self.size or min(unique) < 1 or len(unique) != len(valid_numbers)):
            return self.WRONG
        if unique == list(range(1, self.size + 1)):
            return self.CORRECT
        return self.NOT_COMPLETED
    
    def check_row(self, position):
        numbers = self.get_row(position)
        return self.check_numbers(numbers)

    def check_column(self, position):
        numbers = self.get_column(position)
        return self.check_numbers(numbers)
    
    def check_box(self, position):
        numbers = self.get_box(position)
        return self.check_numbers(numbers)
    
    def check_position(self, position):
        box = self.check_box(position)
        column = self.check_column(position)
        row = self.check_row(position)
        if self.WRONG in [box, column, row]:
            return self.WRONG
        if self.CORRECT in [box, column, row]:
            return self.CORRECT
        return self.NOT_COMPLETED
    
    def get_at_position(self, position):
        return self.board[int(position.y)][int(position.x)]
    
    def set_at_position(self, position, val):
        self.board[int(position.y)][int(position.x)] = val