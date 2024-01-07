import pygame as pg
import sys
import copy
from statics import *
from render import Render
from drag import Drag
from arbiter import arbiter
from piece import *
from engine import *
import os, psutil
import gc
import asyncio
import time

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        #Set caption of window
        pg.display.set_caption("Tony's Chess")
        #create instance of render class:
        self.entity = Render()
        self.to_move = "W"
        self.human_turn = True
        self.pieces_captured = []
        self.state = "Play" # can be finished. press R to go back to play. 
        self.first_move = True
        self.eval = 0 #even at the begining of the game
        self.holding = False


    def main(self):
        human_plays_w = True
        engine_plays_b = True 
        AI = engine()
        #process = psutil.Process()
        #self.entity.draw_pieces(self.screen, None)
        while True:
            #print(self.holding)
            #human_turn = (human_plays_w and self.to_move == "W") or (not human_plays_w and self.to_move == "B")
            self.entity.draw_background(self.screen)
            self.entity.show_moves(self.screen)
            self.entity.draw_pieces(self.screen, None)
            board = self.entity.board
            board_AI = copy.deepcopy(board)
            dragger = self.entity.dragger
            dragger_AI = copy.deepcopy(dragger)
            if(self.state == "Play"):
                self.eval = 0
            self.entity.draw_captured_pieces(self.screen, self.pieces_captured, self.eval)
            if dragger.get_drag_flag():
                dragger.update_image(self.screen)
            pg.display.update()
            stall = False
            fin = None
            #pg.display.update()
            #dragger_AI = self.entity.dragger_AI
            #board = self.entity.board 
            Arbiter_instance = arbiter()
            Arbiter_instance_AI = copy.deepcopy(Arbiter_instance)
            #if(self.state == "Play"):
            #    self.eval = AI.eval_board(board)
            #self.entity.draw_captured_pieces(self.screen, self.pieces_captured, self.eval)
           # if(AI.white_lose(board) and self.first_move != True and self.state == "Play"):
           #     if(AI.am_I_in_check(board, "W")):
           #       print("Black wins by checkmate!")
           #       self.to_move = "W"
           #       self.state = "finished" 
           #       self.eval = '#'
           #     else:
           #         board.get_board()
           #         print("Draw via stalemate!")
           #         self.to_move = "W"
           #         self.state = "finished"
            #if(dragger.get_piece() != None and dragger.get_piece().get_name() != "King"):
            #    Arbiter_instance.can_castle(board, dragger)
            #    print("YO CHILL", piece, piece.get_color(), piece.get_castle_long(), piece.get_castle_short())
            #print(AI.eval_board(board))
            #print(self.eval)
            if self.human_turn == False and self.state == "Play" and stall  == False : #AI turn to play.
                #print(dragger.get_drag_flag()) 
                #ai_choice =  AI.recursive_move_search(board, Arbiter_instance_AI, dragger_AI, 1)
                #AI.am_I_in_check(board, "W")
                ai_choice =  AI.nonrec_move_search(board, Arbiter_instance_AI, dragger_AI)
                #AI.best_move = [] 
                #ai_choice = AI.smart_move_search(board)
                #print(ai_choice)
                if(ai_choice == (None, None)):
                    #if we are in check... Then white checkmated black.
                    if(AI.am_I_in_check(board, "B")):
                        print("White wins by checkmate!")
                        self.to_move = "W"
                        self.state = "finished"
                        self.eval = '#'
                    else:  #if not... then its a stalemate.
                        #print("HERE")
                        print("Draw via stalemate!")
                        self.to_move = "W"
                        self.state = "finished"
                        
                        
                elif(ai_choice != (None, None)):
                    #print(ai_choice)
                    move = ai_choice[1]
                    move_piece = ai_choice[0]
                    initial_pos_piece = move_piece.get_initial_pos()
                    piece = board.squares[initial_pos_piece[1]][initial_pos_piece[0]].get_piece()
                    #print(initial_pos_piece)
                    final_pos = move
                    if(piece.get_name() == "Pawn" and piece.get_color() == "B" and move[0] == 7):
                        queen_Piece_B = Queen(final_pos, "B")
                        piece = queen_Piece_B
                        board.get_black_pieces().remove(ai_choice[0])
                        board.get_pieces().remove(ai_choice[0])
                        board.get_black_pieces().append(piece)
                        board.get_pieces().append(piece)
                        #print(len( board.get_black_pieces()))
                        piece.set_initial_position((move[0], move[1]))
                    if(board.squares[final_pos[0]][final_pos[1]].get_piece() != None):
                        temp_piece = board.squares[final_pos[0]][final_pos[1]].get_piece()
                        #remove from board.black_piece list and piece list. 
                        if(temp_piece.get_color() == "B"):
                            board.get_black_pieces().remove(temp_piece)
                            board.get_pieces().remove(temp_piece)
                        elif(temp_piece.get_color() == "W"):
                            board.get_white_pieces().remove(temp_piece)
                            board.get_pieces().remove(temp_piece)
                            #print(len(board.get_pieces()),len(board.get_white_pieces()), len(board.get_black_pieces()))
                        self.pieces_captured.append(temp_piece)
                    board.squares[move[0]][move[1]].set_piece(piece) #make the move
                    board.squares[initial_pos_piece[1]][initial_pos_piece[0]].set_piece(None) #clear original square
                    if(piece.get_name() == "King"):
                        #check long side white piece... 
                        if(piece.get_castle_long() and move == (0,2)):#castle long side selected by white
                            rook = board.squares[0][0].get_piece()
                            board.squares[0][3].set_piece(rook)
                            board.squares[0][0].set_piece(None)
                            rook.set_initial_position((0,3))
                        if(piece.get_castle_short() and move == (0,6)):#castle short side selected by white
                            rook = board.squares[0][7].get_piece()
                            board.squares[0][5].set_piece(rook)
                            board.squares[0][7].set_piece(None)
                            rook.set_initial_position((0,5))
                    piece.set_hasMoved_flag(True)
                    piece.set_initial_position((move[0], move[1]))
                    #print(piece.get_initial_pos(), move)
                    dragger_AI.save_initial_direct(piece.get_initial_pos())
                    dragger_AI.set_piece(piece)
                    #print(dragger_AI.get_piece(), dragger_AI.get_piece().get_color())
                    Arbiter_instance_AI.set_piece(piece)
                    Arbiter_instance_AI.check_valid_moves(board, dragger_AI, True, False, None)
                    #board.get_board()

                self.to_move = "W"
                self.human_turn = True

            if(AI.white_lose(board) and self.first_move != True and self.state == "Play"):
                #if(AI.can_take_enemy_king(board, dragger_AI, Arbiter_instance_AI)):
                #if(AI.checking):
                if(AI.am_I_in_check(board, "W")):
                    print("Black wins by checkmate!")
                    self.to_move = "W"
                    self.state = "finished" 
                    self.eval = '#'
                else:
                    #board.get_board()
                    #for piece in board.get_black_pieces():
                    #    print(piece, (piece.get_initial_pos()[1], piece.get_initial_pos()[0]), piece.get_valid_moves())
                    print("Draw via stalemate!")
                    self.to_move = "W"
                    self.state = "finished"
        
            for event in pg.event.get():
                if(self.human_turn):
                    #print(len(board.get_pieces()), len(board.get_white_pieces()), len(board.get_black_pieces()))
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.state == "Play": #and pg.MOUSEBUTTONDOWN == 1: #click
                        dragger.update_coordinates(event.pos)
                        clicked_row = dragger.get_position()[1] // SQSIZE
                        clicked_col = dragger.get_position()[0] // SQSIZE 
                        if(clicked_row <= 7 and clicked_col <= 7 and clicked_row >= 0 and clicked_col >= 0):
                            self.holding = True
                            #dragger.update_coordinates(event.pos)
                            #clicked_row = dragger.get_position()[1] // SQSIZE
                            #clicked_col = dragger.get_position()[0] // SQSIZE 
                            #print("clicked on ", (clicked_row, clicked_col))
                            #if(clicked_row <= 7 and clicked_col <= 7 and clicked_row >= 0 and clicked_col >= 0):
                            if(board.squares[clicked_row][clicked_col].has_piece()): #check if selected square contains a piece.
                                if(self.to_move == board.squares[clicked_row][clicked_col].get_piece().get_color()):
                                        piece = board.squares[clicked_row][clicked_col].get_piece()
                                        #print(piece)
                                        dragger.save_initial(event.pos)
                                        dragger.set_piece(piece)
                                        #self.entity.show_moves(self.screen)
                                        Arbiter_instance.set_piece(piece)
                                        Arbiter_instance.check_valid_moves(board, dragger, True, False, None)
                                        if(dragger.get_piece().get_name() == "King"):
                                            Arbiter_instance.can_castle(board, dragger)
                                            if(dragger.get_piece().get_castle_long()):
                                                dragger.get_piece().get_valid_moves().append((clicked_row, clicked_col - 2))
                                            else:
                                                if((clicked_row, clicked_col - 2) in dragger.get_piece().get_valid_moves()):
                                                    dragger.get_piece().get_valid_moves().remove((clicked_row, clicked_col - 2))

                                            if(dragger.get_piece().get_castle_short()):
                                                dragger.get_piece().get_valid_moves().append((clicked_row, clicked_col + 2))
                                            else:
                                                if((clicked_row, clicked_col + 2) in dragger.get_piece().get_valid_moves()):
                                                    dragger.get_piece().get_valid_moves().remove((clicked_row, clicked_col + 2))

                                            #print(dragger.get_piece().get_valid_moves())
                                        #self.entity.show_moves(self.screen)
                                        #if(piece.get_name() == 'King'):
                                        #    #check if can castle. 
                                        #    Arbiter_instance.can_castle(board, dragger)
                                        #    print("YO CHILL", piece, piece.get_color(), piece.get_castle_long(), piece.get_castle_short())
                                else:
                                    if(self.to_move == "W"):
                                        print("Sorry, white to move!")
                                    elif(self.to_move == "B"):
                                        print("Sorry, black to move!")

                    elif event.type == pg.MOUSEMOTION and self.state == "Play": #drag
                        if(dragger.get_drag_flag() == True):
                            dragger.update_coordinates(event.pos)
                            #dragger.update_image(self.screen)
                        #self.entity.show_moves(self.screen)

                    elif event.type == pg.MOUSEBUTTONUP and self.state == "Play": #let go
                        self.holding = False
                        if(dragger.get_piece() != None):
                            piece = dragger.get_piece()
                            initial_pos  = (dragger.get_initial_pos()[1], dragger.get_initial_pos()[0])
                            dragger.undo_drag()
                            final_pos = (event.pos[1] // SQSIZE, event.pos[0] // SQSIZE)
                            if(final_pos in piece.get_valid_moves()):
                                if(piece.get_name() == "Pawn"):
                                    if(piece.get_color() == "W" and final_pos[0] == 0):
                                        queen_Piece_W = Queen(final_pos, "W")
                                        piece = queen_Piece_W
                                        board.get_white_pieces().remove(board.squares[initial_pos[0]][initial_pos[1]].get_piece())
                                        board.get_pieces().remove(board.squares[initial_pos[0]][initial_pos[1]].get_piece())
                                        board.get_white_pieces().append(piece)
                                        board.get_pieces().append(piece)
                                    elif(piece.get_color() == "B" and final_pos[0] == 7):
                                        queen_Piece_B = Queen(final_pos, "B")
                                        piece = queen_Piece_B
                                        board.get_black_pieces().remove(board.squares[initial_pos[0]][initial_pos[1]].get_piece())
                                        board.get_pieces().remove(board.squares[initial_pos[0]][initial_pos[1]].get_piece())
                                        board.get_black_pieces().append(piece)
                                        board.get_pieces().append(piece)
                                if(final_pos != initial_pos): # wont empty a square if no movement takes place. 
                                    if(board.squares[final_pos[0]][final_pos[1]].get_piece() != None):
                                        temp_piece = board.squares[final_pos[0]][final_pos[1]].get_piece()
                                        if(temp_piece.get_color() == "B"):
                                            board.get_black_pieces().remove(temp_piece)
                                            board.get_pieces().remove(temp_piece)
                                        elif(temp_piece.get_color() == "W"):
                                            board.get_white_pieces().remove(temp_piece)
                                            board.get_pieces().remove(temp_piece)
                                        self.pieces_captured.append(temp_piece)
                                    board.squares[final_pos[0]][final_pos[1]].set_piece(piece)
                                    board.squares[initial_pos[0]][initial_pos[1]].set_piece(None)
                                    #self.entity.draw_pieces(self.screen, (final_pos))
                                    #print(final_pos)
                                    if(piece.get_name() == "King" and piece.get_color() == "W"):
                                        #check long side white piece... 
                                        if(piece.get_castle_long() and final_pos == (7,2)):#castle long side selected by white
                                            rook = board.squares[7][0].get_piece()
                                            board.squares[7][3].set_piece(rook)
                                            board.squares[7][0].set_piece(None)
                                            rook.set_initial_position((7,3))
                                        if(piece.get_castle_short() and final_pos == (7,6)):#castle short side selected by white
                                            rook = board.squares[7][7].get_piece()
                                            board.squares[7][5].set_piece(rook)
                                            board.squares[7][7].set_piece(None)
                                            rook.set_initial_position((7,5))
                                    #self.entity.draw_pieces(self.screen)
                                    #elif(piece.get_name() == "King" and piece.get_color() == "B"):
                                    #    #check long side white piece... 
                                    #    if(piece.get_castle_long() and final_pos == (0,2)):#castle long side selected by white
                                    #        rook = board.squares[0][0].get_piece()
                                    #        board.squares[0][3].set_piece(rook)
                                    #        board.squares[0][0].set_piece(None)
                                    #        rook.set_initial_position((0,3))
                                    #    if(piece.get_castle_short() and final_pos == (0,6)):#castle short side selected by white
                                    #        rook = board.squares[0][7].get_piece()
                                    #        board.squares[0][5].set_piece(rook)
                                    #        board.squares[0][7].set_piece(None)
                                    #        rook.set_initial_position((0,5))

                                    piece.set_hasMoved_flag(True)
                                    piece.set_initial_position((final_pos[0], final_pos[1]))
                                    fin = final_pos
                                    dragger.save_initial(event.pos)
                                    dragger.set_piece(piece)
                                    Arbiter_instance.set_piece(piece)
                                    Arbiter_instance.check_valid_moves(board, dragger, True, False, piece)
                                    #AI.am_I_in_check(board, "W")
                                    if(self.first_move):
                                        self.first_move = False
                                    if(self.to_move == "W"): #alternate turn update to_move variable. 
                                        self.to_move = "B"  
                                        self.human_turn = False
                                        stall = True
                                    else:
                                        self.to_move = "W"

                            dragger.undo_drag()
                            #dragger.set_drag_flag(False)

                    elif event.type == pg.MOUSEBUTTONDOWN and event.button == 3 and self.state == "Play": #reset drag if misclick!
                        dragger.undo_drag()

                #if event.type == pg.KEYDOWN:
                ##for reseting the game back..
                #    if event.key == pg.K_r: #press r to restart. 
                #        self.entity.restart()
                #        dragger = self.entity.dragger
                #        board = self.entity.board
                #        self.to_move = "W"
                #        self.state = "Play"
                #        self.first_move = True
                #        self.eval = 0
                #        self.pieces_captured = []
                #        self.holding = False
                if(event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
                    if(event.pos[0] >= 520 and event.pos[0] <= 575 and event.pos[1] >= 400 and event.pos[1] <= 450): #clicking on reset button... 
                        self.entity.restart()
                        dragger = self.entity.dragger
                        board = self.entity.board
                        self.to_move = "W"
                        self.state = "Play"
                        self.first_move = True
                        self.eval = 0
                        self.pieces_captured = []
                        self.holding = False
                if event.type == pg.QUIT: #close app
                    pg.quit()
                    sys.exit()

            #await asyncio.sleep(0)
            
                #pg.display.update()
            #self.entity.draw_pieces(self.screen, None)
            #pg.display.update()
            #print(process.memory_info().rss) #check memory usage


game_instance = Game()
game_instance.main()
