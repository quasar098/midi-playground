from utils import *
from discord_rpc import setrpc
from os import listdir
from os.path import isfile, join
from zipfile import ZipFile
from typing import Any
from io import BytesIO
from json import loads
import pygame


class Song:
    def __init__(self, name: str, song_artist: str, mapper: str,
                 song_file: str, audio_file: str, version: int = -1, filepath: Optional[str] = None,
                 is_from_osu_file: bool = False):
        self.is_from_osu_file = is_from_osu_file
        self.song_file_name: str = song_file
        self.audio_file_name: str = audio_file if audio_file is not None else self.song_file_name
        self.mapper = mapper
        self.fp = filepath
        self.song_artist = song_artist
        self.name = name
        self.version = version  # metadata format version, not the map version
        self.music_offset = 0  # put integer that represents milliseconds, negative is music is before

        self.anim = 0
        col = pygame.Color(229, 97, 196)
        selected_col = pygame.Color(50, 203, 255)

        reset_rect = pygame.Rect((0, 0, int(Config.SCREEN_WIDTH / 2), SongSelector.ITEM_HEIGHT))

        self.surface: pygame.Surface = pygame.Surface((int(Config.SCREEN_WIDTH / 2), SongSelector.ITEM_HEIGHT), pygame.SRCALPHA)
        self.selected_surface: pygame.Surface = pygame.Surface((int(Config.SCREEN_WIDTH / 2), SongSelector.ITEM_HEIGHT), pygame.SRCALPHA)

        overlay_surf = pygame.Surface((int(Config.SCREEN_WIDTH / 2), SongSelector.ITEM_HEIGHT), pygame.SRCALPHA)

        pygame.draw.rect(self.surface, col.lerp((0, 0, 0), 0.4), reset_rect, border_radius=6)
        pygame.draw.rect(self.surface, col, reset_rect.inflate(-8, -8), border_radius=2)
        pygame.draw.rect(self.selected_surface, selected_col.lerp((0, 0, 0), 0.4), reset_rect, border_radius=6)
        pygame.draw.rect(self.selected_surface, selected_col, reset_rect.inflate(-8, -8), border_radius=2)

        title_surface: pygame.Surface = get_font(36).render(self.name, True, (0, 0, 6))
        overlay_surf.blit(title_surface, title_surface.get_rect(topright=overlay_surf.get_rect().topright).move(-20, 20))

        if not is_from_osu_file:
            details_surface: pygame.Surface = get_font(
                24).render(f"Song by {self.song_artist} | Mapped by {self.mapper}", True, (0, 0, 0))
        else:
            details_surface: pygame.Surface = get_font(24).render(f"WARNING: EXPERIMENTAL!!!", True, (0, 0, 0))
        overlay_surf.blit(details_surface, details_surface.get_rect(bottomright=overlay_surf.get_rect().bottomright).move(-20, -20))

        self.surface.blit(overlay_surf, (0, 0))
        self.selected_surface.blit(overlay_surf, (0, 0))

        self.before_hover = False

    def __repr__(self):
        return f"<Song({self.song_file_name}, audio={self.audio_file_name})>"


def song_from_osu_file(contents: str, songfilepath: str, zipfilepath: str) -> Song:
    audio_name = ""
    name = ""
    artist = ""
    mapper = ""

    for line in contents.splitlines(False):
        if line.startswith("AudioFilename: "):
            audio_name = line.removeprefix("AudioFilename: ")
        if line.startswith("Title:"):
            name = line.removeprefix("Title:").lstrip()
        if line.startswith("Artist:"):
            artist = line.removeprefix("Artist:").lstrip()
        if line.startswith("Creator:"):
            mapper = line.removeprefix("Creator:").lstrip()
        if line.startswith("Version:"):
            # janky asf but whatever
            mapper += f' | {line.removeprefix("Version:").lstrip()}'

    return Song(
        name=name, song_artist=artist, mapper=mapper,
        song_file=songfilepath, audio_file=audio_name,
        version=-2, filepath=zipfilepath, is_from_osu_file=True
    )


def make_songs_from_osz(fpath: str) -> list[Song]:
    songs = []
    with ZipFile(fpath) as zf:
        files = zf.filelist
        for fileinfo in files:
            if fileinfo.filename.endswith(".osu"):
                songs.append(song_from_osu_file(zf.read(fileinfo.filename).decode('utf-8'), fileinfo.filename, fpath))
    return songs


