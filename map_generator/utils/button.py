import pygame
from pygame.locals import *


clicked = False

class Button:

    button_col = (25, 190, 225)
    click_col = (50, 150, 255)	
    text_col = (0, 0, 0)
    width = 180
    height = 70

    def __init__(self, x, y, screen, font, text) -> None:
        self.x = x
        self.y = y
        self.screen = screen
        self.font = font
        self.text = text

    def draw(self):
        global clicked
        action = False
        pos = pygame.mouse.get_pos()
        
        button_rect = Rect(self.x, self.y, self.width, self.height)

        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(self.screen, self.click_col, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True
            else:
                pygame.draw.rect(self.screen, self.button_col, button_rect)
        else:
            pygame.draw.rect(self.screen, self.button_col, button_rect)

        text_img = self.font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        self.screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 25))
        return action