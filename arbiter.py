from piece  import Piece
from board import Board 
from drag import Drag
from statics import *
import copy
import gc

class arbiter():  #will determine legal moves for selected piece at the time of selection. 

    def __init__(self, piece = None):
        self.piece = piece 
        self.valid_moves = [] #will send this list to the piece object and update it as the game goes on.. 
        self.check_flag = False #will begin as false

    #setters. 
    def set_piece(self, selected_piece):
        self.piece = selected_piece

    def set_valid_moves(self, new_valid_moves):
        self.valid_moves = new_valid_moves
    #getters. 
    def get_piece(self):
        return self.piece
    def get_valid_moves(self):
        return self.valid_moves
    def get_check_flag(self):
        return self.check_flag
    def send_valid_moves(self): #method to update the valid moves list for the piece object. 
        self.piece.update_valid_moves(self.valid_moves)
    def set_valid_moves_outer(self, new_moves, piece):
        piece.update_valid_moves(new_moves)

    def check_confirmed(self, list_pieces, dragger):
        if(list_pieces == []): #no checks found -> empty list. 
            self.check_flag = False
            dragger.set_in_check((False, None, []))
        else:
            temp =  []
            for tup in list_pieces:
                piece = tup[0]
                king = tup[1]
                temp.append(piece.get_initial_pos())
                #print("Check detected from " + piece.get_name() +" on "+king.get_color() +" "+ str(king.get_name()))
            dragger.set_in_check((True, king, temp))

    def find_all_valid_moves(self, board, piece, move_list, initial_pos, dragger):
        checks_found = [] 
        temp_board_OG = copy.deepcopy(board)
        #temp_board_OG_2 = copy.deepcopy(board)
        temp_piece = copy.deepcopy(piece)
        color = temp_piece.get_color()
        temp_list = copy.deepcopy(move_list)
        for move in move_list:
            #print(move)
            if(color == "B"): #moving a black piece : check if white pieces will hit king as result of move. 
                temp_board = copy.deepcopy(temp_board_OG)
                temp_board.squares[move[0]][move[1]].set_piece(temp_piece) # make move on fake board in memory.. 
                temp_board.squares[initial_pos[1]][initial_pos[0]].set_piece(None) # make move on fake board in memory.. 
                #check if any white pieces will hit king as result of move
                temp_dragger_B = Drag()
                for row in range(RWS):
                    for col in range(CLS):
                        p = temp_board.squares[row][col].get_piece()
                        #check if possible moves of the piece will include hitting black king... 
                        if(p !=None and p.get_color() == "W"):
                            p.set_initial_position((row, col))
                            temp_dragger_B.save_initial_direct((col, row))
                            temp_dragger_B.set_piece(p)
                            self.check_valid_moves(temp_board, temp_dragger_B, True, True, None)
                            #print(p.get_valid_moves())
                            for m in p.get_valid_moves():
                                if(temp_board.squares[m[0]][m[1]].get_piece() != None and temp_board.squares[m[0]][m[1]].get_piece().get_name() == "King" and 
                                    temp_board.squares[m[0]][m[1]].get_piece().get_color() == "B"):
                                    if(move in temp_list): #avoid no more move
                                        temp_list.remove(move)  
                #del temp_board
                #del temp_dragger_B

            elif(color == "W"):
                #print("HI",temp_piece )
                temp_board = copy.deepcopy(temp_board_OG)
                temp_board.squares[move[0]][move[1]].set_piece(temp_piece) # make move on fake board in memory.. 
                temp_board.squares[initial_pos[1]][initial_pos[0]].set_piece(None) # make move on fake board in memory.. 
                temp_dragger_W = Drag()
                #check if any white pieces will hit king as result of move
                for row in range(RWS):
                    for col in range(CLS):
                        p_W = temp_board.squares[row][col].get_piece()
                        #f = copy.deepcopy(temp_board_2.squares[row][col].get_piece())
                        #check if possible moves of the piece will include hitting black king... 
                        if(p_W != None and p_W.get_color() == "B"):
                            p_W.set_initial_position((row, col))
                            temp_dragger_W.save_initial_direct((col, row))
                            temp_dragger_W.set_piece(p_W)
                            self.check_valid_moves(temp_board, temp_dragger_W, True, True, None)
                            #print(p_W, p_W.get_valid_moves())
                            for m in p_W.get_valid_moves(): 
                                #if(p_W.get_name() == "Bishop"):
                                    #print(m, p_W, p_W.get_initial_pos())
                                if(temp_board.squares[m[0]][m[1]].get_piece()!=None and temp_board.squares[m[0]][m[1]].get_piece().get_name() == "King" and 
                                    temp_board.squares[m[0]][m[1]].get_piece().get_color() == "W"):
                                    if(move in temp_list): #avoid no more move
                                        temp_list.remove(move)
        return temp_list

    def is_check(self, move_list, board, piece, initial_pos, dragger): #will check if move will cause a check to occur i.e pinned pieces.
        checks_found = [] 
        temp_board_OG = copy.deepcopy(board)
        #temp_board_OG_2 = copy.deepcopy(board)
        temp_piece = copy.deepcopy(piece)
        color = temp_piece.get_color()
        temp_list = copy.deepcopy(move_list)
        for move in move_list:
            #print(move)
            if(color == "B"): #moving a black piece : check if white pieces will hit king as result of move. 
                temp_board = copy.deepcopy(temp_board_OG)
                temp_board.squares[move[0]][move[1]].set_piece(temp_piece) # make move on fake board in memory.. 
                temp_board.squares[initial_pos[1]][initial_pos[0]].set_piece(None) # make move on fake board in memory.. 
                #check if any white pieces will hit king as result of move
                temp_dragger_B = Drag()
                for row in range(RWS):
                    for col in range(CLS):
                        p = temp_board.squares[row][col].get_piece()
                        p_OF1 = board.squares[row][col].get_piece()
                        #check if possible moves of the piece will include hitting black king... 
                        if(p !=None and p.get_color() == "W"):
                            p.set_initial_position((row, col))
                            temp_dragger_B.save_initial_direct((col, row))
                            temp_dragger_B.set_piece(p)
                            self.check_valid_moves(temp_board, temp_dragger_B, True, True, None)
                            #print(p.get_valid_moves())
                            for m in p.get_valid_moves():
                                if(temp_board.squares[m[0]][m[1]].get_piece() != None and temp_board.squares[m[0]][m[1]].get_piece().get_name() == "King" and 
                                    temp_board.squares[m[0]][m[1]].get_piece().get_color() == "B"):
                                    if(move in temp_list): #avoid no more move
                                        temp_list.remove(move)  
                #del temp_board
                #del temp_dragger_B

            elif(color == "W"):
                temp_board = copy.deepcopy(temp_board_OG)
                temp_board.squares[move[0]][move[1]].set_piece(temp_piece) # make move on fake board in memory.. 
                temp_board.squares[initial_pos[1]][initial_pos[0]].set_piece(None) # make move on fake board in memory.. 
                temp_dragger_W = Drag()
                #check if any white pieces will hit king as result of move
                for row in range(RWS):
                    for col in range(CLS):
                        p_W = temp_board.squares[row][col].get_piece()
                        p_OF = board.squares[row][col].get_piece()
                        #f = copy.deepcopy(temp_board_2.squares[row][col].get_piece())
                        #check if possible moves of the piece will include hitting black king... 
                        if(p_W != None and p_W.get_color() == "B"):
                            p_W.set_initial_position((row, col))
                            temp_dragger_W.save_initial_direct((col, row))
                            temp_dragger_W.set_piece(p_W)
                            self.check_valid_moves(temp_board, temp_dragger_W, True, True, None)
                            #print(p_W, p_W.get_valid_moves())
                            for m in p_W.get_valid_moves(): 
                                #if(p_W.get_name() == "Bishop"):
                                    #print(m, p_W, p_W.get_initial_pos())
                                if(temp_board.squares[m[0]][m[1]].get_piece()!=None and temp_board.squares[m[0]][m[1]].get_piece().get_name() == "King" and 
                                    temp_board.squares[m[0]][m[1]].get_piece().get_color() == "W"):
                                    if(move in temp_list): #avoid no more move
                                        temp_list.remove(move) 
                #del temp_board
                #del temp_dragger_W
        if(color == "B"): #moving a black piece : check if white pieces will hit king as result of move. 
            temp_board_2 = copy.deepcopy(board)
            #check if any white pieces will hit king as result of move
            temp_dragger_C = Drag()
            for row in range(RWS):
                for col in range(CLS):
                    b = copy.deepcopy(temp_board_2.squares[row][col].get_piece())
                    #check if possible moves of the piece will include hitting black king... 
                    #check for any checking threats current board...
                    if(b!=None and b.get_color() == "W"):
                       #print(b, b.get_initial_pos())
                       b.set_initial_position((row, col))
                       temp_dragger_C.save_initial_direct((col, row))
                       temp_dragger_C.set_piece(b)
                       #self.check_valid_moves(temp_board_2, temp_dragger_C, True, True) s
                       self.check_valid_moves(temp_board_2, temp_dragger_C, False, True, board.squares[row][col].get_piece()) 
                      # self.set_valid_moves_outer(b.get_valid_moves(), board.squares[row][col].get_piece())
                       #print(b, b.get_initial_pos(), b.get_valid_moves())
                       for n in b.get_valid_moves():
                           #self.set_valid_moves_outer(b.get_valid_moves(), board.squares[row][col].get_piece())
                           if(temp_board_2.squares[n[0]][n[1]].get_piece() != None and temp_board_2.squares[n[0]][n[1]].get_piece().get_name() == "King" and 
                               temp_board_2.squares[n[0]][n[1]].get_piece().get_color() == "B"):
                                checks_found.append((b, n, temp_board_2.squares[n[0]][n[1]].get_piece()))
            #del temp_board_2
            #del temp_dragger_C
        elif(color == "W"):
            temp_board_2 = copy.deepcopy(board)
            temp_dragger_Z = Drag()
            #check if any white pieces will hit king as result of move
            for row in range(RWS):
                for col in range(CLS):
                    f = copy.deepcopy(temp_board_2.squares[row][col].get_piece())
                    #check if possible moves of the piece will include hitting black king... 
                    if(f!=None and f.get_color() == "B"):
                        f.set_initial_position((row, col))
                        temp_dragger_Z.save_initial_direct((col, row))
                        temp_dragger_Z.set_piece(f)
                        #self.check_valid_moves(temp_board_2, temp_dragger_Z, True, True) 
                        self.check_valid_moves(temp_board_2, temp_dragger_Z, False, True, board.squares[row][col].get_piece()) 
                        #self.set_valid_moves_outer(f.get_valid_moves(), board.squares[row][col].get_piece())
                        for n in f.get_valid_moves():
                            #self.set_valid_moves_outer(f.get_valid_moves(), board.squares[row][col].get_piece())
                            if(temp_board_2.squares[n[0]][n[1]].get_piece() != None and temp_board_2.squares[n[0]][n[1]].get_piece().get_name() == "King" and 
                                temp_board_2.squares[n[0]][n[1]].get_piece().get_color() == "W"):
                                checks_found.append((f, n, temp_board_2.squares[n[0]][n[1]].get_piece()))                
            #del temp_board_2
            #del temp_dragger_Z
        self.check_confirmed(checks_found, dragger)
        #del temp_board_OG
        #gc.collect()
        return temp_list

    #misc.
    def scout(self, board, dragger, move_list, flag1, flag2, piece_2):
        move_list_filtered_2 = []
        move_list_filtered = []
        initial_pos = dragger.get_initial_pos()
        #print(initial_pos)
        piece = dragger.get_piece()
        for coords in move_list:
            if(board.squares[coords[0]][coords[1]].get_piece() != None): #if moving to a square with same color piece. )
                if(board.squares[coords[0]][coords[1]].get_piece().get_color() != piece.get_color()):
                    move_list_filtered_2.append(coords)
            else:
                move_list_filtered_2.append(coords)
        if(flag1 == True and flag2 == True and piece_2 != None):
            self.set_valid_moves_outer(move_list_filtered_2, piece_2)
            
        elif(flag1 == True and flag2 == True):
            self.set_valid_moves_outer(move_list_filtered_2, dragger.get_piece())
            
        elif(flag1 == False and flag2 == False):
            move_list_filtered =self.is_check(move_list_filtered_2, board, piece, initial_pos, dragger) 
            self.set_valid_moves(move_list_filtered_2)
            #return self.check_king(move_list_filtered, dragger, board)

        elif(flag1 == True and flag2 == False):
            move_list_filtered = self.is_check(move_list_filtered_2, board, piece, initial_pos, dragger) 
            self.set_valid_moves(move_list_filtered)

        elif(flag1 == False and flag2 == True):
            move_list_filtered = self.find_all_valid_moves(board, piece, move_list_filtered_2, initial_pos, dragger)
            #print("WAGWAN", piece_2, move_list_filtered)
            self.set_valid_moves_outer(move_list_filtered, piece_2)

        #if(dragger.get_piece().get_name() == "Bishop" and dragger.get_piece().get_color() == "W" and flag2):
            #print(dragger.get_piece(), move_list_filtered_2, flag1, flag2)
        #print(flag1, flag2, dragger.get_initial_pos())
        self.send_valid_moves()
    
    def check_pawn_moves(self, board, dragger, dir, flag1, flag2, piece):
        temp = [] # max of 8 possible moves.
        possible_moves = [] 
        #king moves in one square intervals in all directions. EX: if king is on square 4, 5. Valid moves are 
        initial_piece_position = dragger.get_initial_pos() #fetch initial piece position (col :x, row :y)
        #print(dragger.get_piece(), initial_piece_position)
        #fetch possible squares if board is empty..
        row, col = initial_piece_position[1], initial_piece_position[0]
        #print(dragger.get_piece(), dragger.get_piece().get_color(), dragger.get_position())
        #check if pawn can do the start square skip. +2 instead of +1 in the row number. 
        #set row, vary col : 
        temp.append((row+(-1*dir), col)) #move forward. 
        temp.append((row+(-1*dir), col-1))#only if can eat on either side. 
        temp.append((row+(-1*dir), col+1))#only if can eat on either side. 
        if(dragger.get_piece().get_color() == 'B' and initial_piece_position[1] == 1):# if black check if pawn on starting 2nd rank [row num 1]
            if(board.squares[row+1][col].get_piece() == None):
                temp.append((row+(-2*dir), col)) #move forward 2 squares. 
        if(dragger.get_piece().get_color() == 'W' and initial_piece_position[1] == 6): # if white check if pawn on starting 7th rank [row num 6]
            if(board.squares[row-1][col].get_piece() == None):
                temp.append((row+(-2*dir), col)) #move forward 2 squares. 
        for i in range(len(temp)):
            coord = temp[i]
            #ceck edges of map:
            if(i == 0 or i ==3):
                if (coord[0] > 7 or coord[1] > 7 or coord[0] < 0 or coord[1] < 0) == False:
                    if(board.squares[coord[0]][coord[1]].get_piece() == None): #check that no piece is in front of pawn before movement. 
                        possible_moves.append(coord)
                else: 
                    pass
            elif(i==1 or i==2):
                if(coord[1] > 7):
                    pass
                else:
                    if (coord[0] > 7 or coord[1] > 7 or coord[0] < 0 or coord[1] < 0) == False:
                        piece_temp = board.squares[coord[0]][coord[1]].get_piece()
                        if(piece_temp != None and piece_temp.get_color() != dragger.get_piece().get_color()):
                            possible_moves.append(coord)
                        else:
                            pass
        #print(dragger.get_piece(), initial_piece_position, possible_moves)
        self.scout(board, dragger, possible_moves, flag1, flag2, piece)

    def check_rook_moves(self, board, dragger, flag1, flag2, piece):
        possible_moves = []
        initial_piece_position = dragger.get_initial_pos() #fetch initial piece position (col :x, row :y)
        row, col = initial_piece_position[1], initial_piece_position[0]
        R_flag = True #right flag if false... Means max right movement was found. 
        L_flag = True #left flag if false... Means max left movement was found.
        U_flag = True #up flag if false means max up movement was found. 
        D_flag = True #down flag if false means max down movement was found. 
        for i in range(1,8):
            #check if new location contains same color stop piece.. See doc to understand what a stop piece is for the rook. Same concept for bishop/Queen. 
            if(col + i <= 7 and R_flag != False): #check if not out of bounds...
                if(board.squares[row][col+i].get_piece() != None):
                    R_flag = False
                    if(board.squares[row][col+i].get_piece().get_color() != dragger.get_piece().get_color()):
                        #print("lol")
                        possible_moves.append((row, col+i))
            else:
                R_flag = False
            if(col - i >= 0 and L_flag != False):
                #print(possible_moves, col, i, col - i)
                if(board.squares[row][col-i].get_piece() != None):
                    L_flag = False
                    if(board.squares[row][col-i].get_piece().get_color() != dragger.get_piece().get_color()):
                        possible_moves.append((row, col-i))
            else:
                L_flag = False
            if(row - i >= 0 and U_flag != False):
                if(board.squares[row-i][col].get_piece() != None):
                    U_flag = False
                    if(board.squares[row-i][col].get_piece().get_color() != dragger.get_piece().get_color()):
                        possible_moves.append((row-i, col))
            else:
                U_flag = False
            if(row + i <= 7 and D_flag != False):
                if(board.squares[row+i][col].get_piece() != None):
                    D_flag = False
                    if(board.squares[row+i][col].get_piece().get_color() != dragger.get_piece().get_color()):
                        possible_moves.append((row+i, col))
            else:
                D_flag = False
            #move right
            if(R_flag):
                possible_moves.append((row, col+i))
            #move left
            if(L_flag):
                #print(row, col - i, i)
                possible_moves.append((row, col-i))
            #move up 
            if(U_flag):
                possible_moves.append((row-i, col))
            #move down
            if(D_flag):
                possible_moves.append((row+i, col))
        self.scout(board, dragger, possible_moves, flag1, flag2, piece)

    def check_knight_moves(self, board, dragger, flag1, flag2, piece):
        temp = [] # max of 8 possible moves.
        possible_moves = [] 
        initial_piece_position = dragger.get_initial_pos() #fetch initial piece position (col :x, row :y)
        #fetch possible squares if board is empty..
        row, col = initial_piece_position[1], initial_piece_position[0]
        #set row, vary col : 
        temp.append((row+2, col+1))
        temp.append((row+2, col-1))
        temp.append((row-2, col+1))
        temp.append((row-2, col-1))
        temp.append((row-1, col+2))
        temp.append((row+1, col+2))
        temp.append((row+1, col-2))
        temp.append((row-1, col-2))
        for coord in temp:
            #ceck edges of map:
            if (coord[0] > 7 or coord[1] > 7 or coord[0] < 0 or coord[1] < 0) == False:
                possible_moves.append(coord)
            else: 
                pass
        self.scout(board, dragger, possible_moves, flag1, flag2, piece)

    def check_bishop_moves(self, board, dragger, flag1, flag2, piece):
        possible_moves = []
        initial_piece_position = dragger.get_initial_pos() #fetch initial piece position (col :x, row :y)
        #print(initial_piece_position, flag2)
        row, col = initial_piece_position[1], initial_piece_position[0]
        #straigh line moves. (Logic of rook)
        R_flag = True #right flag if false... Means max right movement was found. 
        L_flag = True #left flag if false... Means max left movement was found.
        U_flag = True #up flag if false means max up movement was found. 
        D_flag = True #down flag if false means max down movement was found. 
        #Diags line moves. (logic like bishop)
        UR_flag = True #right flag if false... Means max right movement was found. 
        UL_flag = True #left flag if false... Means max left movement was found.
        DR_flag = True #Down Right flag if false means max up movement was found. 
        DL_flag = True #Down Left if false means max down movement was found. 
        for i in range(1,8):
            #check if new location contains same color stop piece.. See doc to understand what a stop piece is for the rook. Same concept for bishop/Queen. 
            if(col + i <= 7 and row - i >= 0 and UR_flag != False): #check if not out of bounds...
                if(board.squares[row-i][col+i].get_piece() != None):
                    UR_flag = False
                    if(board.squares[row-i][col+i].get_piece().get_color() != dragger.get_piece().get_color()):
                        possible_moves.append((row-i, col+i))
            else:
                UR_flag = False
            if(col - i >= 0 and row - i >= 0 and UL_flag != False):
                #print(possible_moves, col, i, col - i)
                if(board.squares[row-i][col-i].get_piece() != None):
                    UL_flag = False
                    if(board.squares[row-i][col-i].get_piece().get_color() != dragger.get_piece().get_color()):
                        possible_moves.append((row-i, col-i))
            else:
                UL_flag = False
            if(row + i <= 7 and col + i <= 7 and DR_flag != False):
                if(board.squares[row+i][col+i].get_piece() != None):
                    DR_flag = False
                    if(board.squares[row+i][col+i].get_piece().get_color() != dragger.get_piece().get_color()):
                        possible_moves.append((row+i, col+i))
            else:
                DR_flag = False
            if(row + i <= 7 and col - i >= 0 and DL_flag != False):
                if(board.squares[row+i][col-i].get_piece() != None):
                    DL_flag = False
                    if(board.squares[row+i][col-i].get_piece().get_color() != dragger.get_piece().get_color()):
                        possible_moves.append((row+i, col-i))
            else:
                DL_flag = False
            #move right
            if(UR_flag):
                possible_moves.append((row-i, col+i))
            #move left
            if(UL_flag):
                #print(row, col - i, i)
                possible_moves.append((row-i, col-i))
            #move up 
            if(DR_flag):
                possible_moves.append((row+i, col+i))
            #move down
            if(DL_flag):
                possible_moves.append((row+i, col-i))
        self.scout(board, dragger, possible_moves, flag1, flag2, piece)

    def check_queen_moves(self, board, dragger, flag1, flag2, piece):
        possible_moves = []
        initial_piece_position = dragger.get_initial_pos() #fetch initial piece position (col :x, row :y)
        row, col = initial_piece_position[1], initial_piece_position[0]
         #straigh line moves. (Logic of rook)
        R_flag = True #right flag if false... Means max right movement was found. 
        L_flag = True #left flag if false... Means max left movement was found.
        U_flag = True #up flag if false means max up movement was found. 
        D_flag = True #down flag if false means max down movement was found. 
        #Diags line moves. (logic like bishop)
        UR_flag = True #right flag if false... Means max right movement was found. 
        UL_flag = True #left flag if false... Means max left movement was found.
        DR_flag = True #Down Right flag if false means max up movement was found. 
        DL_flag = True #Down Left if false means max down movement was found. 
        for i in range(1,8):
            #check if new location contains same color stop piece.. See doc to understand what a stop piece is for the rook. Same concept for bishop/Queen. 
            if(col + i <= 7 and row - i >= 0 and UR_flag != False): #check if not out of bounds...
                if(board.squares[row-i][col+i].get_piece() != None):
                    UR_flag = False
                    if(board.squares[row-i][col+i].get_piece().get_color() != dragger.get_piece().get_color()):
                        possible_moves.append((row-i, col+i))
            else:
                UR_flag = False
            if(col - i >= 0 and row - i >= 0 and UL_flag != False):
                #print(possible_moves, col, i, col - i)
                if(board.squares[row-i][col-i].get_piece() != None):
                    UL_flag = False
                    if(board.squares[row-i][col-i].get_piece().get_color() != dragger.get_piece().get_color()):
                        possible_moves.append((row-i, col-i))
            else:
                UL_flag = False
            if(row + i <= 7 and col + i <= 7 and DR_flag != False):
                if(board.squares[row+i][col+i].get_piece() != None):
                    DR_flag = False
                    if(board.squares[row+i][col+i].get_piece().get_color() != dragger.get_piece().get_color()):
                        possible_moves.append((row+i, col+i))
            else:
                DR_flag = False
            if(row + i <= 7 and col - i >= 0 and DL_flag != False):
                if(board.squares[row+i][col-i].get_piece() != None):
                    DL_flag = False
                    if(board.squares[row+i][col-i].get_piece().get_color() != dragger.get_piece().get_color()):
                        possible_moves.append((row+i, col-i))
            else:
                DL_flag = False
            
            #straight line moves logic...
            if(col + i <= 7 and R_flag != False): #check if not out of bounds...
                if(board.squares[row][col+i].get_piece() != None):
                    R_flag = False
                    if(board.squares[row][col+i].get_piece().get_color() != dragger.get_piece().get_color()):
                        #print("lol")
                        possible_moves.append((row, col+i))
            else:
                R_flag = False
            if(col - i >= 0 and L_flag != False):
                #print(possible_moves, col, i, col - i)
                if(board.squares[row][col-i].get_piece() != None):
                    L_flag = False
                    if(board.squares[row][col-i].get_piece().get_color() != dragger.get_piece().get_color()):
                        possible_moves.append((row, col-i))
            else:
                L_flag = False
            if(row - i >= 0 and U_flag != False):
                if(board.squares[row-i][col].get_piece() != None):
                    U_flag = False
                    if(board.squares[row-i][col].get_piece().get_color() != dragger.get_piece().get_color()):
                        possible_moves.append((row-i, col))
            else:
                U_flag = False
            if(row + i <= 7 and D_flag != False):
                if(board.squares[row+i][col].get_piece() != None):
                    D_flag = False
                    if(board.squares[row+i][col].get_piece().get_color() != dragger.get_piece().get_color()):
                        possible_moves.append((row+i, col))
            else:
                D_flag = False
            
            #move right
            if(UR_flag):
                possible_moves.append((row-i, col+i))
            #move left
            if(UL_flag):
                #print(row, col - i, i)
                possible_moves.append((row-i, col-i))
            #move up 
            if(DR_flag):
                possible_moves.append((row+i, col+i))
            #move down
            if(DL_flag):
                possible_moves.append((row+i, col-i))
            #move right
            if(R_flag):
                possible_moves.append((row, col+i))
            #move left
            if(L_flag):
                #print(row, col - i, i)
                possible_moves.append((row, col-i))
            #move up 
            if(U_flag):
                possible_moves.append((row-i, col))
            #move down
            if(D_flag):
                possible_moves.append((row+i, col))
        self.scout(board, dragger, possible_moves, flag1, flag2, piece)

    def can_castle(self, board, dragger): #row, col
        piece = dragger.get_piece()
        flags = [True, True] #long short
        if(piece.get_color() == "B"):
            if(piece.get_hasMoved_flag() == False and board.squares[0][0].get_piece() != None and board.squares[0][0].get_piece().get_name() == "Rook"
               and board.squares[0][0].get_piece().get_hasMoved_flag() == False): #checking LONG side for black.
                if(board.squares[0][1].get_piece() == None and board.squares[0][2].get_piece() == None and board.squares[0][3].get_piece() == None):#check no pieces are between king in rook. 
                    #check if any piece is going to check th squares in between.. 
                    for p in board.get_white_pieces():
                        if(p.get_name() == "Pawn"):
                                row, col = p.get_initial_pos()[1], p.get_initial_pos()[0]
                                #print(p.get_name(), p.get_color(), p.get_initial_pos(), (row, col))
                                #print((row, col))
                                if((row-1,col+1) == (0,1) or (row-1,col+1) == (0,2) or (row-1,col+1) == (0,3) or (row-1,col-1) == (0,1) or 
                                   (row-1,col-1) == (0,2) or (row-1,col-1) == (0,3)):
                                    flags[0] = False
                                
                        for move in p.get_valid_moves():
                            if(move == (0,1) or move == (0,2) or move == (0,3)):
                                flags[0] = False
                else:
                    flags[0] = False
            else:
                flags[0] = False

            if(piece.get_hasMoved_flag() == False and board.squares[0][7].get_piece() != None and board.squares[0][7].get_piece().get_name() == "Rook"
               and board.squares[0][7].get_piece().get_hasMoved_flag() == False): #checking SHORT side for black.
                if(board.squares[0][6].get_piece() == None and board.squares[0][5].get_piece() == None):#check no pieces are between king in rook. 
                    #print(board.squares[0][5].get_piece(), board.squares[0][6].get_piece())
                    for p in board.get_white_pieces():
                        if(p.get_name() == "Pawn"):
                                row, col = p.get_initial_pos()[1], p.get_initial_pos()[0]
                                #print(p.get_name(), p.get_color(), p.get_initial_pos(), (row, col))
                                #print(p, p.get_initial_pos())
                                #print((row-1,col+1), (row-1,col+1), (row-1,col-1), (row-1,col-1))
                                if(((row-1,col-1) == (0,6)) or ((row-1,col-1) == (0,5)) or ((row-1,col+1) == (0,5)) or ((row-1,col+1) == (0,6))): #(row, col) format
                                    #if(move != (0,5) and move != (0,6)):
                                    #print("YO 1 ")
                                    flags[1] = False
                                    
                        for move in p.get_valid_moves():
                            if(move == (0,5) or move == (0,6)):
                                #print("YO 2 ")
                                flags[1] = False
                else:
                    #print(board.squares[0][5].get_piece(), board.squares[0][6].get_piece())
                    flags[1] = False
            else:
                #print(board.squares[0][5].get_piece(), board.squares[0][6].get_piece())
                flags[1] = False
        
        elif(piece.get_color() == "W"):  
            #print(piece.get_hasMoved_flag(),  board.squares[7][0].get_piece(),  board.squares[7][0].get_piece().get_name(), 
                   #board.squares[7][0].get_piece().get_hasMoved_flag())
            if(piece.get_hasMoved_flag() == False and board.squares[7][0].get_piece() != None and board.squares[7][0].get_piece().get_name() == "Rook"
               and board.squares[7][0].get_piece().get_hasMoved_flag() == False): #checking LONG side for white.
                if(board.squares[7][1].get_piece() == None and board.squares[7][2].get_piece() == None and board.squares[7][3].get_piece() == None ):#check no pieces are between king in rook. 
                    #check if any piece is going to check th squares in between.. 
                    for p in board.get_black_pieces():
                        if(p.get_name() == "Pawn"):
                                row, col = p.get_initial_pos()[1], p.get_initial_pos()[0]
                                if((row+1,col+1) == (7,1) or (row+1,col+1) == (7,2) or (row+1,col+1) == (7,3) or (row+1,col-1) == (0,1) or 
                                   (row+1,col-1) == (7,2) or (row+1,col-1) == (7,3)):
                                   #if(move != (7,1) and move != (7,2) and move != (7,3)):
                                        flags[0] = False
                        for move in p.get_valid_moves():
                            if(move == (7,1) or move == (7,2) or move == (7,3)):
                                flags[0] = False
                else:
                    flags[0] = False
            else:
                flags[0] = False
                            
            if(piece.get_hasMoved_flag() == False and board.squares[7][7].get_piece() != None and board.squares[7][7].get_piece().get_name() == "Rook"
               and board.squares[7][7].get_piece().get_hasMoved_flag() == False): #checking SHORT side for white.
                if(board.squares[7][6].get_piece() == None and board.squares[7][5].get_piece() == None):#check no pieces are between king in rook. 
                   for p in board.get_black_pieces():
                        if(p.get_name() == "Pawn"):
                                row, col = p.get_initial_pos()[1], p.get_initial_pos()[0]
                                #print((row, col))
                                if((row+1,col+1) == (7,5) or (row+1,col+1) == (7,6) or (row+1,col-1) == (7,5) or (row+1,col-1) == (7,6)):
                                    #if(move != (7,5) and move != (7,6)):
                                        flags[1] = False
                        for move in p.get_valid_moves():
                            if(move == (7,5) or move == (7,6)):
                                flags[1] = False
                else:
                    flags[1] = False
            else:
                flags[1] = False
        dragger.get_piece().set_castle_flags(flags)
        #print(dragger.get_piece(), dragger.get_piece().get_castle_long(), dragger.get_piece().get_castle_short())
    
   
         
    def check_king_moves(self, board, dragger, flag1, flag2, piece):
        #self.can_castle(board, dragger)
        temp = [] # max of 8 possible moves.
        possible_moves = [] 
        #king moves in one square intervals in all directions. EX: if king is on square 4, 5. Valid moves are 
        initial_piece_position = dragger.get_initial_pos() #fetch initial piece position (col :x, row :y)
        #fetch possible squares if board is empty..
        row, col = initial_piece_position[1], initial_piece_position[0]
        #set row, vary col : 
        temp.append((row, col+1))
        temp.append((row, col-1))
        temp.append((row+1, col))
        temp.append((row-1, col))
        temp.append((row-1, col-1))
        temp.append((row+1, col+1))
        temp.append((row+1, col-1))
        temp.append((row-1, col+1))
        #checking castle rights.
        #print(dragger.get_piece(),dragger.get_piece().get_castle_long(), dragger.get_piece().get_castle_short() )
        if(dragger.get_piece().get_castle_long()):
            temp.append((row, col-2))
        if(dragger.get_piece().get_castle_short()):
            temp.append((row, col + 2))
        for coord in temp:
            #ceck edges of map:
            if (coord[0] > 7 or coord[1] > 7 or coord[0] < 0 or coord[1] < 0) == False:
                possible_moves.append(coord)
            else: 
                pass
        #print(self.can_castle(board, dragger))
        self.scout(board, dragger, possible_moves, flag1, flag2, piece)
    
    #CHECKING VALID MOVES based on current location 
    def check_valid_moves(self, board, dragger, flag1, flag2, piece):
        if(dragger.get_piece() == None): #if no piece is selected... 
            return None 
        elif(dragger.get_piece().get_name() == 'Pawn'):
            if(dragger.get_piece().get_color() == 'B'):
                dir = -1 #black goes down the board
            else:
                dir = 1 #white goes up the board
            #print(self.piece, self.piece.get_color(), dir)
            #print(dragger.get_piece(), dragger.get_piece().get_color(), dir)
            self.check_pawn_moves(board, dragger, dir, flag1, flag2, piece)
        elif(dragger.get_piece().get_name() == 'Rook'):
            self.check_rook_moves(board, dragger, flag1, flag2, piece)
        elif(dragger.get_piece().get_name() == 'Knight'):
            self.check_knight_moves(board, dragger, flag1, flag2, piece)
        elif(dragger.get_piece().get_name() == 'Bishop'):
            self.check_bishop_moves(board, dragger, flag1, flag2, piece)
        elif(dragger.get_piece().get_name() == 'Queen'):
            #print(self.piece, self.piece.get_color(), dragger.get_initial_pos(), self.piece.get_initial_pos())
            self.check_queen_moves(board, dragger, flag1, flag2, piece)
        elif(dragger.get_piece().get_name() == 'King'):
            self.check_king_moves(board, dragger, flag1, flag2, piece)
    


