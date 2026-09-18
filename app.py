# -*- coding: utf-8 -*-

import math
import random
import sys

import pygame


# ============================================================
# APPLICATION
# ============================================================

APP_NAME = "Extreme Message Animator"

FPS = 60

MAX_MESSAGE_LENGTH = 5000

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# ============================================================
# INITIALIZE
# ============================================================

pygame.init()
pygame.font.init()

display_info = pygame.display.Info()

SCREEN_WIDTH = display_info.current_w
SCREEN_HEIGHT = display_info.current_h

if SCREEN_WIDTH < 800:
    SCREEN_WIDTH = 1024

if SCREEN_HEIGHT < 600:
    SCREEN_HEIGHT = 768

pygame.display.set_caption(APP_NAME)

CLOCK = pygame.time.Clock()

FONT_NAME = pygame.font.match_font("arial")

if FONT_NAME is None:
    FONT_NAME = pygame.font.get_default_font()


# ============================================================
# COLOR
# ============================================================

def hsv_to_rgb(h, s, v):

    h = h % 360.0

    c = v * s

    x = c * (
        1.0 -
        abs(((h / 60.0) % 2.0) - 1.0)
    )

    m = v - c

    if h < 60:
        r = c
        g = x
        b = 0

    elif h < 120:
        r = x
        g = c
        b = 0

    elif h < 180:
        r = 0
        g = c
        b = x

    elif h < 240:
        r = 0
        g = x
        b = c

    elif h < 300:
        r = x
        g = 0
        b = c

    else:
        r = c
        g = 0
        b = x

    return (
        int((r + m) * 255),
        int((g + m) * 255),
        int((b + m) * 255)
    )


# ============================================================
# HELPERS
# ============================================================

def clamp(value, minimum, maximum):

    if value < minimum:
        return minimum

    if value > maximum:
        return maximum

    return value


def wrap_text(text, font, maximum_width):

    words = text.split()

    if not words:
        return [""]

    lines = []

    current = words[0]

    for word in words[1:]:

        candidate = current + " " + word

        if font.size(candidate)[0] <= maximum_width:

            current = candidate

        else:

            lines.append(current)

            current = word

    lines.append(current)

    return lines


def ease_out_back(value):

    c1 = 1.70158
    c3 = c1 + 1.0

    return (
        1.0
        + c3 * (value - 1.0) ** 3
        + c1 * (value - 1.0) ** 2
    )


# ============================================================
# PARTICLE
# ============================================================

class Particle(object):

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.reset()

    def reset(self):

        self.x = random.uniform(
            -self.width * 0.2,
            self.width * 1.2
        )

        self.y = random.uniform(
            -self.height * 0.2,
            self.height * 1.2
        )

        self.vx = random.uniform(
            -1.0,
            1.0
        )

        self.vy = random.uniform(
            -1.0,
            1.0
        )

        self.speed = random.uniform(
            0.3,
            2.2
        )

        self.radius = random.uniform(
            1.0,
            4.0
        )

        self.depth = random.uniform(
            0.2,
            1.0
        )

        self.hue = random.uniform(
            0,
            360
        )

    def update(self, dt, speed):

        center_x = self.width * 0.5
        center_y = self.height * 0.5

        dx = self.x - center_x
        dy = self.y - center_y

        self.x += (
            dx
            * self.depth
            * self.speed
            * dt
            * speed
            * 0.12
        )

        self.y += (
            dy
            * self.depth
            * self.speed
            * dt
            * speed
            * 0.12
        )

        self.depth += (
            dt
            * 0.12
            * speed
        )

        self.hue += dt * 55

        if (
            self.x < -self.width * 0.5
            or self.x > self.width * 1.5
            or self.y < -self.height * 0.5
            or self.y > self.height * 1.5
            or self.depth > 1.8
        ):

            self.reset()

    def draw(self, surface):

        size = int(
            self.radius
            * (
                0.5
                + self.depth * 1.7
            )
        )

        if size < 1:
            size = 1

        color = hsv_to_rgb(
            self.hue,
            0.9,
            1.0
        )

        pygame.draw.circle(
            surface,
            color,
            (
                int(self.x),
                int(self.y)
            ),
            size
        )