def make_song_from_zip(fpath: str) -> Song:
    with ZipFile(fpath) as zf:
        metadata_info = zf.getinfo("metadata.json")
        metadata: dict[str, Any] = loads(zf.read(metadata_info))
        if "name" not in metadata:
            raise InvalidSongError(f"No name in metadata of {fpath}")
        if "mapper" not in metadata:
            raise InvalidSongError(f"No mapper in metadata of {fpath}")
        if "audio_file" not in metadata:
            raise InvalidSongError(f"No audio_file in metadata of {fpath}")
        if "song_file" not in metadata:
            raise InvalidSongError(f"No song_file in metadata of {fpath}")
        if "version" not in metadata:
            raise InvalidSongError(f"No version in metadata of {fpath}")
        name = metadata.get("name")
        artist = metadata.get("artist", metadata.get("author", "Unknown Artist"))
        mapper = metadata.get("mapper")
        audio_file = metadata.get("audio_file")
        song_file = metadata.get("song_file")
        version = metadata.get("version", -1)
        new_song = Song(name, audio_file=audio_file, song_file=song_file, song_artist=artist, mapper=mapper, version=version, filepath=fpath)
        if metadata.get("version") >= 2:
            new_song.music_offset = metadata.get("music_offset", 0)
        return new_song


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
        self.play_button_rect = pygame.Rect(Config.SCREEN_WIDTH - 300, 150, 250, 100)
        self.play_button_text = get_font(48).render(lang_key("play"), True, (0, 0, 0))
        self.back_button_rect = pygame.Rect(Config.SCREEN_WIDTH - 300, 20, 250, 150 - 40)
        self.back_button_text = get_font(48).render(lang_key("back"), True, (0, 0, 0))

    def reload_songs(self):
        self.songs = []
        for song_name in reversed(listdir("songs")):
            path = join("songs", song_name)
            if isfile(path):
                if path.lower().endswith(".zip") or path.lower().endswith(".midiplayground"):
                    self.songs.append(make_song_from_zip(path))
                if path.lower().endswith(".osz"):
                    self.songs.extend(make_songs_from_osz(path))

    def get_song_rect(self, index: int):
        rect = pygame.Rect(
            -200,
            index * (SongSelector.ITEM_HEIGHT + SongSelector.ITEM_SPACING) + 100 + self.scroll,
            int(Config.SCREEN_WIDTH / 2),
            SongSelector.ITEM_HEIGHT
        )
        rect.move_ip(-int(abs(Config.SCREEN_HEIGHT / 2 - rect.centery)) / 10, 0)
        rect.move_ip(interpolate_fn(self.songs[index].anim) * 60, 0)
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
                        if self.selected_index == index:
                            continue
                        play_sound("select.mp3")
                        with ZipFile(song.fp) as zf:
                            if song.audio_file_name.lower().endswith(".osu"):
                                pygame.mixer.music.load(zf.read(song.audio_file_name))
                            else:
                                with zf.open(song.audio_file_name) as f:
                                    pygame.mixer.music.load(BytesIO(f.read()))
                        pygame.mixer.music.set_volume(Config.volume/100)
                        pygame.mixer.music.play()
                        self.selected_index = index
                        setrpc(song.name)
                        return
                if self.play_button_rect.collidepoint(pygame.mouse.get_pos()):
                    if self.selected_index+1:
                        play_sound("select.mp3")
                        pygame.mixer.music.stop()
                        self.active = False
                        return self.songs[self.selected_index]

                if self.back_button_rect.collidepoint(pygame.mouse.get_pos()):
                    play_sound("select.mp3")
                    self.active = False
                    return True

    def draw(self, screen: pygame.Surface):
        if self.active:
            self.anim += 1.8 / FRAMERATE
        else:
            self.anim = 0

        self.anim = max(min(self.anim, 1), 0)
        if self.anim == 0:
            return

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

            # for anim
            if new_hover:
                if self.anim == 0:
                    self.anim = 0.3
                song.anim += 3.6 / FRAMERATE
            else:
                song.anim -= 3.6 / FRAMERATE

            song.anim = max(min(song.anim, 1), 0)

            if self.selected_index == index:
                # song.selected_surface.set_alpha(int(self.anim*255))
                screen.blit(song.selected_surface, rect.move(80, 0))
            else:
                # song.surface.set_alpha(int(self.anim*255))
                screen.blit(song.surface, rect)

        if self.scroll > 100:
            self.scroll_velocity -= self.scroll/2000

        self.back_button_rect.x = Config.SCREEN_WIDTH - 500 * interpolate_fn(self.anim) + 200
        back_button_hovered = self.back_button_rect.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(screen, pygame.Color(226, 109, 92).lerp((0, 0, 0), 0.4), self.back_button_rect, border_radius=8)
        pygame.draw.rect(
            screen, pygame.Color(226, 109, 92).lerp(
                (255, 255, 255), back_button_hovered * 0.1
            ), self.back_button_rect.inflate(-8, -8), border_radius=2
        )
        screen.blit(self.back_button_text, self.back_button_text.get_rect(center=self.back_button_rect.center))

        # only continue from here if something is selected
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
