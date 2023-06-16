from utils import *
import pygame
from hiticon import HitIcon, HitLevel


class Scorekeeper:
    def __init__(self, world):
        self.world = world
        self.unhit_notes: list[float] = []
        self.hit_icons: list[HitIcon] = []
        self.hp = 100
        self.shown_hp = 0

    @property
    def life_bar_rect(self):
        return pygame.Rect((10, 10, int(Config.SCREEN_WIDTH/2-30), 30))

    def draw(self, screen: pygame.Surface, current_time: float, misses: int):
        self.hp = max(0, min(self.hp, 100))
        bg_color = get_colors().get("hp_bar_background", pygame.Color(34, 51, 59))
        border_color = get_colors().get("hp_bar_border", pygame.Color(10, 9, 8))
        fill_colors = get_colors().get("hp_bar_fill", (
            pygame.Color(156, 198, 155), pygame.Color(189, 228, 168), pygame.Color(215, 242, 186)
        ))
        screen.fill(border_color, self.life_bar_rect)
        inner = self.life_bar_rect.inflate(-8, -8)
        screen.fill(bg_color, inner)
        bar_width = inner.width / len(fill_colors)
        bar_hp_repr = 100 / len(fill_colors)
        leftover = self.shown_hp
        for _ in range(len(fill_colors)):
            chunk_rect = inner.copy()
            chunk_rect.x = inner.x + bar_width * _
            width = min(max(leftover, 0), int(bar_hp_repr)+1)/bar_hp_repr*bar_width
            leftover -= bar_hp_repr
            chunk_rect.width = width
            screen.fill(fill_colors[_], chunk_rect)
        if current_time > 0:
            self.hp -= Config.hp_drain_rate/FRAMERATE
        hp_show_damping = 10
        self.shown_hp = self.shown_hp*(1-hp_show_damping/FRAMERATE)+self.hp*(hp_show_damping/FRAMERATE)

        # remove unhit notes
        to_remove = []
        for timestamp in self.unhit_notes:
            if timestamp+0.12 < current_time:  # 120ms late is missed note
                self.hp -= 6
                self.hit_icons.append(HitIcon(HitLevel.miss, self.world.square.pos))
                to_remove.append(timestamp)
                misses += 1

        for t_remove in to_remove:
            self.unhit_notes.remove(t_remove)

        return misses

    def do_keypress(self, current_time: float, misses: int):
        # negative closest means hit before, positive means hit after
        for timestamp in self.unhit_notes:
            offset = current_time-timestamp
            if offset > 0.06:  # 60ms late - 120ms late
                self.hit_icons.append(HitIcon(HitLevel.late, self.world.square.pos.copy()))
                self.hp -= 1
                misses += 1


            elif offset > -0.06:  # 60ms early - 60ms late
                self.hit_icons.append(HitIcon(HitLevel.perfect, self.world.square.pos.copy()))
                self.hp += 3

            elif offset > -0.09:  # 60ms early - 90ms early
                self.hit_icons.append(HitIcon(HitLevel.good, self.world.square.pos.copy()))
                self.hp -= 1

            elif offset > -0.12:  # 90ms early - 120ms early
                self.hit_icons.append(HitIcon(HitLevel.early, self.world.square.pos.copy()))
                self.hp -= 2
                misses += 1

            else:
                return misses
            self.unhit_notes.remove(timestamp)
            return misses
    
    def should_hit(self, current_time: float, blacklist: list):
        # negative closest means hit before, positive means hit after
        for timestamp in self.unhit_notes:
            offset = current_time-timestamp
            if timestamp in blacklist: continue
            if offset > 0.06:  # 60ms late - 120ms late
                pass

            elif offset > -0.06:  # 60ms early - 60ms late
                blacklist.append(timestamp)
                return True, blacklist

            elif offset > -0.09:  # 60ms early - 90ms early
                pass

            elif offset > -0.12:  # 90ms early - 120ms early
                pass

            else:
                return False, blacklist
            
            return False, blacklist
