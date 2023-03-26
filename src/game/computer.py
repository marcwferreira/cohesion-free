from collections import deque, Counter
import copy, random, functools
from .utils import move_piece
from queue import PriorityQueue

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

    return result

# Define function to check if a state is the goal state
def is_goal_state(state):
    pieces_color = [piece.color for piece in state]
    return len(set(pieces_color)) == len(pieces_color)

def bfs(start_board, rows, cols):
    
    # Define queue for BFS
    queue = deque([(start_board,[])])
    
    # List of visited board configurations
    visited_boards = [sorted(start_board)]
    
    # Define fucnction to generate new states
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

    return [] # -> Change so returns when no solution is found

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
                #print("new generated board: using {} and {}".format(i,direction))
                if new_board != False:
                    if sorted(new_board) not in visited_boards:
                        new_states.append((new_board,copy.deepcopy(moves)+[[i,direction]]))
                        visited_boards.append(sorted(new_board))
        return new_states
    
    while stack:
        state, moves = stack.pop()
        if is_goal_state(state):
            return moves
        for new_state, new_moves in generate_states(state, moves):
            stack.append([new_state, new_moves])

    return []

def iterative_dfs(start_board,rows,cols):

    def iterative_deepening_dfs(start_board, rows, cols):
        depth = 0
        while True:
            print(depth)
            result = depth_limited_dfs(start_board, rows, cols, depth)
            if result is not None:
                return result
            depth += 1

    def depth_limited_dfs(start_board, rows, cols, depth):
        visited_boards = [sorted(start_board)]
        stack = [(start_board, [])]
        while stack:
            state, moves = stack.pop()
            if is_goal_state(state):
                return moves
            if len(moves) == depth:
                continue
            for new_state, new_moves in generate_states(state, moves, rows, cols):
                if sorted(new_state) not in visited_boards:
                    stack.append((new_state, moves + [new_moves]))
                    visited_boards.append(sorted(new_state))
        return None

    def generate_states(state, moves, rows, cols):
        new_states = []
        for i in range(len(state)):
            for direction in ["up", "down", "left", "right"]:
                new_board = move_piece(copy.deepcopy(state), rows, cols, i, direction)
                if new_board != False:
                    new_states.append((new_board, [i, direction]))
        return new_states

    moves = iterative_deepening_dfs(start_board, rows, cols)
        
    return moves

def greedy_search(start_board, rows, cols):
    
    # Define list for storing the current state
    current_state = (start_board,[])

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
    
    def evaluation_function(state_move): #TODO
        return -1 # not complete
    
    # Perform greedy search
    while True:
        (cur_state, cur_moves) = current_state
        next_states = generate_states(cur_state, cur_moves)
        if is_goal_state(cur_state) or not next_states:
            break
        best_next_state = max(next_states, key=evaluation_function)
        current_state = best_next_state

    return current_state[1] # if is_goal_state(current_state) else []

def a_star(start_board, rows, cols):
    # Define the priority queue for A*
    priority_queue = PriorityQueue()
    # Add the start board to the priority queue with priority as 0
    priority_queue.put((0, start_board, []))
    # Define the set of visited board configurations
    visited_boards = [sorted(start_board)]
    
    # Define function to generate new states
    def generate_states(state, moves):
        new_states = []
        for i in range(len(state)):
            for direction in ["up", "down", "left", "right"]:
                new_board = move_piece(copy.deepcopy(state), rows, cols, i, direction)
                if new_board != False:
                    if sorted(new_board) not in visited_boards:
                        # Calculate the priority of the new state
                        priority = len(moves) + 1 + evaluation_function(new_board, rows, cols)
                        # Add the new state to the priority queue with calculated priority
                        new_states.append((priority, new_board, copy.deepcopy(moves) + [(i, direction)]))
                        visited_boards.append(sorted(new_board))
        return new_states
    
    # Define the heuristic function
    def evaluation_function(board, rows, cols):
        result = 0
        piece_colors = []
        distance_pieces=[]
        for piece in board:
            piece_colors.append(piece.color)

            min_x, max_x = 0, 1000
            min_y, max_y = 0, 1000
            for coord in piece.coords:
                if coord[0] < min_x:
                    min_x = coord[0]
                elif coord[0] > max_x:
                    max_x = coord[0]
                if coord[1] < min_x:
                    min_x = coord[1]
                elif coord[1] > max_x:
                    max_x = coord[1]

            # Size of pieces plays a negative impact in result, this is to prevent soft blocks
            result -= (max_x-min_x)
            result -= (max_y-min_y)

            for piece2 in board:
                if piece == piece2:
                    continue
                distance_pieces.append(piece.calculate_dist(piece2))

        result -= len(piece_colors) # number of pieces on board have negative impact on result

        # Calculate distance form pieces of the same color TODO
        

        return -1
    
    # Performing A*
    while not priority_queue.empty():
        test, state, moves = priority_queue.get()
        print("current state to avaliate:")
        print(test)
        print(state)
        print(moves)
        print("#######################################################")
        if is_goal_state(state):
            return moves
        for new_priority, new_state, new_moves in generate_states(state, moves):
            # Add the new state to the priority queue with calculated priority
            priority_queue.put((new_priority, new_state, new_moves))

    return []