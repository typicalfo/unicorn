import time
import random
import math
from picounicorn import PicoUnicorn
from picographics import PicoGraphics, DISPLAY_UNICORN_PACK

picounicorn = PicoUnicorn()
graphics = PicoGraphics(display=DISPLAY_UNICORN_PACK)

WIDTH = picounicorn.get_width()
HEIGHT = picounicorn.get_height()

def draw_matrix():
    if not hasattr(draw_matrix, "drops"):
        draw_matrix.drops = [None] * WIDTH
        draw_matrix.green_pens = [graphics.create_pen(0, int(255 * (i / 4)), 0) for i in range(5)]

    graphics.set_pen(graphics.create_pen(0, 0, 0))
    graphics.clear()

    for x in range(WIDTH):
        drop = draw_matrix.drops[x]
        if drop is None or drop['y'] > HEIGHT + drop['length']:
            if random.random() < 0.2:  # Adjusted chance for small height
                length = random.randint(2, HEIGHT)
                drop = {'y': 0, 'length': length}
                draw_matrix.drops[x] = drop
            else:
                continue

        # Draw the drop with fading trail
        for i in range(drop['length']):
            yy = drop['y'] - i
            if 0 <= yy < HEIGHT:
                brightness = min(4, drop['length'] - i - 1)
                graphics.set_pen(draw_matrix.green_pens[brightness])
                graphics.pixel(x, yy)

        drop['y'] += 1

def draw_old_school():
    if not hasattr(draw_old_school, "ball_x"):
        draw_old_school.ball_x = WIDTH // 2
        draw_old_school.ball_y = HEIGHT // 2
        draw_old_school.vx = 1
        draw_old_school.vy = 1
        draw_old_school.color = graphics.create_pen(255, 255, 255)

    graphics.set_pen(graphics.create_pen(0, 0, 0))
    graphics.clear()

    graphics.set_pen(draw_old_school.color)
    graphics.pixel(draw_old_school.ball_x, draw_old_school.ball_y)

    # Update position
    draw_old_school.ball_x += draw_old_school.vx
    draw_old_school.ball_y += draw_old_school.vy

    if draw_old_school.ball_x <= 0 or draw_old_school.ball_x >= WIDTH - 1:
        draw_old_school.vx = -draw_old_school.vx

    if draw_old_school.ball_y <= 0 or draw_old_school.ball_y >= HEIGHT - 1:
        draw_old_school.vy = -draw_old_school.vy

def draw_doom():
    if not hasattr(draw_doom, "heat"):
        draw_doom.heat = [[0 for _ in range(HEIGHT)] for _ in range(WIDTH)]
        # Doom fire palette approximation
        draw_doom.colors = [
            graphics.create_pen(0, 0, 0),
            graphics.create_pen(50, 0, 0),
            graphics.create_pen(100, 0, 0),
            graphics.create_pen(200, 50, 0),
            graphics.create_pen(255, 100, 0),
            graphics.create_pen(255, 200, 0),
            graphics.create_pen(255, 255, 100)
        ]

    # Seed the bottom row
    for x in range(WIDTH):
        draw_doom.heat[x][HEIGHT - 1] = random.randint(0, len(draw_doom.colors) - 1)

    # Propagate fire upwards with decay
    for y in range(HEIGHT - 2, -1, -1):
        for x in range(WIDTH):
            below = draw_doom.heat[x][y + 1]
            left = draw_doom.heat[x - 1][y + 1] if x > 0 else below
            right = draw_doom.heat[x + 1][y + 1] if x < WIDTH - 1 else below
            avg = (below + left + right + below) // 4
            draw_doom.heat[x][y] = max(0, avg - random.randint(0, 1))  # Random decay for flicker

    # Draw
    for x in range(WIDTH):
        for y in range(HEIGHT):
            graphics.set_pen(draw_doom.colors[draw_doom.heat[x][y]])
            graphics.pixel(x, y)

def draw_disco():
    for x in range(WIDTH):
        for y in range(HEIGHT):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            pen = graphics.create_pen(r, g, b)
            graphics.set_pen(pen)
            graphics.pixel(x, y)

# Mode definitions
modes = {
    "matrix": draw_matrix,
    "old_school": draw_old_school,
    "doom": draw_doom,
    "disco": draw_disco,
}

# Button mappings
button_to_mode = {
    PicoUnicorn.BUTTON_A: "matrix",
    PicoUnicorn.BUTTON_B: "old_school",
    PicoUnicorn.BUTTON_X: "doom",
    PicoUnicorn.BUTTON_Y: "disco",
}

current_mode = "matrix"

print("Controls:")
print("Button A: Matrix style rain")
print("Button B: Old school bouncing ball")
print("Button X: Doom fire animation")
print("Button Y: Disco party lights")

while True:
    # Check for button presses to switch modes
    for button, md in button_to_mode.items():
        if picounicorn.is_pressed(button):
            if current_mode != md:
                current_mode = md
                # Reset states by deleting attributes
                for mode_func in modes.values():
                    if hasattr(mode_func, "drops"):
                        del mode_func.drops
                    if hasattr(mode_func, "ball_x"):
                        del mode_func.ball_x
                        del mode_func.ball_y
                        del mode_func.vx
                        del mode_func.vy
                    if hasattr(mode_func, "heat"):
                        del mode_func.heat
            while picounicorn.is_pressed(button):
                time.sleep(0.01)
            break

    # Execute the current mode
    modes[current_mode]()

    picounicorn.update(graphics)

    time.sleep(1.0 / 60)