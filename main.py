from time import time as get_current_time
import random
from world import World
from camera import Camera
from utils import *
import pygame


def do_bouncing() -> None:
    """Example of bad code"""

    random.seed(Config.seed)

    # load notes
    notes = read_midi_file(Config.midi_file_name)
    notes = [(note[0], note[1], note[2]) for note in notes]
    if len(notes):
        notes.append((notes[-1][0], notes[-1][1]+Config.last_bounce_delay, notes[-1][2]))

    # pygame stuff
    music_has_played = False
    offset_happened = False
    pygame.init()
    pygame.display.set_caption("bouncing squares")
    pygame.mixer.init()

    font = pygame.font.SysFont("Arial", 30)
    camera_ctrl_text = font.render("Manual Camera Control Activated", True, (0, 255, 0))

    pygame.mouse.set_visible(False)
    pygame.mixer.music.load(Config.audio_file_name)

    # the big guns
    camera = Camera()
    camera.lock_type = CameraFollow(Config.camera_mode)
    world = World()

    safe_areas: list[pygame.Rect] = world.gen_future_bounces(notes)
    world.start_time = get_current_time()
    pygame.mixer.music.set_volume(Config.volume/100)

    # preload square
    if len(world.future_bounces):
        world.square.pos = world.future_bounces[0].square_pos
        world.square.dir = [0, 0]  # freeze square

    screen = pygame.display.set_mode(
        [Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT],
        pygame.FULLSCREEN | pygame.HWACCEL | pygame.HWSURFACE | pygame.SCALED,
        vsync=1
    )

    screen_rect = screen.get_rect()
    clock = pygame.time.Clock()

    # game loop
    running = True
    while running:
        if not music_has_played:
            if not offset_happened:
                for bnc_change in world.future_bounces:
                    bnc_change.time += Config.GLOBAL_TIME_OFFSET/1000
            offset_happened = True
            if world.time > Config.GLOBAL_TIME_OFFSET/1000:
                music_has_played = True
                song_load_before = get_current_time()
                pygame.mixer.music.play()
                for bnc_change in world.future_bounces:
                    bnc_change.time += (get_current_time()-song_load_before)/1000

        screen.fill(Config.Colors.wall_color)

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mouse.set_visible(True)
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mouse.set_visible(True)
                    running = False
                if event.key == pygame.K_TAB:
                    camera.locked_on_square = not camera.locked_on_square
                if 97+26 > event.key >= 97 or event.key == pygame.K_SPACE:  # press a to z key
                    world.handle_keypress()

        # set world time
        world.update_time()

        # move camera (only works if not locked on square)
        camera.attempt_movement()

        # handle square bounces
        world.handle_bouncing(world.square)

        # move square
        world.square.reg_move()

        # square in center of camera if locked
        if camera.locked_on_square:
            camera.follow(world.square)

        # bounce anim
        sqrect = camera.offset(world.square.rect)
        if (world.time - 0.25) + Config.music_offset / 1000 < world.square.last_bounce_time:
            lerp = abs((world.time - 0.25 + Config.music_offset / 1000) - world.square.last_bounce_time) * 5
            lerp = lerp ** 2  # square it for better-looking interpolation
            if world.square.latest_bounce_direction:
                sqrect.inflate_ip((lerp * 5, -10 * lerp))
            else:
                sqrect.inflate_ip((-10 * lerp, lerp * 5))

        total_rects = 0

        # safe areas
        for safe_area in safe_areas:
            offsetted = camera.offset(safe_area)
            if offsetted.colliderect(screen_rect):
                total_rects += 1
                pygame.draw.rect(screen, Config.Colors.bg_color, offsetted)

        # draw pegs
        for bounce in world.rectangles:
            offsetted = camera.offset(bounce)
            if offsetted.colliderect(screen_rect):
                total_rects += 1
                pygame.draw.rect(screen, Config.Colors.wall_color, offsetted)

        # particles
        for particle in world.particles:
            pygame.draw.rect(screen, Config.Colors.bg_color, camera.offset(particle.rect))
        for remove_particle in [particle for particle in world.particles if particle.age()]:
            world.particles.remove(remove_particle)

        mimic = font.render(world.latest_thing, True, (255, 255, 255))
        screen.blit(mimic, (100, 100))

        # draw square outline
        pygame.draw.rect(screen, (0, 0, 0), sqrect)
        square_color_index = round((world.square.dir_x + 1)/2 + world.square.dir_y + 1)
        world.square.register_past_color(Config.Colors.square_colors[square_color_index])
        sq_surf = world.square.get_surface(tuple(sqrect.inflate(-int(Config.SQUARE_SIZE/5), -int(Config.SQUARE_SIZE/5))[2:]))
        screen.blit(sq_surf, sq_surf.get_rect(center=sqrect.center))

        if not camera.locked_on_square:
            screen.blit(camera_ctrl_text, (10, 10))

        pygame.display.flip()
        clock.tick(FRAMERATE)

    pygame.quit()
