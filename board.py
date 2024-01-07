
from statics import *
from square import Square
from piece import *
import inspect

class Board():
    def __init__(self):
        #print(inspect.stack()[1][3])
        self.squares = [[0,0,0,0,0,0,0,0] for col in range(CLS)]
        self.pieces_list= []
        self.white_pieces_list = [] 
        self.black_pieces_list = []
        self.create()
        self.add_pieces('W')
        self.add_pieces('B')
        self.create_pieces_list()

    def build_black_pieces_list(self):
        for piece in self.pieces_list:
            if(piece.get_color() == "B"):
                self.black_pieces_list.append(piece)

    def build_white_pieces_list(self):
        for piece in self.pieces_list:
            if(piece.get_color() == "W"):
                self.white_pieces_list.append(piece)

    def get_board(self):
        temp = []
        temp1 = [] 
        for n in self.squares:
            for square in n:
                temp1.append(square.get_piece().get_name() if square.get_piece()!= None else square.get_piece())
            temp.append(temp1)
            temp1 = []
        for i in temp:
            print(i)
    def get_pieces(self):
        return self.pieces_list
    
    def get_black_pieces(self):
        return self.black_pieces_list

    def get_white_pieces(self):
        return self.white_pieces_list
        
    def create(self): #create the board
        #loop and initialize a square object for each 0 in self.squares list.
        for row in range(RWS):
            for col in range(CLS):
                self.squares[row][col] = Square(row, col)

    def create_pieces_list(self):
        #print(inspect.stack()[1][3])
        self.pieces_list= [] #reset the list and build again. 
        self.white_pieces_list = [] #reset the list and build again.
        self.black_pieces_list = [] #reset the list and build again.
        for row in range(RWS):
            for col in range(CLS):
                if(self.squares[row][col].get_piece() != None):
                    self.pieces_list.append(self.squares[row][col].get_piece())
                    if(self.squares[row][col].get_piece().get_color() == "W"):
                        self.white_pieces_list.append(self.squares[row][col].get_piece())
                    if(self.squares[row][col].get_piece().get_color() == "B"):
                        self.black_pieces_list.append(self.squares[row][col].get_piece())
        self.piece_list = list(set(self.pieces_list))
        self.white_pieces_list = list(set(self.white_pieces_list))
        self.black_pieces_list = list(set(self.black_pieces_list))
        

                    
    def add_pieces(self, color): #add pieces to the board [Black or white]
        #print(inspect.stack()[1][3])
        pawn_row, other_row = (6, 7) if color == 'W' else (1,0)
        #Pawns
        for col in range(CLS):
            #self.squares[pawn_row][col] = Square(pawn_row, col, Pawn((pawn_row, col), color))
            self.squares[pawn_row][col] = Square(pawn_row, col, Pawn((col, pawn_row), color))

        #knights 
        self.squares[other_row][1] = Square(other_row, 1, Knight((1, other_row), color))
        self.squares[other_row][6] = Square(other_row, 6, Knight((6, other_row), color))

        #Bishops 
        self.squares[other_row][2] = Square(other_row, 2, Bishop((2, other_row), color))
        self.squares[other_row][5] = Square(other_row, 5, Bishop((5, other_row), color))

        #Rooks 
        self.squares[other_row][0] = Square(other_row, 0, Rook((0, other_row), color))
        self.squares[other_row][7] = Square(other_row, 7, Rook((7, other_row), color))

        #Queen
        self.squares[other_row][3] = Square(other_row, 3, Queen((3, other_row), color))

        #King
        self.squares[other_row][4] = Square(other_row, 4, King((4, other_row), color))
