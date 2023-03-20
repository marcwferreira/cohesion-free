import pygame
from random import random, randint
from .constants import GREY, DARK_GREY, ROWS, SQUARE_SIZE, MENUS_HEIGHT, title_font
from .constants import BLUE, RED, GREEN, YELLOW, BLACK, COLORS_LIST, ROTATION_LIST
from .constants import WIDTH, HEIGHT
from .constants import SHAPE_LIST
from .piece import Piece
from .button import Button
from .board import Board
from .utils import addEles, generateWhiteNoise

def computer_move_cal(board):
    #it has to choose a piece and a movement to make -> returns a list
    # for now it is hardcoded, just to config it
    return [[0,'down'],[1,'left']] # we'll need to do functions to see if a movement is possible