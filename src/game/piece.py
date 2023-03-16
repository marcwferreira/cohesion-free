import pygame
import math
from .constants import RED, GREEN, BLUE, YELLOW, SQUARE_SIZE, MENUS_HEIGHT
from .constants import WIDTH, HEIGHT

class Piece:
    def __init__(self, row, col, angle, color, shape):
        self.color = color
        self.selected = False
        self.coords = []
        self.calc_coords(row, col, angle, shape) # List of coordinates the shape occupies

    # Calculates all the coordinates for the blocks needed to position the piece
    def calc_coords(self,row,col,angle, shape):

        self.coords = shape[:]

        #rotation object
        if angle != 0:
            self.rotate_piece(angle, 0)

        #Moving the object to correct location
        for idx in range(len(self.coords)):
            self.coords[idx] = [self.coords[idx][0]+row,self.coords[idx][1]+col]
    
    # Rotates the piece and fix the coordinates so that it can be better positioned on the board
    def rotate_piece(self, angle, invert):

        # Get size of shape to fix coordinates after rotating
        x_fix_value = y_fix_value = 0
        for coord in self.coords:
            if coord[0] > x_fix_value:
                x_fix_value = coord[0]
            if coord[1] > y_fix_value:
                y_fix_value = coord[0]

        rot_angle = -math.radians(angle % 360)

        # Rotate the piece
        for idx in range(len(self.coords)):
            self.coords[idx] = [round(self.coords[idx][0]*math.cos(rot_angle) - self.coords[idx][1]*math.sin(rot_angle)),
                                round(self.coords[idx][0]*math.sin(rot_angle) + self.coords[idx][1]*math.cos(rot_angle))]
            
        # Fix coordinates after rotation
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

    # Check if the piece was clicked
    def check_click(self,square_size):
        mouse_pos = pygame.mouse.get_pos() #check mouse position
        left_click = pygame.mouse.get_pressed()[0] #check pressed button on mouse
        for coord in self.coords:
            button_rect = pygame.rect.Rect((coord[0]*square_size,MENUS_HEIGHT+coord[1]*square_size),(square_size, square_size))
            #check if when left mouse button is pressed on mouse it is on top of button
            if left_click and button_rect.collidepoint(mouse_pos):
                self.selected = True
                return True
            else:
               continue
        return False
            
    def remove_select(self):
        self.selected = False

    def group_shapes(self, shape2): #idk if this the best way of doing this
        return None
    

    def check_collision(self, piece2):
        return None
    
    
    def move(self,direction):
       if direction == 'down':
        #dumb way to do it
        for idx in range(len(self.coords)):
            self.coords[idx] = [self.coords[idx][0],self.coords[idx][1]+1]
        #check if it can move (from every single coordinate -> to the position of movement)

        #move every single coordinate
    
    def draw(self, win, square_size):
        for coord in self.coords:
            pygame.draw.rect(win, self.color, (coord[0]*square_size,MENUS_HEIGHT+coord[1]*square_size,square_size,square_size))

    #debug purposes
    def __repr__(self):
        return str("{} {}".format(self.color,self.coords))

