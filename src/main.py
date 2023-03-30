## Main
#   This is the main file of the program, it it responsible for the game loop.
#   The game loop is composed of 3 function:
#       - play_config() which displays the game's configurations before it begins,
#         this is responsible for gathering player input on the type of game before
#         a game.
#       - playing() is responsible for the game loop it self (during a gameplay), not
#         not only that but it is also responsible for the pause menu and end game screen.
#       - main_menu() is responsible for the main menu of the game.
#
#   These functions are responsible for showing content on the screen and also gathering user input
#
#   made by:
#   - Catarina Barbosa
#   - Francisca Andrade
#   - Marcos Ferreira​
#
#   03/16/2023

import pygame, time
from enum import Enum
from game.constants import WIDTH, HEIGHT, BLACK, WHITE, MENUS_HEIGHT, title_font
from game.board import Board
from game.button import Button
from game.computer import computer_move_cal

FPS = 60
clock = pygame.time.Clock()

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cohesion Free")

#define possible states for the game loop
class GameState(Enum):
    MAIN_MENU = 1
    PLAY_CONFIG = 2
    PLAYING = 3
    QUIT = 4

game_state = GameState.MAIN_MENU
board_size,game_type = 4,0
computer = False
bot_algorithm = 'dfs'

# Screen and game input when user is configuring the game (screen that shows right before a game is started)
def play_config():
    SCREEN.fill(WHITE)
    global game_state
    global board_size
    global game_type
    global bot_algorithm
    run = True

    # Define default size of buttons for this screen
    button_width, button_height = 200, 50

    # List of possible A.I. algorithms in case of a computer game
    bot_configs = ['bfs','dfs','it. dfs','greedy','a*']

    # Buttons for the interface
    if(computer):
        select_left_button = Button("<-", WIDTH/4-button_width/2-15, 260, button_width, button_height, True)
        select_right_button = Button("->", 3*WIDTH/4-button_width/2+15, 260, button_width, button_height, True)
    decrease_button = Button("DECREASE BOARD", WIDTH/4-button_width/2-15, 170, button_width, button_height, True)
    increase_button = Button("INCREASE BOARD", 3*WIDTH/4-button_width/2+15, 170, button_width, button_height, True)
    random_button = Button("RANDOM START", WIDTH/2-button_width/2, 350, button_width, button_height, True)
    one_button = Button("LV. 1 (4x4)", WIDTH/4-button_width/2+10, 450, button_width, button_height, True)
    two_button = Button("LV. 2 (4x4)", 3*WIDTH/4-button_width/2-10, 450, button_width, button_height, True)
    three_button = Button("LV. 3 (4x4)", WIDTH/4-button_width/2+10, 550, button_width, button_height, True)
    four_button = Button("LV. 4 (4x4)", 3*WIDTH/4-button_width/2-10, 550, button_width, button_height, True)
    return_button= Button("RETURN", WIDTH/2-button_width/2, 650, button_width, button_height, True)

    # Text for the interface
    title_text=title_font.render("Game Configuration", True, BLACK)
    title_rect = title_text.get_rect()

    # Screen Loop
    while run:
        SCREEN.fill(WHITE)
        clock.tick(FPS)

        size_text=title_font.render('{} X {}'.format(board_size, board_size), True, BLACK)
        size_rect = size_text.get_rect()

        if(computer):
            bot_text=title_font.render(bot_algorithm, True, BLACK)
            bot_rect = bot_text.get_rect()
        
        # Getting user input
        for event in pygame.event.get():
            # Closing the game
            if event.type == pygame.QUIT:
                run = False
                game_state =GameState.QUIT
            
            # Events in case of a mouse trigger
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Buttons to configure board size
                if decrease_button.check_click():
                    if board_size > 4: 
                        board_size -= 1
                elif increase_button.check_click():
                    if board_size < 12:
                        board_size += 1

                # In case of a computer game these will select the A.I. algorithm
                if(computer):
                    if select_left_button.check_click():
                        bot_algorithm = bot_configs[(bot_configs.index(bot_algorithm)-1)%len(bot_configs)]
                        print(bot_algorithm)
                    elif select_right_button.check_click():
                        bot_algorithm = bot_configs[(bot_configs.index(bot_algorithm)+1)%len(bot_configs)]   
                        print(bot_algorithm) 
                
                # Different buttons for a random game or predefined board
                if random_button.check_click():
                    run = False
                    game_type = 0
                    game_state = GameState.PLAYING
                elif one_button.check_click():
                    run = False
                    game_type = 1
                    board_size = 4
                    game_state = GameState.PLAYING
                elif two_button.check_click():
                    run = False
                    game_type = 2
                    board_size = 4
                    game_state = GameState.PLAYING
                elif three_button.check_click():
                    run = False
                    game_type = 3
                    board_size = 4
                    game_state = GameState.PLAYING
                elif four_button.check_click():
                    run = False
                    game_type = 4
                    board_size = 4
                    game_state = GameState.PLAYING
                elif return_button.check_click():
                    run = False
                    game_state = GameState.MAIN_MENU

        # Rendering the screen
        SCREEN.blit(title_text, (WIDTH/2-title_rect.width/2, 100))
        SCREEN.blit(size_text, (WIDTH/2-size_rect.width/2, 170+size_rect.height/2))
        if(computer):
            select_left_button.draw(SCREEN)
            select_right_button.draw(SCREEN)
            SCREEN.blit(bot_text, (WIDTH/2-bot_rect.width/2, 260+size_rect.height/2))
        increase_button.draw(SCREEN)
        decrease_button.draw(SCREEN)
        random_button.draw(SCREEN)
        one_button.draw(SCREEN)
        two_button.draw(SCREEN)
        three_button.draw(SCREEN)
        four_button.draw(SCREEN)
        return_button.draw(SCREEN)
        pygame.display.update()