# ============================================================
# LIGHT STREAK
# ============================================================

class LightStreak(object):

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.reset()

    def reset(self):

        self.x = random.uniform(
            -self.width,
            self.width
        )

        self.y = random.uniform(
            0,
            self.height
        )

        self.length = random.uniform(
            self.width * 0.04,
            self.width * 0.25
        )

        self.speed = random.uniform(
            self.width * 0.2,
            self.width * 0.8
        )

        self.hue = random.uniform(
            0,
            360
        )

        self.angle = random.uniform(
            -0.08,
            0.08
        )

    def update(self, dt, speed):

        self.x += (
            self.speed
            * dt
            * speed
        )

        self.hue += dt * 40

        if self.x > self.width + self.length:

            self.reset()

            self.x = -self.length

    def draw(self, surface):

        color = hsv_to_rgb(
            self.hue,
            1.0,
            1.0
        )

        dx = (
            math.cos(self.angle)
            * self.length
        )

        dy = (
            math.sin(self.angle)
            * self.length
        )

        pygame.draw.line(
            surface,
            color,
            (
                int(self.x),
                int(self.y)
            ),
            (
                int(self.x - dx),
                int(self.y - dy)
            ),
            2
        )


# ============================================================
# TEXT
# ============================================================

def create_text(text, requested_size, maximum_width):

    size = int(requested_size)

    if size < 20:
        size = 20

    font = pygame.font.Font(
        FONT_NAME,
        size
    )

    lines = wrap_text(
        text,
        font,
        maximum_width
    )

    while len(lines) > 8 and size > 24:

        size -= 3

        font = pygame.font.Font(
            FONT_NAME,
            size
        )

        lines = wrap_text(
            text,
            font,
            maximum_width
        )

    return font, lines


def draw_text(
    surface,
    message,
    center_x,
    center_y,
    font_size,
    hue,
    scale,
    rotation,
    animation_time
):

    maximum_width = int(
        SCREEN_WIDTH * 0.82
    )

    font, lines = create_text(
        message,
        font_size,
        maximum_width
    )

    line_height = font.get_linesize()

    total_height = (
        len(lines)
        * line_height
    )

    start_y = (
        center_y
        - total_height / 2
    )

    index = 0

    for line in lines:

        color = hsv_to_rgb(
            hue + index * 28,
            1.0,
            1.0
        )

        text_surface = font.render(
            line,
            True,
            color
        )

        wave = math.sin(
            animation_time * 2.0
            + index * 0.7
        ) * 8.0

        pulse = (
            1.0
            + math.sin(
                animation_time * 3.0
                + index
            ) * 0.025
        )

        final_scale = (
            scale
            * pulse
        )

        if final_scale < 0.05:
            final_scale = 0.05

        transformed = pygame.transform.rotozoom(
            text_surface,
            rotation,
            final_scale
        )

        text_x = int(center_x)

        text_y = int(
            start_y
            + index * line_height
            + line_height / 2
            + wave
        )

        rect = transformed.get_rect(
            center=(
                text_x,
                text_y
            )
        )

        # Glow
        for extra, alpha in (
            (30, 25),
            (18, 40),
            (8, 70)
        ):

            glow = pygame.transform.smoothscale(
                transformed,
                (
                    transformed.get_width()
                    + extra,
                    transformed.get_height()
                    + extra
                )
            )

            glow.set_alpha(alpha)

            glow_rect = glow.get_rect(
                center=rect.center
            )

            surface.blit(
                glow,
                glow_rect
            )

        surface.blit(
            transformed,
            rect
        )

        index += 1


# ============================================================
# ENERGY RINGS
# ============================================================

