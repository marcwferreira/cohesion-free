## Constants
#   This file aggregates constants needed for the game into one document for 
#   easier and faster modifiction.
#
#   made by:
#   - Catarina Barbosa
#   - Francisca Andrade
#   - Marcos Ferreira​
#
#   03/16/2023

import pygame

pygame.font.init()

WIDTH, HEIGHT = 600, 800
MENUS_HEIGHT = 100

#colors for the blocks
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

COLORS_LIST = [RED,GREEN,BLUE,YELLOW]

#colors for the board and UI
GREY = (128, 128, 128)
DARK_GREY = (50, 50, 50)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#game font 
title_font=pygame.font.SysFont("monospace", 30)

#pieces shapes
S_SHAPE = [[0,1],[0,2],[1,1],[2,0],[2,1]]

#    **
#    *
#   **

I_SHAPE_1 = [[0,0],[0,1]]

#    *
#    *

I_SHAPE_2 = [[0,0],[1,0],[2,0]]

#    *
#    *
#    *

O_SHAPE = [[0,0],[1,0],[0,1],[1,1]]

#    **
#    **

J_SHAPE = [[0,1],[1,0],[1,1]]

#    *
#   **

L_SHAPE = [[0,0],[1,0],[2,0],[2,1]]

#    *
#    *
#    **

T_SHAPE = [[0,0],[1,0],[2,0],[1,1],[2,1]]

#   ***
#    *
#    *

UNIT_SHAPE = [[0,0]]

#    *

C_SHAPE = [[0,0],[1,0],[0,1],[0,2],[2,1]]

#  **
#  *
#  **

SHAPE_LIST = [S_SHAPE, I_SHAPE_1, I_SHAPE_2, O_SHAPE, J_SHAPE, L_SHAPE, T_SHAPE, UNIT_SHAPE, C_SHAPE]

#buttons color
BUTTON_BACKGROUND = (128, 128, 128)
BUTTON_TEXT = (255, 255, 255)
BUTTON_BACKGROUND_PRESSSED = (50, 50, 50)
BUTTON_DISABLED = (20, 20, 20)