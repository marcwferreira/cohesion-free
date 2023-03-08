import pygame
import math
from .constants import RED, GREEN, BLUE, YELLOW, SQUARE_SIZE, MENUS_HEIGHT
from .constants import WIDTH, HEIGHT

class Piece:
    def __init__(self, row, col, angle, color, shape):
        # used to generate the piece
        # information to store
        self.color = color
        self.selected = False
        self.coords = []
        self.calc_coords(row, col, angle, shape) #list of coordinates the shape occupies

    def calc_coords(self,row,col,angle, shape):

        self.coords = shape[:]

        #rotation object
        if angle != 0:
            self.rotate_piece(angle, 0)

        #temporary
        for idx in range(len(self.coords)):
            self.coords[idx] = [self.coords[idx][0]+row,self.coords[idx][1]+col]
    

    def rotate_piece(self, angle, invert):
        #get size of shape to fix coordinates after rotating
        x_fix_value = y_fix_value = 0
        for coord in self.coords:
            if coord[0] > x_fix_value:
                x_fix_value = coord[0]
            if coord[1] > y_fix_value:
                y_fix_value = coord[0]

        rot_angle = -math.radians(angle % 360)

        #rotate the piece
        for idx in range(len(self.coords)):
            self.coords[idx] = [self.coords[idx][0]*math.cos(rot_angle) - self.coords[idx][1]*math.sin(rot_angle),
                                self.coords[idx][0]*math.sin(rot_angle) + self.coords[idx][1]*math.cos(rot_angle)]
            
        #fix coordinates after rotation
        if angle == 90:
            x_fix, y_fix = 0, y_fix_value
        elif angle == 180:
            x_fix, y_fix = x_fix_value,y_fix_value
        elif angle == 270:
            x_fix, y_fix = x_fix_value, 0
        else:
            x_fix = y_fix = 0

        for idx in range(len(self.coords)):
            self.coords[idx] = [self.coords[idx][0]+x_fix,self.coords[idx][1]+y_fix]


    def group_shapes(self, shape2): #idk if this the best way of doing this
        return None
    

    def check_collision(self, piece2):
        return None
    
    
    def move(self):
        return None
        #check if it can move (from every single coordinate)

        #move every single coordinate
    
    def draw(self, win, square_size):
        
        for coord in self.coords:
            pygame.draw.rect(win, self.color, (coord[0]*square_size,MENUS_HEIGHT+coord[1]*square_size,square_size,square_size))

    #debug purposes
    def __repr__(self):
        return str("{} {}".format(self.color,self.coords))

