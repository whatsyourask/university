import sys
import pygame
from bullet import Bullet
from rebel import Rebel
from time import sleep


def check_keydown_events(event, settings, screen, ship, bullets):
    # Responds to keystrokes
    if event.key == pygame.K_RIGHT:
        # Move spaceship to right
        ship.mv_right = True
    elif event.key == pygame.K_LEFT:
        # Move spaceship to left
         ship.mv_left = True
    elif event.key == pygame.K_SPACE:
        fire(settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event,ship):
    # Responds to the release of keys
    if event.key == pygame.K_RIGHT:
        # Stop move spaceship to right
        ship.mv_right = False
    elif event.key == pygame.K_LEFT:
        # Stop move spaceship to left
        ship.mv_left = False


def check_events(settings, screen, stats, score, button, ship, rebels, bullets):
    # Track keyboard and mouse events
    for event in pygame.event.get(): # Cycle of events
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,settings, screen, ship, bullets)
            check_keydown_events(event, settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(settings, screen, stats, score, button, 
                    ship, rebels, bullets, mouse_x, mouse_y)


def check_play_button(settings, screen, stats, score, button, 
        ship, rebels, bullets, mouse_x, mouse_y):
    # Start new game
    button_clicked = button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        settings.initialize_dynamic_settings()
        stats.reset_stats()
        stats.game_active = True
        # Reset score and level images
        score.prep_score()
        score.prep_high_score()
        score.prep_level()
        score.prep_ships()
        rebels.empty()
        bullets.empty()
        create_fleet(settings, screen, ship, rebels)
        ship.center_ship()
        pygame.mouse.set_visible(False)


def update_screen(g_settings, screen, stats, score, ship, rebels, bullets, button):
    # Update screen =_=
    screen.fill(g_settings.bg_color)
    # All bullets outputs in back of ships screens
    for bullet in bullets.sprites():
        bullet.draw()
    ship.draw()
    rebels.draw(screen)
    score.show()
    if not stats.game_active:
        button.draw()
    pygame.display.flip()


def update_bullets(settings, screen, stats, score, ship, rebels, bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_rebel_collisions(settings, screen, stats, score, ship, rebels, bullets)
    

def check_bullet_rebel_collisions(settings, screen, stats, score, ship, rebels, bullets):
    collisions = pygame.sprite.groupcollide(bullets, rebels, True, True)
    # Check for create a new rebels part
    if len(rebels) == 0:
        # Destroy existing bullets
        bullets.empty()
        settings.increase_speed()
        # Leveling
        stats.level += 1
        score.prep_level()
        create_fleet(settings, screen, ship, rebels)
    if collisions:
        for rebels in collisions.values():
            stats.score += settings.rebel_points * len(rebels)
            score.prep_score()
            check_high_score(stats, score)


def fire(settings, screen, ship, bullets):
    # Create a new bullets and include it in group bullets
    if len(bullets) < settings.bullets_allowed:
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)


def get_num_rebels_x(settings, rebel_width):
    # Calculate number of rebels in fleet
    available_space_x = settings.screen_width - 2 * rebel_width
    num_rebels_x = int(available_space_x / (2 * rebel_width))
    return num_rebels_x


def get_num_rows(settings, ship_height, rebel_height):
    # Define rows number
    available_space_y = (settings.screen_height 
            - 3 * rebel_height) - ship_height
    num_rows = int(available_space_y / (2 * rebel_height))
    return num_rows


def create_rebel(settings, screen, rebels, rebel_num, row_num):
    # Create rebel and move it
    rebel = Rebel(settings, screen)
    rebel_width = rebel.rect.width
    rebel.x = rebel_width + 2 * rebel_width * rebel_num
    rebel.rect.x = rebel.x
    rebel.rect.y = rebel.rect.height + 2 * rebel.rect.height * row_num
    rebels.add(rebel)


def create_fleet(settings, screen, ship, rebels):
    # Create fleet of rebels
    rebel = Rebel(settings, screen)
    num_rebels_x = get_num_rebels_x(settings, rebel.rect.width)
    num_rows = get_num_rows(settings, ship.rect.height, rebel.rect.height)
    for row_num in range(num_rows):
        for rebel_num in range(num_rebels_x):
            create_rebel(settings, screen, rebels, rebel_num, row_num)


def update_rebels(settings, screen,  stats, score, ship, rebels, bullets):
    # Check if the fleet has reached the edge of the screen
    check_fleet_edges(settings, rebels)
    # Update position all rebels in fleet
    rebels.update()
    # Check collisions "Rebel-Ship"
    if pygame.sprite.spritecollideany(ship, rebels):
        ship_hit(settings, screen, stats, score, ship, rebels, bullets)
    # Check rebels reaching the bottom of the screen
    check_rebels_bottom(settings, screen, stats, score, ship, rebels, bullets)


def check_fleet_edges(settings, rebels):
    # React to an rebel reaching the edge of screen
    for rebel in rebels.sprites():
        if rebel.check_edges():
            change_fleet_direction(settings, rebels)
            break


def change_fleet_direction(settings, rebels):
    # Let down all fleet and change fleet direction
    for rebel in rebels.sprites():
        rebel.rect.y += settings.fleet_drop_speed
    settings.fleet_direction *= -1


def ship_hit(settings, screen, stats, score, ship, rebels, bullets):
    # Process ship hit with rebel
    if stats.ship_left > 0:
        stats.ship_left -= 1
        # Update game information
        score.prep_ships()
        # Clear lists rebels and bullets
        rebels.empty()
        bullets.empty()
        # Create a new fleet and set ship in center
        create_fleet(settings, screen, ship, rebels)
        ship.center_ship()
        # Pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_rebels_bottom(settings, screen, stats, score, ship, rebels, bullets):
    screen_rect = screen.get_rect()
    for rebel in rebels.sprites():
        if rebel.rect.bottom >= screen_rect.bottom:
            ship_hit(settings, screen, stats, score, ship, rebels, bullets)
            break


def check_high_score(stats, score):
    # Check a new high score has appeared
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        score.prep_high_score()