# Screen and game input during a gameplay, also pause menu and end game screen
def playing():
    SCREEN.fill(WHITE)
    global game_state
    run = True

    screen_types = 0
    end_type = "lost"

    # Buttons for the interface
    button_width, button_height = 200, 50
    pause_button = Button("||", WIDTH/100, MENUS_HEIGHT/4, button_height, button_height, True)
    resume_button = Button("RESUME", WIDTH/2-button_width/2, 250, button_width, button_height, True)
    restart_button = Button("RESTART", WIDTH/2-button_width/2, 350, button_width, button_height, True)
    menu_button = Button("MAIN MENU", WIDTH/2-button_width/2, 450, button_width, button_height, True)

    # Initialize a board for the game
    board = Board(board_size,board_size, game_type)

    #draw the screen for the first time (needed for the computer mode)
    board.draw_squares(SCREEN)
    board.draw_pieces(SCREEN)
    pause_button.draw(SCREEN)
    pygame.display.update()

    # Compute the set of moves when in computer game
    if(computer):
        board_sizes = board.get_board_size()
        board_pieces = board.get_pieces()
        move_list = computer_move_cal(board_pieces[:],board_sizes[0],board_sizes[1],bot_algorithm)
        print("this is the result from bot:")
        print(move_list)

    # Screen Loop
    while run:
        SCREEN.fill(WHITE)

        # Seleting which screen to show (game, pause or end)
        if screen_types == 0: # screen for game

            # Getting inputs from user
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    game_state =GameState.QUIT

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Menu buttons
                    if pause_button.check_click():
                        screen_types = 1

                    if(not computer):
                        # Check board buttons
                        board.check_pieced_click()
                        #check for movement buttons
                        board.check_move_piece()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        screen_types = 1
                    if(not computer):
                        if board.return_if_selected():
                            if event.key == pygame.K_w:
                                board.move_piece('up')
                            elif event.key == pygame.K_a:
                                board.move_piece('left')
                            elif event.key == pygame.K_s:
                                board.move_piece('down')
                            elif event.key == pygame.K_d:
                                board.move_piece('right') 
       
            # If it is a computer game, computer will make the next move
            if(computer):
                print(move_list)
                if len(move_list) > 0:
                    current_move = move_list.pop(0)
                    #if current_move[0] == -1:
                    #    print('game not possible anymore')
                    board.select_piece(current_move[0])
                    board.move_piece(current_move[1])
                    time.sleep(0.3)
                else:
                    if board.check_end():
                        end_type = "won"
                    screen_types = 2

            # check if player won the game
            if board.check_end():
                end_type = "won"
                screen_types = 2

            board.draw_squares(SCREEN)
            board.draw_pieces(SCREEN)
            pause_button.draw(SCREEN)
            pygame.display.update()
        elif screen_types == 2: # screen for game end

            # Generate text to be displayed
            title_text=title_font.render("Game {}".format(end_type), True, BLACK)
            title_rect = title_text.get_rect()
            score_text=title_font.render("Number of movements: {}".format(board.num_movements), True, BLACK)
            score_rect = score_text.get_rect()

            # Getting user input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    game_state =GameState.QUIT

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.check_click():
                        end_type = "lost"
                        board = Board(board_size,board_size, game_type)
                        if(computer): # If restarting a computer game, recalculate moves
                            board_pieces = board.get_pieces()
                            move_list = computer_move_cal(board_pieces[:],board_sizes[0],board_sizes[1],bot_algorithm)
                        screen_types = 0
                    elif menu_button.check_click():
                        run = False
                        game_state = GameState.MAIN_MENU

            # Updating screen
            SCREEN.blit(title_text, (WIDTH/2-title_rect.width/2, 100))
            SCREEN.blit(score_text, (WIDTH/2-score_rect.width/2, 150))
            restart_button.draw(SCREEN)
            menu_button.draw(SCREEN)
            pygame.display.update()
        else: # pause menu

            # Text to be displayed
            title_text=title_font.render("PAUSED", True, BLACK)
            title_rect = title_text.get_rect()

            # Getting user input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    game_state =GameState.QUIT

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if resume_button.check_click():
                        screen_types = 0
                    elif restart_button.check_click():
                        board = Board(board_size,board_size, game_type)
                        screen_types = 0
                    elif menu_button.check_click():
                        run = False
                        game_state = GameState.MAIN_MENU
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        screen_types = 0

            # Update screen
            SCREEN.blit(title_text, (WIDTH/2-title_rect.width/2, 100))
            resume_button.draw(SCREEN)
            restart_button.draw(SCREEN)
            menu_button.draw(SCREEN)
            pygame.display.update()

