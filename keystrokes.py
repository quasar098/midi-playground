from utils import *
import pygame


class Keystrokes:
    def __init__(self):
        self.keys: list[str] = []
        self.key_surfaces: dict[str, pygame.Surface] = {}
        self.chars = "abcdefghijklmnopqrstuvwxyz"
        for possible_to_hit in self.chars:
            self.key_surfaces[possible_to_hit] = get_font("./assets/poppins-regular.ttf", 36).render(
                possible_to_hit, True, get_colors()["background"]
            )

    def draw(self, screen: pygame.Surface):
        default_rect = pygame.Rect(10, Config.SCREEN_HEIGHT-60, 50, 50)
        for _ in range(97, 97+26):
            char = self.chars[_-97]
            if pygame.key.get_pressed()[_]:
                if char not in self.keys:
                    self.keys.append(char)
            else:
                if char in self.keys:
                    self.keys.remove(char)

        for key in self.keys:
            pygame.draw.rect(screen, (0, 0, 0), default_rect)
            pygame.draw.rect(screen, get_colors()["hallway"], default_rect.inflate(-2, -2))
            screen.blit(self.key_surfaces[key], self.key_surfaces[key].get_rect(center=default_rect.center))
            default_rect.x += 60
