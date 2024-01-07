import pygame as pg
from statics import *


class Drag():

    def __init__(self):
        self.drag_Flag = False
        self.click_X = 0
        self.click_Y = 0
        self.initial_col = 0 
        self.initial_row = 0
        self.selected_piece = None
        self.in_check = (False, None, []) #True // king coords that is in check // coords of piece(s) that is/are checking the king
    #getters
    def get_piece(self):
        return self.selected_piece
    def get_drag_flag(self) -> bool:
        return self.drag_Flag
    def get_initial_pos(self):
        return (self.initial_col, self.initial_row)
    def get_position(self):
        return (self.click_X, self.click_Y)
    def get_check_flag(self):
        return self.in_check
    #setters
    def set_in_check(self, value):
        self.in_check = value

    def update_coordinates(self, position):
        self.click_X = position[0]
        self.click_Y = position[1]
    def set_drag_flag(self, new_flag):
        self.drag_Flag = new_flag

    def set_piece(self, piece):
        self.selected_piece = piece
        self.set_drag_flag(True)
        #print(piece)
    #MISC
    def save_initial_direct(self, position):
        self.initial_row = position[1]
        self.initial_col = position[0]
    def save_initial(self, position):
        self.initial_col = position[0] // SQSIZE
        self.initial_row = position[1] // SQSIZE
    
    def undo_drag(self):
        self.selected_piece = None
        self.set_drag_flag(False)
    
    def update_image(self, s):
        #center_temp = [None, None]
        #check if dragging image in boundaries.. >= .
        if(self.click_X > 471):
           self.click_X = 471
        elif(self.click_X < 25):
            self.click_X = 25 
        if(self.click_Y > 471):
            self.click_Y = 471
        elif(self.click_Y < 25):
            self.click_Y = 25
        #self.click_X, self.click_Y = center_temp[0], center_temp[1]
        image_center = (self.click_X, self.click_Y)
        image = pg.image.load(self.selected_piece.image)
        self.selected_piece.textureRect = image.get_rect(center = image_center)
        s.blit(image, self.selected_piece.textureRect)
        #pg.display.update()
        #self.piece.image_
    
    

