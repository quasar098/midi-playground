import pygame
from utils import *


class ErrorScreen:
    def __init__(self, msg="Error: Unknown"):
        self.msg = msg
        self.active = False

    def draw(self, screen: pygame.Surface):
        if not self.active:
            return
        error_msg_surface = get_font("./assets/poppins-regular.ttf", 18).render(self.msg, (0, 0, 0), True)
        press_esc_to_exit = get_font("./assets/poppins-regular.ttf", 24).render("Press escape to go back", (0, 0, 0), True)
        screen.blit(error_msg_surface, error_msg_surface.get_rect(center=(Config.SCREEN_WIDTH/2, Config.SCREEN_HEIGHT/3)))
        screen.blit(press_esc_to_exit, press_esc_to_exit.get_rect(center=(Config.SCREEN_WIDTH/2, Config.SCREEN_HEIGHT*(2/3))))
