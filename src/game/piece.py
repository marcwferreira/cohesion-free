import pygame
import math
from .constants import MENUS_HEIGHT
from .utils import addEles, manhattanDist

class Piece:
    def __init__(self, row, col, angle, color, shape):
        self.color = color
        self.coords = []
        self.calc_coords(row, col, angle, shape) # List of coordinates the shape occupies

    def __eq__(self,other):
        if not isinstance(other, Piece):
            # don't attempt to compare against unrelated types
            return NotImplemented
        
        if self.color == other.color:
            self_list = [tuple(lst) for lst in self.coords]
            other_list = [tuple(lst) for lst in other.coords]
            if set(self_list) == set(other_list):
                return True
        return False
    
    def __lt__(self,other):
        if self.color < other.color:
            return True
        if self.coords < other.coords:
            return True

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
                return True
            else:
               continue
        return False

    def group_shapes(self, shape2):
        self.coords.extend(shape2.coords)
    
    # Check if two pieces are touching each other and are the same color
    def check_collision(self, piece2):
        if self.color == piece2.color:
            for coord1 in self.coords:
                for coord2 in piece2.coords:
                    if manhattanDist(coord1,coord2) <= 1: 
                        self.group_shapes(piece2)
                        return True
        return False
    
    # Calculates the distance (manhattan distance) from this piece to another one
    def calculate_dist(self,piece2):
        dist = 1000
        for coord1 in self.coords:
            for coord2 in piece2.coords:
                dist_measured = manhattanDist(coord1,coord2)
                dist = min(dist,dist_measured)
        return dist
    
    def move(self,direction):
        dir_add = -1 if (direction == 'left' or direction == 'up') else 1
        if direction == 'up' or direction == 'down':
            self.coords = list(map(addEles,self.coords,([[0,dir_add]]*len(self.coords))))
        elif direction == 'left' or direction == 'right':
            self.coords = list(map(addEles,self.coords,([[dir_add,0]]*len(self.coords))))
    
    def draw(self, win, square_size):
        for coord in self.coords:
            pygame.draw.rect(win, self.color, (coord[0]*square_size,MENUS_HEIGHT+coord[1]*square_size,square_size,square_size))

    #debug purposes
    def __repr__(self):
        return str("{} {}".format(self.color,self.coords))

