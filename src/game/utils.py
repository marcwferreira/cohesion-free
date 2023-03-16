
def addEles(list1,list2):
    return [sum(x) for x in zip(list1, list2)]

def manhattanDist(coord1, coord2):
    dist = 0
    for coord1_i,coord2_i in zip(coord1,coord2):
        dist += abs(coord1_i - coord2_i)
    return dist