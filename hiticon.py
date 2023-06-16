from utils import *
import pygame


class HitLevel(Enum):
    early = 0
    good = 1
    perfect = 2
    late = 3
    miss = 4


class HitIcon:
    surfaces: dict[HitLevel, pygame.Surface] = {}

    def __init__(self, lvl: HitLevel, pos: Union[tuple[int, int], list[int]]):
        if len(HitIcon.surfaces) == 0:
            for level in HitLevel:
                HitIcon.surfaces[level] = pygame.image.load(f"./assets/{level.name}.png").convert_alpha()

        self.pos = pos
        self.lvl = lvl
        self.age_left = 500
        self.surf = HitIcon.surfaces[lvl].copy()

    def draw(self, screen: pygame.Surface, camera):
        self.age_left -= 500/FRAMERATE
        self.surf.set_alpha(int(max(min(self.age_left, 255), 0)))
        screen.blit(self.surf, camera.offset(self.surf.get_rect(center=self.pos)))
        return self.age_left <= 0
