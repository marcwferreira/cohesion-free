import pygame
import random
from .constants import GREY, DARK_GREY, ROWS, SQUARE_SIZE, MENUS_HEIGHT
from .constants import WIDTH, HEIGHT

class Board:
    def __init__(self, rows, cols):
        self.board = []
        self.rows = rows
        self.cols = cols
        self.selected_piece = None
        
    def draw_squares(self,win):

        square_size = WIDTH/self.rows

        pygame.draw.rect(win, DARK_GREY, (0, MENUS_HEIGHT, WIDTH, HEIGHT-2*MENUS_HEIGHT))
        for row in range(self.rows):
            for col in range(row % 2, self.rows, 2):
                pygame.draw.rect(win, GREY, (row*square_size, MENUS_HEIGHT+ col*square_size,square_size,square_size))


    def create_board(self, level):
        if level == 1:
            return None
        elif level == 1:
            return None
        elif level == 1:
            return None
        elif level == 1:
            return None
        else:
            for row in range(self.rows):
                self.board.append([])
                for col in range(self.cols):
                    #find way to appd pieces, since they are different sizes
                    pass
            return None