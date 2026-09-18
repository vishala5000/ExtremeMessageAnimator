import math
import random
import sys
import pygame

pygame.init()
pygame.font.init()

APP_NAME = "Extreme Message Animator"

# ---------------------------------------------------------
# DISPLAY
# ---------------------------------------------------------

info = pygame.display.Info()
WINDOW_WIDTH = info.current_w
WINDOW_HEIGHT = info.current_h

screen = pygame.display.set_mode(
    (WINDOW_WIDTH, WINDOW_HEIGHT),
    pygame.FULLSCREEN | pygame.DOUBLEBUF
)

pygame.display.set_caption(APP_NAME)

clock = pygame.time.Clock()

# ---------------------------------------------------------
# COLORS
# ---------------------------------------------------------

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# ---------------------------------------------------------
# FONT
# ---------------------------------------------------------

FONT_PATH = pygame.font.match_font("arial")

if FONT_PATH:
    BASE_FONT = FONT_PATH
else:
    BASE_FONT = None


# ---------------------------------------------------------
# HSV COLOR
# ---------------------------------------------------------

def hsv_to_rgb(h, s=1.0, v=1.0):
    h = h % 360.0

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
        int((b + m) * 255)
    )


# ---------------------------------------------------------
# TEXT WRAPPING
# ---------------------------------------------------------

def wrap_text(text, font, max_width):
    words = text.split()

    if not words:
        return [""]

    lines = []
    current = words[0]

    for word in words[1:]:
        test = current + " " + word

        if font.size(test)[0] <= max_width:
            current = test
        else:
            lines.append(current)
            current = word

    lines.append(current)

    return lines


# ---------------------------------------------------------
# PARTICLES
# ---------------------------------------------------------

class Particle:

    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.uniform(0, WINDOW_WIDTH)
        self.y = random.uniform(0, WINDOW_HEIGHT)

        angle = random.uniform(0, math.tau)
        speed = random.uniform(0.3, 2.5)

        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        self.radius = random.uniform(1.0, 4.0)

        self.hue = random.uniform(0, 360)

        self.alpha = random.randint(70, 220)

    def update(self, dt):
        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60

        self.hue += dt * 35

        if (
            self.x < -20
            or self.x > WINDOW_WIDTH + 20
            or self.y < -20
            or self.y > WINDOW_HEIGHT + 20
        ):
            self.reset()

    def draw(self, surface):
        color = hsv_to_rgb(self.hue, 1, 1)

        glow = pygame.Surface(
            (int(self.radius * 8), int(self.radius * 8)),
            pygame.SRCALPHA
        )

        center = glow.get_width() // 2

        pygame.draw.circle(
            glow,
            (*color, 25),
            (center, center),
            int(self.radius * 4)
        )

        pygame.draw.circle(
            glow,
            (*color, self.alpha),
            (center, center),
            max(1, int(self.radius))
        )

        surface.blit(
            glow,
            (
                int(self.x - center),
                int(self.y - center)
            )
        )


particles = [
    Particle()
    for _ in range(220)
]


# ---------------------------------------------------------
# LIGHT STREAKS
# ---------------------------------------------------------

class Streak:

    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.uniform(-WINDOW_WIDTH, WINDOW_WIDTH)
        self.y = random.uniform(0, WINDOW_HEIGHT)

        self.length = random.uniform(80, 400)
        self.speed = random.uniform(5, 18)

        self.hue = random.uniform(0, 360)

        self.angle = random.uniform(-0.15, 0.15)

    def update(self, dt):
        self.x += self.speed * dt * 60

        self.hue += dt * 40

        if self.x > WINDOW_WIDTH + self.length:
            self.reset()
            self.x = -self.length

    def draw(self, surface):
        color = hsv_to_rgb(self.hue, 1, 1)

        dx = math.cos(self.angle) * self.length
        dy = math.sin(self.angle) * self.length

        start = (
            int(self.x),
            int(self.y)
        )

        end = (
            int(self.x - dx),
            int(self.y - dy)
        )

        pygame.draw.line(
            surface,
            color,
            start,
            end,
            2
        )


streaks = [
    Streak()
    for _ in range(28)
]


# ---------------------------------------------------------
# ENERGY RINGS
# ---------------------------------------------------------

def draw_energy_rings(surface, t):

    cx = WINDOW_WIDTH // 2
    cy = WINDOW_HEIGHT // 2

    max_radius = min(WINDOW_WIDTH, WINDOW_HEIGHT) * 0.48

    for i in range(9):

        phase = t * (0.7 + i * 0.04) + i

        radius = (
            max_radius * (0.25 + i * 0.085)
            + math.sin(phase) * 15
        )

        hue = t * 55 + i * 40

        color = hsv_to_rgb(
            hue,
            1,
            1
        )

        rect = pygame.Rect(
            cx - radius,
            cy - radius,
            radius * 2,
            radius * 2
        )

        start_angle = phase
        end_angle = phase + math.pi * 1.5

        pygame.draw.arc(
            surface,
            color,
            rect,
            start_angle,
            end_angle,
            2
        )


