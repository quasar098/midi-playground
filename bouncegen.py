from shared import *
import pygame
from time import time as get_current_time
from typing import Union
import random
from sys import setrecursionlimit
setrecursionlimit(10000)  # increase if more notes


WIDTH, HEIGHT = 1920, 1080
CAMERA_SPEED = 500
SQUARE_SIZE = 50
PLATFORM_WIDTH_PERCENT = 10
GLOBAL_TIME_OFFSET = 1000
PARTICLE_SPEED = 10
WALL_COLOR = pygame.Color((60, 63, 65))
BG_COLOR = pygame.Color((214, 209, 205))
SQUARE_COLORS = [
    (224, 26, 79),
    (173, 247, 182),
    (249, 194, 46),
    (83, 179, 203)
]


class Particle:
    def __init__(self, pos: list[float], delta: list[float]):
        self.pos = pos.copy()
        self.size = random.randint(7, 14)
        self.delta = delta.copy()
        self.delta[0] += random.randint(-4, 4)/8
        self.delta[1] += random.randint(-4, 4)/8

    def age(self):
        self.size -= 15/FRAMERATE
        self.x += self.delta[0] * PARTICLE_SPEED
        self.y += self.delta[1] * PARTICLE_SPEED
        self.x = self.x * 1-(10/FRAMERATE)
        self.y = self.y * 1-(10/FRAMERATE)
        return self.size <= 0

    @property
    def x(self):
        return self.pos[0]
    
    @x.setter
    def x(self, val: float):
        self.pos[0] = val

    @property
    def y(self):
        return self.pos[1]

    @y.setter
    def y(self, val: float):
        self.pos[1] = val

    @property
    def rect(self):
        return pygame.Rect(self.x-self.size/2, self.y-self.size/2, *(2*[self.size]))


class Bounce:
    def __init__(self, sq_pos: list[int], sq_dir: list[int], time: float, bounce_dir: int):
        self.square_pos = sq_pos  # new square position
        self.square_dir = sq_dir  # new square direction
        self.bounce_dir = bounce_dir  # which way to continue (?), 0 = horiz, 1 = vert
        self.time = time  # time during bounce

    def get_collision_rect(self):
        sx, sy = self.square_pos
        if self.bounce_dir == 0:
            # bounce left or right wall
            if self.square_dir[0] == -1:
                # right wall
                return pygame.Rect(
                    sx+SQUARE_SIZE/2,
                    sy-10,
                    10,
                    20
                )
            elif self.square_dir[0] == 1:
                # left wall
                return pygame.Rect(
                    sx-10-SQUARE_SIZE/2,
                    sy-10,
                    10,
                    20
                )
        elif self.bounce_dir == 1:
            # bounce top or bottom wall
            if self.square_dir[1] == -1:
                # bottom wall
                return pygame.Rect(
                    sx-10,
                    sy+SQUARE_SIZE/2,
                    20,
                    10
                )
            elif self.square_dir[1] == 1:
                # top wall
                return pygame.Rect(
                    sx-10,
                    sy-10-SQUARE_SIZE/2,
                    20,
                    10
                )

    def copy(self) -> "Bounce":
        return Bounce(self.square_pos, self.square_dir, self.time, self.bounce_dir)

    def __repr__(self):
        return f"<Bounce(sp={self.square_pos}, sd={self.square_dir}, time={self.time}, bd={self.bounce_dir})"


