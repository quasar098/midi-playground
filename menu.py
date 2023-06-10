import pygame
from utils import *
from math import sin, pi
from typing import Callable


def draw_beveled_rectangle(surf: pygame.Surface, color: pygame.Color, rect: pygame.Rect) -> None:
    """i think they're called bevels"""
    pygame.draw.rect(surf, color.lerp((0, 0, 0), 0.4), rect.inflate(7, 7), border_radius=4)
    pygame.draw.rect(surf, color, rect, border_radius=2)


def interpolate_fn(n):
    """Interpolate sigmoidally from 0-1"""
    n = min(max(n, 0), 1)

    return sin(pi*(n - 0.5))/2 + 0.5


class MenuOption:
    HEIGHT = 118
    SPACING = 16

    def __init__(self, title: str, color: pygame.Color):
        font = get_font("./assets/poppins-regular.ttf", 72)
        self.title_surface = font.render(title, True, color.lerp((0, 0, 0), 0.7))
        self.brighter_title_surface = font.render(title, True, color.lerp((0, 0, 0), 0.2))
        self.id = title.replace(" ", '-').lower()
        self.color = color
        self.hover_anim: float = 0
        self.shadow_surface = pygame.Surface((self.brighter_title_surface.get_rect().width+100, MenuOption.HEIGHT), pygame.SRCALPHA)
        for _ in range(100):
            chopped = pygame.transform.chop(self.brighter_title_surface, pygame.Rect(0, 109-_, 0, 600))
            self.shadow_surface.blit(chopped, (_, _))

    def update_hover(self, y_value: int) -> None:
        wide_rect = pygame.Rect(0, y_value, Config.SCREEN_WIDTH, MenuOption.HEIGHT)
        wide_rect.move_ip(int(Config.SCREEN_WIDTH / 2) - 30 * interpolate_fn(self.hover_anim), 0)
        if wide_rect.collidepoint(pygame.mouse.get_pos()):
            self.hover_anim += 6 / FRAMERATE
        else:
            self.hover_anim -= 3 / FRAMERATE
        self.hover_anim = max(min(self.hover_anim, 1), 0)

    def get_rect(self, y_value: int) -> pygame.Rect:
        wide_rect = pygame.Rect(0, y_value, Config.SCREEN_WIDTH, MenuOption.HEIGHT)
        wide_rect.move_ip(int(Config.SCREEN_WIDTH / 2) - 60 * interpolate_fn(self.hover_anim), 0)
        return wide_rect


class Menu:
    def __init__(self):
        self.menu_options: list[MenuOption] = [
            MenuOption("Play", pygame.Color(214, 247, 163)),
            MenuOption("Config", pygame.Color(196, 255, 178)),
            MenuOption("Contribute", pygame.Color(183, 227, 204)),
            MenuOption("Open Songs Folder", pygame.Color(125, 130, 184)),
            MenuOption("Quit", pygame.Color(226, 109, 92))
        ]
        self.anim = 1
        self.supposed_to_be_shown = True

    def draw(self, screen: pygame.Surface):
        if self.supposed_to_be_shown:
            self.anim += 0.9/FRAMERATE
        else:
            self.anim -= 0.9/FRAMERATE
        self.anim = max(min(self.anim, 1), 0)
        if not self.anim:
            return
        for index, option in enumerate(self.menu_options):
            yv = index * (option.HEIGHT + option.SPACING) + 250
            if self.anim == 1:
                option.update_hover(yv)
            rect = option.get_rect(yv).move(interpolate_fn(1 - self.anim) * (int(Config.SCREEN_WIDTH / 2) + 300), 0)
            draw_beveled_rectangle(screen, option.color, rect)
            text_rect = option.title_surface.get_rect(midleft=rect.midleft)
            screen.blit(option.shadow_surface, text_rect.move(30, 0))
            screen.blit(option.title_surface, text_rect.move(30, 0))

    def handle_event(self, event: pygame.event.Event):
        if not self.anim:
            return
        for index, option in enumerate(self.menu_options):
            rect = option.get_rect(index * (option.HEIGHT + option.SPACING) + 250)
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and rect.collidepoint(
                    pygame.mouse.get_pos())) \
                    or (event.type == pygame.KEYDOWN and event.key == 49 + index):
                return option.id
