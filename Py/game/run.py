import pygame
from settings import *
from spaceship import *
from button import *
import functions as func
from pygame.sprite import Group
from game_stats import *
from score import *

def run():
    # init game and create screen object
    pygame.init() # init preference that need pygame for normal work
    g_settings = Settings() # init Settings object
    screen = pygame.display.set_mode((g_settings.screen_width,
        g_settings.screen_height)) # create display
    pygame.display.set_caption("Rebel Invasion") # set a name
    # Create the spaceship
    ship = Spaceship(g_settings, screen)
    # Create the bullets
    bullets = Group()
    # Create the rebels
    rebels = Group()
    # Create stats
    stats = GameStats(g_settings)
    # Create button
    button = Button(g_settings, screen, "Play game")
    # Create score
    score = Score(g_settings, screen, stats)
    func.create_fleet(g_settings, screen, ship, rebels)
    # Start general game cycle
    while True:
        func.check_events(g_settings, screen, stats, score, button,  ship, rebels, bullets)
        if stats.game_active:
            ship.update()
            func.update_bullets(g_settings, screen, stats, score, ship, rebels, bullets)
            func.update_rebels(g_settings, screen, stats, score, ship, rebels, bullets)
        func.update_screen(g_settings, screen, stats, score, 
                ship, rebels, bullets, button)
        # Display last drew screen
        pygame.display.flip()


run()
