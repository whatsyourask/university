# class for save all game settings Alien Invasion"
class Settings():
    # init game settings
    def __init__(self):
        # Screen paramethers
        self.screen_width = 1280
        self.screen_height = 1024
        self.bg_color = (0, 0, 0)
        # Ship paramethers
        self.ship_limit = 3
        # Bullet paramethers
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255,255,255)
        self.bullets_allowed = 5
        self.fleet_drop_speed = 10
        self.fleet_direction = 1 # right +1,left -1
        # game acceleration rate
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()
        # Calculate points
        self.rebel_points = 50

    
    def initialize_dynamic_settings(self):
        # Initialize settings
        self.ship_speed = 1.5
        self.bullet_speed = 3
        self.rebel_speed = 1


    def increase_speed(self):
        # Increase speed settings and rebels price
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.rebel_speed *= self.speedup_scale
        self.rebel_points = int(self.rebel_points * self.score_scale)
