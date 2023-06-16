import pygame
from utils import *
from bounce import Bounce


class Square:
    def __init__(self, x: float = 0, y: float = 0, dx: int = 1, dy: int = 1):
        self.pos: list[float] = [x, y]
        self.dir: list[int] = [dx, dy]
        self.last_bounce_time = -100
        self.latest_bounce_direction = 0  # 0 = horiz, 1 = vert
        self.past_colors = []
        self.died = False

    def register_past_color(self, col: tuple[int, int, int]):
        for _ in range(max(Config.square_swipe_anim_speed, 1)):
            self.past_colors.insert(0, col)
        while len(self.past_colors) > Config.SQUARE_SIZE*4/5:
            self.past_colors.pop()

    def get_surface(self, size: tuple[int, int]):
        ss = int(Config.SQUARE_SIZE*4/5)
        surf = pygame.Surface((ss, ss))
        for index, col in enumerate(self.past_colors):
            y = index if self.dir_y != 1 else ss-1-index
            pygame.draw.line(surf, col, (0, y), (ss, y))
        return pygame.transform.scale(surf, size)

    def copy(self) -> "Square":
        new = Square(*self.pos, *self.dir)
        new.last_bounce_time = self.last_bounce_time
        new.latest_bounce_direction = self.latest_bounce_direction
        return new

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]

    def title_screen_physics(self, bounding: pygame.Rect):
        self.reg_move()
        r = self.rect
        if r.right > bounding.right:
            self.dir[0] = -1
            self.latest_bounce_direction = 0
        elif r.left < bounding.left:
            self.dir[0] = 1
            self.latest_bounce_direction = 0
        elif r.bottom > bounding.bottom:
            self.dir[1] = -1
            self.latest_bounce_direction = 1
        elif r.top < bounding.top:
            self.dir[1] = 1
            self.latest_bounce_direction = 1
        else:
            return False
        self.last_bounce_time = get_current_time()
        return True

    def draw(self, screen: pygame.Surface, sqrect: pygame.Rect):
        if self.died:
            return
        pygame.draw.rect(screen, (0, 0, 0), sqrect)
        square_color_index = round((self.dir_x + 1)/2 + self.dir_y + 1)
        self.register_past_color(get_colors()["square"][square_color_index % len(get_colors()["square"])])
        sq_surf = self.get_surface(tuple(sqrect.inflate(-int(Config.SQUARE_SIZE/5), -int(Config.SQUARE_SIZE/5))[2:]))
        screen.blit(sq_surf, sq_surf.get_rect(center=sqrect.center))

    @x.setter
    def x(self, val: int):
        self.pos[0] = val

    @y.setter
    def y(self, val: int):
        self.pos[1] = val

    @property
    def dir_x(self):
        return self.dir[0]

    @property
    def dir_y(self):
        return self.dir[1]

    @property
    def rect(self):
        return pygame.Rect(self.x-Config.SQUARE_SIZE/2, self.y-Config.SQUARE_SIZE/2, *([Config.SQUARE_SIZE]*2))

    def obey_bounce(self, bounce: Bounce):
        # planned bounces
        self.pos = bounce.square_pos
        self.dir = bounce.square_dir
        self.latest_bounce_direction = bounce.bounce_dir
        self.last_bounce_time = bounce.time
        return

    def reg_move(self):
        self.x += self.dir_x*Config.square_speed/FRAMERATE
        self.y += self.dir_y*Config.square_speed/FRAMERATE
