import pygame
from utils import *
from math import e as eulers_number
from typing import Callable


def draw_beveled_rectangle(surf: pygame.Surface, color: pygame.Color, rect: pygame.Rect) -> None:
    """i think they're called bevels"""
    pygame.draw.rect(surf, (0, 0, 0), rect.inflate(7, 7), border_radius=6)
    pygame.draw.rect(surf, color, rect)


def sigmoid_transform(n):
    """Interpolate sigmoidally from 0-1"""
    n = min(max(n, 0), 1)
    if n == 0:
        return 0
    if n == 1:
        return 1

    return (1/(1+(eulers_number**(-8*n+2.8))))**2*1.012


class MenuOption:
    HEIGHT = 118
    SPACING = 16

    def __init__(self, title: str, color: pygame.Color, callback: Optional[Callable] = None):
        self.title = title
        self.callback = callback
        self.color = color
        self.hover_anim: float = 0

    def get_rect_for_render(self, y_value: int) -> pygame.Rect:
        wide_rect = pygame.Rect(0, y_value, Config.SCREEN_WIDTH, MenuOption.HEIGHT)
        wide_rect.move_ip(400 - 100*sigmoid_transform(self.hover_anim), 0)
        if wide_rect.collidepoint(pygame.mouse.get_pos()):
            self.hover_anim += 7/FRAMERATE
        else:
            self.hover_anim -= 1.6/FRAMERATE
        self.hover_anim = max(min(self.hover_anim, 1), 0)
        return wide_rect


class Menu:
    def __init__(self):
        self.menu_options: list[MenuOption] = [
            MenuOption("Play", pygame.Color(214, 247, 163)),
            MenuOption("Theatre", pygame.Color(196, 255, 178)),
            MenuOption("Config", pygame.Color(183, 227, 204)),
            MenuOption("Open Songs Folder", pygame.Color(125, 130, 184), lambda: print('todo do this')),
        ]

    def draw(self, screen: pygame.Surface):
        for index, option in enumerate(self.menu_options):
            draw_beveled_rectangle(screen, option.color, option.get_rect_for_render(index * (option.HEIGHT + option.SPACING) + 300))
