import pygame
from pygame.sprite import Sprite


class Rebel(Sprite):
    def __init__(self, settings, screen):
        # Initialize rebel and set him start position
        super(Rebel, self).__init__()
        self.screen = screen
        self.settings = settings
        # Download rebel image and set attribute rect
        self.image = pygame.image.load('images/rebel.png')
        i_width = 1800
        i_height = 927
        coef = 20
        self.image = pygame.transform.scale(self.image,
                (int(i_width/coef),int(i_height/coef))) # 736x414,only int
        self.rect = self.image.get_rect()
        # Every new rebel appear in left upper screen angle
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # Save just rebel position
        self.x = float(self.rect.x)


    def draw(self):
        self.screen.blit(self.image, self.rect)

    
    def update(self):
        # Move rebel right
        self.x += (self.settings.rebel_speed * self.settings.fleet_direction)
        self.rect.x = self.x


    def check_edges(self):
        # Return True if rebel is end of screen
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
