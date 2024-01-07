from board import Board
import random
import copy

class engine():
    def __init__(self):
        self.invalid = []
        self.best_move = [] #piece, move, eval
        self.center_squares = [(3,3), (4,3), (4,4), (3,4)] #col, row
        self.checking = False

    def can_take_enemy_king(self, board, dragger, arbitter_instance): #method will check if a check was done on enemy. AKA white... 
        #self.update_all_valid_moves(board, dragger, arbitter_instance)
        arbitter_instance.check_valid_moves(board, dragger, True, False, None)
        flag = False
        for piece in board.get_black_pieces():
            #print("MEOW", piece, (piece.get_initial_pos()[1], piece.get_initial_pos()[0]), piece.get_valid_moves())
            for move in piece.get_valid_moves():
                if(board.squares[move[0]][move[1]].get_piece() != None and board.squares[move[0]][move[1]].get_piece() == "King"
                   and board.squares[move[0]][move[1]].get_piece().get_color() == "W" ):
                    #print("MEOW", piece, move)
                    flag = True
                    return flag
        return flag

    def eval_board(self, board): #convert board position to numerical value to use for min max.
        #print(board.get_board())
        #check for checkmate. 
        mate_Skew_W = -1000000 #if black mates white in curr position. 
        mate_Skew_B =  1000000 #if white mates black in curr position. 
        total = 0
        for piece_W in board.get_white_pieces(): #loop all white peices
            if(piece_W.get_valid_moves() != None):
                mate_Skew_W = 0
            #add bais to pieces in better locations. 
            if(piece_W.get_name() == "Pawn"):
                if(piece_W.get_initial_pos() in self.center_squares):
                    piece_W.increase_value(1.5)
            elif(piece_W.get_name() == "Knight"):
                multiplier = len(piece_W.get_valid_moves())
                piece_W.increase_value(0.05*multiplier) #can increase up to 0.4 if knight can move to 8 different squares
            total += piece_W.get_value()

        for piece_B in board.get_black_pieces(): #loop all black peices
            if(piece_B.get_valid_moves() != None):
                mate_Skew_B = 0
            if(piece_B.get_name() == "Pawn"):
                if(piece_B.get_initial_pos() in self.center_squares):
                    piece_B.increase_value(1.5)
            elif(piece_B.get_name() == "Knight"):
                multiplier = len(piece_B.get_valid_moves())
                piece_B.increase_value(0.05*multiplier) #can increase up to 0.4 if knight can move to 8 different squares
            total -= piece_B.get_value()
        total = total + mate_Skew_B + mate_Skew_W
        #print(total,mate_Skew_B, mate_Skew_W)
        return total
    
    def white_lose(self, board): #will check if white has lost. Black wins by checkmate. 
        flag = True
       # print(len(board.get_white_pieces()))
        for piece in board.get_white_pieces(): # make sure to only look at pieces with available moves...
            #print(f'{piece.get_name()} on {piece.get_initial_pos()} can move to {piece.get_valid_moves()}')
            if(piece.get_valid_moves() != []):  #piece can move somewhere. 
                flag = False
                break
        return flag
    
    def am_I_in_check(self, board, color):
        flag = False
        if(color == "B"):
            for piece in board.get_white_pieces(): # make sure to only look at pieces with available moves...
                #print(f'{piece.get_name()} on {piece.get_initial_pos()} can move to {piece.get_valid_moves()}')
                if(piece.get_valid_moves() != []): 
                    for move in piece.get_valid_moves():
                        #check if "B" king is target. 
                        #print(board.squares[move[0]][move[1]].get_piece().get_name(), board.squares[move[0]][move[1]].get_piece().get_name()
                        if(board.squares[move[0]][move[1]].get_piece() != None and
                           board.squares[move[0]][move[1]].get_piece().get_name() == "King" and 
                           board.squares[move[0]][move[1]].get_piece().get_color() == color):
                            flag = True
                            break
        elif(color == "W"):
            for piece in board.get_black_pieces(): # make sure to only look at pieces with available moves...
                #print(f'{piece.get_name()} on {piece.get_initial_pos()} can move to {piece.get_valid_moves()}')
                if(piece.get_valid_moves() != []): 
                    for move in piece.get_valid_moves():
                        #check if "W" king is target. 
                        #print(board.squares[move[0]][move[1]].get_piece().get_name(), board.squares[move[0]][move[1]].get_piece().get_name()
                        if(board.squares[move[0]][move[1]].get_piece() != None and
                           board.squares[move[0]][move[1]].get_piece().get_name() == "King" and 
                           board.squares[move[0]][move[1]].get_piece().get_color() == color):
                            flag = True
                            break
        
        return flag 
    
    def update_all_valid_moves(self, board, dragger, Arbiter_instance):
        Arbiter_instance.check_valid_moves(board, dragger, False, False, None)

    def move_finder(self, board): 
        possible_pieces = []
        for piece in board.get_black_pieces(): # make sure to only look at pieces with available moves...
            #print(f'{piece.get_name()} on {piece.get_initial_pos()} can move to {piece.get_valid_moves()}')
            if(piece.get_valid_moves() != []): 
                possible_pieces.append(piece)
        if(possible_pieces == []): #no moves found there for it may be a checkmate/Stalemate. 
            return (None, None)
        else:
            #print(possible_pieces)
            num = random.randint(0, len(possible_pieces)-1) #random piece
            move_piece = possible_pieces[num] #random piece
            #fetch the piece's initial position...
            initial_pos = move_piece.get_initial_pos()
            #print(move_piece, initial_pos)
            num2 = random.randint(0, len(move_piece.get_valid_moves())-1) # random move from random piece
            move = move_piece.get_valid_moves()[num2] # random move from random piece
            return (move_piece, move)
        
        
    def make_fake_move(self, board, move, piece): #returns a fake board upon making the fake move. 
        temp_board = copy.deepcopy(board)
        temp_piece = copy.deepcopy(piece)
        temp_board.create_pieces_list()
        #if(piece.get_color() == "W" and piece.get_name() == "Queen" and move == (4,6)):
        #    print("HI 1", temp_board.get_board())
        col, row = temp_piece.get_initial_pos()[0], piece.get_initial_pos()[1]  #col, row
        #print(move, piece, temp_board.squares[move[0]][move[1]].get_piece())
        #create a fake board. 
        #if(temp_piece.get_color() == "B"):
        #    print(temp_piece, (temp_piece.get_initial_pos()[1], temp_piece.get_initial_pos()[0]), move, temp_board.get_board())
        #print("OG", temp_board.get_board())
        #ceck if the move will consume another piece. 
        #print(piece,  (piece.get_initial_pos()[1], piece.get_initial_pos()[0]), move, temp_board.squares[move[0]][move[1]].get_piece())
        if(temp_board.squares[move[0]][move[1]].get_piece() != None): # means a piece is to be consumed. 
            eaten_piece = temp_board.squares[move[0]][move[1]].get_piece()
            if(eaten_piece.get_color() == "W"): 
                temp_board.get_white_pieces().remove(eaten_piece) #remove it from fake board pieces lists
                temp_board.get_pieces().remove(eaten_piece) #remove it from fake board pieces list
            elif(eaten_piece.get_color() == "B"):
                temp_board.get_black_pieces().remove(eaten_piece) #remove it from fake board pieces
                temp_board.get_pieces().remove(eaten_piece) #remove it from fake board pieces list
        #make the move...
        temp_board.squares[row][col].set_piece(None) #empty initial position
        temp_board.squares[move[0]][move[1]].set_piece(temp_piece) 
        #if(piece.get_color() == "B"):
        #    print("FINAL", temp_board.get_board())
        if(piece.get_name() == "King"): #castling for black pieces.  #put this in a method. If piece is white call white method, if black call black method. 
            #check long side white piece... 
            if(piece.get_castle_long() and move == (0,2)):#castle long side selected by white
                rook = temp_board.squares[0][0].get_piece()
                temp_board.squares[0][3].set_piece(rook)
                temp_board.squares[0][0].set_piece(None)
                rook.set_initial_position((0,3))
            if(piece.get_castle_short() and move == (0,6)):#castle short side selected by white
                rook = temp_board.squares[0][7].get_piece()
                temp_board.squares[0][5].set_piece(rook)
                temp_board.squares[0][7].set_piece(None)
                rook.set_initial_position((0,5))
        temp_piece.set_hasMoved_flag(True)
        temp_piece.set_initial_position((move[0], move[1])) #set the piece's position to the new one move 
        #if(piece.get_color() == "W" and piece.get_name() == "Queen" and move == (4,6)):
        #    print("HI 2", temp_board.get_board(), len(temp_board.get_black_pieces()))
        return temp_board

    def max_white_move(self, board, dragger_temp, arbitter): #will find best move of current position for white. 
        #print(board.get_board())
        possible_pieces = []
        #comparison variable
        best_move = (None,None,None) #format : (piece, move, eval of board after move) #None means no move was analyzed 
        all_equal = True
        #fetch all possible black moves...
        for piece in board.get_white_pieces(): # make sure to only look at pieces with available moves...
            #print(f'{piece.get_name()} on {piece.get_initial_pos()} can move to {piece.get_valid_moves()}')
            if(piece.get_valid_moves() != []): 
                possible_pieces.append(piece)
                #loop through possible piece moves.
                piece_temp = copy.deepcopy(piece)
                for move in piece_temp.get_valid_moves():
                    #perform the move on a fake board in memory and evaluate board.
                    col, row = piece_temp.get_initial_pos()[0], piece_temp.get_initial_pos()[1]  #col, row
                    #make the move on fake board. 
                    board_copy = self.make_fake_move(board, move, piece_temp) #fetch the board with move on it
                    board_copy.create_pieces_list()
                    #self.update_all_valid_moves(board_copy, dragger_temp, arbitter)
                    #if(move == (4,6) and piece_temp.get_name() == "Queen"):
                    #    print("HIT", board_copy.get_board(), len(board.get_white_pieces()), len(board.get_black_pieces()))
                    #get eval of board after fake move...
                    #if(move == (1,5) and piece_temp.get_name() == "Queen"):
                    #    print()
                    curr_eval = self.eval_board(board_copy)
                    #if(move == (4,6) and piece_temp.get_name() == "Queen"):
                    #    print("HIT", board_copy.get_board(), len(board.get_white_pieces()), len(board.get_black_pieces()), curr_eval)
                    #print(board_copy.get_board(), piece, (piece.get_initial_pos()[1], piece.get_initial_pos()[0]), move, curr_eval)
                    if(best_move[2] == None): #means this is the first analysis. Just take the value found as the best one. 
                        best_move = (piece, move, curr_eval)
                    elif(curr_eval > best_move[2]): #check if the new eval is better for black (more negative) #for now skip moves that are equal will look into them later. 
                        best_move = (piece, move, curr_eval) #replace with the new found best for black..
                        all_equal = False
                    elif(curr_eval == best_move[2]):
                        num = random.randint(0,1)
                        if(num == 1):
                           best_move = (piece, move, curr_eval) 
                        else:
                            pass
        
        best_move_result = (best_move[0], best_move[1])
        #print("White best move ", best_move)
        return best_move
    
    def no_moves(self, board, color):
        if(color == "B"): #check if B has no moves. 
            flag = True
            for piece in board.get_black_pieces():
                if(piece.get_valid_moves() != []):
                    flag = False
                    break
        elif(color == "W"): #check if W has no moves. 
            flag = True
            for piece in board.get_white_pieces():
                if(piece.get_valid_moves() != []):
                    flag = False
                    break
        return flag
    
    def nonrec_move_search(self, board, arbitter_instance, dragger):
        #print(depth)
        no_moves = True
        self.best_move = [] 
        arbitter = copy.deepcopy(arbitter_instance)
        dragger_temp = copy.deepcopy(dragger)
        #zer_board = copy.deepcopy(board)
        #loop through all black moves possible. 
        if(self.no_moves(board, "B")):
            self.best_move = [None, None, None]
        #while(depth != 0):
        for piece in board.get_black_pieces():
            #print(piece_B, piece_B.get_valid_moves())
            #loop through the pieces moves. 
            piece_B = copy.deepcopy(piece)
            for move_B in piece_B.get_valid_moves():
                no_moves = False
                dragger_temp.set_piece(piece_B)
                arbitter.set_piece(piece_B)
                #piece_B = copy.deepcopy(piece) ???????????????????????????????????????????????????????????
                board_after_black_move = self.make_fake_move(board, move_B, piece_B)
                board_after_black_move.create_pieces_list()
               # print("BLACK", piece_B, (piece.get_initial_pos()[1], piece.get_initial_pos()[0]), move_B)
                #board_after_black_move.get_board()
                #print("HI 0")
                self.update_all_valid_moves(board_after_black_move, dragger_temp, arbitter)
                #print("HI 1")
                #check all the white moves possible from this position. 
                current_eval = self.max_white_move(board_after_black_move, dragger_temp, arbitter)
                #print("B move: ",piece, (piece.get_initial_pos()[1], piece.get_initial_pos()[0]), move_B )
                if(current_eval != (None, None, None)):
                    pass
                    #print("W move: ", current_eval[0], (current_eval[0].get_initial_pos()[1], current_eval[0].get_initial_pos()[0]), current_eval[1], current_eval[2])
                #print("HI 2")
                #print("WHITE", current_eval[0], (current_eval[0].get_initial_pos()[1], current_eval[0].get_initial_pos()[0]), current_eval[2], board_after_black_move.get_board())
                if(current_eval == (None, None, None)): #white has no moves. 
                    if(self.am_I_in_check(board_after_black_move, "W")): #the black move is checkmate for white. 
                        self.best_move = [piece, move_B, -1000069]
                        res = (self.best_move[0], self.best_move[1])
                        return res
                #elif(current_eval != (None, None, None)): 
                #board_after_white_move = self.make_fake_move(board_after_black_move, current_eval[1], current_eval[0])
                #print("HI 3")
                if(self.best_move == []): #if first iteration...
                    self.best_move = [piece, move_B, current_eval[2]]
                else:
                    #compare with the pevious biggest val. 
                    if(current_eval != (None, None, None) and self.best_move[2] != None):
                        #print('HERE', current_eval, self.best_move[2])
                        if(current_eval[2] < self.best_move[2]):
                            #print(current_eval[2], self.best_move[2], piece, (piece.get_initial_pos()[1], piece.get_initial_pos()[0]), move_B)
                            equal = False
                            #better move is found for black...
                            self.best_move = [piece, move_B, current_eval[2]] #update new best. 
        #self.recursive_move_search(board_after_white_move, arbitter_instance, dragger, depth-1) #rec call to method. 
        #if(equal): #no better move is found. play a random move. 

        #if(depth == 0):
        if(no_moves != True):
            self.checking = self.can_take_enemy_king(board_after_black_move, dragger, arbitter_instance)
        res = (self.best_move[0], self.best_move[1])
        return res
                
    def recursive_move_search(self, board, arbitter_instance, dragger, depth):
        #print(depth)
        #arbitter = copy.deepcopy(arbitter_instance)
        #dragger_temp = copy.deepcopy(dragger)
        #zer_board = copy.deepcopy(board)
        #loop through all black moves possible. 
        if(self.no_moves(board, "B")):
            self.best_move = [None, None, None]

        while(depth != 0):
            for piece_B in board.get_black_pieces():
                print(piece_B, piece_B.get_valid_moves())
                #loop through the pieces moves. 
                for move_B in piece_B.get_valid_moves():
                    dragger.set_piece(piece_B)
                    arbitter_instance.set_piece(piece_B)
                    board_after_black_move = self.make_fake_move(board, move_B, piece_B)
                    #print("HI 0")
                    self.update_all_valid_moves(board_after_black_move, dragger, arbitter_instance)
                    #print("HI 1")
                    #check all the white moves possible from this position. 
                    current_eval = self.max_white_move(board_after_black_move)
                    #print("HI 2")
                    if(current_eval == (None, None, None)): #white has no moves. 
                        if(self.am_I_in_check(board_after_black_move, "W")): #the black move is checkmate for white. 
                            self.best_move = [piece_B, move_B, -1000069]
                            res = (self.best_move[0], self.best_move[1])
                            return res
                    #elif(current_eval != (None, None, None)): 
                    board_after_white_move = self.make_fake_move(board_after_black_move, current_eval[1], current_eval[0])
                    #print("HI 3")
                    if(self.best_move == []): #if first iteration...
                        self.best_move = [piece_B, move_B, current_eval[2]]
                    else:
                        #compare with the pevious biggest val. 
                        if(current_eval[2] < self.best_move[2]):
                            #better move is found for black...
                            self.best_move = [piece_B, move_B, current_eval[2]] #update new best. 
            self.recursive_move_search(board_after_white_move, arbitter_instance, dragger, depth-1) #rec call to method. 

        if(depth == 0):
            res = (self.best_move[0], self.best_move[1])
            return res
       
    def smart_move_search(self, board):  #improved move finder #will do a depth of 1 to begin with [no thinking ahead]
        possible_pieces = []
        #comparison variable
        best_move = (None,None,None) #format : (piece, move, eval of board after move) #None means no move was analyzed 
        all_equal = True
        #fetch all possible black moves...
        for piece in board.get_black_pieces(): # make sure to only look at pieces with available moves...
            #print(f'{piece.get_name()} on {piece.get_initial_pos()} can move to {piece.get_valid_moves()}')
            if(piece.get_valid_moves() != []): 
                possible_pieces.append(piece)
                #loop through possible piece moves.
                piece_temp = copy.deepcopy(piece)
                for move in piece.get_valid_moves():
                    #perform the move on a fake board in memory and evaluate board.
                    col, row = piece_temp.get_initial_pos()[0], piece_temp.get_initial_pos()[1]  #col, row
                    #make the move on fake board. 
                    board_copy = self.make_fake_move(board, move, piece_temp) #fetch the board with move on it
                    #get eval of board after fake move...
                    curr_eval = self.eval_board(board_copy)
                    if(best_move[2] == None): #means this is the first analysis. Just take the value found as the best one. 
                        best_move = (piece, move, curr_eval)
                    elif(curr_eval < best_move[2]): #check if the new eval is better for black (more negative) #for now skip moves that are equal will look into them later. 
                        best_move = (piece, move, curr_eval) #replace with the new found best for black..
                        all_equal = False
                    elif(curr_eval == best_move[2]):
                        num = random.randint(0,1)
                        if(num == 1):
                           best_move = (piece, move, curr_eval) 
                        else:
                            pass
        
        best_move_result = (best_move[0], best_move[1])
        #print(best_move_result)
        return best_move_result
    



    def testing(self, board):
        board.get_board()
        for piece in board.get_white_pieces(): # make sure to only look at pieces with available moves...
            print(f'{piece.get_name()} on {piece.get_initial_pos()} can move to {piece.get_valid_moves()}')





