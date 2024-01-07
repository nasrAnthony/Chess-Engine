import math 
import os

class Piece():
    #W => White
    #B => Black
    def __init__(self, coord, type, color, value, image = None, image_rect = None):
        self.name = type
        self.color = color
        #for AI:
        #if(self.color == 'W'):
        #    Bias = 1 
        #else:
        #    Bias = -1
        self.valid_moves = [] 
        self.moved = False
        self.value = value #*Bias
        self.image = image
        self.set_image()
        self.textureRect = image_rect
        self.row = coord[1]
        self.col = coord[0]
        self.checking = False
        self.has_moved = False #used to check if king moved (condition for castling)
        self.castle_short = False
        self.castle_long = False

    def get_hasMoved_flag(self):
        return self.has_moved
    def get_initial_pos(self):
        return (self.col, self.row)
    def get_name(self):
        return self.name
    def get_color(self):
        return self.color
    def set_image(self):
        self.image = os.path.join(f'Assets/Pieces/{self.color}/{self.name}.png')
    def get_valid_moves(self):
        return self.valid_moves
    def get_value(self):
        return self.value
    def get_check_flag(self):
        return self.checking
    def record_moves(self, move):
        self.moves.append(move)
    def update_valid_moves(self, VML): #VML = Valid moves list... 
        self.valid_moves = VML
    def clear_valid_moves(self):
        self.valid_moves = []
    def set_initial_position(self, pos):
        self.col = pos[1]
        self.row = pos[0]
    def set_check_flag(self, flag):
        self.checking = flag
    def set_hasMoved_flag(self, flag):
        self.has_moved = flag
    def set_castle_flags(self, flags):
        self.castle_long = flags[0]
        self.castle_short = flags[1]
    def get_castle_long(self):
        return self.castle_long
    def get_castle_short(self):
        return self.castle_short
    def increase_value(self, inc):
        self.value += inc

class Pawn(Piece): # pawns can move in one direction defined by their color... 
    
    def __init__(self, coord, color):
        if(color == 'W'):
           self.direction = -1 
        else:
            self.direction = 1 
        super().__init__(coord, 'Pawn', color, 1.0)

class Bishop(Piece):

    def __init__(self, coord, color):
        super().__init__(coord, 'Bishop', color, 3.15)

class Knight(Piece):

    def __init__(self, coord, color):
        super().__init__(coord, 'Knight', color, 3.0)
    
class Rook(Piece):

    def __init__(sself, coord, color):
        super().__init__(coord, 'Rook', color, 5.0)

class Queen(Piece):

    def __init__(self, coord, color):
        super().__init__(coord, 'Queen', color, 9.0)

class King(Piece):

    def __init__(self, coord, color):
        #super().__init__(coord, 'King', color, math.inf)
        super().__init__(coord, 'King', color, 0)
