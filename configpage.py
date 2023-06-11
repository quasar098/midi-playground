from utils import *
import pygame
from typing import Any


class ConfigOption:
    def __init__(self, attr):
        self.attr = attr

    def draw(self, screen: pygame.Surface, topleft: tuple[float, float]) -> tuple[float, float]:
        pass

    def get_next_pos(self, curr: tuple[float, float]) -> tuple[float, float]:
        pass

    def handle_event(self, topleft: tuple[float, float], event: pygame.event.Event) -> tuple[float, float]:
        pass


class ConfigOptionMultiselectInteger(ConfigOption):
    def __init__(self, attr: str, options: dict[Any]):
        super().__init__(attr)
        self.options = options
        fn = get_font("./assets/poppins-regular.ttf")
        self.rendered_options = [fn.render(f"{self.formatted_title}: {options[option]}", True, (0, 0, 0)) for option in options]

    @property
    def formatted_title(self):
        return " ".join(_.capitalize() for _ in self.attr.replace("_", ' ').split(" "))

    @property
    def selected_index(self):
        return getattr(Config, "camera_mode")

    @selected_index.setter
    def selected_index(self, val: int):
        setattr(Config, "camera_mode", val)

    # noinspection PyMethodMayBeStatic
    def rect(self, tl: tuple[float, float]):
        return pygame.Rect(tl[0], tl[1], 500, 80)

    @property
    def selected_surf(self):
        return self.rendered_options[self.selected_index]

    def get_next_pos(self, curr: tuple[float, float]) -> tuple[float, float]:
        return curr[0], curr[1]+100

    def handle_event(self, topleft: tuple[float, float], event: pygame.event.Event) -> tuple[float, float]:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect(topleft).collidepoint(pygame.mouse.get_pos()):
                    print("clicked")
        return self.get_next_pos(topleft)

    def draw(self, screen: pygame.Surface, topleft: tuple[float, float]) -> tuple[float, float]:
        sr = self.rect(topleft)
        pygame.draw.rect(screen, (0, 0, 0), sr, border_radius=8)
        pygame.draw.rect(screen, (220, 220, 220), sr.inflate(-8, -8), border_radius=2)
        screen.blit(self.selected_surf, self.selected_surf.get_rect(center=self.rect(topleft).center))

        return self.get_next_pos(topleft)


class ConfigPage:
    def __init__(self):
        self.active = False
        self.options: list[ConfigOption] = [
            ConfigOptionMultiselectInteger("camera_mode", options={0: "Center", 1: "Lazy", 2: "Smoothed (Default)", 3: "Predictive"})
        ]

    def handle_event(self, event: pygame.event.Event):
        if not self.active:
            return
        prev_pos = (100, 100)
        for option in self.options:
            prev_pos = option.handle_event(prev_pos, event)

    def draw(self, screen: pygame.Surface):
        if not self.active:
            return
        prev_pos = (100, 100)
        for option in self.options:
            prev_pos = option.draw(screen, prev_pos)
