import pygame
from .constants import BUTTON_TEXT, BUTTON_BACKGROUND, BUTTON_BACKGROUND_PRESSSED, BUTTON_DISABLED

pygame.font.init()

button_font = pygame.font.Font('freesansbold.ttf',18)

class Button():
    def __init__(self, text, x_pos, y_pos, x_size, y_size, enabled):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_size = x_size
        self.y_size = y_size
        self.text = text
        self.enabled = enabled
        
    def draw(self,win):
        button_text = button_font.render(self.text, True, BUTTON_TEXT)
        text_size = button_text.get_rect()
        button_rect = pygame.rect.Rect((self.x_pos, self.y_pos),(self.x_size, self.y_size))
        if(self.enabled):
            if self.check_click():
                pygame.draw.rect(win, BUTTON_BACKGROUND_PRESSSED, button_rect, 0, 5)
            else:
                pygame.draw.rect(win, BUTTON_BACKGROUND, button_rect, 0, 5)
        else:
            pygame.draw.rect(win, BUTTON_DISABLED, button_rect, 0, 5)
        win.blit(button_text, ( (self.x_pos+self.x_size/2)-text_size.width/2, (self.y_pos+self.y_size/2)-text_size.height/2 ))

    def change_enabled(self,new):
        if new == True:
            self.enabled = True
        else:
            self.enabled = False

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos() #check mouse position
        left_click = pygame.mouse.get_pressed()[0] #check pressed button on mouse
        button_rect = pygame.rect.Rect((self.x_pos, self.y_pos),(self.x_size, self.y_size)) #button rectangle

        #check if when left mouse button is pressed on mouse it is on top of button
        if left_click and button_rect.collidepoint(mouse_pos) and self.enabled:
            return True
        else:
            return False