def draw_rings(surface, time_value, intensity):

    center_x = int(
        SCREEN_WIDTH * 0.5
    )

    center_y = int(
        SCREEN_HEIGHT * 0.5
    )

    base = min(
        SCREEN_WIDTH,
        SCREEN_HEIGHT
    )

    for i in range(10):

        phase = (
            time_value
            * (
                0.5
                + i * 0.03
            )
            + i * 0.7
        )

        radius = (
            base
            * (
                0.10
                + i * 0.047
            )
            + math.sin(phase)
            * 12
        )

        radius *= intensity

        if radius < 1:
            continue

        rect = pygame.Rect(
            int(center_x - radius),
            int(center_y - radius),
            int(radius * 2),
            int(radius * 2)
        )

        color = hsv_to_rgb(
            time_value * 50
            + i * 35,
            1.0,
            0.8
        )

        pygame.draw.arc(
            surface,
            color,
            rect,
            phase,
            phase + math.pi * 1.35,
            2
        )


# ============================================================
# INPUT SCREEN
# ============================================================

def input_screen():

    width = min(
        SCREEN_WIDTH,
        1200
    )

    height = min(
        SCREEN_HEIGHT,
        800
    )

    pygame.display.set_mode(
        (
            width,
            height
        ),
        pygame.RESIZABLE
    )

    window = pygame.display.get_surface()

    title_font = pygame.font.Font(
        FONT_NAME,
        44
    )

    normal_font = pygame.font.Font(
        FONT_NAME,
        25
    )

    input_font = pygame.font.Font(
        FONT_NAME,
        27
    )

    button_font = pygame.font.Font(
        FONT_NAME,
        24
    )

    message = ""

    running = True

    while running:

        CLOCK.tick(FPS)

        width, height = window.get_size()

        current_time = (
            pygame.time.get_ticks()
            / 1000.0
        )

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if event.type == pygame.VIDEORESIZE:

                width = event.w
                height = event.h

                window = pygame.display.set_mode(
                    (
                        width,
                        height
                    ),
                    pygame.RESIZABLE
                )

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    pygame.quit()
                    sys.exit()

                elif event.key == pygame.K_BACKSPACE:

                    message = message[:-1]

                elif event.key == pygame.K_RETURN:

                    if message.strip():

                        return message.strip()

                else:

                    if (
                        event.unicode
                        and len(message)
                        < MAX_MESSAGE_LENGTH
                    ):

                        message += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:

                mouse_x, mouse_y = event.pos

                button = pygame.Rect(
                    width // 2 - 180,
                    height - 135,
                    360,
                    65
                )

                if button.collidepoint(
                    mouse_x,
                    mouse_y
                ):

                    if message.strip():

                        return message.strip()

        window.fill(
            (
                3,
                3,
                7
            )
        )

        # Background particles
        for i in range(45):

            angle = (
                current_time * 0.12
                + i * 0.5
            )

            x = (
                width / 2
                + math.cos(angle)
                * width
                * 0.45
            )

            y = (
                height / 2
                + math.sin(
                    angle * 1.15
                )
                * height
                * 0.42
            )

            color = hsv_to_rgb(
                current_time * 60
                + i * 10,
                1.0,
                1.0
            )

            pygame.draw.circle(
                window,
                color,
                (
                    int(x),
                    int(y)
                ),
                2
            )

        # Title
        title_color = hsv_to_rgb(
            current_time * 70,
            1.0,
            1.0
        )

        title = title_font.render(
            "EXTREME MESSAGE ANIMATOR",
            True,
            title_color
        )

        title_rect = title.get_rect(
            center=(
                width // 2,
                90
            )
        )

        window.blit(
            title,
            title_rect
        )

        subtitle = normal_font.render(
            "Enter your message",
            True,
            WHITE
        )

        subtitle_rect = subtitle.get_rect(
            center=(
                width // 2,
                155
            )
        )

        window.blit(
            subtitle,
            subtitle_rect
        )

        # Input box
        box_width = min(
            width - 60,
            900
        )

        box_height = 210

        box = pygame.Rect(
            width // 2 - box_width // 2,
            height // 2 - 115,
            box_width,
            box_height
        )

        pygame.draw.rect(
            window,
            (
                12,
                12,
                18
            ),
            box,
            border_radius=18
        )

        border_color = hsv_to_rgb(
            current_time * 80,
            1.0,
            1.0
        )

        pygame.draw.rect(
            window,
            border_color,
            box,
            3,
            border_radius=18
        )

        if message:

            lines = wrap_text(
                message,
                input_font,
                box.width - 40
            )

            lines = lines[-5:]

            y = box.y + 20

            for line in lines:

                rendered = input_font.render(
                    line,
                    True,
                    WHITE
                )

                window.blit(
                    rendered,
                    (
                        box.x + 20,
                        y
                    )
                )

                y += input_font.get_linesize()

        else:

            placeholder = input_font.render(
                "Type something amazing...",
                True,
                (
                    90,
                    90,
                    100
                )
            )

            window.blit(
                placeholder,
                (
                    box.x + 20,
                    box.y + 20
                )
            )

        # Character counter
        counter = normal_font.render(
            "%d / %d" % (
                len(message),
                MAX_MESSAGE_LENGTH
            ),
            True,
            (
                100,
                100,
                110
            )
        )

        window.blit(
            counter,
            (
                box.right
                - counter.get_width()
                - 15,
                box.bottom
                - counter.get_height()
                - 10
            )
        )

        # Button
        button = pygame.Rect(
            width // 2 - 180,
            height - 135,
            360,
            65
        )

        pygame.draw.rect(
            window,
            border_color,
            button,
            border_radius=15
        )

        button_text = button_font.render(
            "START ANIMATION",
            True,
            BLACK
        )

        button_rect = button_text.get_rect(
            center=button.center
        )

        window.blit(
            button_text,
            button_rect
        )

        hint_font = pygame.font.Font(
            FONT_NAME,
            17
        )

        hint = hint_font.render(
            "ENTER = Start    ESC = Exit",
            True,
            (
                100,
                100,
                110
            )
        )

        hint_rect = hint.get_rect(
            center=(
                width // 2,
                height - 30
            )
        )

        window.blit(
            hint,
            hint_rect
        )

        pygame.display.flip()


