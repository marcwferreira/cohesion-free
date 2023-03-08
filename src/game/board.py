import pygame
import random
from .constants import GREY, DARK_GREY, ROWS, SQUARE_SIZE, MENUS_HEIGHT
from .constants import BLUE, RED, GREEN, YELLOW
from .constants import WIDTH, HEIGHT
from .constants import SHAPE_LIST
from .piece import Piece

class Board:
    def __init__(self, rows, cols):
        self.pieces = [] # this is a list of pieces on the map
        self.rows = rows
        self.cols = cols
        self.selected_piece = None
        self.square_size = WIDTH/self.rows

        self.create_board(0)
        
    def draw_squares(self,win):

        pygame.draw.rect(win, DARK_GREY, (0, MENUS_HEIGHT, WIDTH, HEIGHT-2*MENUS_HEIGHT))
        for row in range(self.rows):
            for col in range(row % 2, self.rows, 2):
                pygame.draw.rect(win, GREY, (row*self.square_size, MENUS_HEIGHT+ col*self.square_size,self.square_size,self.square_size))


    def draw_pieces(self,win):
        for piece in self.pieces:
            piece.draw(win,self.square_size)


    def create_board(self, level):
        if level == 1:
            return None
        elif level == 2:
            return None
        elif level == 3:
            return None
        elif level == 4:
            return None
        else: #this means it is a random game
            test_piece = Piece(0,0, 0, BLUE, SHAPE_LIST[4])
            self.pieces.append(test_piece)
            test_piece2 = Piece(2,0,90, RED, SHAPE_LIST[4])
            self.pieces.append(test_piece2)
            test_piece3 = Piece(0,2,180, GREEN, SHAPE_LIST[4])
            self.pieces.append(test_piece3)
            test_piece4 = Piece(2,2,270, YELLOW, SHAPE_LIST[4])
            self.pieces.append(test_piece4)