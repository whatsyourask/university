import pygame.font


class Button():
    def __init__(self, settings, screen, msg):
        # Initialize button attribute
        self.screen = screen
        self.screen_rect = screen.get_rect()
        # Set size and internals of buttons
        self.width, self.height = 200, 50
        self.button_color = (27, 27, 27)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        # Building object button rect and leveling
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        # Message of button create only one time
        self.prep_msg(msg)


    def prep_msg(self, msg):
        # Transform msg in rectangle and center text
        self.msg_image = self.font.render(msg, True, self.text_color,
                self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center


    def draw(self):
        # Display empty button and output message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
