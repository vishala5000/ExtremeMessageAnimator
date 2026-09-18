import math
import random
import sys
import pygame

pygame.init()
pygame.font.init()

APP_NAME = "Extreme Message Animator"
FPS = 60
MAX_MESSAGE_LENGTH = 5000

info = pygame.display.Info()
SCREEN_W = info.current_w
SCREEN_H = info.current_h

pygame.display.set_caption(APP_NAME)

FONT_PATH = pygame.font.match_font("arial") or pygame.font.get_default_font()

clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# =========================================================
# COLOR
# =========================================================

def hsv_to_rgb(h, s=1.0, v=1.0):
    h %= 360.0

    c = v * s
    x = c * (1 - abs((h / 60.0) % 2 - 1))
    m = v - c

    if h < 60:
        r, g, b = c, x, 0
    elif h < 120:
        r, g, b = x, c, 0
    elif h < 180:
        r, g, b = 0, c, x
    elif h < 240:
        r, g, b = 0, x, c
    elif h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x

    return (
        int((r + m) * 255),
        int((g + m) * 255),
        int((b + m) * 255),
    )


# =========================================================
# HELPERS
# =========================================================

def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


def wrap_text(text, font, max_width):
    words = text.split()
    if not words:
        return [""]

    lines = []
    current = words[0]

    for word in words[1:]:
        candidate = current + " " + word

        if font.size(candidate)[0] <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word

    lines.append(current)
    return lines


def ease_out_back(x):
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def ease_in_out(x):
    x = clamp(x, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)


# =========================================================
# PARTICLES
# =========================================================

class Particle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.reset(random.uniform(0, 1))

    def reset(self, depth=None):
        self.x = random.uniform(-self.width * 0.2, self.width * 1.2)
        self.y = random.uniform(-self.height * 0.2, self.height * 1.2)

        self.depth = (
            random.uniform(0.15, 1.0)
            if depth is None
            else depth
        )

        self.speed = random.uniform(0.3, 2.2)
        self.size = random.uniform(1.0, 4.5)
        self.hue = random.uniform(0, 360)
        self.alpha = random.randint(80, 230)

    def update(self, dt, speed_multiplier):
        cx = self.width * 0.5
        cy = self.height * 0.5

        dx = self.x - cx
        dy = self.y - cy

        self.x += dx * self.depth * self.speed * dt * 0.12
        self.y += dy * self.depth * self.speed * dt * 0.12

        self.depth += (
            dt * 0.10 * speed_multiplier * self.speed
        )

        self.hue += dt * 55

        if (
            self.x < -self.width * 0.4
            or self.x > self.width * 1.4
            or self.y < -self.height * 0.4
            or self.y > self.height * 1.4
            or self.depth > 1.8
        ):
            self.reset(0.15)

    def draw(self, surface):
        size = max(
            1,
            int(self.size * (0.5 + self.depth * 1.7))
        )

        color = hsv_to_rgb(
            self.hue,
            0.9,
            1.0
        )

        pygame.draw.circle(
            surface,
            color,
            (int(self.x), int(self.y)),
            size
        )


# =========================================================
# LIGHT STREAKS
# =========================================================

class LightStreak:
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
            self.width * 0.30
        )

        self.speed = random.uniform(
            self.width * 0.25,
            self.width * 0.9
        )

        self.hue = random.uniform(0, 360)

        self.angle = random.uniform(
            -0.08,
            0.08
        )

    def update(self, dt, speed_multiplier):
        self.x += (
            self.speed
            * dt
            * speed_multiplier
        )

        self.hue += dt * 45

        if self.x > self.width + self.length:
            self.reset()
            self.x = -self.length

    def draw(self, surface):
        color = hsv_to_rgb(
            self.hue,
            0.95,
            1
        )

        dx = math.cos(self.angle) * self.length
        dy = math.sin(self.angle) * self.length

        pygame.draw.line(
            surface,
            color,
            (int(self.x), int(self.y)),
            (
                int(self.x - dx),
                int(self.y - dy)
            ),
            2
        )


