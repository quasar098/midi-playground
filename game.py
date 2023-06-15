from utils import *
import pygame
from world import World
import random
from camera import Camera
from particle import Particle


class Game:
    def __init__(self):
        self.active = False
        self.notes = []
        self.camera = Camera()
        self.world = World()
        self.safe_areas: list[pygame.Rect] = []
        self.camera_ctrl_text = get_font("./assets/poppins-regular.ttf", 24).render("Manual Camera Control Activated", True, (0, 255, 0))
        self.music_has_played = False
        self.offset_happened = False
        self.loading_text = get_font("./assets/poppins-regular.ttf", 24).render("Loading...", True, (255, 255, 255))

    def start_song(self, screen: pygame.Surface, song_path: str = None):
        random.seed(Config.seed)
        # load song and notes
        if song_path is None:
            song_path = join("songs", Config.midi_file_name)

        notes = read_midi_file(song_path)
        notes = [(note[0], note[1], note[2]) for note in notes]
        self.notes = notes

        # other settings

        self.world = World()
        self.music_has_played = False
        self.offset_happened = False
        self.camera.lock_type = CameraFollow(Config.camera_mode)
        screen.fill(get_colors()["background"])
        pygame.display.flip()

        def update_loading_screen(pdone: int):
            screen.fill(get_colors()["background"], pygame.Rect(0, 0, Config.SCREEN_WIDTH, 100))
            message = f"{pdone}% done loading" if pdone != 100 else "Removing duplicate rectangles"
            if pdone < 70:
                if random.randint(1, 3) == 1:
                    return
            if pdone < 40:
                if random.randint(1, 9) != 1:
                    return
            screen.blit(get_font("./assets/poppins-regular.ttf", 60).render(message, True, get_colors()["hallway"]), (10, 10))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return True
            pygame.display.flip()

        try:
            self.safe_areas = self.world.gen_future_bounces(self.notes, update_loading_screen)
        except UserCancelsLoading:
            return True
        self.world.start_time = get_current_time()
        self.world.square.dir = [0, 0]
        self.world.square.pos = self.world.future_bounces[0].square_pos

    def draw(self, screen: pygame.Surface):
        self.world.scorekeeper.penalize_misses(self.world.time)

        if not self.active:
            return

        if not self.music_has_played:
            if not self.offset_happened:
                for bnc_change in self.world.future_bounces:
                    bnc_change.time += Config.start_playing_delay / 1000
            self.offset_happened = True
            if self.world.time > Config.start_playing_delay/1000:
                self.music_has_played = True
                song_load_before = get_current_time()
                pygame.mixer.music.play()
                for bnc_change in self.world.future_bounces:
                    bnc_change.time += (get_current_time()-song_load_before)/1000

        screen_rect = screen.get_rect()

        # set world time
        self.world.update_time()

        # move camera (only works if not locked on square)
        self.camera.attempt_movement()

        # handle square bounces
        self.world.handle_bouncing(self.world.square)

        # move square
        self.world.square.reg_move()

        # square in center of camera if locked
        if self.camera.locked_on_square:
            self.camera.follow(self.world.square)

        # bounce anim
        sqrect = self.camera.offset(self.world.square.rect)
        if (self.world.time - 0.25) + Config.music_offset / 1000 < self.world.square.last_bounce_time:
            lerp = abs((self.world.time - 0.25 + Config.music_offset / 1000) - self.world.square.last_bounce_time) * 5
            lerp = lerp ** 2  # square it for better-looking interpolation
            if self.world.square.latest_bounce_direction:
                sqrect.inflate_ip((lerp * 5, -10 * lerp))
            else:
                sqrect.inflate_ip((-10 * lerp, lerp * 5))

        # safe areas
        total_rects = 0
        for safe_area in self.safe_areas:
            offsetted = self.camera.offset(safe_area)
            if screen_rect.colliderect(offsetted):
                total_rects += 1
                pygame.draw.rect(screen, get_colors()["hallway"], offsetted)

        # draw pegs
        for bounce in self.world.rectangles:
            offsetted = self.camera.offset(bounce)
            if offsetted.colliderect(screen_rect):
                total_rects += 1
                pygame.draw.rect(screen, get_colors()["background"], offsetted)

        # particles
        for particle in self.world.particles:
            pygame.draw.rect(screen, get_colors()["hallway"], self.camera.offset(particle.rect))
        for remove_particle in [particle for particle in self.world.particles if particle.age()]:
            self.world.particles.remove(remove_particle)

        mimic = get_font("./assets/poppins-regular.ttf", 24).render(self.world.scorekeeper.latest_message, True, (255, 255, 255))
        screen.blit(mimic, (100, 100))

        # draw square
        self.world.square.draw(screen, sqrect)

        if not self.camera.locked_on_square:
            screen.blit(self.camera_ctrl_text, (10, 10))

    def handle_event(self, event: pygame.event.Event):
        if not self.active:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                for rect in self.safe_areas:
                    debug_rect(rect)
            if event.key == pygame.K_ESCAPE:
                return True
            if event.key == pygame.K_TAB:
                self.camera.locked_on_square = not self.camera.locked_on_square
            if self.camera.locked_on_square:
                if 97+26 > event.key >= 97 or event.key == pygame.K_SPACE:  # press a to z key
                    self.world.handle_keypress()
