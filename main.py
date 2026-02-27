from utils import *
from menu import Menu
from game import Game
from configpage import ConfigPage
from songselector import SongSelector
from errorscreen import ErrorScreen
from discord_rpc import *
from os import getcwd
from platform import system as get_os
from config import save_to_file
import debuginfo
import webbrowser
import pygame
from array import array


def main():
    # patch to fix mouse on high dpi displays
    if "Windows" in get_os():
        from ctypes import windll
        windll.user32.SetProcessDPIAware()
    # patch to fix opengl error on mac
    elif "Darwin" in get_os():
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True)

    # pygame and other boilerplate
    n_frames = 0
    pygame.mixer.music.load("./assets/mainmenu.mp3")
    pygame.mixer.music.set_volume(Config.volume / 100)
    pygame.mixer.music.play(loops=-1, start=2)

    clock = pygame.time.Clock()

    flags = pygame.HWACCEL | pygame.HWSURFACE | pygame.OPENGL | pygame.DOUBLEBUF
    do_vsync = 1
    if "Linux" in get_os():
        do_vsync = 0  # otherwise error of "regular vsync for OpenGL not available" at least that's what i got under wsl
    # noinspection PyUnusedLocal
    if [Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT] == [pygame.display.Info().current_w,pygame.display.Info().current_h]:
        flags |= pygame.FULLSCREEN
    
    real_screen = pygame.display.set_mode(
        [Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT],
        flags,
        vsync=do_vsync
    )
    screen = pygame.Surface([Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT])

    # noinspection PyBroadException
    try:
        pygame.display.set_caption("Midi Playground")
        pygame.display.set_icon(pygame.image.load("./assets/icon.png").convert_alpha())
    except Exception as e:
        print(e)

    # moderngl stuff
    ctx = moderngl.create_context()
    Config.ctx = ctx

    quad_buffer = ctx.buffer(data=array('f', [
        # position, uv coords
        -1.0, 1.0, 0.0, 0.0,  # topleft
        1.0, 1.0, 1.0, 0.0,  # topright
        -1.0, -1.0, 0.0, 1.0,  # bottomleft
        1.0, -1.0, 1.0, 1.0  # bottomright
    ]))

    vert_shader = '''
    #version 330 core
    
    in vec2 vert;
    in vec2 texcoord;
    out vec2 uvs;
    
    void main() {
        uvs = texcoord;
        gl_Position = vec4(vert.x, vert.y, 0.0, 1.0);
    }
    '''

    with open(f"./assets/shaders/{Config.shader_file_name}") as shader_file:
        frag_shader = shader_file.read()

    glsl_program = ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
    render_object = ctx.vertex_array(glsl_program, [(quad_buffer, '2f 2f', 'vert', 'texcoord')])

    Config.glsl_program = glsl_program
    Config.render_object = render_object
    Config.screen = screen

    # the big guns
    menu = Menu()
    song_selector = SongSelector()
    config_page = ConfigPage()
    error_screen = ErrorScreen()
    game = Game()

    # game loop
    running = True
    while running:
        n_frames += 1
        # thanks to TheCodingCrafter for the implementation
        if Config.theme == "rainbow":
            to_set_as_rainbow = pygame.Color((0, 0, 0))
            to_set_as_rainbow2 = pygame.Color((0, 0, 0))
            to_set_as_rainbow.hsva = (((pygame.time.get_ticks() / 1000) * Config.rainbow_speed) % 360, 100, 75, 100)
            to_set_as_rainbow2.hsva = ((((pygame.time.get_ticks() / 1000) * Config.rainbow_speed) + 180) % 360, 100, 75, 100)
            get_colors()["background"] = to_set_as_rainbow
            get_colors()["hallway"] = to_set_as_rainbow2
            get_colors()["square"][0] = to_set_as_rainbow

        screen.fill(get_colors()["background"])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # artificial lag spike for debugging purposes
                if event.key == pygame.K_F12:
                    total = 0
                    for _ in range(10_000_000):
                        total += 1
                if event.key == pygame.K_F3:
                    print("Debug information copied to clipboard")
                    debuginfo.print_debug_info()
                if event.key == pygame.K_F2:
                    if game.active:
                        debuginfo.debug_rectangles(game.safe_areas)
                if event.key == pygame.K_ESCAPE:
                    if song_selector.active:
                        song_selector.active = False
                        menu.active = True
                        if song_selector.selected_index + 1:
                            pygame.mixer.music.load("./assets/mainmenu.mp3")
                            pygame.mixer.music.set_volume(Config.volume / 100)
                            pygame.mixer.music.play(loops=-1, start=2)
                            song_selector.selected_index = -1
                        continue
                    if game.active:
                        game.active = False
                        song_selector.active = True
                        pygame.mixer.music.load("./assets/mainmenu.mp3")
                        pygame.mixer.music.set_volume(Config.volume / 100)
                        pygame.mixer.music.play(loops=-1, start=2)
                        song_selector.selected_index = -1
                        continue
                    if config_page.active:
                        config_page.active = False
                        menu.active = True
                        continue
                    if error_screen.active:
                        error_screen.active = False
                        song_selector.active = True
                        continue
                    running = False

            # handle menu events
            option_id = menu.handle_event(event)
            if option_id:
                if option_id == "open-songs-folder":
                    open_file(join(getcwd(), "songs"))
                    continue
                if option_id == "contribute":
                    webbrowser.open("https://github.com/quasar098/midi-playground")
                    continue
                menu.active = False
                if option_id == "config":
                    config_page.active = True
                if option_id == "play":
                    song_selector.active = True
                    song_selector.reload_songs()
                if option_id == "quit":
                    running = False
                continue

            # handle song selector events
            song = song_selector.handle_event(event)
            if song:
                if isinstance(song, bool):
                    menu.active = True
                    if song_selector.selected_index + 1:
                        pygame.mixer.music.load("./assets/mainmenu.mp3")
                        pygame.mixer.music.set_volume(Config.volume / 100)
                        pygame.mixer.music.play(loops=-1, start=2)
                        song_selector.selected_index = -1
                    continue
                # starting song now
                Config.current_song = song
                game.active = True
                if msg := game.start_song(screen):
                    if isinstance(msg, str):
                        game.active = False
                        error_screen.active = True
                        error_screen.msg = msg
                    else:
                        game.active = False
                        song_selector.active = True
                    pygame.mixer.music.load("./assets/mainmenu.mp3")
                    pygame.mixer.music.set_volume(Config.volume / 100)
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
        game.draw(screen, n_frames)
        song_selector.draw(screen)
        config_page.draw(screen)
        menu.draw(screen, n_frames)
        error_screen.draw(screen)

        update_screen(screen, glsl_program, render_object)

        Config.dt = clock.tick(FRAMERATE) / 1000

    # setup discord rpc
    if Config.discord_rpc:
        startrpc()

    pygame.quit()
    save_to_file()


if __name__ == '__main__':
    main()
