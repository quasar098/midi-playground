from utils import *
import pygame
import pygame_gui as pgui
import webbrowser


class ConfigPage:
    @property
    def made_with_pgui_rect(self):
        return self.made_with_pgui_surf.get_rect(bottomleft=(30, Config.SCREEN_HEIGHT-30))

    def __init__(self):
        self.active = False
        self.made_with_pgui_surf = get_font("./assets/poppins-regular.ttf").render("Config page made with pygame_gui library", True, (255, 255, 255))

        # pygame_gui stuff
        self.ui_manager = pgui.UIManager((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        self.back_button = pgui.elements.UIButton(
            relative_rect=pygame.Rect((Config.SCREEN_WIDTH-120, 30, 90, 30)),
            text="Back",
            manager=self.ui_manager
        )

        # all attributes matching /s_.+/ are "s"ettings

        self.s_camera_mode = pgui.elements.UIDropDownMenu(
            ["Center", "Lazy", "Smoothed (Default)", "Predictive"],
            relative_rect=pygame.Rect((300, 30, 300, 30)),
            starting_option=["Center", "Lazy", "Smoothed (Default)", "Predictive"][Config.camera_mode],
            manager=self.ui_manager
        )
        self.s_camera_mode_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((30, 30, 240, 30)),
            text="Camera mode:",
            manager=self.ui_manager
        )

        self.s_seed = pgui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((300, 90, 300, 30)),
            placeholder_text="Default is random number",
            manager=self.ui_manager
        )
        self.s_seed.set_allowed_characters('numbers')
        self.s_seed.set_text(str(Config.seed if Config.seed is not None else ''))
        self.s_seed_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((30, 90, 240, 30)),
            text="RNG seed:",
            manager=self.ui_manager
        )

        self.s_start_playing_delay = pgui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((300, 150, 300, 30)),
            start_value=Config.start_playing_delay,
            value_range=(1000, 5000),
            manager=self.ui_manager
        )
        self.s_start_playing_delay_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((30, 150, 240, 30)),
            text=f"Starting time delay ({self.s_start_playing_delay.get_current_value()}ms):",
            manager=self.ui_manager
        )

        self.s_max_notes = pgui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((300, 210, 300, 30)),
            placeholder_text="Default is infinity",
            manager=self.ui_manager
        )
        self.s_max_notes.set_allowed_characters('numbers')
        self.s_max_notes.set_text(str(Config.max_notes if Config.max_notes is not None else ''))
        self.s_max_notes_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((30, 210, 240, 30)),
            text="Max notes to generate:",
            manager=self.ui_manager
        )

        self.s_bounce_min_spacing = pgui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((300, 270, 300, 30)),
            start_value=Config.bounce_min_spacing,
            value_range=(5, 50),
            manager=self.ui_manager
        )
        self.s_bounce_min_spacing_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((30, 270, 240, 30)),
            text=f"Bounce min spacing ({Config.bounce_min_spacing}ms):",
            manager=self.ui_manager
        )

        self.s_square_speed = pgui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((300, 330, 300, 30)),
            start_value=Config.square_speed,
            value_range=(100, 2000),
            manager=self.ui_manager
        )
        self.s_square_speed_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((30, 330, 240, 30)),
            text=f"Square speed ({Config.square_speed} pixels/s):",
            manager=self.ui_manager
        )

        self.s_music_offset = pgui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((300, 390, 300, 30)),
            start_value=Config.music_offset,
            value_range=(-500, 500),
            manager=self.ui_manager
        )
        self.s_music_offset_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((30, 390, 240, 30)),
            text=f"Music offset ({Config.music_offset}ms):",
            manager=self.ui_manager
        )

        self.s_direction_change_chance = pgui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((300, 450, 300, 30)),
            start_value=Config.direction_change_chance,
            value_range=(0, 100),
            manager=self.ui_manager
        )
        self.s_direction_change_chance_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((30, 450, 240, 30)),
            text=f"Change dir chance ({Config.direction_change_chance}%):",
            manager=self.ui_manager
        )

        self.s_hp_drain_rate = pgui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((300, 510, 300, 30)),
            start_value=Config.hp_drain_rate,
            value_range=(-5, 20),
            manager=self.ui_manager
        )
        self.s_hp_drain_rate_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((30, 510, 240, 30)),
            text=f"HP drain rate ({Config.hp_drain_rate}/s):",
            manager=self.ui_manager
        )

        # audio and general settings

        self.s_game_volume = pgui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((930, 30, 300, 30)),
            start_value=Config.volume,
            value_range=(0, 100),
            manager=self.ui_manager
        )
        self.s_game_volume_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((630, 30, 240, 30)),
            text=f"Music volume ({Config.volume}%):",
            manager=self.ui_manager
        )

        self.s_color_theme = pgui.elements.UIDropDownMenu(
            [theme for theme in Config.color_themes],
            relative_rect=pygame.Rect((930, 90, 300, 30)),
            starting_option=Config.theme,
            manager=self.ui_manager
        )
        self.s_color_theme_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((630, 90, 240, 30)),
            text="Color theme:",
            manager=self.ui_manager
        )

        self.s_theatre_mode = pgui.elements.UIDropDownMenu(
            ["Off", "On"],
            relative_rect=pygame.Rect((930, 150, 300, 30)),
            starting_option=["Off", "On"][int(Config.theatre_mode)],
            manager=self.ui_manager
        )
        self.s_theatre_mode_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((630, 150, 240, 30)),
            text="Theatre mode:",
            manager=self.ui_manager
        )

        # particle trail
        self.s_particle_trail = pgui.elements.UIDropDownMenu(
            ["Off", "On"],
            relative_rect=pygame.Rect((930, 210, 300, 30)),
            starting_option=["Off", "On"][int(Config.particle_trail)],
            manager=self.ui_manager
        )
        self.s_particle_trail_label = pgui.elements.UILabel(
            relative_rect=pygame.Rect((630, 210, 240, 30)),
            text="Particle trail:",
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

        if event.type == pgui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.s_camera_mode:
                play_sound("wood.wav")
                Config.camera_mode = "CLSP".index(event.text[0])
            if event.ui_element == self.s_color_theme:
                play_sound("wood.wav")
                Config.theme = event.text
            if event.ui_element == self.s_theatre_mode:
                play_sound("wood.wav")
                Config.theatre_mode = bool("fn".index(event.text[1]))
            if event.ui_element == self.s_particle_trail:
                play_sound("wood.wav")
                Config.particle_trail = bool("fn".index(event.text[1]))

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
                self.s_start_playing_delay_label.set_text(f"Starting time delay ({event.value}ms):")
                Config.start_playing_delay = event.value
            if event.ui_element == self.s_bounce_min_spacing:
                self.s_bounce_min_spacing_label.set_text(f"Bounce min spacing ({event.value}ms):")
                Config.bounce_min_spacing = event.value
            if event.ui_element == self.s_square_speed:
                rounded = round(event.value, -2)
                self.s_square_speed_label.set_text(f"Square speed ({rounded} pixels/s):")
                Config.square_speed = rounded
            if event.ui_element == self.s_game_volume:
                self.s_game_volume_label.set_text(f"Music volume ({event.value}%):")
                Config.volume = event.value
                pygame.mixer.music.set_volume(event.value/100)
            if event.ui_element == self.s_music_offset:
                self.s_music_offset_label.set_text(f"Music offset ({event.value}ms):")
                Config.music_offset = event.value
            if event.ui_element == self.s_direction_change_chance:
                self.s_direction_change_chance_label.set_text(f"Change dir chance ({event.value}%):")
                Config.direction_change_chance = event.value
            if event.ui_element == self.s_hp_drain_rate:
                self.s_hp_drain_rate_label.set_text(f"HP drain rate ({event.value}/s):")
                Config.hp_drain_rate = event.value

        self.ui_manager.process_events(event)

    def draw(self, screen: pygame.Surface):
        if not self.active:
            return
        self.ui_manager.update(1/FRAMERATE)  # supposed to use dt but whatever
        self.ui_manager.draw_ui(screen)

        screen.blit(self.made_with_pgui_surf, self.made_with_pgui_rect)
