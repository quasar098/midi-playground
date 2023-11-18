from utils import *
import pygame


class Keystrokes:
    def __init__(self):
        self.keys: list[str] = []
        self.key_surfaces: dict[str, pygame.Surface] = {}
        for ascii_keycode in range(97, 123):
            self.key_surfaces[ascii_keycode] = get_font("./assets/poppins-regular.ttf", 36).render(
                chr(ascii_keycode), True, (0, 0, 0)
            )
        self.keycodes = list(range(97, 123)) + list(range(1073741903, 1073741907))
        self.key_surfaces[pygame.K_LEFT] = pygame.image.load("./assets/keystrokeicons/left.png").convert_alpha()
        self.key_surfaces[pygame.K_RIGHT] = pygame.image.load("./assets/keystrokeicons/right.png").convert_alpha()
        self.key_surfaces[pygame.K_DOWN] = pygame.image.load("./assets/keystrokeicons/down.png").convert_alpha()
        self.key_surfaces[pygame.K_UP] = pygame.image.load("./assets/keystrokeicons/up.png").convert_alpha()
        self.key_surfaces["click"] = pygame.image.load("./assets/keystrokeicons/click.png").convert_alpha()

    def draw(self, screen: pygame.Surface):
        default_rect = pygame.Rect(10, Config.SCREEN_HEIGHT - 60, 50, 50)
        for keycode in self.keycodes:
            if pygame.key.get_pressed()[keycode]:
                if keycode not in self.keys:
                    self.keys.append(keycode)
            else:
                if keycode in self.keys:
                    self.keys.remove(keycode)
        if pygame.mouse.get_pressed()[0]:
            if "click" not in self.keys:
                self.keys.append("click")
        else:
            if "click" in self.keys:
                self.keys.remove("click")

        for key in self.keys:
            pygame.draw.rect(screen, (0, 0, 0), default_rect)
            pygame.draw.rect(screen, (230, 233, 236), default_rect.inflate(-2, -2))
            screen.blit(self.key_surfaces[key], self.key_surfaces[key].get_rect(center=default_rect.center))
            default_rect.x += 60
