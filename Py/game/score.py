import pygame.font
from pygame.sprite import Group
from spaceship import *


class Score():
    def __init__(self, settings, screen, stats):
        # Initialize attribute score
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats
        # Settings font for score output
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        # Preparation original image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()


    def prep_score(self):
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color,
                self.settings.bg_color)
        # Score output in right upper part of screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20


    def prep_high_score(self):
        # Preparation high score in graphic image
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                self.text_color, self.settings.bg_color)
        # High score compare by center
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
    

    def prep_level(self):
        # Preparation level in graphic image
        self.level_image = self.font.render(str(self.stats.level), True,
                self.text_color, self.settings.bg_color)
        # Level is displayed under the current score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10


    def prep_ships(self):
        # Reports the number of ships remaining
        self.ships = Group()
        for ship_num in range(self.stats.ship_left):
            ship = Spaceship(self.settings, self.screen)
            ship.rect.x = 10 + ship_num * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)


    def show(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
