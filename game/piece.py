import pygame
from .constants import RED, GREEN, BLUE, YELLOW, SQUARE_SIZE, MENUS_HEIGHT

class Piece:
    def __init__(self, row, col, color, shape):
        self.row = row
        self.col = col
        self.color = color
        self. shape = shape
        self.selected = False
        self.coords = []

        self.x = self.y = 0

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col
        self.y = SQUARE_SIZE * self.row

    def change_shape(self): #idk if this the best way of doing this
        return None
    
    def move(self):
        return None
        #check if it can move (from every single coordinate)

        #move every single coordinate
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x*SQUARE_SIZE, MENUS_HEIGHT+ self.y*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))

    #debug purposes
    def __repr__(self):
        return str(self.color)+" "+str(self.shape)

