import pygame
from random import random, randint
from .constants import GREY, DARK_GREY, ROWS, SQUARE_SIZE, MENUS_HEIGHT, title_font
from .constants import BLUE, RED, GREEN, YELLOW, BLACK, COLORS_LIST, ROTATION_LIST
from .constants import WIDTH, HEIGHT
from .constants import SHAPE_LIST
from .piece import Piece
from .button import Button
from .utils import addEles, generateWhiteNoise

class Board:
    def __init__(self, rows, cols, type):
        self.pieces = [] # this is a list of pieces on the map
        self.rows = rows
        self.cols = cols
        self.selected_piece = None
        self.square_size = WIDTH/self.rows
        self.create_board(type)
        self.num_movements = 0

        # Buttons to move the pieces
        self.move_down = Button("V", WIDTH/5-50/2, HEIGHT-3*MENUS_HEIGHT/4,50,50,False)
        self.move_left = Button("<", 2*WIDTH/5-50/2, HEIGHT-3*MENUS_HEIGHT/4,50,50,False)
        self.move_right = Button(">", 3*WIDTH/5-50/2, HEIGHT-3*MENUS_HEIGHT/4,50,50,False)
        self.move_up = Button("^", 4*WIDTH/5-50/2, HEIGHT-3*MENUS_HEIGHT/4,50,50,False)
        
    def draw_squares(self,win):
        # Draws the checkboard of the board
        pygame.draw.rect(win, DARK_GREY, (0, MENUS_HEIGHT, WIDTH, HEIGHT-2*MENUS_HEIGHT))
        for row in range(self.rows):
            for col in range(row % 2, self.rows, 2):
                pygame.draw.rect(win, GREY, (row*self.square_size, MENUS_HEIGHT+ col*self.square_size,self.square_size,self.square_size))

        #draw buttons for piece movement 
        self.move_down.draw(win)
        self.move_left.draw(win)
        self.move_right.draw(win)
        self.move_up.draw(win)

        #draw number of movements on top
        win.blit(title_font.render("NUMBER OF MOVES:{}".format(self.num_movements), True, BLACK),(4*WIDTH/10,1.5*MENUS_HEIGHT/4))

    def draw_pieces(self,win):
        for piece in self.pieces:
            piece.draw(win,self.square_size)

    def get_pieces(self):
        return self.pieces
    
    def select_piece(self,piece):
        self.selected_piece = piece

    # Function that checks if any of the buttons for selecting pieces were clicked
    def check_pieced_click(self):
        for idx in range(len(self.pieces)):
            if self.pieces[idx].check_click(self.square_size):
                self.selected_piece = idx #remember to change pieces being selected -> this might be for outline
                self.move_down.change_enabled(True)
                self.move_up.change_enabled(True)
                self.move_left.change_enabled(True)
                self.move_right.change_enabled(True)

    def return_if_selected(self):
        return self.selected_piece != None

    def move_piece(self,direction):
        dir_correct = -1 if (direction == 'left' or direction == 'up') else 1 # -1 to move to th or up because of how the coords work
        piece_compare = [self.pieces[self.selected_piece].coords[0]]
        if direction == 'up' or direction == 'down':
            # Get squares to verify if movement is possible
            for coord in self.pieces[self.selected_piece].coords:
                if coord[0] not in [item[0] for item in piece_compare]:
                    piece_compare.append(coord)
                else:
                    for idx in range(len(piece_compare)):
                        if piece_compare[idx][0] == coord[0] and coord[1] > piece_compare[idx][1] and direction == 'down': piece_compare[idx] = coord
                        elif piece_compare[idx][0] == coord[0] and coord[1] < piece_compare[idx][1] and direction == 'up': piece_compare[idx] = coord
            # Add 1 or -1 to every y coord in the comparisson coords to get the matching cells to compare
            piece_compare = list(map(addEles,piece_compare,([[0,dir_correct]]*len(piece_compare))))
            # Verify collision with other pieces
            for idx in range(len(self.pieces)):
                if idx == self.selected_piece: continue
                if len([element for element in piece_compare if element in self.pieces[idx].coords]) != 0: return False
            for square in self.pieces[self.selected_piece].coords: # Verify collision with board walls
                if square[1] >= (self.cols-1) and dir_correct == 1: return False 
                elif square[1] <= 0 and dir_correct == -1: return False
            #move piece
            self.pieces[self.selected_piece].move(direction)
            #increase score
            self.num_movements += 1
        elif direction == 'left' or direction == 'right':
            # Get squares to verify if movement is possible
            for coord in self.pieces[self.selected_piece].coords:
                if coord[1] not in [item[1] for item in piece_compare]:
                    piece_compare.append(coord)
                else:
                    for idx in range(len(piece_compare)):
                        if piece_compare[idx][1] == coord[1] and coord[0] > piece_compare[idx][0] and direction == 'right': piece_compare[idx] = coord
                        elif piece_compare[idx][1] == coord[1] and coord[0] < piece_compare[idx][0] and direction == 'left': piece_compare[idx] = coord
            # Add 1 or -1 to every y coord in the comparisson coords to get the matching cells to compare
            piece_compare = list(map(addEles,piece_compare,([[dir_correct,0]]*len(piece_compare))))
            # Verify collision with other pieces
            for idx in range(len(self.pieces)):
                if idx == self.selected_piece: continue
                if len([element for element in piece_compare if element in self.pieces[idx].coords]) != 0: return False
            for square in self.pieces[self.selected_piece].coords: # Verify collision with board walls
                if square[0] >= (self.rows-1) and dir_correct == 1: return False 
                elif square[0] <= 0 and dir_correct == -1: return False
            #move piece
            self.pieces[self.selected_piece].move(direction)
            #increase score
            self.num_movements += 1
        #check if collisions (for pieces grouping) happendes
        self.check_collisions()

    def check_collisions(self):
        pieces_remove = []
        for idx in range(len(self.pieces)):
            if idx == self.selected_piece: continue
            if self.pieces[self.selected_piece].check_collision(self.pieces[idx]):
                pieces_remove.append(idx)
        if len(pieces_remove) != 0: 
            self.selected_piece = None
            self.move_down.change_enabled(False)
            self.move_up.change_enabled(False)
            self.move_left.change_enabled(False)
            self.move_right.change_enabled(False)
        for i in sorted(pieces_remove, reverse=True):
            del self.pieces[i]

    # Check if buttons to move piece were pressed and starts action
    def check_move_piece(self):
        if self.move_down.check_click():
            self.move_piece('down')
        elif self.move_left.check_click():
            self.move_piece('left')
        elif self.move_right.check_click():
            self.move_piece('right')
        elif self.move_up.check_click():
            self.move_piece('up')

    def check_end(self):
        pieces_color = [piece.color for piece in self.pieces]
        if len(set(pieces_color)) == len(pieces_color): 
            return True
        return False       

    def create_board(self, level):
        if level == 1:
            red_piece1 = Piece(0, 0, 270, RED, SHAPE_LIST[4])
            self.pieces.append(red_piece1)
            green_piece1 = Piece(1, 0, 0, GREEN, SHAPE_LIST[7])
            self.pieces.append(green_piece1)
            blue_piece = Piece(3, 0, 0, BLUE, SHAPE_LIST[7])
            self.pieces.append(blue_piece)
            green_piece2 = Piece(2, 2, 180, GREEN, SHAPE_LIST[4])
            self.pieces.append(green_piece2)
            red_piece2 = Piece(3, 3, 0, RED, SHAPE_LIST[7])
            self.pieces.append(red_piece2)
        elif level == 2:
            red_piece = Piece(1, 0, 0, RED, SHAPE_LIST[3])
            self.pieces.append(red_piece)
            green_piece1 = Piece(0, 0, 0, GREEN, SHAPE_LIST[7])
            self.pieces.append(green_piece1)
            blue_piece1 = Piece(3, 0, 0, BLUE, SHAPE_LIST[7])
            self.pieces.append(blue_piece1)
            green_piece2 = Piece(2, 2, 0, GREEN, SHAPE_LIST[7])
            self.pieces.append(green_piece2)
            blue_piece2 = Piece(0, 3, 0, BLUE, SHAPE_LIST[7])
            self.pieces.append(blue_piece2)
            green_piece3 = Piece(3, 3, 0, GREEN, SHAPE_LIST[7])
            self.pieces.append(green_piece3)
            blue_piece3 = Piece(1, 2, 0, BLUE, SHAPE_LIST[7])
            self.pieces.append(blue_piece3)
        elif level == 3:
            blue_piece = Piece(0, 0, 0, BLUE, SHAPE_LIST[3])
            self.pieces.append(blue_piece)
            green_piece1 = Piece(2, 0, 0, GREEN, SHAPE_LIST[7])
            self.pieces.append(green_piece1)
            green_piece2 = Piece(2, 2, 0, GREEN, SHAPE_LIST[7])
            self.pieces.append(green_piece2)
            red_piece1 = Piece(0, 3, 90, RED, SHAPE_LIST[1])
            self.pieces.append(red_piece1)
            red_piece2 = Piece(3, 0, 0, RED, SHAPE_LIST[1])
            self.pieces.append(red_piece2)
            yellow_piece1 = Piece(0, 2, 0, YELLOW, SHAPE_LIST[7])
            self.pieces.append(yellow_piece1)
            yellow_piece2 = Piece(2, 1, 0, YELLOW, SHAPE_LIST[7])
            self.pieces.append(yellow_piece2)
            yellow_piece3 = Piece(3, 2, 0, YELLOW, SHAPE_LIST[7])
            self.pieces.append(yellow_piece3)
        elif level == 4:
            green_piece1 = Piece(1, 0, 0, GREEN, SHAPE_LIST[7])
            self.pieces.append(green_piece1)
            green_piece2 = Piece(2, 1, 0, GREEN, SHAPE_LIST[7])
            self.pieces.append(green_piece2)
            green_piece3 = Piece(3, 0, 0, GREEN, SHAPE_LIST[7])
            self.pieces.append(green_piece3)
            green_piece4 = Piece(3, 2, 0, GREEN, SHAPE_LIST[7])
            self.pieces.append(green_piece4)
            red_piece1 = Piece(0, 1, 0, RED, SHAPE_LIST[7])
            self.pieces.append(red_piece1)
            red_piece2 = Piece(1, 2, 0, RED, SHAPE_LIST[7])
            self.pieces.append(red_piece2)
            red_piece3 = Piece(2, 0, 0, RED, SHAPE_LIST[7])
            self.pieces.append(red_piece3)
            red_piece4 = Piece(3, 1, 0, RED, SHAPE_LIST[7])
            self.pieces.append(red_piece4)
            blue_piece1 = Piece(0, 0, 0, BLUE, SHAPE_LIST[7])
            self.pieces.append(blue_piece1)
            blue_piece2 = Piece(0, 2, 0, BLUE, SHAPE_LIST[7])
            self.pieces.append(blue_piece2)
            blue_piece3 = Piece(1, 1, 0, BLUE, SHAPE_LIST[7])
            self.pieces.append(blue_piece3)
            blue_piece4 = Piece(2, 2, 0, BLUE, SHAPE_LIST[7])
            self.pieces.append(blue_piece4)
        else: #this means it is a random game
            # Generate pearl noise map for random piece generation
            noise = generateWhiteNoise(self.rows,self.cols,2)

            # Tranform noise map into pieces and add then to the board
            for i in range(len(noise)):
                for j in range(len(noise[i])):
                    if noise[i][j] < len(COLORS_LIST):
                        new_unit_piece =  Piece(i,j,0,COLORS_LIST[noise[i][j]],SHAPE_LIST[7])
                        grouped = False
                        for piece in self.pieces:
                            if piece.check_collision(new_unit_piece):
                                piece.group_shapes(new_unit_piece)
                                grouped = True
                                break
                        if not grouped:
                            self.pieces.append(new_unit_piece)
                        
