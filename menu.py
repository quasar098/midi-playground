from particle import Particle
from square import Square
from utils import *
from random import randint
import pygame


def draw_beveled_rectangle(surf: pygame.Surface, color: pygame.Color, rect: pygame.Rect) -> None:
    """i think they're called bevels"""
    pygame.draw.rect(surf, color.lerp((0, 0, 0), 0.4), rect.inflate(8, 8), border_radius=4)
    pygame.draw.rect(surf, color, rect, border_radius=2)


class MenuOption:
    HEIGHT = (Config.SCREEN_HEIGHT//9)-2
    SPACING = 16

    def __init__(self, id_: str, color: pygame.Color):
        self.id = id_
        title = lang_key(id_)  # translate the actual title
        self.color = color
        self.before_hover = False
        self.hover_anim: float = 0

        # this type of graphics programming is hands down the most boring thing i've ever done
        font = get_font(Config.SCREEN_HEIGHT // 15)
        title_surface = font.render(title, True, color.lerp((0, 0, 0), 0.7))
        brighter_title_surface = font.render(title, True, color.lerp((0, 0, 0), 0.2))
        shadow_surface = pygame.Surface((brighter_title_surface.get_rect().width + 100, MenuOption.HEIGHT), pygame.SRCALPHA)
        for _ in range(100):
            chopped = pygame.transform.chop(brighter_title_surface, pygame.Rect(0, MenuOption.HEIGHT-9+lang_key("font-menu-shadow-length-offset") - _, 0, 600))
            shadow_surface.blit(chopped, (_, _))

        self.surface = pygame.Surface((int(Config.SCREEN_WIDTH / 2 + 300), self.HEIGHT + 8), pygame.SRCALPHA)
        draw_beveled_rectangle(self.surface, self.color, pygame.Rect(4, 4, Config.SCREEN_WIDTH, MenuOption.HEIGHT))
        title_rect = title_surface.get_rect(midleft=self.surface.get_rect().midleft).move(50, 0)
        self.surface.blit(shadow_surface, shadow_surface.get_rect(midleft=title_rect.midleft).move(0, lang_key("font-menu-shadow-offset")))
        self.surface.blit(title_surface, title_rect)

    def update_hover(self, y_value: int) -> None:
        wide_rect = pygame.Rect(0, y_value, Config.SCREEN_WIDTH, MenuOption.HEIGHT)
        wide_rect.move_ip(int(Config.SCREEN_WIDTH / 2) - 30 * interpolate_fn(self.hover_anim), 0)
        if wide_rect.collidepoint(pygame.mouse.get_pos()):
            self.hover_anim += 9 / FRAMERATE
        else:
            self.hover_anim -= 3 / FRAMERATE
        self.hover_anim = max(min(self.hover_anim, 1), 0)

    def get_rect(self, y_value: int) -> pygame.Rect:
        wide_rect = pygame.Rect(0, y_value, Config.SCREEN_WIDTH, MenuOption.HEIGHT)
        wide_rect.move_ip(int(Config.SCREEN_WIDTH / 2) - 60 * interpolate_fn(self.hover_anim), 0)
        return wide_rect


class Menu:
    def __init__(self):
        self.menu_options: list[MenuOption] = [
            MenuOption("play", pygame.Color(214, 247, 163)),
            MenuOption("config", pygame.Color(196, 255, 178)),
            MenuOption("contribute", pygame.Color(183, 227, 204)),
            MenuOption("open-songs-folder", pygame.Color(125, 130, 184)),
            MenuOption("quit", pygame.Color(226, 109, 92))
        ]
        self.anim = 1
        # note that there are spaces after each line of code in the marquee text
        self.marquee_text = lang_key("title-marquee")
        self.title_surf = get_font(72).render(lang_key("title"), True, get_colors()["hallway"])
        self.marquee_surf = get_font(24).render(self.marquee_text, True, get_colors()["hallway"])
        self.flags = {}
        for language in TRANSLATIONS:
            self.flags[language] = pygame.image.load(f"./assets/flags/{language}.png").convert_alpha()
        self.prev_active = True
        self.active = True
        self.square = Square(100, 320)
        self.particles: list[Particle] = []

        self.left_lang_rect: Optional[pygame.Rect] = None
        self.right_lang_rect: Optional[pygame.Rect] = None
        self.requires_restart_surf: Optional[pygame.Surface] = None

    @property
    def screensaver_rect(self):
        return pygame.Rect(0, 0, int(Config.SCREEN_WIDTH / 2 - 100), Config.SCREEN_HEIGHT).inflate(-100, -100)

    def draw(self, screen: pygame.Surface, n_frames: int):
        if self.active:
            if self.anim == 0:
                self.anim = 0.3
            self.anim += 1.8 / FRAMERATE
        else:
            self.anim -= 1.8 / FRAMERATE
        self.anim = max(min(self.anim, 1), 0)
        if not self.anim:
            return

        if self.active and not self.prev_active:
            self.title_surf = get_font(72).render("midi-playground", True, get_colors()["hallway"])
            self.marquee_surf = get_font(24).render(self.marquee_text, True, get_colors()["hallway"])
        self.prev_active = self.active

        # interesting here
        if self.active:
            # x_offset = interpolate_fn(1-self.anim)*(self.screensaver_rect.width*2)
            x_offset = 0

            sqrect = self.square.rect
            if (get_current_time() - 0.25) < self.square.last_bounce_time:
                lerp = abs((get_current_time() - 0.25) - self.square.last_bounce_time) * 5
                lerp = lerp ** 2  # square it for better-looking interpolation
                if self.square.latest_bounce_direction:
                    sqrect.inflate_ip((lerp * 5, -10 * lerp))
                else:
                    sqrect.inflate_ip((-10 * lerp, lerp * 5))

            pygame.draw.rect(screen, get_colors()["hallway"], self.screensaver_rect.move(-x_offset, 0))

            # particle trail
            if Config.particle_trail:
                # every 2 frames add a particle
                if n_frames % 2 == 0:
                    new = Particle(self.square.pos, [0, 0], True)
                    new.color = get_colors()["background"]
                    new.delta = [randint(-10, 10)/20, randint(-10, 10)/20]
                    self.particles.append(new)

            # particles
            for particle in self.particles:
                pygame.draw.rect(screen, particle.color, particle.rect)
            for remove_particle in [particle for particle in self.particles if particle.age()]:
                self.particles.remove(remove_particle)

            self.square.draw(screen, sqrect.move(-x_offset, 0))
            bounced = self.square.title_screen_physics(self.screensaver_rect.move(-x_offset, 0))
            if bounced:
                latest_dir = self.square.latest_bounce_direction
                sd = self.square.dir.copy()
                sd[latest_dir] *= -1
                sd[1-latest_dir] = 0
                sp = self.square.pos
                for _ in range(Config.particle_amount):
                    new = Particle([sp[0]+randint(-10, 10), sp[1]+randint(-10, 10)], sd)
                    self.particles.append(new)

        # title text
        title_surf_loc_rect = self.title_surf.get_rect(midtop=(Config.SCREEN_WIDTH*3/4, 60))
        self.title_surf.set_alpha(max(int(interpolate_fn(self.anim)*400-145), 0))
        screen.blit(self.title_surf, title_surf_loc_rect)

        # marquee text
        time = pygame.time.get_ticks()
        cropped_marquee = pygame.Surface((self.title_surf.get_width(), self.marquee_surf.get_height()), pygame.SRCALPHA)
        draw_marquee_position = [self.title_surf.get_width()-time/5, 0]
        while draw_marquee_position[0] < -self.marquee_surf.get_width():
            draw_marquee_position[0] += self.marquee_surf.get_width()+self.title_surf.get_width()+10
        cropped_marquee.blit(self.marquee_surf, draw_marquee_position)
        cropped_marquee.set_alpha(max(int(interpolate_fn(self.anim)*400-145), 0))
        screen.blit(cropped_marquee, cropped_marquee.get_rect(topleft=title_surf_loc_rect.bottomleft))

        # options
        for index, option in enumerate(self.menu_options):
            y_value = index * (option.HEIGHT + option.SPACING) + 250
            # update the hover if completely active
            if self.anim == 1:
                option.update_hover(y_value)

            # draw the option
            x_movement = interpolate_fn(1 - self.anim) * 60

            rect = option.get_rect(y_value).move(x_movement, 0)
            option.surface.set_alpha(int(interpolate_fn(self.anim)*255))
            screen.blit(option.surface, rect)

            # for sounds
            new_hover = rect.collidepoint(pygame.mouse.get_pos())
            if new_hover and not option.before_hover:
                play_sound("wood.wav")
            option.before_hover = new_hover

        # flag chooser
        current_flag = self.flags[Config.language]
        cfrect = current_flag.get_rect(bottomright=(Config.SCREEN_WIDTH-100, Config.SCREEN_HEIGHT-30))
        screen.blit(current_flag, cfrect)
        left_arrow = get_font(72, "poppins-regular.ttf").render("<", True, get_colors()["hallway"])
        right_arrow = get_font(72, "poppins-regular.ttf").render(">", True, get_colors()["hallway"])
        self.left_lang_rect = left_arrow.get_rect(midright=cfrect.midleft).move(-5, 5)
        screen.blit(left_arrow, self.left_lang_rect)
        self.right_lang_rect = right_arrow.get_rect(midleft=cfrect.midright).move(5, 5)
        screen.blit(right_arrow, self.right_lang_rect)
        if self.requires_restart_surf is not None:
            screen.blit(self.requires_restart_surf, self.requires_restart_surf.get_rect(midbottom=cfrect.midtop).move(0, -10))

    def handle_event(self, event: pygame.event.Event):
        if not self.active:
            return
        for index, option in enumerate(self.menu_options):
            rect = option.get_rect(index * (option.HEIGHT + option.SPACING) + 250)
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and rect.collidepoint(
                    pygame.mouse.get_pos())) \
                    or (event.type == pygame.KEYDOWN and event.key == 49 + index):
                play_sound("select.mp3")
                return option.id
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in (1, 2, 3):
                # inflate for more enjoyment (aim trainer minigame !?!? crazy)
                if self.square.rect.inflate(20, 20).collidepoint(pygame.mouse.get_pos()):
                    play_sound("wood.wav", 1)
                    self.square.dir[randint(0, 1)] *= -1
                if self.right_lang_rect.inflate(10, 10).collidepoint(pygame.mouse.get_pos()):
                    play_sound("wood.wav", 1)
                    languages = list(TRANSLATIONS.keys())
                    Config.language = languages[(languages.index(Config.language)+1) % len(languages)]
                    self.requires_restart_surf = get_font(18).render(lang_key('restart-required'), True, get_colors()["hallway"])
                if self.left_lang_rect.inflate(10, 10).collidepoint(pygame.mouse.get_pos()):
                    play_sound("wood.wav", 1)
                    languages = list(TRANSLATIONS.keys())
                    Config.language = languages[(languages.index(Config.language)-1) % len(languages)]
                    self.requires_restart_surf = get_font(18).render(lang_key('restart-required'), True, get_colors()["hallway"])
