## Computer
#   This contains the different A.I. algorithms that are used with the computer games.
#
#   made by:
#   - Catarina Barbosa
#   - Francisca Andrade
#   - Marcos Ferreira​
#
#   03/16/2023

from collections import deque
import copy
from .utils import move_piece
from queue import PriorityQueue

# Wrapper Function to call the proper A.I. algorithm when in a coputer game
def computer_move_cal(board_pieces, board_height, board_width, algorithm):

    # Make a copy of the board to nopt break the original
    board_copy = copy.deepcopy(board_pieces)

    # Choose the algorithm
    if algorithm == "bfs":
        result = bfs(board_copy, board_width, board_height)
    elif algorithm == 'dfs':
        result = dfs(board_copy, board_width, board_height)
    elif algorithm == "it. dfs":
        result = bfs(board_copy, board_width, board_height)
    elif algorithm == "greedy":
        result = greedy_search(board_copy, board_width, board_height)
    elif algorithm == "a*":
        result = a_star(board_copy, board_width, board_height)
    else:
        result = dfs(board_copy, board_width, board_height)

    # Return the list of movements it found at the end
    return result

# Define function to check if a state is the goal state
def is_goal_state(state):
    pieces_color = [piece.color for piece in state]
    return len(set(pieces_color)) == len(pieces_color)

# BFS algorithm
def bfs(start_board, rows, cols):
    
    # Define queue for BFS
    queue = deque([(start_board,[])])
    
    # List of visited board configurations
    visited_boards = [sorted(start_board)]
    
    # Define function to generate new states
    def generate_states(state, moves):
        new_states = []
        for i in range(len(state)):
            for direction in ["up", "down", "left", "right"]:
                new_board = move_piece(copy.deepcopy(state), rows, cols, i, direction)
                print("new generated board: using {} and {}".format(i,direction))
                if new_board != False:
                    if sorted(new_board) not in visited_boards:
                        new_states.append((new_board,copy.deepcopy(moves)+[[i,direction]]))
                        visited_boards.append(sorted(new_board))
        return new_states
    
    # Performing BFS
    while queue:
        state, moves = queue.popleft()
        if is_goal_state(state):
            return moves
        for new_state, new_moves in generate_states(state, moves):
            queue.append([new_state, new_moves])
        if not queue:
            return moves

    return [] # If a list of moves to win the game can't be found return an empty list (this means the compute gave up on the game)

# DFS function
def dfs(start_board, rows, cols):

    # List of visited board configurations
    visited_boards = [sorted(start_board)]

    # Define stack for DFS
    stack = [(start_board,[])]

    # Define fucnction to generate new states
    def generate_states(state, moves):
        new_states = []
        for i in range(len(state)):
            for direction in ["up", "down", "left", "right"]:
                new_board = move_piece(copy.deepcopy(state), rows, cols, i, direction)
                if new_board != False:
                    if sorted(new_board) not in visited_boards:
                        new_states.append((new_board,copy.deepcopy(moves)+[[i,direction]]))
                        visited_boards.append(sorted(new_board))
        return new_states
    
    # Performing DFS
    while stack:
        state, moves = stack.pop()
        if is_goal_state(state):
            return moves
        for new_state, new_moves in generate_states(state, moves):
            stack.append([new_state, new_moves])
        if not stack:
            return moves

    return [] # If a list of moves to win the game can't be found return an empty list (this means the compute gave up on the game)

# Iterative deepening search algorithm
def iterative_dfs(start_board,rows,cols):
    """
    Function to perform an iterative depth-first search on the board.
    Takes three arguments: start_board, rows, cols.
    """
    def depth_limited_dfs(start_board, rows, cols, depth):
        visited_boards = [sorted(start_board)]
        stack = [(start_board, [])]
        
        # Loop until the stack is empty.
        while stack:
            state, moves = stack.pop()
            
            # If the popped state is the goal state, return the moves.
            if is_goal_state(state):
                return moves
            
            # If the depth limit has been reached, continue to the next iteration.
            if len(moves) == depth:
                continue
            
            # Generate new states from the current state.
            for new_state, new_moves in generate_states(state, rows, cols):
                if sorted(new_state) not in visited_boards:
                    stack.append((new_state, moves + [new_moves]))
                    visited_boards.append(sorted(new_state))
        
        # If the loop completes without finding a goal state, return None.
        return None

    # Define function to generate new states
    # This function tried to move every piece in each direction and if finds a new board configuration saves it    
    def generate_states(state, rows, cols):
        new_states = []
        
        # Loop through each piece in the board.
        for i in range(len(state)):
            for direction in ["up", "down", "left", "right"]:
                new_board = move_piece(copy.deepcopy(state), rows, cols, i, direction)
                # If the new board is valid, add it to the list of new states along with the move that led to it.
                if new_board != False:
                    new_states.append((new_board, [i, direction]))
        
        return new_states
    
    depth = 0
    
    # Loop until a goal state is found,
    while True:    
        # Call depth_limited_dfs with the current depth.
        result = depth_limited_dfs(start_board, rows, cols, depth)
        
        if result is not None:
            return result
        
        if depth > 100: # To prevent an infinite loop the max depth of the search allowed is 100
            break
        
        # Increment the depth and continue to the next iteration of the loop.
        depth += 1

    return [] # If a list of moves to win the game can't be found return an empty list (this means the compute gave up on the game)

