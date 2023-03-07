import pygame

WIDTH, HEIGHT = 600, 800
MENUS_HEIGHT = 100
ROWS, COLS = 4,4 #this is a test -> it will be not fixed
SQUARE_SIZE = WIDTH//ROWS #this is also not used for tests

#colors for the blocks
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (0, 255, 255)

#colors for the board
GREY = (128, 128, 128)
DARK_GREY = (50, 50, 50)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#pieces shapes
S_SHAPE = []
Z_SHAPE = []
I_SHAPE = []
O_SHAPE = []
J_SHAPE = []
L_SHAPE = []
T_SHAPE = []

SHAPE_LIST = [S_SHAPE, Z_SHAPE, I_SHAPE, O_SHAPE, J_SHAPE, L_SHAPE, T_SHAPE]

#buttons color
BUTTON_BACKGROUND = (128, 128, 128)
BUTTON_TEXT = (255, 255, 255)
BUTTON_BACKGROUND_PRESSSED = (50, 50, 50)
BUTTON_DISABLED = (20, 20, 20)