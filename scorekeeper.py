from utils import *
import pygame


class Scorekeeper:
    def __init__(self):
        self.unhit_notes: list[float] = []
        self.score = 0
        self.latest_message: Optional[str] = None

    def penalize_misses(self, current_time: float):
        new = []
        for note in self.unhit_notes:
            t = current_time - note + Config.music_offset / 1000 - Config.start_playing_delay / 1000
            if t > 0.1:
                self.score -= 100
                self.latest_message = f"Score: {self.score}"
                continue
            new.append(note)
        self.unhit_notes = new

    def attempt_log(self, current_time: float):
        # negative closest means hit before, positive means hit after
        abs_closest = 100
        closest = 100
        to_remove = None
        for unhit in self.unhit_notes:
            t = current_time - unhit + Config.music_offset / 1000 - Config.start_playing_delay / 1000
            if abs(t) < abs_closest:
                abs_closest = int(abs(t)*100)/100
                closest = int(t*100)/100
                to_remove = unhit
        if closest > 0.1 or closest < -0.08:
            self.score -= 300
            self.latest_message = f"Score: {self.score}"
            return
        if to_remove is not None:
            self.unhit_notes.remove(to_remove)
        if closest > 0.04:
            self.score += 100
        elif closest > -0.02:
            self.score += 300
        elif closest > -0.04:
            self.score += 100
        else:
            self.score -= 100
        self.latest_message = f"Score: {self.score}"