# =========================================================
# BURST PARTICLES
# =========================================================

class Burst:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = width * 0.5
        self.y = height * 0.5
        self.particles = []

        for _ in range(140):
            angle = random.uniform(0, math.tau)
            speed = random.uniform(150, 900)

            self.particles.append({
                "x": self.x,
                "y": self.y,
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "life": random.uniform(0.5, 1.8),
                "maxlife": 1.8,
                "size": random.uniform(1, 5),
                "hue": random.uniform(0, 360),
            })

    def update(self, dt):
        alive = False

        for p in self.particles:
            if p["life"] > 0:
                alive = True

                p["x"] += p["vx"] * dt
                p["y"] += p["vy"] * dt

                p["vx"] *= 0.985
                p["vy"] *= 0.985

                p["life"] -= dt

        return alive

    def draw(self, surface):
        for p in self.particles:
            if p["life"] <= 0:
                continue

            alpha = int(
                clamp(
                    p["life"] / p["maxlife"],
                    0,
                    1
                ) * 255
            )

            color = hsv_to_rgb(
                p["hue"],
                1,
                1
            )

            pygame.draw.circle(
                surface,
                color,
                (
                    int(p["x"]),
                    int(p["y"])
                ),
                max(
                    1,
                    int(p["size"])
                )
            )


# =========================================================
# ENERGY RINGS
# =========================================================

def draw_energy_rings(surface, t, intensity):
    cx = SCREEN_W * 0.5
    cy = SCREEN_H * 0.5

    base = min(
        SCREEN_W,
        SCREEN_H
    )

    for i in range(12):
        phase = (
            t * (0.5 + i * 0.035)
            + i * 0.8
        )

        radius = (
            base * (0.10 + i * 0.045)
            + math.sin(phase) * 12
        )

        radius *= intensity

        rect = pygame.Rect(
            int(cx - radius),
            int(cy - radius),
            int(radius * 2),
            int(radius * 2)
        )

        color = hsv_to_rgb(
            t * 55 + i * 30,
            0.95,
            0.8
        )

        start = phase
        end = phase + math.pi * (
            0.8 + 0.5 * math.sin(phase * 0.7)
        )

        pygame.draw.arc(
            surface,
            color,
            rect,
            start,
            end,
            2
        )


# =========================================================
# TEXT RENDERING
# =========================================================

def render_text_lines(
    text,
    font_size,
    max_width
):
    font_size = int(font_size)

    font = pygame.font.Font(
        FONT_PATH,
        max(20, font_size)
    )

    lines = wrap_text(
        text,
        font,
        max_width
    )

    while (
        len(lines) > 8
        and font_size > 24
    ):
        font_size -= 4

        font = pygame.font.Font(
            FONT_PATH,
            font_size
        )

        lines = wrap_text(
            text,
            font,
            max_width
        )

    return font, lines