class Square:
    def __init__(self, x: float = WIDTH/2, y: float = HEIGHT/2, dx: int = 1, dy: int = 1):
        self.pos: list[float, float] = [x, y]
        self.dir: list[int, int] = [dx, dy]
        self.last_bounce_time = -100
        self.speed = 500
        self.latest_bounce_direction = 0  # 0 = horiz, 1 = vert
        self.past_colors = []

    def register_past_color(self, col: tuple[int, int, int]):
        self.past_colors.insert(0, col)
        self.past_colors.insert(0, col)
        self.past_colors.insert(0, col)
        while len(self.past_colors) > SQUARE_SIZE*4/5:
            self.past_colors.pop()

    def get_surface(self, size: tuple[int, int]):
        ss = int(SQUARE_SIZE*4/5)
        surf = pygame.Surface((ss, ss))
        for index, col in enumerate(self.past_colors):
            y = index if self.dir_y != 1 else ss-1-index
            pygame.draw.line(surf, col, (0, y), (ss, y))
        return pygame.transform.scale(surf, size)

    def copy(self) -> "Square":
        new = Square(*self.pos, *self.dir)
        new.last_bounce_time = self.last_bounce_time
        new.latest_bounce_direction = self.latest_bounce_direction
        new.speed = self.speed
        return new

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]

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
        return pygame.Rect(self.x-SQUARE_SIZE/2, self.y-SQUARE_SIZE/2, *([SQUARE_SIZE]*2))

    def obey_bounce(self, bounce: Bounce):
        # planned bounces
        self.pos = bounce.square_pos
        self.dir = bounce.square_dir
        self.latest_bounce_direction = bounce.bounce_dir
        self.last_bounce_time = bounce.time
        return

    def reg_move(self):
        self.x += self.dir_x*self.speed/FRAMERATE
        self.y += self.dir_y*self.speed/FRAMERATE


class Camera:
    def __init__(self, x: int = WIDTH/2, y: int = HEIGHT/2):
        self.x = x
        self.y = y
        # ?x, ?y are variables for misc things
        self.ax = 0
        self.ay = 0
        self.bx = 0
        self.by = 0
        self.locked_on_square = True
        self.lock_type: CameraFollow = CameraFollow(2)

    @property
    def pos(self):
        return self.x, self.y

    @pos.setter
    def pos(self, val: Union[tuple[int, int], list[int]]):
        self.x, self.y = val

    def offset(self, pos_or_rect: Union[pygame.Rect, tuple[int, int]]) -> Union[pygame.Rect, list[int]]:
        if isinstance(pos_or_rect, pygame.Rect):
            return pos_or_rect.move(-self.x, -self.y)
        else:
            return [pos_or_rect[0]-self.x, pos_or_rect[1]-self.y]

    def follow(self, square: Square):
        if self.lock_type == CameraFollow.Centre:
            self.pos = [square.x - WIDTH/2, square.y - HEIGHT/2]
        if self.lock_type == CameraFollow.Lazy:
            lazy_follow_distance = 250
            while square.x - WIDTH + lazy_follow_distance > self.x:
                self.x += 1
            while square.y - HEIGHT + lazy_follow_distance > self.y:
                self.y += 1
            while square.x - lazy_follow_distance < self.x:
                self.x -= 1
            while square.y - lazy_follow_distance < self.y:
                self.y -= 1
        if self.lock_type == CameraFollow.Smoothed:
            self.x = (square.x - WIDTH/2)*3/FRAMERATE + self.x-3*self.x/FRAMERATE
            self.y = (square.y - HEIGHT/2)*3/FRAMERATE + self.y-3*self.y/FRAMERATE
        if self.lock_type == CameraFollow.Predictive:
            self.ax = (square.x - WIDTH/2)*3/FRAMERATE + self.ax-3*self.ax/FRAMERATE
            self.ay = (square.y - HEIGHT/2)*3/FRAMERATE + self.ay-3*self.ay/FRAMERATE
            damping = 1
            self.bx = square.x - damping*(self.ax - square.x) - WIDTH/2 - WIDTH/2*damping
            self.by = square.y - damping*(self.ay - square.y) - HEIGHT/2 - HEIGHT/2*damping
            self.x = self.x*(1-3/FRAMERATE)+self.bx*3/FRAMERATE
            self.y = self.y*(1-3/FRAMERATE)+self.by*3/FRAMERATE