# Screen and game input when in the main menu
def main_menu():
    SCREEN.fill(WHITE)
    global game_state, computer
    run = True

    # Defining necessry buttons for the interface
    button_width, button_height = 200, 50
    play_button = Button("PLAY", WIDTH/2-button_width/2, 250, button_width, button_height, True)
    computer_button = Button("COMPUTER", WIDTH/2-button_width/2, 350, button_width, button_height, True)
    quit_button = Button("QUIT", WIDTH/2-button_width/2, 450, button_width, button_height, True)

    # Define text to be displayed
    title_text=title_font.render("Cohesion Free v1.0 - alpha", True, BLACK)
    title_rect = title_text.get_rect()

    # Screen loop
    while run:
        
        # Getting user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                game_state =GameState.QUIT
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_click():
                    run = False
                    computer = False
                    game_state = GameState.PLAY_CONFIG
                elif computer_button.check_click():
                    run = False
                    computer = True
                    game_state = GameState.PLAY_CONFIG
                elif quit_button.check_click():
                    run = False
                    game_state =GameState.QUIT

        # Updating screen
        SCREEN.blit(title_text, (WIDTH/2-title_rect.width/2, 100))
        play_button.draw(SCREEN)
        computer_button.draw(SCREEN)
        quit_button.draw(SCREEN)
        pygame.display.update()

# Main game loop
def main():
    while True:
        if game_state == GameState.MAIN_MENU:
            main_menu()
        elif game_state == GameState.PLAY_CONFIG:
            play_config()
        elif game_state == GameState.PLAYING:
            playing()
        else:
            break
    pygame.quit()
    
# Program start
main()