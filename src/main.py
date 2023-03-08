import pygame
from enum import Enum
from game.constants import WIDTH, HEIGHT, BLACK, WHITE
from game.board import Board
from game.button import Button

pygame.font.init()

FPS = 60
clock = pygame.time.Clock()

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cohesion Free")

title_font=pygame.font.SysFont("monospace", 30)

#define states for game
class GameState(Enum):
    MAIN_MENU = 1
    PLAY_CONFIG = 2
    PLAYING = 3
    QUIT = 4

game_state = GameState.MAIN_MENU
board_size = 4

# screen when configurating a game (before a game starts)
def play_config():
    SCREEN.fill(WHITE)
    global game_state
    global board_size
    run = True

    button_width, button_height = 200, 50

    decrease_button = Button("DECREASE BOARD", WIDTH/4-button_width/2-15, 250, button_width, button_height, True)
    increase_button = Button("INCREASE BOARD", 3*WIDTH/4-button_width/2+15, 250, button_width, button_height, True)
    random_button = Button("RANDOM START", WIDTH/2-button_width/2, 350, button_width, button_height, True)
    one_button = Button("LV. 1 (4x4)", WIDTH/4-button_width/2+10, 450, button_width, button_height, True)
    two_button = Button("LV. 2 (6x6)", 3*WIDTH/4-button_width/2-10, 450, button_width, button_height, True)
    three_button = Button("LV. 3 (8x8)", WIDTH/4-button_width/2+10, 550, button_width, button_height, True)
    four_button = Button("LV. 4 (12x12)", 3*WIDTH/4-button_width/2-10, 550, button_width, button_height, True)
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
                    game_state =GameState.PLAYING
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

    pause_menu = False

    button_width, button_height = 200, 50

    resume_button = Button("RESUME", WIDTH/2-button_width/2, 250, button_width, button_height, True)
    restart_button = Button("RESTART", WIDTH/2-button_width/2, 350, button_width, button_height, True)
    menu_button = Button("MAIN MENU", WIDTH/2-button_width/2, 450, button_width, button_height, True)

    board = Board(board_size,board_size)

    while run:
        SCREEN.fill(WHITE)
        if not pause_menu:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    game_state =GameState.QUIT

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause_menu = True

            board.draw_squares(SCREEN)
            board.draw_pieces(SCREEN)
            pygame.display.update()
        else:

            title_text=title_font.render("PAUSED", True, BLACK)
            title_rect = title_text.get_rect()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    game_state =GameState.QUIT

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if resume_button.check_click():
                        pause_menu = False
                    elif restart_button.check_click():
                        print("TODO")
                    elif menu_button.check_click():
                        run = False
                        game_state = GameState.MAIN_MENU
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause_menu = False

            SCREEN.blit(title_text, (WIDTH/2-title_rect.width/2, 100))
            resume_button.draw(SCREEN)
            restart_button.draw(SCREEN)
            menu_button.draw(SCREEN)
            pygame.display.update()


# main menu screen
def main_menu():
    SCREEN.fill(WHITE)
    global game_state
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
                    game_state = GameState.PLAY_CONFIG
                elif computer_button.check_click():
                    run = False
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