def draw_text_with_glow(
    surface,
    text,
    center_x,
    center_y,
    font_size,
    hue,
    scale,
    rotation,
    wave_time
):

    max_width = int(
        SCREEN_W * 0.82
    )

    font, lines = render_text_lines(
        text,
        font_size,
        max_width
    )

    line_height = font.get_linesize()

    total_height = (
        len(lines) * line_height
    )

    top = center_y - total_height / 2

    # Individual-line rendering
    for line_index, line in enumerate(lines):

        line_surface = font.render(
            line,
            True,
            hsv_to_rgb(
                hue + line_index * 24,
                1,
                1
            )
        )

        # Per-line movement
        wave = math.sin(
            wave_time * 2.0
            + line_index * 0.7
        ) * 8

        # Individual letter-like energy effect
        pulse = (
            1
            + math.sin(
                wave_time * 3
                + line_index
            ) * 0.025
        )

        final_scale = (
            scale
            * pulse
        )

        if final_scale < 0.05:
            final_scale = 0.05

        transformed = pygame.transform.rotozoom(
            line_surface,
            rotation
            + math.sin(
                wave_time * 1.4
                + line_index
            ) * 0.8,
            final_scale
        )

        rect = transformed.get_rect(
            center=(
                int(center_x),
                int(
                    top
                    + line_index * line_height
                    + line_height / 2
                    + wave
                )
            )
        )

        # Glow layers
        for extra, alpha in [
            (36, 18),
            (24, 28),
            (14, 45),
            (7, 75),
        ]:

            glow = pygame.transform.smoothscale(
                transformed,
                (
                    transformed.get_width() + extra,
                    transformed.get_height() + extra
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

        # Main text
        surface.blit(
            transformed,
            rect
        )

    return total_height


# =========================================================
# FULLSCREEN ANIMATION
# =========================================================

def animation_screen(message):

    global SCREEN_W, SCREEN_H

    pygame.display.set_mode(
        (SCREEN_W, SCREEN_H),
        pygame.FULLSCREEN
        | pygame.DOUBLEBUF
    )

    particles = [
        Particle(SCREEN_W, SCREEN_H)
        for _ in range(260)
    ]

    streaks = [
        LightStreak(SCREEN_W, SCREEN_H)
        for _ in range(40)
    ]

    bursts = []

    start_ticks = pygame.time.get_ticks()

    paused = False

    speed = 1.0

    intensity = 1.0

    running = True

    while running:

        dt = clock.tick(FPS) / 1000.0

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

        if not paused:

            elapsed = (
                pygame.time.get_ticks()
                - start_ticks
            ) / 1000.0

            t = elapsed * speed

            # ---------------------------------------------
            # Background
            # ---------------------------------------------

            screen = pygame.display.get_surface()

            screen.fill(BLACK)

            # ---------------------------------------------
            # Subtle animated radial glow
            # ---------------------------------------------

            glow_surface = pygame.Surface(
                (SCREEN_W, SCREEN_H),
                pygame.SRCALPHA
            )

            cx = SCREEN_W // 2
            cy = SCREEN_H // 2

            for radius in range(
                int(min(SCREEN_W, SCREEN_H) * 0.55),
                20,
                -45
            ):

                alpha = int(
                    2
                    + 8
                    * (
                        radius
                        / min(
                            SCREEN_W,
                            SCREEN_H
                        )
                    )
                )

                color = hsv_to_rgb(
                    t * 35
                    + radius * 0.2,
                    1,
                    1
                )

                pygame.draw.circle(
                    glow_surface,
                    (
                        color[0],
                        color[1],
                        color[2],
                        alpha
                    ),
                    (cx, cy),
                    radius
                )

            screen.blit(
                glow_surface,
                (0, 0)
            )

            # ---------------------------------------------
            # Particles
            # ---------------------------------------------

            for particle in particles:
                particle.update(
                    dt,
                    speed
                )
                particle.draw(screen)

            # ---------------------------------------------
            # Light streaks
            # ---------------------------------------------

            for streak in streaks:
                streak.update(
                    dt,
                    speed
                )
                streak.draw(screen)

            # ---------------------------------------------
            # Rings
            # ---------------------------------------------

            draw_energy_rings(
                screen,
                t,
                intensity
            )

            # ---------------------------------------------
            # Cinematic camera movement
            # ---------------------------------------------

            shake_amount = (
                math.sin(t * 6.0)
                * 5.0
                * intensity
            )

            center_x = (
                SCREEN_W / 2
                + math.sin(t * 0.55)
                * SCREEN_W
                * 0.018
                + shake_amount
            )

            center_y = (
                SCREEN_H / 2
                + math.cos(t * 0.47)
                * SCREEN_H
                * 0.014
            )

            # ---------------------------------------------
            # Intro zoom
            # ---------------------------------------------

            cycle = elapsed % 9.0

            if cycle < 1.8:

                progress = cycle / 1.8

                zoom = (
                    0.08
                    + ease_out_back(progress)
                    * 0.92
                )

            else:

                zoom = (
                    1.0
                    + math.sin(
                        t * 2.4
                    ) * 0.035
                )

            # ---------------------------------------------
            # Periodic explosion
            # ---------------------------------------------

            if (
                cycle < 0.08
                and not bursts
            ):
                bursts.append(
                    Burst(
                        SCREEN_W,
                        SCREEN_H
                    )
                )

            if cycle > 0.15:
                # Allow another burst next cycle
                if len(bursts) > 0:
                    bursts = [
                        b for b in bursts
                        if b.update(dt)
                    ]

            for burst in bursts:
                burst.draw(screen)

            # ---------------------------------------------
            # Dynamic hue
            # ---------------------------------------------

            hue = (
                t * 85
                + math.sin(t * 0.4) * 45
            )

            # ---------------------------------------------
            # Text
            # ---------------------------------------------

            base_size = int(
                min(
                    SCREEN_W,
                    SCREEN_H
                ) * 0.105
            )

            draw_text_with_glow(
                screen,
                message,
                center_x,
                center_y,
                base_size,
                hue,
                zoom,
                math.sin(t * 1.5) * 1.4,
                t
            )

            # ---------------------------------------------
            # Cinematic flash
            # ---------------------------------------------

            flash_phase = (
                math.sin(t * math.pi * 0.85)
                ** 30
            )

            if flash_phase > 0.35:

                alpha = int(
                    clamp(
                        flash_phase * 38
                        * intensity,
                        0,
                        42
                    )
                )

                flash = pygame.Surface(
                    (SCREEN_W, SCREEN_H),
                    pygame.SRCALPHA
                )

                flash.fill(
                    (
                        255,
                        255,
                        255,
                        alpha
                    )
                )

                screen.blit(
                    flash,
                    (0, 0)
                )

            # ---------------------------------------------
            # HUD
            # ---------------------------------------------

            hud_font = pygame.font.Font(
                FONT_PATH,
                17
            )

            hud = hud_font.render(
                "ESC EXIT   R NEW MESSAGE   "
                "SPACE PAUSE   ← → SPEED   ↑ ↓ INTENSITY",
                True,
                (75, 75, 75)
            )

            screen.blit(
                hud,
                (
                    20,
                    SCREEN_H
                    - hud.get_height()
                    - 15
                )
            )

            pygame.display.flip()

        else:

            # Pause screen
            overlay = pygame.Surface(
                (SCREEN_W, SCREEN_H),
                pygame.SRCALPHA
            )

            overlay.fill(
                (0, 0, 0, 150)
            )

            screen = pygame.display.get_surface()

            screen.blit(
                overlay,
                (0, 0)
            )

            pause_font = pygame.font.Font(
                FONT_PATH,
                50
            )

            pause_text = pause_font.render(
                "PAUSED",
                True,
                WHITE
            )

            rect = pause_text.get_rect(
                center=(
                    SCREEN_W // 2,
                    SCREEN_H // 2
                )
            )

            screen.blit(
                pause_text,
                rect
            )

            pygame.display.flip()


# =========================================================
# INPUT WINDOW
# =========================================================

def input_screen():

    width = min(
        SCREEN_W,
        1250
    )

    height = min(
        SCREEN_H,
        820
    )

    pygame.display.set_mode(
        (width, height),
        pygame.RESIZABLE
    )

    window = pygame.display.get_surface()

    title_font = pygame.font.Font(
        FONT_PATH,
        48
    )

    subtitle_font = pygame.font.Font(
        FONT_PATH,
        25
    )

    input_font = pygame.font.Font(
        FONT_PATH,
        28
    )

    button_font = pygame.font.Font(
        FONT_PATH,
        25
    )

    message = ""

    running = True

    while running:

        dt = clock.tick(FPS) / 1000.0

        width, height = window.get_size()

        t = pygame.time.get_ticks() / 1000.0

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if event.type == pygame.VIDEORESIZE:

                width, height = event.w, event.h

                window = pygame.display.set_mode(
                    (width, height),
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

                mx, my = event.pos

                button_rect = pygame.Rect(
                    width // 2 - 190,
                    height - 145,
                    380,
                    70
                )

                if button_rect.collidepoint(
                    mx,
                    my
                ):

                    if message.strip():
                        return message.strip()

        window.fill(
            (3, 3, 7)
        )

        # ---------------------------------------------
        # Animated background
        # ---------------------------------------------

        for i in range(70):

            angle = (
                t * 0.12
                + i * math.tau / 70
            )

            radius_x = width * 0.46
            radius_y = height * 0.42

            x = (
                width / 2
                + math.cos(angle) * radius_x
            )

            y = (
                height / 2
                + math.sin(angle * 1.13)
                * radius_y
            )

            color = hsv_to_rgb(
                t * 65 + i * 7,
                1,
                1
            )

            pygame.draw.circle(
                window,
                color,
                (int(x), int(y)),
                2
            )

        # ---------------------------------------------
        # Title
        # ---------------------------------------------

        title_color = hsv_to_rgb(
            t * 80,
            1,
            1
        )

        title = title_font.render(
            "EXTREME MESSAGE ANIMATOR",
            True,
            title_color
        )

        title_rect = title.get_rect(
            center=(width // 2, 100)
        )

        window.blit(
            title,
            title_rect
        )

        subtitle = subtitle_font.render(
            "Turn any message into a cinematic fullscreen animation",
            True,
            (210, 210, 220)
        )

        subtitle_rect = subtitle.get_rect(
            center=(width // 2, 165)
        )

        window.blit(
            subtitle,
            subtitle_rect
        )

        # ---------------------------------------------
        # Input box
        # ---------------------------------------------

        box_width = min(
            width - 80,
            950
        )

        box_height = 210

        box = pygame.Rect(
            width // 2 - box_width // 2,
            height // 2 - 125,
            box_width,
            box_height
        )

        pygame.draw.rect(
            window,
            (12, 12, 18),
            box,
            border_radius=20
        )

        border_color = hsv_to_rgb(
            t * 75,
            1,
            1
        )

        pygame.draw.rect(
            window,
            border_color,
            box,
            3,
            border_radius=20
        )

        if message:

            lines = wrap_text(
                message,
                input_font,
                box.width - 40
            )

            visible_lines = lines[-5:]

            y = box.y + 22

            for line in visible_lines:

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
                "Type your message here...",
                True,
                (90, 90, 100)
            )

            window.blit(
                placeholder,
                (
                    box.x + 20,
                    box.y + 25
                )
            )

        # Character count
        count = subtitle_font.render(
            f"{len(message)} / {MAX_MESSAGE_LENGTH}",
            True,
            (100, 100, 110)
        )

        window.blit(
            count,
            (
                box.right - count.get_width() - 18,
                box.bottom - count.get_height() - 12
            )
        )

        # ---------------------------------------------
        # Start button
        # ---------------------------------------------

        button = pygame.Rect(
            width // 2 - 190,
            height - 145,
            380,
            70
        )

        pygame.draw.rect(
            window,
            border_color,
            button,
            border_radius=18
        )

        button_text = button_font.render(
            "START ANIMATION",
            True,
            BLACK
        )

        button_text_rect = button_text.get_rect(
            center=button.center
        )

        window.blit(
            button_text,
            button_text_rect
        )

        hint = pygame.font.Font(
            FONT_PATH,
            18
        ).render(
            "Press ENTER to start • ESC to exit",
            True,
            (100, 100, 110)
        )

        hint_rect = hint.get_rect(
            center=(
                width // 2,
                height - 40
            )
        )

        window.blit(
            hint,
            hint_rect
        )

        pygame.display.flip()


# =========================================================
# MAIN
# =========================================================

def main():

    while True:

        message = input_screen()

        animation_screen(
            message
        )


if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:

        pygame.quit()
        sys.exit(0)
