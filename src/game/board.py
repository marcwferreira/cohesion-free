import pygame
import random
from .constants import GREY, DARK_GREY, ROWS, SQUARE_SIZE, MENUS_HEIGHT
from .constants import BLUE, RED, GREEN, YELLOW
from .constants import WIDTH, HEIGHT
from .constants import SHAPE_LIST
from .piece import Piece
from .button import Button

class Board:
    def __init__(self, rows, cols):
        self.pieces = [] # this is a list of pieces on the map
        self.rows = rows
        self.cols = cols
        self.selected_piece = None
        self.square_size = WIDTH/self.rows
        self.create_board(0)

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


    def draw_pieces(self,win):
        for piece in self.pieces:
            piece.draw(win,self.square_size)

    def get_pieces(self):
        return self.pieces

    # Function that checks if any of the buttons for selecting pieces were clicked
    def check_pieced_click(self):
        for idx in range(len(self.pieces)):
            if self.pieces[idx].check_click(self.square_size):
                self.selected_piece = idx #remember to change pieces being selected -> this might be for outline
                self.move_down.change_enabled(True)
                self.move_up.change_enabled(True)
                self.move_left.change_enabled(True)
                self.move_right.change_enabled(True)
    
    #todo
    def check_move_piece(self):
        piece = self.pieces[self.selected_piece]
        piece_compare = []
        if self.move_down.check_click():
            # Get squares to verify if movement is possible
            piece_compare.append(piece.coords[0])
            for coord in piece.coords:
                if coord[0] not in [item[0] for item in piece_compare]:
                    piece_compare.append(coord)
                else:
                    for idx in range(len(piece_compare)):
                        if piece_compare[idx][0] == coord[0]:
                            if coord[1] > piece_compare[idx][1]:
                                piece_compare[idx] = coord
                            else:
                                break
            #dumb way to do this for now
            for j in range(len(piece_compare)):
                piece_compare[j] = [piece_compare[j][0],piece_compare[j][1]+1]
            # Verify if movement is possible
            for idx in range(len(self.pieces)):
                #do not compare with piece to move
                if idx == self.selected_piece:
                    continue
                if len([element for element in piece_compare if element in self.pieces[idx].coords]) != 0:
                    return False
            #move
            self.pieces[self.selected_piece].move('down')
            print('possible to move')
            #print(piece_compare)
            #move

        elif self.move_left.check_click():
                # Get squares to verify if movement is possible
                piece_compare.append(piece.coords[0])
                for coord in piece.coords:
                    if coord[0] not in [item[0] for item in piece_compare]:
                        piece_compare.append(coord)
                    else:
                        for idx in range(len(piece_compare)):
                            if piece_compare[idx][0] == coord[0]:
                                if coord[1] > piece_compare[idx][1]:
                                    piece_compare[idx] = coord
                                else:
                                    break
                #dumb way to do this for now
                for j in range(len(piece_compare)):
                    piece_compare[j] = [piece_compare[j][0]-1,piece_compare[j][1]]
                # Verify if movement is possible
                for idx in range(len(self.pieces)):
                    #do not compare with piece to move
                    if idx == self.selected_piece:
                        continue
                    if len([element for element in piece_compare if element in self.pieces[idx].coords]) != 0:
                        return False
                #move
                self.pieces[self.selected_piece].move('left')
                print('possible to move')
                #print(piece_compare)
                #move
        
        elif self.move_right.check_click():
                # Get squares to verify if movement is possible
                piece_compare.append(piece.coords[0])
                for coord in piece.coords:
                    if coord[0] not in [item[0] for item in piece_compare]:
                        piece_compare.append(coord)
                    else:
                        for idx in range(len(piece_compare)):
                            if piece_compare[idx][0] == coord[0]:
                                if coord[1] > piece_compare[idx][1]:
                                    piece_compare[idx] = coord
                                else:
                                    break
                #dumb way to do this for now
                for j in range(len(piece_compare)):
                    piece_compare[j] = [piece_compare[j][0]+1,piece_compare[j][1]]
                # Verify if movement is possible
                for idx in range(len(self.pieces)):
                    #do not compare with piece to move
                    if idx == self.selected_piece:
                        continue
                    if len([element for element in piece_compare if element in self.pieces[idx].coords]) != 0:
                        return False
                #move
                self.pieces[self.selected_piece].move('right')
                print('possible to move')
                #print(piece_compare)
                #move
        
        elif self.move_up.check_click():
             # Get squares to verify if movement is possible
            piece_compare.append(piece.coords[0])
            for coord in piece.coords:
                if coord[0] not in [item[0] for item in piece_compare]:
                    piece_compare.append(coord)
                else:
                    for idx in range(len(piece_compare)):
                        if piece_compare[idx][0] == coord[0]:
                            if coord[1] > piece_compare[idx][1]:
                                piece_compare[idx] = coord
                            else:
                                break
            #dumb way to do this for now
            for j in range(len(piece_compare)):
                piece_compare[j] = [piece_compare[j][0],piece_compare[j][1]-1]
            # Verify if movement is possible
            for idx in range(len(self.pieces)):
                #do not compare with piece to move
                if idx == self.selected_piece:
                    continue
                if len([element for element in piece_compare if element in self.pieces[idx].coords]) != 0:
                    return False
            #move
            self.pieces[self.selected_piece].move('up')
            print('possible to move')
            #print(piece_compare)
            #move
            return None
        #check collision
    
    #todo
    def check_end(self):
        return None

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
            #test_piece3 = Piece(0,2,180, GREEN, SHAPE_LIST[4])
            #self.pieces.append(test_piece3)
            test_piece4 = Piece(2,2,270, YELLOW, SHAPE_LIST[4])
            self.pieces.append(test_piece4)