# ============================================================
# FULLSCREEN ANIMATION
# ============================================================

def animation_screen(message):

    pygame.display.set_mode(
        (
            SCREEN_WIDTH,
            SCREEN_HEIGHT
        ),
        pygame.FULLSCREEN
        | pygame.DOUBLEBUF
    )

    screen = pygame.display.get_surface()

    particles = []

    for _ in range(220):

        particles.append(
            Particle(
                SCREEN_WIDTH,
                SCREEN_HEIGHT
            )
        )

    streaks = []

    for _ in range(35):

        streaks.append(
            LightStreak(
                SCREEN_WIDTH,
                SCREEN_HEIGHT
            )
        )

    running = True

    paused = False

    speed = 1.0

    intensity = 1.0

    animation_start = (
        pygame.time.get_ticks()
    )

    while running:

        dt = (
            CLOCK.tick(FPS)
            / 1000.0
        )

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    running = False

                elif event.key == pygame.K_r:

                    running = False

                elif event.key == pygame.K_SPACE:

                    paused = not paused

                elif event.key == pygame.K_UP:

                    intensity = clamp(
                        intensity + 0.1,
                        0.4,
                        2.5
                    )

                elif event.key == pygame.K_DOWN:

                    intensity = clamp(
                        intensity - 0.1,
                        0.4,
                        2.5
                    )

                elif event.key == pygame.K_RIGHT:

                    speed = clamp(
                        speed + 0.1,
                        0.3,
                        3.0
                    )

                elif event.key == pygame.K_LEFT:

                    speed = clamp(
                        speed - 0.1,
                        0.3,
                        3.0
                    )

        if paused:

            overlay = pygame.Surface(
                (
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT
                )
            )

            overlay.fill(
                (
                    0,
                    0,
                    0
                )
            )

            overlay.set_alpha(160)

            screen.blit(
                overlay,
                (
                    0,
                    0
                )
            )

            pause_font = pygame.font.Font(
                FONT_NAME,
                50
            )

            pause_text = pause_font.render(
                "PAUSED",
                True,
                WHITE
            )

            pause_rect = pause_text.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    SCREEN_HEIGHT // 2
                )
            )

            screen.blit(
                pause_text,
                pause_rect
            )

            pygame.display.flip()

            continue

        elapsed = (
            pygame.time.get_ticks()
            - animation_start
        ) / 1000.0

        t = elapsed * speed

        # Black background
        screen.fill(BLACK)

        # Particles
        for particle in particles:

            particle.update(
                dt,
                speed
            )

            particle.draw(
                screen
            )

        # Streaks
        for streak in streaks:

            streak.update(
                dt,
                speed
            )

            streak.draw(
                screen
            )

        # Energy rings
        draw_rings(
            screen,
            t,
            intensity
        )

        # Camera movement
        center_x = (
            SCREEN_WIDTH / 2
            + math.sin(t * 0.55)
            * SCREEN_WIDTH
            * 0.018
        )

        center_y = (
            SCREEN_HEIGHT / 2
            + math.cos(t * 0.47)
            * SCREEN_HEIGHT
            * 0.014
        )

        # Cinematic shake
        center_x += (
            math.sin(t * 6.0)
            * 4.0
            * intensity
        )

        center_y += (
            math.cos(t * 5.0)
            * 3.0
            * intensity
        )

        # Intro zoom
        cycle = elapsed % 8.0

        if cycle < 1.7:

            progress = cycle / 1.7

            zoom = (
                0.08
                + ease_out_back(progress)
                * 0.92
            )

        else:

            zoom = (
                1.0
                + math.sin(t * 2.4)
                * 0.035
            )

        # Dynamic hue
        hue = (
            t * 85
            + math.sin(t * 0.5)
            * 40
        )

        # Text
        font_size = int(
            min(
                SCREEN_WIDTH,
                SCREEN_HEIGHT
            )
            * 0.105
        )

        draw_text(
            screen,
            message,
            center_x,
            center_y,
            font_size,
            hue,
            zoom,
            math.sin(t * 1.5) * 1.4,
            t
        )

        # Flash
        flash_value = (
            math.sin(t * math.pi * 0.8)
            ** 24
        )

        if flash_value > 0.3:

            alpha = int(
                clamp(
                    flash_value
                    * 30
                    * intensity,
                    0,
                    40
                )
            )

            flash = pygame.Surface(
                (
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT
                )
            )

            flash.fill(WHITE)

            flash.set_alpha(
                alpha
            )

            screen.blit(
                flash,
                (
                    0,
                    0
                )
            )

        # Controls
        hud_font = pygame.font.Font(
            FONT_NAME,
            16
        )

        hud = hud_font.render(
            "ESC EXIT   R NEW MESSAGE   "
            "SPACE PAUSE   "
            "LEFT/RIGHT SPEED   "
            "UP/DOWN INTENSITY",
            True,
            (
                70,
                70,
                70
            )
        )

        screen.blit(
            hud,
            (
                15,
                SCREEN_HEIGHT
                - hud.get_height()
                - 12
            )
        )

        pygame.display.flip()


# ============================================================
# MAIN
# ============================================================

def main():

    while True:

        message = input_screen()

        animation_screen(
            message
        )


if __name__ == "__main__":

    try:

        main()

    except Exception as error:

        pygame.quit()

        # Make sure errors are visible during testing.
        print("")
        print("Extreme Message Animator error:")
        print(str(error))
        print("")

        raise
