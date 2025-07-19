from picounicorn import PicoUnicorn
from picographics import PicoGraphics, DISPLAY_UNICORN_PACK
import time
import random
import math

# Initialize both PicoUnicorn and PicoGraphics
picounicorn = PicoUnicorn()
graphics = PicoGraphics(display=DISPLAY_UNICORN_PACK)

# Get dimensions
w = picounicorn.get_width()
h = picounicorn.get_height()

# Create base colors
BLACK = graphics.create_pen(0, 0, 0)

# PARTICLE SYSTEM (Enhanced version with that color scheme you liked!)
class Particle:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.x = random.uniform(0, w)
        self.y = random.uniform(0, h)
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.5, 0.5)
        self.life = 1.0
        self.decay = random.uniform(0.01, 0.03)
        self.color_type = random.randint(0, 3)  # Different color schemes
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= self.decay
        
        # Wrap around edges
        if self.x < 0: self.x = w
        if self.x > w: self.x = 0
        if self.y < 0: self.y = h
        if self.y > h: self.y = 0
        
        if self.life <= 0:
            self.reset()
    
    def get_color(self):
        brightness = int(255 * self.life)
        if self.color_type == 0:
            # Orange/yellow fire colors
            return (brightness, brightness // 2, brightness // 4)
        elif self.color_type == 1:
            # Cyan/blue electric
            return (brightness // 4, brightness // 2, brightness)
        elif self.color_type == 2:
            # Purple/magenta
            return (brightness, brightness // 4, brightness // 2)
        else:
            # Green matrix style
            return (0, brightness, brightness // 4)

# Initialize particle system
particles = []

# RETRO GAME ANIMATIONS

# 1. SPACE INVADERS STYLE
def space_invaders():
    """Classic space invaders marching animation"""
    # Simple invader shape (5x3)
    invader1 = [
        [0,1,0,1,0],
        [1,1,1,1,1],
        [1,0,1,0,1]
    ]
    invader2 = [
        [0,1,0,1,0],
        [1,1,1,1,1],
        [0,1,0,1,0]
    ]
    
    for frame in range(100):
        graphics.set_pen(BLACK)
        graphics.clear()
        
        # Animate between two frames
        current_invader = invader1 if (frame // 10) % 2 == 0 else invader2
        
        # Move invaders
        offset_x = (frame // 2) % (w + 5) - 5
        
        # Draw multiple invaders
        for row in range(2):
            for col in range(3):
                x_pos = offset_x + col * 6
                y_pos = row * 4 + 1
                
                # Draw invader
                for y, row_data in enumerate(current_invader):
                    for x, pixel in enumerate(row_data):
                        if pixel and 0 <= x_pos + x < w and 0 <= y_pos + y < h:
                            # Classic green color
                            color = graphics.create_pen(0, 255, 0)
                            graphics.set_pen(color)
                            graphics.pixel(x_pos + x, y_pos + y)
        
        picounicorn.update(graphics)
        time.sleep(0.05)

# 2. PACMAN CHASE
def pacman_chase():
    """Pacman chasing dots with ghost"""
    for frame in range(200):
        graphics.set_pen(BLACK)
        graphics.clear()
        
        # Pacman position
        pac_x = (frame * 0.2) % (w + 4) - 2
        pac_y = h // 2
        
        # Draw dots
        for x in range(0, w, 2):
            if x > pac_x + 2:  # Only draw dots Pacman hasn't eaten
                dot_color = graphics.create_pen(255, 255, 0)
                graphics.set_pen(dot_color)
                graphics.pixel(x, pac_y)
        
        # Draw Pacman (simple circle with mouth)
        pac_color = graphics.create_pen(255, 255, 0)
        graphics.set_pen(pac_color)
        
        # Pacman body
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if abs(dx) + abs(dy) <= 1:  # Simple circle shape
                    px = int(pac_x + dx)
                    py = pac_y + dy
                    if 0 <= px < w and 0 <= py < h:
                        # Don't draw mouth area
                        if not (dx > 0 and dy == 0 and (frame // 5) % 2 == 0):
                            graphics.pixel(px, py)
        
        # Draw ghost following
        ghost_x = int(pac_x - 5)
        if ghost_x >= 0:
            # Ghost colors cycle
            ghost_colors = [(255, 0, 0), (255, 192, 203), (0, 255, 255), (255, 165, 0)]
            r, g, b = ghost_colors[(frame // 20) % 4]
            ghost_color = graphics.create_pen(r, g, b)
            graphics.set_pen(ghost_color)
            
            # Simple ghost shape
            for y in range(3):
                for x in range(3):
                    if ghost_x + x < w:
                        graphics.pixel(ghost_x + x, pac_y - 1 + y)
        
        picounicorn.update(graphics)
        time.sleep(0.03)

# 3. TETRIS FALLING BLOCKS
def tetris_blocks():
    """Falling tetris pieces"""
    # Tetris pieces (simplified)
    pieces = [
        [[1,1,1,1]],  # I piece
        [[1,1],[1,1]],  # O piece
        [[1,1,1],[0,1,0]],  # T piece
        [[1,1,0],[0,1,1]],  # Z piece
    ]
    
    # Colors for pieces
    piece_colors = [
        (0, 255, 255),    # Cyan
        (255, 255, 0),    # Yellow
        (128, 0, 128),    # Purple
        (255, 0, 0),      # Red
    ]
    
    # Fallen pieces grid
    grid = [[0 for _ in range(w)] for _ in range(h)]
    
    for _ in range(50):
        # New piece
        piece_type = random.randint(0, len(pieces) - 1)
        piece = pieces[piece_type]
        piece_color = piece_colors[piece_type]
        piece_x = random.randint(0, w - len(piece[0]))
        piece_y = 0
        
        # Fall animation
        while piece_y < h - len(piece):
            graphics.set_pen(BLACK)
            graphics.clear()
            
            # Draw fallen pieces
            for y in range(h):
                for x in range(w):
                    if grid[y][x]:
                        color = graphics.create_pen(*grid[y][x])
                        graphics.set_pen(color)
                        graphics.pixel(x, y)
            
            # Draw falling piece
            color = graphics.create_pen(*piece_color)
            graphics.set_pen(color)
            for y, row in enumerate(piece):
                for x, pixel in enumerate(row):
                    if pixel and piece_x + x < w:
                        graphics.pixel(piece_x + x, piece_y + y)
            
            picounicorn.update(graphics)
            time.sleep(0.1)
            
            # Check collision
            can_fall = True
            for y, row in enumerate(piece):
                for x, pixel in enumerate(row):
                    if pixel:
                        if piece_y + y + 1 >= h or grid[piece_y + y + 1][piece_x + x]:
                            can_fall = False
                            break
            
            if can_fall:
                piece_y += 1
            else:
                # Lock piece in place
                for y, row in enumerate(piece):
                    for x, pixel in enumerate(row):
                        if pixel and piece_y + y < h and piece_x + x < w:
                            grid[piece_y + y][piece_x + x] = piece_color
                break

# 4. SNAKE GAME
def snake_game():
    """Classic snake moving around"""
    snake = [(w//2, h//2)]
    direction = (1, 0)
    food = (random.randint(0, w-1), random.randint(0, h-1))
    
    for frame in range(200):
        # Auto-steer snake towards food (AI snake!)
        if frame % 10 == 0:
            head_x, head_y = snake[0]
            food_x, food_y = food
            
            if abs(food_x - head_x) > abs(food_y - head_y):
                direction = (1 if food_x > head_x else -1, 0)
            else:
                direction = (0, 1 if food_y > head_y else -1)
        
        # Move snake
        if frame % 5 == 0:
            head_x, head_y = snake[0]
            new_head = ((head_x + direction[0]) % w, (head_y + direction[1]) % h)
            
            snake.insert(0, new_head)
            
            # Check food collision
            if new_head == food:
                food = (random.randint(0, w-1), random.randint(0, h-1))
            else:
                snake.pop()  # Remove tail if no food eaten
        
        # Draw
        graphics.set_pen(BLACK)
        graphics.clear()
        
        # Draw snake with gradient
        for i, (x, y) in enumerate(snake):
            brightness = 255 - (i * 20)
            color = graphics.create_pen(0, max(50, brightness), 0)
            graphics.set_pen(color)
            graphics.pixel(x, y)
        
        # Draw food (blinking)
        if (frame // 5) % 2:
            food_color = graphics.create_pen(255, 0, 0)
            graphics.set_pen(food_color)
            graphics.pixel(food[0], food[1])
        
        picounicorn.update(graphics)
        time.sleep(0.03)

# 5. PONG
def pong_game():
    """Classic Pong animation"""
    ball_x, ball_y = w // 2, h // 2
    ball_vx, ball_vy = 0.3, 0.2
    paddle1_y = h // 2
    paddle2_y = h // 2
    
    for frame in range(300):
        # Update ball
        ball_x += ball_vx
        ball_y += ball_vy
        
        # Ball collision with top/bottom
        if ball_y <= 0 or ball_y >= h - 1:
            ball_vy = -ball_vy
        
        # Ball collision with paddles
        if ball_x <= 1 and abs(ball_y - paddle1_y) < 2:
            ball_vx = abs(ball_vx)
        elif ball_x >= w - 2 and abs(ball_y - paddle2_y) < 2:
            ball_vx = -abs(ball_vx)
        
        # Ball out of bounds
        if ball_x < 0 or ball_x > w:
            ball_x, ball_y = w // 2, h // 2
            ball_vx = 0.3 if random.random() > 0.5 else -0.3
        
        # AI paddles follow ball
        paddle1_y += (ball_y - paddle1_y) * 0.1
        paddle2_y += (ball_y - paddle2_y) * 0.1
        
        # Draw
        graphics.set_pen(BLACK)
        graphics.clear()
        
        # Draw paddles
        paddle_color = graphics.create_pen(255, 255, 255)
        graphics.set_pen(paddle_color)
        
        for i in range(-1, 2):
            if 0 <= int(paddle1_y) + i < h:
                graphics.pixel(0, int(paddle1_y) + i)
            if 0 <= int(paddle2_y) + i < h:
                graphics.pixel(w - 1, int(paddle2_y) + i)
        
        # Draw ball
        ball_color = graphics.create_pen(255, 255, 255)
        graphics.set_pen(ball_color)
        graphics.pixel(int(ball_x), int(ball_y))
        
        # Draw center line
        for y in range(0, h, 2):
            graphics.pixel(w // 2, y)
        
        picounicorn.update(graphics)
        time.sleep(0.02)

# 6. ENHANCED PARTICLE TRAILS (Your favorite!)
def enhanced_particle_trails():
    """Multiple particle systems with different behaviors"""
    global particles
    
    # Initialize different particle types
    particles = []
    # Fire particles
    for _ in range(8):
        p = Particle()
        p.color_type = 0  # Orange/fire
        p.vy = random.uniform(-0.8, -0.3)  # Upward
        p.vx = random.uniform(-0.2, 0.2)
        p.y = h - 1
        particles.append(p)
    
    # Electric particles
    for _ in range(6):
        p = Particle()
        p.color_type = 1  # Cyan/electric
        p.vx = random.uniform(-1, 1)
        p.vy = 0
        particles.append(p)
    
    # Spiral particles
    for _ in range(6):
        p = Particle()
        p.color_type = 2  # Purple
        particles.append(p)
    
    trail_buffer = [[0 for _ in range(w)] for _ in range(h)]
    
    for frame in range(200):
        # Fade trail buffer
        for y in range(h):
            for x in range(w):
                if trail_buffer[y][x] > 0:
                    trail_buffer[y][x] = max(0, trail_buffer[y][x] - 15)
        
        # Update particles
        for i, p in enumerate(particles):
            p.update()
            
            # Special behaviors
            if p.color_type == 2:  # Spiral motion
                angle = frame * 0.1 + i
                p.vx = math.cos(angle) * 0.3
                p.vy = math.sin(angle) * 0.3
            
            # Add to trail buffer
            px, py = int(p.x), int(p.y)
            if 0 <= px < w and 0 <= py < h:
                trail_buffer[py][px] = min(255, trail_buffer[py][px] + int(255 * p.life))
        
        # Draw everything
        graphics.set_pen(BLACK)
        graphics.clear()
        
        # Draw trails
        for y in range(h):
            for x in range(w):
                if trail_buffer[y][x] > 0:
                    val = trail_buffer[y][x]
                    # Create gradient trail effect
                    r = min(255, val)
                    g = min(255, val // 2)
                    b = min(255, val // 4)
                    color = graphics.create_pen(r, g, b)
                    graphics.set_pen(color)
                    graphics.pixel(x, y)
        
        # Draw particles
        for p in particles:
            px, py = int(p.x), int(p.y)
            if 0 <= px < w and 0 <= py < h:
                r, g, b = p.get_color()
                color = graphics.create_pen(r, g, b)
                graphics.set_pen(color)
                graphics.pixel(px, py)
        
        picounicorn.update(graphics)
        time.sleep(0.02)

# 7. GALAGA STYLE ATTACK PATTERNS
def galaga_attack():
    """Enemies diving in formation"""
    for wave in range(3):
        enemies = []
        # Create enemy formation
        for i in range(4):
            enemies.append({
                'x': i * 4 + 2,
                'y': -2 - i,
                'type': i % 2,
                'angle': 0
            })
        
        for frame in range(150):
            graphics.set_pen(BLACK)
            graphics.clear()
            
            # Update enemies
            for enemy in enemies:
                # Sine wave diving pattern
                enemy['angle'] += 0.1
                enemy['y'] += 0.15
                enemy['x'] += math.sin(enemy['angle']) * 0.5
                
                # Wrap around
                if enemy['y'] > h + 2:
                    enemy['y'] = -2
                    enemy['x'] = random.randint(1, w-2)
                
                # Draw enemy
                ex, ey = int(enemy['x']), int(enemy['y'])
                if 0 <= ex < w and 0 <= ey < h:
                    if enemy['type'] == 0:
                        color = graphics.create_pen(255, 0, 255)  # Magenta
                    else:
                        color = graphics.create_pen(0, 255, 255)  # Cyan
                    graphics.set_pen(color)
                    graphics.pixel(ex, ey)
                    
                    # Simple enemy shape
                    if 0 <= ex-1 < w:
                        graphics.pixel(ex-1, ey)
                    if 0 <= ex+1 < w:
                        graphics.pixel(ex+1, ey)
            
            # Player ship at bottom
            player_x = w // 2 + int(math.sin(frame * 0.05) * 3)
            ship_color = graphics.create_pen(0, 255, 0)
            graphics.set_pen(ship_color)
            if h-1 >= 0:
                graphics.pixel(player_x, h-1)
                if player_x-1 >= 0:
                    graphics.pixel(player_x-1, h-1)
                if player_x+1 < w:
                    graphics.pixel(player_x+1, h-1)
            
            picounicorn.update(graphics)
            time.sleep(0.02)

# 8. MATRIX RAIN ENHANCED
def matrix_rain_enhanced():
    """Enhanced matrix rain with multiple speeds and glyphs"""
    drops = []
    for x in range(w):
        drops.append({
            'y': random.uniform(-h, 0),
            'speed': random.uniform(0.2, 0.8),
            'length': random.randint(3, 6),
            'brightness': random.uniform(0.5, 1.0)
        })
    
    for frame in range(200):
        # Fade effect
        for y in range(h):
            for x in range(w):
                fade = graphics.create_pen(0, 0, 0)
                graphics.set_pen(fade)
                graphics.pixel(x, y)
        
        # Update drops
        for x, drop in enumerate(drops):
            drop['y'] += drop['speed']
            
            # Draw drop with tail
            for i in range(drop['length']):
                y = int(drop['y'] - i)
                if 0 <= y < h:
                    if i == 0:
                        # Bright head
                        brightness = int(255 * drop['brightness'])
                        color = graphics.create_pen(brightness//4, brightness, brightness//2)
                    else:
                        # Fading tail
                        fade_factor = 1 - (i / drop['length'])
                        brightness = int(150 * fade_factor * drop['brightness'])
                        color = graphics.create_pen(0, brightness, brightness//4)
                    
                    graphics.set_pen(color)
                    graphics.pixel(x, y)
            
            # Reset if off screen
            if drop['y'] - drop['length'] > h:
                drop['y'] = random.uniform(-h, -2)
                drop['speed'] = random.uniform(0.2, 0.8)
                drop['length'] = random.randint(3, 6)
                drop['brightness'] = random.uniform(0.5, 1.0)
        
        picounicorn.update(graphics)
        time.sleep(0.03)

# Main showcase loop
print("Retro Arcade & Particle Paradise!")
print("A: Skip | B: Pause | X: Slower | Y: Faster")

animation_speed = 1.0
current_anim = 0

animations = [
    ("Enhanced Particle Trails", enhanced_particle_trails),
    ("Space Invaders", space_invaders),
    ("Pac-Man Chase", pacman_chase),
    ("Tetris Blocks", tetris_blocks),
    ("Snake Game", snake_game),
    ("Pong", pong_game),
    ("Galaga Attack", galaga_attack),
    ("Matrix Rain Enhanced", matrix_rain_enhanced),
]

while True:
    # Check buttons
    if picounicorn.is_pressed(picounicorn.BUTTON_A):
        current_anim = (current_anim + 1) % len(animations)
        time.sleep(0.2)  # Debounce
    
    if picounicorn.is_pressed(picounicorn.BUTTON_X):
        animation_speed = max(0.5, animation_speed * 0.8)
    
    if picounicorn.is_pressed(picounicorn.BUTTON_Y):
        animation_speed = min(2.0, animation_speed * 1.2)
    
    # Run current animation
    name, func = animations[current_anim]
    print(f"Playing: {name}")
    func()
    
    # Auto-advance
    current_anim = (current_anim + 1) % len(animations)