#####################################
#                                   #
#   Heuristics ALgorithms           #
#                                   #
#####################################

# Evaluation Function Used
def evaluation_function(info_tuple, rows, cols):

    # Definying a point system
    result = 0

    # Getting the board
    board = info_tuple[0]

    # test if the number of pieces decreased
    num_pieces = len(board)
    
    distance_pieces=[] # Calculate the distances between all pieces of the same color
    for piece in board:

        # test for smaller size of pieces
        min_x, max_x = 0, 1000
        min_y, max_y = 0, 1000
        for coord in piece.coords:
            # test for smaller size of pieces
            if coord[0] < min_x:
                min_x = coord[0]
            elif coord[0] > max_x:
                max_x = coord[0]
            if coord[1] < min_x:
                min_x = coord[1]
            elif coord[1] > max_x:
                max_x = coord[1]

        # Size of pieces plays a negative impact in result, this is to prevent soft blocks
        result += 5*(max_x-min_x)
        result += 5*(max_y-min_y) # PLEASE DON'T FORGET TO NORMALIZE

          # Test for pieces closer to the edges
        result += 2*min(min_x,rows-max_x)
        result += 2*min(min_y,rows-max_y) # PLEASE DON'T FORGET TO NORMALIZE

        # test for distance of pieces
        for piece2 in board:
            if piece == piece2:
                continue
            elif piece.color != piece2.color:
                continue
            distance_pieces.append(piece.calculate_dist(piece2))

    # Calculating the result   

    result += 10*num_pieces # since we are trying to minimize the points the fewer the pieces the better! WILL NEED NORMLIZATION

    for dist in distance_pieces:
        result += dist

    return result


# Greedy Seach Algorithm
def greedy_search(start_board, rows, cols):
    
    # Define list for storing the current state
    current_state = (start_board,[])

    # List of visited board configurations
    visited_boards = [sorted(start_board)]

    # Define function to generate new states
    # This function tried to move every piece in each direction and if finds a new board configuration saves it
    def generate_states(state, moves):
        new_states = []
        for i in range(len(state)):
            for direction in ["up", "down", "left", "right"]:
                new_board = move_piece(copy.deepcopy(state), rows, cols, i, direction)
                print("new generated board: using {} and {}".format(i,direction))
                if new_board != False:
                        if sorted(new_board) not in visited_boards:
                            new_states.append((new_board,copy.deepcopy(moves)+[[i,direction]]))
                            visited_boards.append(sorted(new_board))
        return new_states
    
    # Perform greedy search
    while True:
        (cur_state, cur_moves) = current_state
        next_states = generate_states(cur_state, cur_moves)
        if is_goal_state(cur_state) or not next_states:
            break
        best_next_state = min(next_states, key=lambda x: evaluation_function(x,rows,cols))
        current_state = best_next_state

    return current_state[1] # returns a list of move even if a game can't be won

# A Start Algorithm
def a_star(start_board, rows, cols):
    # Define the priority queue for A*
    priority_queue = PriorityQueue()
    # Add the start board to the priority queue with priority as 0
    priority_queue.put((0, start_board, []))
    # Define the set of visited board configurations
    visited_boards = [sorted(start_board)]
    
    # Define function to generate new states
    # This function tried to move every piece in each direction and if finds a new board configuration saves it
    def generate_states(state, moves):
        new_states = []
        for i in range(len(state)):
            for direction in ["up", "down", "left", "right"]:
                new_board = move_piece(copy.deepcopy(state), rows, cols, i, direction)
                if new_board != False:
                    if sorted(new_board) not in visited_boards:
                        # Calculate the priority of the new state
                        priority = len(moves) + 1 + evaluation_function((new_board, copy.deepcopy(moves) + [(i, direction)]), rows, cols)
                        # Add the new state to the priority queue with calculated priority
                        new_states.append((priority, new_board, copy.deepcopy(moves) + [(i, direction)]))
                        visited_boards.append(sorted(new_board))
        return new_states
    
    # Performing A*
    while not priority_queue.empty():
        score, state, moves = priority_queue.get()
        if is_goal_state(state):
            return moves
        for new_priority, new_state, new_moves in generate_states(state, moves):
            # Add the new state to the priority queue with calculated priority
            priority_queue.put((new_priority, new_state, new_moves))

    return [] # If a list of moves to win the game can't be found return an empty list (this means the compute gave up on the game)