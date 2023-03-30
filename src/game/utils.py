## Utils
#   This files contains functions to auxiliates in other tasks.
#   
#   made by:
#   - Catarina Barbosa
#   - Francisca Andrade
#   - Marcos Ferreira​
#
#   03/16/2023

import random
from .constants import COLORS_LIST

# Function to sum two lists element by element
def addEles(list1,list2):
    return [sum(x) for x in zip(list1, list2)]

# Function to calculate the manhattan distance between two coordiantes
def manhattanDist(coord1, coord2):
    dist = 0
    for coord1_i,coord2_i in zip(coord1,coord2):
        dist += abs(coord1_i - coord2_i)
    return dist

# Function to generate a white noise matrix with the defined width and hiehgt
def generateWhiteNoise(width,height,difficulty):
    noise = [[r for r in range(width)] for i in range(height)]

    for i in range(0,height):
        for j in range(0,width):
            noise[i][j] = random.randint(0,len( COLORS_LIST)+difficulty)

    return noise

# Function to move pieces on a board
def move_piece(state_tuple,rows,cols,choosen_piece,direction):
        state = list(state_tuple)
        dir_correct = -1 if (direction == 'left' or direction == 'up') else 1 # -1 to move to th or up because of how the coords work
        piece_compare = [state[choosen_piece].coords[0]]
        if direction == 'up' or direction == 'down':
            # Get squares to verify if movement is possible
            for coord in state[choosen_piece].coords:
                if coord[0] not in [item[0] for item in piece_compare]:
                    piece_compare.append(coord)
                else:
                    for idx in range(len(piece_compare)):
                        if piece_compare[idx][0] == coord[0] and coord[1] > piece_compare[idx][1] and direction == 'down': piece_compare[idx] = coord
                        elif piece_compare[idx][0] == coord[0] and coord[1] < piece_compare[idx][1] and direction == 'up': piece_compare[idx] = coord
            # Add 1 or -1 to every y coord in the comparisson coords to get the matching cells to compare
            piece_compare = list(map(addEles,piece_compare,([[0,dir_correct]]*len(piece_compare))))
            # Verify collision with other pieces
            for idx in range(len(state)):
                if idx == choosen_piece: continue
                if len([element for element in piece_compare if element in state[idx].coords]) != 0: return False
            for square in state[choosen_piece].coords: # Verify collision with board walls
                if square[1] >= (cols-1) and dir_correct == 1: return False 
                elif square[1] <= 0 and dir_correct == -1: return False
            #move piece
            state[choosen_piece].move(direction)

        elif direction == 'left' or direction == 'right':
            # Get squares to verify if movement is possible
            for coord in state[choosen_piece].coords:
                if coord[1] not in [item[1] for item in piece_compare]:
                    piece_compare.append(coord)
                else:
                    for idx in range(len(piece_compare)):
                        if piece_compare[idx][1] == coord[1] and coord[0] > piece_compare[idx][0] and direction == 'right': piece_compare[idx] = coord
                        elif piece_compare[idx][1] == coord[1] and coord[0] < piece_compare[idx][0] and direction == 'left': piece_compare[idx] = coord
            # Add 1 or -1 to every y coord in the comparisson coords to get the matching cells to compare
            piece_compare = list(map(addEles,piece_compare,([[dir_correct,0]]*len(piece_compare))))
            # Verify collision with other pieces
            for idx in range(len(state)):
                if idx == choosen_piece: continue
                if len([element for element in piece_compare if element in state[idx].coords]) != 0: return False
            for square in state[choosen_piece].coords: # Verify collision with board walls
                if square[0] >= (rows-1) and dir_correct == 1: return False 
                elif square[0] <= 0 and dir_correct == -1: return False
            #move piece
            state[choosen_piece].move(direction)
        #check if collisions (for pieces grouping) happendes
        return check_collisions(state,choosen_piece)


# Define function to check collisions when using bot
def check_collisions(state,choosen_piece):
        pieces_remove = []
        for idx in range(len(state)):
            if idx == choosen_piece: continue
            if state[choosen_piece].check_collision(state[idx]):
                pieces_remove.append(idx)
        for i in sorted(pieces_remove, reverse=True):
            del state[i]
        return state
