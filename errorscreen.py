from utils import *
import pygame


class ErrorScreen:
    def __init__(self):
        self.msg = "Unspecified error!!!"
        self.active = False

    def draw(self, screen: pygame.Surface):
        if not self.active:
            return
        error_msg_surface = get_font(18).render(self.msg, True, get_colors()["hallway"])  # todo: cache the error text
        press_esc_to_exit = get_font(24).render("Press escape to go back", True, get_colors()["hallway"])
        screen.blit(error_msg_surface, error_msg_surface.get_rect(center=(Config.SCREEN_WIDTH / 2, Config.SCREEN_HEIGHT / 3)))
        screen.blit(press_esc_to_exit, press_esc_to_exit.get_rect(center=(Config.SCREEN_WIDTH / 2, Config.SCREEN_HEIGHT * (2 / 3))))
