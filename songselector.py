import pygame
from utils import *
from os import listdir


class Song:
    def __init__(self, midi_file: str, audio_file: Optional[str] = None):
        self.midi_file_name: str = midi_file
        self.audio_file_name: str = audio_file if audio_file is not None else self.midi_file_name
        text_surface: pygame.Surface = get_font("./assets/poppins-regular.ttf", 48).render(self.title, True, (0, 0, 6))
        col = pygame.Color(229, 97, 196)
        selected_col = pygame.Color(50, 203, 255)

        reset_rect = pygame.Rect((0, 0, int(Config.SCREEN_WIDTH / 2), SongSelector.ITEM_HEIGHT))

        self.surface: pygame.Surface = pygame.Surface((int(Config.SCREEN_WIDTH / 2), SongSelector.ITEM_HEIGHT), pygame.SRCALPHA)
        self.selected_surface: pygame.Surface = pygame.Surface((int(Config.SCREEN_WIDTH / 2), SongSelector.ITEM_HEIGHT), pygame.SRCALPHA)

        pygame.draw.rect(self.surface, col.lerp((0, 0, 0), 0.4), reset_rect, border_radius=6)
        pygame.draw.rect(self.surface, col, reset_rect.inflate(-8, -8), border_radius=2)
        pygame.draw.rect(self.selected_surface, selected_col.lerp((0, 0, 0), 0.4), reset_rect, border_radius=6)
        pygame.draw.rect(self.selected_surface, selected_col, reset_rect.inflate(-8, -8), border_radius=2)

        self.surface.blit(text_surface, text_surface.get_rect(midright=self.surface.get_rect().midright).move(-20, 0))
        self.selected_surface.blit(text_surface, text_surface.get_rect(midright=self.surface.get_rect().midright).move(-20, 0))

        self.before_hover = False

    @property
    def title(self):
        return " ".join(_.capitalize() for _ in self.audio_file_name[:-4].replace(" ", '-').split("-"))

    def __repr__(self):
        return f"<Song({self.midi_file_name}, audio={self.audio_file_name})>"


class SongSelector:
    ITEM_HEIGHT = 140
    ITEM_SPACING = 10
    SCROLL_SPEED = 20

    def __init__(self):
        self.songs: list[Song] = []
        self.reload_songs()
        self.scroll = 0
        self.scroll_velocity = 0
        self.active = False
        self.selected_index = -1
        self.anim = 0
        self.play_button_rect = pygame.Rect(Config.SCREEN_WIDTH - 300, 100, 250, 140)
        self.play_button_text = get_font("./assets/poppins-regular.ttf", 48).render("Play", True, (0, 0, 0))

    def reload_songs(self):
        self.songs = []
        for song_name in reversed(listdir("songs")):
            if song_name.endswith("-mainlines.mid"):
                for song in self.songs:
                    if song.audio_file_name[:-4] == song_name[:-14]:
                        song.midi_file_name = song_name
                continue
            self.songs.append(Song(song_name))

    def get_song_rect(self, index: int):
        rect = pygame.Rect(
            -100,
            index * (SongSelector.ITEM_HEIGHT + SongSelector.ITEM_SPACING) + 100 + self.scroll,
            int(Config.SCREEN_WIDTH / 2),
            SongSelector.ITEM_HEIGHT
        )
        rect.move_ip(-int(abs(Config.SCREEN_HEIGHT / 2 - rect.centery)) / 10, 0)
        return rect

    def handle_event(self, event: pygame.event.Event):
        if not self.active:
            return
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_velocity += event.y / 2
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for index, song in enumerate(self.songs):
                    rect = self.get_song_rect(index)
                    if rect.collidepoint(pygame.mouse.get_pos()):
                        play_sound("select.mp3")
                        pygame.mixer.music.load(join(".", "songs", song.audio_file_name))
                        pygame.mixer.music.set_volume(0.7)
                        pygame.mixer.music.play()
                        self.selected_index = index
                        return
                if self.play_button_rect.collidepoint(pygame.mouse.get_pos()):
                    if self.selected_index+1:
                        play_sound("select.mp3")
                        pygame.mixer.music.stop()
                        self.active = False
                        return self.songs[self.selected_index]

    def draw(self, screen: pygame.Surface):
        if self.active:
            self.anim += 1.8 / FRAMERATE
        else:
            self.anim = 0

        self.anim = max(min(self.anim, 1), 0)
        if self.anim == 0:
            return

        rect = None

        self.scroll_velocity = min(max(self.scroll_velocity, -1), 1) * (1 - 8 / FRAMERATE)
        keys = pygame.key.get_pressed()
        self.scroll += self.scroll_velocity * SongSelector.SCROLL_SPEED * (1 + keys[pygame.K_LSHIFT])

        for index, song in enumerate(self.songs):
            rect = self.get_song_rect(index)
            if not screen.get_rect().colliderect(rect):
                continue

            # for sounds
            new_hover = rect.collidepoint(pygame.mouse.get_pos())
            if new_hover and not song.before_hover:
                play_sound("wood.wav")
            song.before_hover = new_hover

            if self.selected_index == index:
                song.selected_surface.set_alpha(int(self.anim*255))
                screen.blit(song.selected_surface, rect)
            else:
                song.surface.set_alpha(int(self.anim*255))
                screen.blit(song.surface, rect)

        if self.scroll > 100:
            self.scroll_velocity -= self.scroll/2000

        if rect is not None:
            bottom = rect.bottom
            if self.scroll < - bottom - 200:
                self.scroll_velocity -= (self.scroll-bottom)/2000

        if not self.selected_index + 1:
            return

        # play button
        self.play_button_rect.x = Config.SCREEN_WIDTH - 500 * interpolate_fn(self.anim) + 200
        play_button_hovered = self.play_button_rect.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(screen, [int(_) for _ in (143 * 0.4, 247 * 0.4, 167 * 0.4)], self.play_button_rect,
                         border_radius=8)
        pygame.draw.rect(
            screen, pygame.Color(143, 247, 167).lerp(
                (255, 255, 255), play_button_hovered * 0.2
            ), self.play_button_rect.inflate(-8, -8), border_radius=2
        )
        screen.blit(self.play_button_text, self.play_button_text.get_rect(center=self.play_button_rect.center))
