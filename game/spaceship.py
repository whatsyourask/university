import pygame
from pygame.sprite import Sprite


class Spaceship(Sprite):
    def __init__(self,settings,screen):
        # Init spaceship and set its start position
        super(Spaceship, self).__init__()
        self.screen = screen
        self.settings = settings
        # Download image and get rectangle
        self.image = pygame.image.load('images/spaceship.png')
        i_width = 1920
        i_height = 1217
        coef = 20
        self.image = pygame.transform.scale(self.image,
                (int(i_width/coef),int(i_height/coef))) # 1920x1217,only int
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # Every new ship appears
        self.rect.centerx = self.screen_rect.centerx
        # Set a object center
        self.rect.bottom = self.screen_rect.bottom # rect for image position
        # Move flags
        self.mv_right = False
        self.mv_left = False
        self.center = float(self.rect.centerx)


    def draw(self):
        # Draw starship in current position
        self.screen.blit(self.image,self.rect)


    def update(self):
        # Update ship position
        if self.mv_right and self.rect.right < self.screen_rect.right:
            self.center += self.settings.ship_speed
        if self.mv_left and self.rect.left > 0:
            self.center -= self.settings.ship_speed
        # Update attribute rect on self.center
        self.rect.centerx = self.center


    def center_ship(self):
        # Set a ship in center
        self.center = self.screen_rect.centerx