# ---------------------------------------------------------
# GLOW TEXT
# ---------------------------------------------------------

def draw_glowing_text(
    surface,
    text,
    center,
    font_size,
    hue,
    pulse,
    angle
):

    # Pulse
    scale = 1.0 + math.sin(pulse) * 0.035

    actual_size = max(
        20,
        int(font_size * scale)
    )

    font = pygame.font.Font(
        BASE_FONT,
        actual_size
    )

    lines = wrap_text(
        text,
        font,
        int(WINDOW_WIDTH * 0.82)
    )

    # Reduce size for long messages
    while len(lines) > 8 and actual_size > 30:

        actual_size -= 4

        font = pygame.font.Font(
            BASE_FONT,
            actual_size
        )

        lines = wrap_text(
            text,
            font,
            int(WINDOW_WIDTH * 0.82)
        )

    color = hsv_to_rgb(
        hue,
        0.95,
        1
    )

    line_height = font.get_linesize()

    total_height = len(lines) * line_height

    y = center[1] - total_height / 2

    # Create large transparent glow surface
    glow_surface = pygame.Surface(
        (WINDOW_WIDTH, WINDOW_HEIGHT),
        pygame.SRCALPHA
    )

    for line in lines:

        text_surface = font.render(
            line,
            True,
            color
        )

        rect = text_surface.get_rect(
            center=(center[0], int(y + line_height / 2))
        )

        # Multiple glow layers
        for blur_size, alpha in [
            (20, 18),
            (12, 28),
            (7, 45)
        ]:

            glow = pygame.transform.smoothscale(
                text_surface,
                (
                    text_surface.get_width() + blur_size,
                    text_surface.get_height() + blur_size
                )
            )

            glow.set_alpha(alpha)

            glow_rect = glow.get_rect(
                center=rect.center
            )

            glow_surface.blit(
                glow,
                glow_rect
            )

        y += line_height

    surface.blit(
        glow_surface,
        (0, 0)
    )

    # Main text
    y = center[1] - total_height / 2

    for line in lines:

        text_surface = font.render(
            line,
            True,
            color
        )

        rect = text_surface.get_rect(
            center=(center[0], int(y + line_height / 2))
        )

        rotated = pygame.transform.rotozoom(
            text_surface,
            angle,
            1.0
        )

        rotated_rect = rotated.get_rect(
            center=rect.center
        )

        surface.blit(
            rotated,
            rotated_rect
        )

        y += line_height


# ---------------------------------------------------------
# FLASH EFFECT
# ---------------------------------------------------------

