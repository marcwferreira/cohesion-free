import random
from .constants import COLORS_LIST

def addEles(list1,list2):
    return [sum(x) for x in zip(list1, list2)]

def manhattanDist(coord1, coord2):
    dist = 0
    for coord1_i,coord2_i in zip(coord1,coord2):
        dist += abs(coord1_i - coord2_i)
    return dist

def generateWhiteNoise(width,height,difficulty):
    noise = [[r for r in range(width)] for i in range(height)]

    for i in range(0,height):
        for j in range(0,width):
            noise[i][j] = random.randint(0,len( COLORS_LIST)+difficulty)

    return noise