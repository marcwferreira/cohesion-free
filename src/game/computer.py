from collections import deque
import copy
from .utils import move_piece

def computer_move_cal(board_pieces, board_height, board_width):
    board_copy = copy.deepcopy(board_pieces)
    result = iterative_dfs(board_copy, board_width, board_height)
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

# TODO
def eval_fuction():
    return None

# TODO
def greedy_search():
    return []

# TODO
def a_star():
    return []
