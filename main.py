from utils import *
from menu import Menu
from game import Game
from configpage import ConfigPage
from songselector import SongSelector
from os import startfile, getcwd
import webbrowser
import pygame


def main():

    # pygame and other boilerplate
    pygame.init()
    pygame.mixer.music.load("./assets/mainmenu.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(loops=-1, start=2)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(
        [Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT],
        pygame.FULLSCREEN | pygame.HWACCEL | pygame.HWSURFACE | pygame.SCALED,
        vsync=1
    )

    # the big guns
    menu = Menu()
    song_selector = SongSelector()
    config_page = ConfigPage()
    game = Game()

    # game loop
    running = True
    while running:
        screen.fill(Config.Colors.wall_color)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if song_selector.active:
                        song_selector.active = False
                        menu.active = True
                        if song_selector.selected_index+1:
                            pygame.mixer.music.load("./assets/mainmenu.mp3")
                            pygame.mixer.music.set_volume(Config.volume/100)
                            pygame.mixer.music.play(loops=-1, start=2)
                            song_selector.selected_index = -1
                        continue
                    if game.active:
                        game.active = False
                        song_selector.active = True
                        pygame.mixer.music.load("./assets/mainmenu.mp3")
                        pygame.mixer.music.set_volume(Config.volume/100)
                        pygame.mixer.music.play(loops=-1, start=2)
                        song_selector.selected_index = -1
                        continue
                    if config_page.active:
                        config_page.active = False
                        menu.active = True
                        continue
                    running = False

            # handle menu events
            option_id = menu.handle_event(event)
            if option_id:
                if option_id == "open-songs-folder":
                    startfile(join(getcwd(), "songs"))
                    continue
                if option_id == "contribute":
                    webbrowser.open("https://github.com/quasar098/midi-playground")
                    continue
                menu.active = False
                if option_id == "config":
                    config_page.active = True
                if option_id == "play":
                    song_selector.active = True
                if option_id == "quit":
                    running = False
                continue

            # handle song selector events
            song = song_selector.handle_event(event)
            if song:
                if isinstance(song, bool):
                    menu.active = True
                    if song_selector.selected_index+1:
                        pygame.mixer.music.load("./assets/mainmenu.mp3")
                        pygame.mixer.music.set_volume(Config.volume/100)
                        pygame.mixer.music.play(loops=-1, start=2)
                        song_selector.selected_index = -1
                    continue
                # starting song now
                Config.midi_file_name = song.midi_file_name
                Config.audio_file_name = song.audio_file_name
                game.active = True
                if game.start_song(screen):
                    game.active = False
                    song_selector.active = True
                    pygame.mixer.music.load("./assets/mainmenu.mp3")
                    pygame.mixer.music.set_volume(Config.volume/100)
                    pygame.mixer.music.play(loops=-1, start=2)

            # handle config page events
            if config_page.handle_event(event):
                config_page.active = False
                menu.active = True

            # handle game events
            if game.handle_event(event):
                game.active = False
                song_selector.active = True

        # draw stuff here
        game.draw(screen)
        song_selector.draw(screen)
        config_page.draw(screen)
        menu.draw(screen)

        pygame.display.flip()
        clock.tick(FRAMERATE)
    pygame.quit()


if __name__ == '__main__':
    main()
