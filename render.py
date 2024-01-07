from statics import *
import pygame as pg
from board import Board
from drag import Drag
from arbiter import arbiter
import time as t 
import os

class Render:

    def __init__(self):
        self.board = Board()
        self.dragger = Drag()
        self.dragger_AI = Drag()
        #colours of squares
        self.light_color = (234, 235, 200)
        self.dark_color = (119, 154, 88)

    def col_to_alpha(self, col):
        col_to_alpha_dict = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        return col_to_alpha_dict[col]
    def draw_captured_pieces(self, s, captured_pieces, evaluation):
        white_captured_pieces = [] 
        black_captured_pieces = []
        for piece in captured_pieces:
            #draw white pieces:
            if(piece.get_color() == "W"):
                white_captured_pieces.append(piece)
            elif(piece.get_color() == "B"):
                black_captured_pieces.append(piece)
        for i in range(len(white_captured_pieces)):
            piece_W = white_captured_pieces[i]
            img = pg.transform.scale(pg.image.load(piece_W.image), (30,30)) #shrink image
            img_center =  (522, 15 + 30 * i)
            piece_W.image_rect = img.get_rect(center = img_center)
            s.blit(img, piece_W.image_rect)
        for j in range(len(black_captured_pieces)):
             #draw black pieces:
            piece_B = black_captured_pieces[j]
            img = pg.transform.scale(pg.image.load(piece_B.image), (30,30))
            img_center =  (570, 15 + 30 * j)
            piece_B.image_rect = img.get_rect(center = img_center)
            s.blit(img, piece_B.image_rect)
        eval = pg.font.SysFont('monospace', 15, bold=True).render(str(evaluation), 1, 'BLACK')
        #eval_pos = (546, 480)
        button_pos = (515, 400)
        reset_button_image = pg.transform.scale(pg.image.load(os.path.join('Assets/button/reset_button.png')), (65,65))
        s.blit(reset_button_image, button_pos)
        #s.blit(eval, eval_pos)

    def draw_background(self, s):
        pg.draw.rect(s, self.light_color, (0, 0 ,WIDTH, HEIGHT))
        pg.draw.line(s, 'BLACK', (496, 0), (496, 496), width = 10)
        for row in range(RWS):
            for column in range(CLS):
                if(row+column)%2 == 0:
                    selected_color = self.light_color
                else:
                    selected_color = self.dark_color
                rect = (column*SQSIZE, row*SQSIZE, SQSIZE, SQSIZE)
                pg.draw.rect(s, selected_color, rect)
                #row coordinates
                if column == 0: #fix col to 0 -> access rows only 
                    color = self.dark_color if row % 2 == 0 else self.light_color
                    label = pg.font.SysFont('monospace', 12, bold=True).render(str(RWS-row), 1, color)
                    label_pos = (1, 5 + row * SQSIZE)
                    s.blit(label, label_pos)
                # col coordinates
                if row == 7: #fix row to 0 -> access cols only
                    color = self.dark_color if (row + column) % 2 == 0 else self.light_color
                    # label
                    lbl = pg.font.SysFont('monospace', 12, bold=True).render(self.col_to_alpha(column), 1, color)
                    lbl_pos = (column * SQSIZE + SQSIZE - 10, HEIGHT - 20)
                    # blit
                    s.blit(lbl, lbl_pos)

    def draw_pieces(self, s, spec):
        #if spec == None:
            for row in range(RWS):
                for col in range(CLS):
                    if(row == self.dragger.get_initial_pos()[1] and col == self.dragger.get_initial_pos()[0] and self.dragger.get_drag_flag()):
                        pass
                    else:
                        if(self.board.squares[row][col].has_piece() and (row, col)!=spec):
                            piece = self.board.squares[row][col].piece
                            img = pg.image.load(piece.image)
                            img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                            piece.image_rect = img.get_rect(center = img_center)
                            s.blit(img, piece.image_rect)
        #else:
        #    piece = self.board.squares[spec[0]][spec[1]].piece
        #    img = pg.image.load(piece.image)
        #    img_center = spec[1] * SQSIZE + SQSIZE // 2, spec[0] * SQSIZE + SQSIZE // 2
        #    piece.image_rect = img.get_rect(center = img_center)
        #    s.blit(img, piece.image_rect)
    
    def show_moves(self, s):
        if(self.dragger.get_drag_flag()):
            #print(self.dragger.get_piece().get_valid_moves())
            for move in self.dragger.get_piece().get_valid_moves():
                rect = (move[1] *SQSIZE, move[0] *SQSIZE, SQSIZE, SQSIZE)
                pg.draw.rect(s, '#FFBF4D', rect, width=3)
            #print(self.dragger.get_piece().get_valid_moves(), self.dragger.get_check_flag())
            if self.dragger.get_check_flag()[0] == True:
                pieces_causing_checks = self.dragger.get_check_flag()[2]
                king_pos = self.dragger.get_check_flag()[1]
                rect_warning = (king_pos[1] *SQSIZE, king_pos[0] *SQSIZE, SQSIZE, SQSIZE) 
                pg.draw.rect(s, '#DC143C', rect_warning, width=0)
                for coords in pieces_causing_checks:
                    rect_warning = (coords[0] *SQSIZE, coords[1] *SQSIZE, SQSIZE, SQSIZE)
                    pg.draw.rect(s, '#DC143C', rect_warning, width=3)

    def restart(self):
        self.__init__()