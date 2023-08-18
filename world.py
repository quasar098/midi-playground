from utils import *
from bounce import Bounce
from particle import Particle
from square import Square
from time import time as get_current_time
from scorekeeper import Scorekeeper
import config
import random
import pygame


class World:
    """it's a cruel world out there"""

    def __init__(self):
        self.future_bounces: list[Bounce] = []
        self.past_bounces: list[Bounce] = []
        self.start_time = 0
        self.time = 0
        self.rectangles: list[pygame.Rect] = []
        self.particles: list[Particle] = []
        self.timestamps = []
        self.square = Square()
        
        self.scorekeeper = Scorekeeper(self, config.is_botplay())

    def update_time(self) -> None:
        self.time = get_current_time() - self.start_time

    def next_bounce(self) -> Bounce:
        self.past_bounces.append(self.future_bounces.pop(0))
        return self.past_bounces[-1]

    def add_particles(self, sp: list[float], sd: list[float]):
        for _ in range(Config.particle_amount):
            new = Particle([sp[0]+random.randint(-10, 10), sp[1]+random.randint(-10, 10)], sd)
            self.particles.append(new)

    def handle_bouncing(self, square: Square):
        if len(self.future_bounces):
            if (self.time * 1000 + Config.music_offset)/1000 > self.future_bounces[0].time:
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

    def handle_keypress(self, time_from_start, misses):
        return self.scorekeeper.do_keypress(time_from_start, misses)

    def gen_future_bounces(self, _start_notes: list[tuple[int, int, int]], percent_update_callback):
        """Recursive solution is necessary"""
        total_notes = len(_start_notes)
        max_percent = 0
        path = []
        safe_areas = []
        force_return = 0

        def recurs(
                square: Square,
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
                if percent_update_callback(f"{max_percent}% done generating map"):
                    raise UserCancelsLoadingError()

            all_bounce_rects = [_bounc.get_collision_rect() for _bounc in bounces_so_far]
            if len(notes) == 0:
                return bounces_so_far
            # print(depth * 100 // total_notes)
            path_segment_start = len(path)
            start_rect = square.rect.copy()
            while True:
                t += 1/FRAMERATE
                square.reg_move(False)
                path.append(square.rect)
                if t > notes[0]:
                    # no collision (we good)
                    bounce_indexes = prev_index_priority

                    # randomly change direction every X% of the time
                    if random.random() * 100 < Config.direction_change_chance:
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
                            prev_index_priority=bounce_indexes.copy(),
                            depth=depth+1
                        )

                        if toextend:
                            return toextend
                        else:
                            bounces_so_far = bounces_so_far[:-1]
                            square.dir[direction_to_bounce] *= -1

                            # instead of trying other path from here, just exit a bit back to try another from previous
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
                    if depth > 200:
                        if random.random() < Config.backtrack_chance:
                            max_percent -= (Config.backtrack_amount * 100 // total_notes) + 1
                            force_return = Config.backtrack_amount

                    while len(path) != path_segment_start:
                        path.pop()
                    return False

        _start_notes = _start_notes[:Config.max_notes] if Config.max_notes is not None else _start_notes

        self.scorekeeper.unhit_notes = remove_too_close_values([_sn for _sn in _start_notes], Config.bounce_min_spacing)

        self.future_bounces = recurs(
            square=self.square.copy(),
            notes=remove_too_close_values(
                [_sn for _sn in _start_notes],
                threshold=Config.bounce_min_spacing
            )
        )

        if self.future_bounces is False:
            raise MapLoadingFailureError("The map failed to generate because of the recursion function. " +
                                         "If the midi has too many notes too close, it may not generate. Maybe try changing the square speed?")

        if len(self.future_bounces) == 0:
            raise MapLoadingFailureError("Map safearea list empty. Please report to the github under the issues tab")

        percent_update_callback("Removing overlapping safe areas")

        # eliminate fully overlapping safe areas
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
        safe_areas = safe_areas

        self.rectangles = [_fb.get_collision_rect() for _fb in self.future_bounces]
        return safe_areas