def draw_flash(surface, t):

    pulse = (math.sin(t * 2.7) + 1) / 2

    alpha = int(
        max(0, (pulse - 0.94) * 800)
    )

    if alpha > 0:

        overlay = pygame.Surface(
            (WINDOW_WIDTH, WINDOW_HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill(
            (255, 255, 255, min(alpha, 35))
        )

        surface.blit(
            overlay,
            (0, 0)
        )


# ---------------------------------------------------------
# ANIMATION
# ---------------------------------------------------------

def run_animation(message):

    running = True

    start_time = pygame.time.get_ticks()

    while running:

        dt = clock.tick(60) / 1000.0

        current_time = pygame.time.get_ticks()

        t = (current_time - start_time) / 1000.0

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_r:
                    running = False

        # Black background
        screen.fill(BLACK)

        # Update particles
        for particle in particles:
            particle.update(dt)
            particle.draw(screen)

        # Update streaks
        for streak in streaks:
            streak.update(dt)
            streak.draw(screen)

        # Energy rings
        draw_energy_rings(
            screen,
            t
        )

        # Dynamic center movement
        cx = (
            WINDOW_WIDTH / 2
            + math.sin(t * 0.8) * WINDOW_WIDTH * 0.025
        )

        cy = (
            WINDOW_HEIGHT / 2
            + math.cos(t * 0.65) * WINDOW_HEIGHT * 0.025
        )

        # Constant color cycling
        hue = t * 75

        # Subtle rotation
        rotation = math.sin(t * 1.7) * 1.5

        # Text
        draw_glowing_text(
            screen,
            message,
            (cx, cy),
            max(
                60,
                int(min(WINDOW_WIDTH, WINDOW_HEIGHT) * 0.105)
            ),
            hue,
            t * 2.8,
            rotation
        )

        # Flash
        draw_flash(
            screen,
            t
        )

        # Small corner information
        small_font = pygame.font.Font(
            BASE_FONT,
            18
        )

        hint = small_font.render(
            "ESC  EXIT    •    R  NEW MESSAGE",
            True,
            (90, 90, 90)
        )

        screen.blit(
            hint,
            (
                WINDOW_WIDTH - hint.get_width() - 25,
                WINDOW_HEIGHT - hint.get_height() - 20
            )
        )

        pygame.display.flip()


# ---------------------------------------------------------
# MESSAGE INPUT SCREEN
# ---------------------------------------------------------

def message_screen():

    pygame.display.set_mode(
        (
            min(WINDOW_WIDTH, 1200),
            min(WINDOW_HEIGHT, 800)
        )
    )

    input_width = 850
    input_height = 180

    window = pygame.display.get_surface()

    width, height = window.get_size()

    font_title = pygame.font.Font(
        BASE_FONT,
        42
    )

    font_input = pygame.font.Font(
        BASE_FONT,
        30
    )

    font_button = pygame.font.Font(
        BASE_FONT,
        28
    )

    message = ""

    running = True

    while running:

        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

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

                    if event.unicode and len(message) < 5000:
                        message += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:

                mx, my = event.pos

                button_rect = pygame.Rect(
                    width // 2 - 150,
                    height // 2 + 130,
                    300,
                    65
                )

                if button_rect.collidepoint(mx, my):

                    if message.strip():
                        return message.strip()

        window.fill(
            (5, 5, 8)
        )

        # Animated background dots
        t = pygame.time.get_ticks() / 1000.0

        for i in range(35):

            x = (
                width / 2
                + math.cos(t * 0.3 + i) * width * 0.45
            )

            y = (
                height / 2
                + math.sin(t * 0.5 + i * 2) * height * 0.45
            )

            color = hsv_to_rgb(
                t * 60 + i * 12,
                1,
                1
            )

            pygame.draw.circle(
                window,
                color,
                (int(x), int(y)),
                2
            )

        title_color = hsv_to_rgb(
            t * 70,
            1,
            1
        )

        title = font_title.render(
            "EXTREME MESSAGE ANIMATOR",
            True,
            title_color
        )

        title_rect = title.get_rect(
            center=(width // 2, 120)
        )

        window.blit(
            title,
            title_rect
        )

        subtitle = font_input.render(
            "Enter your message",
            True,
            WHITE
        )

        subtitle_rect = subtitle.get_rect(
            center=(width // 2, 205)
        )

        window.blit(
            subtitle,
            subtitle_rect
        )

        input_rect = pygame.Rect(
            width // 2 - input_width // 2,
            height // 2 - input_height // 2,
            input_width,
            input_height
        )

        pygame.draw.rect(
            window,
            (15, 15, 20),
            input_rect,
            border_radius=18
        )

        border_color = hsv_to_rgb(
            t * 80,
            1,
            1
        )

        pygame.draw.rect(
            window,
            border_color,
            input_rect,
            width=3,
            border_radius=18
        )

        display_message = message

        if not display_message:
            display_message = "Type something amazing..."

        text_color = (
            (110, 110, 120)
            if not message
            else WHITE
        )

        # Wrap input preview
        lines = wrap_text(
            display_message,
            font_input,
            input_width - 40
        )

        y = input_rect.y + 25

        for line in lines[-4:]:

            rendered = font_input.render(
                line,
                True,
                text_color
            )

            window.blit(
                rendered,
                (
                    input_rect.x + 20,
                    y
                )
            )

            y += 38

        button_rect = pygame.Rect(
            width // 2 - 150,
            height // 2 + 130,
            300,
            65
        )

        pygame.draw.rect(
            window,
            border_color,
            button_rect,
            border_radius=16
        )

        button_text = font_button.render(
            "START ANIMATION",
            True,
            BLACK
        )

        button_text_rect = button_text.get_rect(
            center=button_rect.center
        )

        window.blit(
            button_text,
            button_text_rect
        )

        hint = pygame.font.Font(
            BASE_FONT,
            18
        ).render(
            "Press ENTER to start",
            True,
            (120, 120, 120)
        )

        hint_rect = hint.get_rect(
            center=(width // 2, height - 40)
        )

        window.blit(
            hint,
            hint_rect
        )

        pygame.display.flip()


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    while True:

        message = message_screen()

        # Restore true fullscreen
        pygame.display.set_mode(
            (
                WINDOW_WIDTH,
                WINDOW_HEIGHT
            ),
            pygame.FULLSCREEN | pygame.DOUBLEBUF
        )

        run_animation(
            message
        )


if __name__ == "__main__":
    main()
