from utils import *
import pygame
import pygame_gui as pgui
from io import StringIO
from os import listdir
import webbrowser


class ConfigPage:
    @property
    def made_with_pgui_rect(self):
        return self.made_with_pgui_surf.get_rect(bottomleft=(30, Config.SCREEN_HEIGHT - 30))

    def __init__(self):
        self.active = False
        self.made_with_pgui_surf = get_font(12).render(
            "Config page made with pygame_gui library", True, (255, 255, 255))

        pgui_theme = "{}"
        if lang_key("do-custom-pgui-font"):
            pgui_theme = f"""
            {{
                "label":
                {{
                    "font":
                    {{
                        "name": "hanyisongjian",
                        "regular_path": "./assets/fonts/{lang_key('font')}"
                    }}
                }}
            }}
            """

        # pygame_gui stuff
        self.ui_manager = pgui.UIManager((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT), StringIO(pgui_theme))
        self.back_button = pgui.elements.UIButton(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH - 120, 30, 90, 30)),
            text="Back",
            manager=self.ui_manager
        )

        # all attributes matching /s_.+/ are "s"ettings

        self.s_camera_mode = pgui.elements.UIDropDownMenu(
            ["Center", "Lazy", "Smoothed (Default)", "Predictive"],
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT // 10, 300, 30)),
            starting_option=["Center", "Lazy", "Smoothed (Default)", "Predictive"][Config.camera_mode],
            manager=self.ui_manager
        )
        self.s_camera_mode_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT // 10 - 30, 240, 30)),
            text=lang_key('camera-mode') + ":",
            manager=self.ui_manager
        )

        self.s_seed = pgui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT * 2 // 10, 300, 30)),
            placeholder_text="Default is random number",
            manager=self.ui_manager
        )
        self.s_seed.set_allowed_characters('numbers')
        self.s_seed.set_text(str(Config.seed if Config.seed is not None else ''))
        self.s_seed_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT * 2 // 10 - 30, 240, 30)),
            text=lang_key('rng-seed') + ":",
            manager=self.ui_manager
        )

        self.s_start_playing_delay = pgui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT * 3 // 10, 300, 30)),
            start_value=Config.start_playing_delay,
            value_range=(1000, 5000),
            manager=self.ui_manager
        )
        self.s_start_playing_delay_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT * 3 // 10 - 30, 240, 30)),
            text=lang_key('starting-time-delay') + f" ({self.s_start_playing_delay.get_current_value()}ms):",
            manager=self.ui_manager
        )

        self.s_max_notes = pgui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT * 4 // 10, 300, 30)),
            placeholder_text="Default is infinity",
            manager=self.ui_manager
        )
        self.s_max_notes.set_allowed_characters('numbers')
        self.s_max_notes.set_text(str(Config.max_notes if Config.max_notes is not None else ''))
        self.s_max_notes_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT * 4 // 10 - 30, 240, 30)),
            text=lang_key('max-notes-to-generate') + ":",
            manager=self.ui_manager
        )

        self.s_bounce_min_spacing = pgui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT * 5 // 10, 300, 30)),
            start_value=Config.bounce_min_spacing,
            value_range=(5, 50),
            manager=self.ui_manager
        )
        self.s_bounce_min_spacing_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT * 5 // 10 - 30, 240, 30)),
            text=f"{lang_key('bounce-min-spacing')} ({Config.bounce_min_spacing}ms):",
            manager=self.ui_manager
        )

        self.s_square_speed = pgui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT * 6 // 10, 300, 30)),
            start_value=Config.square_speed,
            value_range=(100, 2000),
            manager=self.ui_manager
        )
        self.s_square_speed_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT * 6 // 10 - 30, 240, 30)),
            text=f"{lang_key('square-speed')} ({Config.square_speed} pixels/s):",
            manager=self.ui_manager
        )

        self.s_music_offset = pgui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT * 7 // 10, 300, 30)),
            start_value=Config.music_offset,
            value_range=(-500, 500),
            manager=self.ui_manager
        )
        self.s_music_offset_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT * 7 // 10 - 30, 240, 30)),
            text=f"{lang_key('music-offset')} ({Config.music_offset}ms):",
            manager=self.ui_manager
        )

        self.s_direction_change_chance = pgui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT * 8 // 10, 300, 30)),
            start_value=Config.direction_change_chance,
            value_range=(0, 100),
            manager=self.ui_manager
        )
        self.s_direction_change_chance_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT * 8 // 10 - 30, 240, 30)),
            text=f"{lang_key('change-dir-chance')} ({Config.direction_change_chance}%):",
            manager=self.ui_manager
        )

        self.s_hp_drain_rate = pgui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT * 9 // 10, 300, 30)),
            start_value=Config.hp_drain_rate,
            value_range=(3, 20),
            manager=self.ui_manager
        )
        self.s_hp_drain_rate_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH // 10, Config.SCREEN_HEIGHT * 9 // 10 - 30, 240, 30)),
            text=f"{lang_key('hp-drain-rate')} ({Config.hp_drain_rate}/s):",
            manager=self.ui_manager
        )

        # audio and general settings

        self.s_discord_rpc_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT * 9 // 10 - 30, 300, 30)),
            text="Discord RPC",
            manager=self.ui_manager
        )

        self.s_discord_rpc = pgui.elements.UIDropDownMenu(
            ["Off", "On"],
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT * 9 // 10, 300, 30)),
            starting_option=["Off", "On"][int(Config.discord_rpc)],
            manager=self.ui_manager
        )

        self.s_game_volume = pgui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT // 10, 300, 30)),
            start_value=Config.volume,
            value_range=(0, 100),
            manager=self.ui_manager
        )
        self.s_game_volume_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT // 10 - 30, 240, 30)),
            text=f"{lang_key('music-volume')} ({Config.volume}%):",
            manager=self.ui_manager
        )

        self.s_color_theme = pgui.elements.UIDropDownMenu(
            [theme for theme in Config.color_themes],
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT * 2 // 10, 300, 30)),
            starting_option=Config.theme,
            manager=self.ui_manager
        )
        self.s_color_theme_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT * 2 // 10 - 30, 240, 30)),
            text=f"{lang_key('color-theme')}:",
            manager=self.ui_manager
        )

        self.s_theatre_mode = pgui.elements.UIDropDownMenu(
            ["Off", "On"],
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT * 3 // 10, 300, 30)),
            starting_option=["Off", "On"][int(Config.theatre_mode)],
            manager=self.ui_manager
        )
        self.s_theatre_mode_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT * 3 // 10 - 30, 240, 30)),
            text=f"{lang_key('theatre-mode')}:",
            manager=self.ui_manager
        )

        self.s_particle_trail = pgui.elements.UIDropDownMenu(
            ["Off", "On"],
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT * 4 // 10, 300, 30)),
            starting_option=["Off", "On"][int(Config.particle_trail)],
            manager=self.ui_manager
        )
        self.s_particle_trail_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT * 4 // 10 - 30, 240, 30)),
            text=f"{lang_key('particle-trail')}:",
            manager=self.ui_manager
        )

        self.s_shader = pgui.elements.UIDropDownMenu(
            [_ for _ in listdir("./assets/shaders/") if _.endswith(".glsl")],
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT * 5 // 10, 300, 30)),
            starting_option=Config.shader_file_name,
            manager=self.ui_manager
        )
        self.s_shader_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect(Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT * 5 // 10 - 30, 240, 30),
            text=f"{lang_key('shader')} ({lang_key('restart-required')}):",
            manager=self.ui_manager
        )

        self.s_do_bounce_color_pegs = pgui.elements.UIDropDownMenu(
            ["Off", "On"],
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT * 6 // 10, 300, 30)),
            starting_option=["Off", "On"][int(Config.do_color_bounce_pegs)],
            manager=self.ui_manager
        )
        self.s_do_bounce_color_pegs_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT * 6 // 10 - 30, 240, 30)),
            text=f"{lang_key('color-pegs-on-bounce')}:",
            manager=self.ui_manager
        )

        self.s_do_particles_on_bounce = pgui.elements.UIDropDownMenu(
            ["Off", "On"],
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT * 7 // 10, 300, 30)),
            starting_option=["Off", "On"][int(Config.do_color_bounce_pegs)],
            manager=self.ui_manager
        )
        self.s_do_particles_on_bounce_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT * 7 // 10 - 30, 240, 30)),
            text=f"{lang_key('particles-on-bounce')}:",
            manager=self.ui_manager
        )
        self.s_resolution = pgui.elements.UIDropDownMenu(
            [str(Config.rSCREEN_WIDTH) + "x" + str(Config.rSCREEN_HEIGHT), "800x600", "1024x768", "1280x720",
             "1920x1080"],
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT * 8 // 10, 300, 30)),
            starting_option=str(Config.SCREEN_WIDTH) + "x" + str(Config.SCREEN_HEIGHT),
            manager=self.ui_manager
        )
        self.s_resolution_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH * 5 / 10, Config.SCREEN_HEIGHT * 8 // 10 - 30, 240, 30)),
            text=f"{lang_key('resolution')} ({lang_key('restart-required')}):",
            manager=self.ui_manager
        )

        # reset button

        self.s_reset_button = pgui.elements.UIButton(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH - 330, Config.SCREEN_HEIGHT - 60, 300, 30)),
            text="Reset to default",
            manager=self.ui_manager
        )

    def handle_event(self, event: pygame.event.Event):
        if not self.active:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.made_with_pgui_rect.collidepoint(pygame.mouse.get_pos()):
                    webbrowser.open("https://github.com/MyreMylar/pygame_gui")

        if event.type == pgui.UI_BUTTON_PRESSED:
            if event.ui_element == self.back_button:
                play_sound("wood.wav")
                return True
            if event.ui_element == self.s_reset_button:
                # todo: rework this
                # todo: this does not work with translation stuffs

                Config.theme = "dark"
                self.s_color_theme.selected_option = "dark"
                self.s_color_theme.current_state.finish()
                self.s_color_theme.current_state.selected_option = "dark"
                self.s_color_theme.current_state.start()

                Config.shader_file_name = "none.glsl"
                self.s_shader.selected_option = "none.glsl"
                self.s_shader.current_state.finish()
                self.s_shader.current_state.selected_option = "none.glsl"
                self.s_shader.current_state.start()

                Config.seed = None
                self.s_seed.set_text("")

                Config.camera_mode = 2
                self.s_camera_mode.selected_option = "Smoothed (Default)"
                self.s_camera_mode.current_state.finish()
                self.s_camera_mode.current_state.selected_option = "Smoothed (Default)"
                self.s_camera_mode.current_state.start()

                Config.start_playing_delay = 3000
                self.s_start_playing_delay.set_current_value(3000)
                self.s_start_playing_delay_label.set_text(
                    f"Starting time delay ({self.s_start_playing_delay.get_current_value()}ms):")

                Config.max_notes = None
                self.s_max_notes.set_text("")

                Config.bounce_min_spacing = 30
                self.s_bounce_min_spacing.set_current_value(30)
                self.s_bounce_min_spacing_label.set_text(f"Bounce min spacing ({Config.bounce_min_spacing}ms):")

                Config.square_speed = 600
                self.s_square_speed.set_current_value(600)
                self.s_square_speed_label.set_text(f"Square speed ({Config.square_speed} pixels/s):")

                Config.volume = 70
                pygame.mixer.music.set_volume(70 / 100)
                self.s_game_volume.set_current_value(70)
                self.s_game_volume_label.set_text(f"Music volume ({Config.volume}%):")

                Config.music_offset = 0
                self.s_music_offset.set_current_value(-300)
                self.s_music_offset_label.set_text(f"Music offset ({Config.music_offset}ms):")

                Config.direction_change_chance = 30
                self.s_direction_change_chance.set_current_value(30)
                self.s_direction_change_chance_label.set_text(f"Change dir chance ({Config.direction_change_chance}%):")

                Config.hp_drain_rate = 10
                self.s_hp_drain_rate.set_current_value(10)
                self.s_hp_drain_rate_label.set_text(f"HP drain rate ({Config.hp_drain_rate}/s):")

                Config.theatre_mode = False
                self.s_theatre_mode.selected_option = "Off"
                self.s_theatre_mode.current_state.finish()
                self.s_theatre_mode.current_state.selected_option = "Off"
                self.s_theatre_mode.current_state.start()

                Config.particle_trail = True
                self.s_particle_trail.selected_option = "On"
                self.s_particle_trail.current_state.finish()
                self.s_particle_trail.current_state.selected_option = "On"
                self.s_particle_trail.current_state.start()

                Config.do_color_bounce_pegs = False
                self.s_do_bounce_color_pegs.selected_option = "Off",
                self.s_do_bounce_color_pegs.current_state.finish()
                self.s_do_bounce_color_pegs.current_state.selected_option = "Off"
                self.s_do_bounce_color_pegs.current_state.start()

                Config.SCREEN_WIDTH = Config.rSCREEN_WIDTH
                Config.SCREEN_HEIGHT = Config.rSCREEN_HEIGHT

                play_sound("wood.wav")

        if event.type == pgui.UI_DROP_DOWN_MENU_CHANGED:
            play_sound("wood.wav")
            if event.ui_element == self.s_camera_mode:
                Config.camera_mode = "CLSP".index(event.text[0])  # awful way of doing this lol
            if event.ui_element == self.s_color_theme:
                Config.theme = event.text
            if event.ui_element == self.s_theatre_mode:
                Config.theatre_mode = bool(["Off", "On"].index(event.text))
            if event.ui_element == self.s_particle_trail:
                Config.particle_trail = bool(["Off", "On"].index(event.text))
            if event.ui_element == self.s_shader:
                Config.shader_file_name = event.text
            if event.ui_element == self.s_do_bounce_color_pegs:
                Config.do_color_bounce_pegs = bool(["Off", "On"].index(event.text))
            if event.ui_element == self.s_do_particles_on_bounce:
                Config.do_particles_on_bounce = bool(["Off", "On"].index(event.text))
            if event.ui_element == self.s_resolution:
                event.text = event.text.split("x")
                Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT = int(event.text[0]), int(event.text[1])
            if event.ui_element == self.s_discord_rpc:
                Config.discord_rpc = bool(["Off", "On"].index(event.text))

        if event.type == pgui.UI_TEXT_ENTRY_CHANGED:
            if event.ui_element == self.s_seed:
                text: str = event.text
                if text.isnumeric() and len(text):
                    Config.seed = int(text)
                else:
                    Config.seed = None
            if event.ui_element == self.s_max_notes:
                text: str = event.text
                if text.isnumeric() and len(text):
                    Config.max_notes = int(text)
                else:
                    Config.max_notes = None

        if event.type == pgui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == self.s_start_playing_delay:
                self.s_start_playing_delay_label.set_text(f"{lang_key('starting-time-delay')} ({event.value}ms):")
                Config.start_playing_delay = event.value
            if event.ui_element == self.s_bounce_min_spacing:
                self.s_bounce_min_spacing_label.set_text(f"{lang_key('bounce-min-spacing')} ({event.value}ms):")
                Config.bounce_min_spacing = event.value
            if event.ui_element == self.s_square_speed:
                rounded = round(event.value, -2)
                self.s_square_speed_label.set_text(f"{lang_key('square-speed')} ({rounded} pixels/s):")
                Config.square_speed = rounded
            if event.ui_element == self.s_game_volume:
                self.s_game_volume_label.set_text(f"{lang_key('music-volume')} ({event.value}%):")
                Config.volume = event.value
                pygame.mixer.music.set_volume(event.value / 100)
            if event.ui_element == self.s_music_offset:
                self.s_music_offset_label.set_text(f"{lang_key('music-offset')} ({event.value}ms):")
                Config.music_offset = event.value
            if event.ui_element == self.s_direction_change_chance:
                self.s_direction_change_chance_label.set_text(f"{lang_key('change-dir-chance')} ({event.value}%):")
                Config.direction_change_chance = event.value
            if event.ui_element == self.s_hp_drain_rate:
                self.s_hp_drain_rate_label.set_text(f"{lang_key('hp-drain-rate')} ({event.value}/s):")
                Config.hp_drain_rate = event.value

        self.ui_manager.process_events(event)

    def draw(self, screen: pygame.Surface):
        if not self.active:
            return
        self.ui_manager.update(1 / FRAMERATE)  # supposed to use dt but whatever
        self.ui_manager.draw_ui(screen)

        screen.blit(self.made_with_pgui_surf, self.made_with_pgui_rect)
