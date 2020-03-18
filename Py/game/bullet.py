import pygame
from pygame.sprite import Sprite

# Class fo control bullets
class Bullet(Sprite):
    def __init__(self, settings, screen, ship):
        # Create bullets in current position
        super(Bullet, self).__init__()
        self.screen = screen
        # Create bullet position and set true position
        self.rect = pygame.Rect(0, 0, settings.bullet_width,
                settings.bullet_height)
        self.rect.centerx = ship.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        # Bullet position keep 
        self.y = float(self.rect.y)
        self.color = settings.bullet_color
        self.speed = settings.bullet_speed
    
    def update(self):
        # Move bullet up on the screen
        # Update bullet position in float format
        self.y -= self.speed
        # Update bullet rectangle
        self.rect.y = self.y

    def draw(self):
        # Output
        pygame.draw.rect(self.screen, self.color, self.rect)