class World:
    """it's a cruel world out there"""

    def __init__(self):
        self.future_bounces: list[Bounce] = []
        self.past_bounces: list[Bounce] = []
        self.start_time = 0
        self.time = 0
        self.bounce_min_space = 0.05
        self.max_notes = None
        self.rectangles: list[pygame.Rect] = []
        self.particles: list[Particle] = []
        self.music_offset = 0
        self.percent_chance_dir_change = 30
        self.backtrack_amount = 20
        self.backtrack_chance = 0.03

    def update_time(self) -> None:
        self.time = get_current_time() - self.start_time

    def next_bounce(self):
        self.past_bounces.append(self.future_bounces.pop(0))
        return self.past_bounces[-1]

    def add_particles(self, sp: list[float], sd: list[float]):
        for _ in range(10):
            new = Particle([sp[0]+random.randint(-10, 10), sp[1]+random.randint(-10, 10)], sd)
            self.particles.append(new)

    def handle_bouncing(self, square: Square):
        if len(self.future_bounces):
            if (self.time * 1000 + self.music_offset)/1000 > self.future_bounces[0].time:
                current_bounce = self.next_bounce()
                before = square.dir.copy()
                square.obey_bounce(current_bounce)
                changed = square.dir.copy()
                for _ in range(2):
                    if before[_] == changed[_]:
                        changed[_] = 0
                    else:
                        changed[_] = -changed[_]
                self.add_particles(square.pos, changed)

                # stop square at end
                if len(self.future_bounces) == 0:
                    square.dir = [0, 0]
                    square.pos = current_bounce.square_pos

    def gen_future_bounces(self, _start_square: Square, _start_notes: list[tuple[int, int, int]]):
        """Recursive solution is necessary"""
        total_notes = len(_start_notes)
        max_percent = 0
        path = []
        safe_areas = []
        force_return = 0

        def recurs(
                square,
                notes: list[float],
                bounces_so_far: list[Bounce] = None,
                prev_index_priority=None,
                t: float = 0,
                depth: int = 0
        ) -> Union[list[Bounce], bool]:
            nonlocal force_return, max_percent
            if prev_index_priority is None:
                prev_index_priority = [0, 1]
            if bounces_so_far is None:
                bounces_so_far = []
            gone_through_percent = (total_notes-len(notes)) * 100 // total_notes
            while gone_through_percent > max_percent:
                max_percent += 1
                print(f"Map {max_percent}% generated")

            all_bounce_rects = [_bounc.get_collision_rect() for _bounc in bounces_so_far]
            if len(notes) == 0:
                return bounces_so_far
            # print(depth * 100 // total_notes)
            path_segment_start = len(path)
            start_rect = square.rect.copy()
            while True:
                t += 1/FRAMERATE
                square.reg_move()
                path.append(square.rect)
                if t > notes[0]:
                    # no collision (we good)
                    bounce_indexes = prev_index_priority

                    # randomly change direction every X% of the time
                    if random.random() * 100 < self.percent_chance_dir_change:
                        bounce_indexes = list(bounce_indexes.__reversed__())

                    # add safe area
                    safe_areas.append(start_rect.union(square.rect))

                    for direction_to_bounce in bounce_indexes:
                        square.dir[direction_to_bounce] *= -1
                        bounces_so_far.append(Bounce(square.pos, square.dir, t, direction_to_bounce))

                        toextend = recurs(
                            square=square.copy(),
                            notes=notes[1:],
                            bounces_so_far=[_b.copy() for _b in bounces_so_far],
                            t=t,
                            prev_index_priority=bounce_indexes.copy().copy(),
                            depth=depth+1
                        )

                        if toextend:
                            return toextend
                        else:
                            bounces_so_far = bounces_so_far[:-1]
                            square.dir[direction_to_bounce] *= -1

                            # instead of trying other path, just exit a bit back to try another
                            if force_return:
                                force_return -= 1
                                while len(path) != path_segment_start:
                                    path.pop()
                                return False

                            continue
                    while len(path) != path_segment_start:
                        path.pop()
                    return False
                othercheck = False
                if len(bounces_so_far):
                    othercheck = bounces_so_far[-1].get_collision_rect().collidelist(path[:-10])+1
                if square.rect.collidelist(all_bounce_rects) != -1 or othercheck:
                    if depth > 300:
                        if random.random() < self.backtrack_chance:
                            print(f"Backtracking at {max_percent}%")
                            max_percent -= (self.backtrack_amount * 100 // total_notes) + 1
                            force_return = self.backtrack_amount

                    while len(path) != path_segment_start:
                        path.pop()
                    return False

        _start_notes = _start_notes[:self.max_notes] if self.max_notes is not None else _start_notes[1:]

        self.future_bounces = recurs(
            square=_start_square.copy(),
            notes=remove_too_close_values(
                [_sn[1] for _sn in _start_notes],
                threshold=self.bounce_min_space
            )
        )
        assert self.future_bounces is not False, "recurs function failed"
        assert len(self.future_bounces) != 0, "no recurs list"

        # eliminate unused safe areas
        print("Eliminating unused safe rectangles")
        safe_areas: list[pygame.Rect]
        while True:
            new = []
            before_safe_count = len(safe_areas)
            for safe1 in safe_areas:
                for safe2 in safe_areas:
                    if safe2 == safe1:
                        continue
                    if safe2.contains(safe1):
                        break
                else:
                    new.append(safe1)
            safe_areas = new.copy()
            after_safe_count = len(safe_areas)
            if after_safe_count == before_safe_count:
                break

        self.rectangles = [_fb.get_collision_rect() for _fb in self.future_bounces]
        return safe_areas


def debug_rect(rect: pygame.Rect):
    """for debugging only"""
    print(f"\\operatorname\x7Bpolygon\x7D({rect.topleft}, {rect.topright}, {rect.bottomright}, {rect.bottomleft})")


def mp(p_, o_):
    """Move a position by offsetting it"""
    return p_[0]+o_[0], p_[1]+o_[1]


def remove_too_close_values(lst: list[float], threshold=0.1) -> list[float]:
    """Assumes the list is sorted"""
    new = []
    before = None
    for _ in lst:
        if before is None:
            before = _
            new.append(_)
            continue
        if before+threshold > _:
            continue
        before = _
        new.append(_)
    return new


def do_the_things(settings=None) -> None:
    """Example of bad code"""

    # settings
    if settings is None:
        settings = {}
    midi_file_name = settings.get("midi_file_name", None)
    assert midi_file_name is not None, "Midi file name is none (try inputting it?)"
    audio_file = settings.get("audio_file", midi_file_name)
    if audio_file is None:
        audio_file = midi_file_name
    camera_mode = settings.get("camera_mode", 2)
    max_notes = settings.get("max_notes", None)
    bounce_min_space = settings.get("bounce_min_space", 0.05)
    sq_speed = settings.get("sq_speed", 500)
    volume = settings.get("volume", 50)
    music_offset = settings.get("music_offset", 300)
    percent_chance_dir_change = settings.get("percent_chance_dir_change", 30)
    last_bounce_offset = settings.get("last_bounce_offset", 1)
    backtrack_chance = settings.get("backtrack_chance", 0.03)
    backtrack_amount = settings.get("backtrack_amount", 20)

    # load notes
    _, notes = read_midi_file(midi_file_name)
    notes = [(note[0], note[1], note[2]) for note in notes]
    if len(notes):
        notes.append((notes[-1][0], notes[-1][1]+last_bounce_offset, notes[-1][2]))

    # pygame stuff
    music_has_played = False
    offset_happened = False
    pygame.init()
    pygame.display.set_caption("bouncing squares")
    pygame.mixer.init()

    font = pygame.font.SysFont("Arial", 30)
    camera_ctrl_text = font.render("Manual Camera Control Activated", True, (0, 255, 0))

    pygame.mouse.set_visible(False)
    pygame.mixer.music.load(audio_file)

    # the big guns
    square = Square()
    square.speed = sq_speed
    camera = Camera()
    camera.lock_type = CameraFollow(camera_mode)
    world = World()
    world.backtrack_chance = backtrack_chance
    world.backtrack_amount = backtrack_amount
    world.max_notes = max_notes
    safe_areas: list[pygame.Rect] = world.gen_future_bounces(square, notes)
    world.start_time = get_current_time()
    world.bounce_min_space = bounce_min_space
    pygame.mixer.music.set_volume(volume/100)
    world.music_offset = music_offset
    world.percent_chance_dir_change = percent_chance_dir_change

    # preload square
    if len(world.future_bounces):
        square.pos = world.future_bounces[0].square_pos
        square.dir = [0, 0]  # freeze square

    screen = pygame.display.set_mode(
        [WIDTH, HEIGHT],
        pygame.FULLSCREEN | pygame.HWACCEL | pygame.HWSURFACE | pygame.SCALED,
        vsync=1
    )

    screen_rect = screen.get_rect()
    clock = pygame.time.Clock()

    # game loop
    running = True
    while running:
        if not music_has_played:
            if not offset_happened:
                for bnc_change in world.future_bounces:
                    bnc_change.time += GLOBAL_TIME_OFFSET/1000
            offset_happened = True
            if world.time > GLOBAL_TIME_OFFSET/1000:
                music_has_played = True
                song_load_before = get_current_time()
                pygame.mixer.music.play()
                for bnc_change in world.future_bounces:
                    bnc_change.time += (get_current_time()-song_load_before)/1000

        screen.fill(WALL_COLOR)

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mouse.set_visible(True)
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mouse.set_visible(True)
                    running = False
                if event.key == pygame.K_TAB:
                    camera.locked_on_square = not camera.locked_on_square

        # set world time
        world.update_time()

        # move camera (only works if not locked on square)
        if not camera.locked_on_square:
            keys = pygame.key.get_pressed()
            shift_mod = (keys[pygame.K_LSHIFT] | keys[pygame.K_RSHIFT]) + 1
            camera.x += (keys[pygame.K_d] - keys[pygame.K_a])*CAMERA_SPEED*shift_mod/FRAMERATE
            camera.y += (keys[pygame.K_s] - keys[pygame.K_w])*CAMERA_SPEED*shift_mod/FRAMERATE

        # handle square bounces
        world.handle_bouncing(square)

        # move square
        square.reg_move()

        # square in center of camera if locked
        if camera.locked_on_square:
            camera.follow(square)

        # bounce anim
        sqrect = camera.offset(square.rect)
        if (world.time - 0.25) + music_offset / 1000 < square.last_bounce_time:
            lerp = abs((world.time - 0.25 + music_offset / 1000) - square.last_bounce_time) * 5
            lerp = lerp ** 2  # square it for better-looking interpolation
            if square.latest_bounce_direction:
                sqrect.inflate_ip((lerp * 5, -10 * lerp))
            else:
                sqrect.inflate_ip((-10 * lerp, lerp * 5))

        total_rects = 0

        # safe areas
        for safe_area in safe_areas:
            offsetted = camera.offset(safe_area)
            if offsetted.colliderect(screen_rect):
                total_rects += 1
                pygame.draw.rect(screen, BG_COLOR, offsetted)

        # draw pegs
        for bounce in world.rectangles:
            offsetted = camera.offset(bounce)
            if offsetted.colliderect(screen_rect):
                total_rects += 1
                pygame.draw.rect(screen, WALL_COLOR, offsetted)

        # particles
        for particle in world.particles:
            pygame.draw.rect(screen, BG_COLOR, camera.offset(particle.rect))
        for remove_particle in [particle for particle in world.particles if particle.age()]:
            world.particles.remove(remove_particle)

        # draw square outline
        pygame.draw.rect(screen, (0, 0, 0), sqrect)
        square_color_index = round((square.dir_x + 1)/2 + square.dir_y + 1)
        square.register_past_color(SQUARE_COLORS[square_color_index])
        sq_surf = square.get_surface(tuple(sqrect.inflate(-int(SQUARE_SIZE/5), -int(SQUARE_SIZE/5))[2:]))
        screen.blit(sq_surf, sq_surf.get_rect(center=sqrect.center))

        if not camera.locked_on_square:
            screen.blit(camera_ctrl_text, (10, 10))

        pygame.display.flip()
        clock.tick(FRAMERATE)

    pygame.quit()
