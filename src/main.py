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

#define states for game
class GameState(Enum):
    MAIN_MENU = 1
    PLAY_CONFIG = 2
    PLAYING = 3
    QUIT = 4

game_state = GameState.MAIN_MENU
board_size,game_type = 4,0
computer = False

# screen when configurating a game (before a game starts)
def play_config():
    SCREEN.fill(WHITE)
    global game_state
    global board_size
    global game_type
    run = True

    button_width, button_height = 200, 50

    decrease_button = Button("DECREASE BOARD", WIDTH/4-button_width/2-15, 250, button_width, button_height, True)
    increase_button = Button("INCREASE BOARD", 3*WIDTH/4-button_width/2+15, 250, button_width, button_height, True)
    random_button = Button("RANDOM START", WIDTH/2-button_width/2, 350, button_width, button_height, True)
    one_button = Button("LV. 1 (4x4)", WIDTH/4-button_width/2+10, 450, button_width, button_height, True)
    two_button = Button("LV. 2 (4x4)", 3*WIDTH/4-button_width/2-10, 450, button_width, button_height, True)
    three_button = Button("LV. 3 (4x4)", WIDTH/4-button_width/2+10, 550, button_width, button_height, True)
    four_button = Button("LV. 4 (4x4)", 3*WIDTH/4-button_width/2-10, 550, button_width, button_height, True)
    return_button= Button("RETURN", WIDTH/2-button_width/2, 650, button_width, button_height, True)

    title_text=title_font.render("Game Configuration", True, BLACK)
    title_rect = title_text.get_rect()

    while run:
        SCREEN.fill(WHITE)
        clock.tick(FPS)

        size_text=title_font.render('{} X {}'.format(board_size, board_size), True, BLACK)
        size_rect = size_text.get_rect()
        
        #game event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                game_state =GameState.QUIT
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if decrease_button.check_click():
                    if board_size > 4: 
                        board_size -= 1
                elif increase_button.check_click():
                    if board_size < 12:
                        board_size += 1
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



        SCREEN.blit(title_text, (WIDTH/2-title_rect.width/2, 100))
        SCREEN.blit(size_text, (WIDTH/2-size_rect.width/2, 250+size_rect.height/2))
        increase_button.draw(SCREEN)
        decrease_button.draw(SCREEN)
        random_button.draw(SCREEN)
        one_button.draw(SCREEN)
        two_button.draw(SCREEN)
        three_button.draw(SCREEN)
        four_button.draw(SCREEN)
        return_button.draw(SCREEN)

        pygame.display.update()

# screen while playing the game
def playing():
    SCREEN.fill(WHITE)
    global game_state
    run = True

    screen_types = 0

    button_width, button_height = 200, 50

    pause_button = Button("||", WIDTH/100, MENUS_HEIGHT/4, button_height, button_height, True)

    resume_button = Button("RESUME", WIDTH/2-button_width/2, 250, button_width, button_height, True)
    restart_button = Button("RESTART", WIDTH/2-button_width/2, 350, button_width, button_height, True)
    menu_button = Button("MAIN MENU", WIDTH/2-button_width/2, 450, button_width, button_height, True)

    board = Board(board_size,board_size, game_type)

    move_list = computer_move_cal(Board.get_pieces)

    while run:
        SCREEN.fill(WHITE)
        if screen_types == 0: # screen for game

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
       
            if(computer):
                #moves_list = [] # this will have the format (piece,movement) -> this is because we have to select a piece and then move it
                # move_list.append(computer_move_cal(Board.get_pieces)) #add new movements -> this will dynamicaaly add new movements, however rn it is hardcoded in queue def
                if len(move_list) > 0:
                    current_move = move_list.pop(0)
                    if current_move[0] == -1:
                        print('game not possible anymore')
                    board.select_piece(current_move[0])
                    board.move_piece(current_move[1])

                # call for computer movement -> it returns a list of movements and from it we will do the movements

            # check if game ended
            if board.check_end():
                screen_types = 2

            board.draw_squares(SCREEN)
            board.draw_pieces(SCREEN)
            pause_button.draw(SCREEN)
            pygame.display.update()
        elif screen_types == 2: # screen for game end

            title_text=title_font.render("YOU WON!", True, BLACK)
            title_rect = title_text.get_rect()
            score_text=title_font.render("Number of movements: {}".format(board.num_movements), True, BLACK)
            score_rect = score_text.get_rect()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    game_state =GameState.QUIT

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.check_click():
                        board = Board(board_size,board_size, game_type)
                        screen_types = 0
                    elif menu_button.check_click():
                        run = False
                        game_state = GameState.MAIN_MENU

            SCREEN.blit(title_text, (WIDTH/2-title_rect.width/2, 100))
            SCREEN.blit(score_text, (WIDTH/2-score_rect.width/2, 150))
            restart_button.draw(SCREEN)
            menu_button.draw(SCREEN)
            pygame.display.update()

        else: # pause menu

            title_text=title_font.render("PAUSED", True, BLACK)
            title_rect = title_text.get_rect()

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

            SCREEN.blit(title_text, (WIDTH/2-title_rect.width/2, 100))
            resume_button.draw(SCREEN)
            restart_button.draw(SCREEN)
            menu_button.draw(SCREEN)
            pygame.display.update()


# main menu screen
def main_menu():
    SCREEN.fill(WHITE)
    global game_state, computer
    run = True

    button_width, button_height = 200, 50

    play_button = Button("PLAY", WIDTH/2-button_width/2, 250, button_width, button_height, True)
    computer_button = Button("COMPUTER", WIDTH/2-button_width/2, 350, button_width, button_height, True)
    quit_button = Button("QUIT", WIDTH/2-button_width/2, 450, button_width, button_height, True)

    title_text=title_font.render("Cohesion Free v1.0 - alpha", True, BLACK)
    title_rect = title_text.get_rect()

    while run:
        clock.tick(FPS)
        
        #game event
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

        SCREEN.blit(title_text, (WIDTH/2-title_rect.width/2, 100))
        play_button.draw(SCREEN)
        computer_button.draw(SCREEN)
        quit_button.draw(SCREEN)

        pygame.display.update()

# main game loop
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
    
#start of the program
main()