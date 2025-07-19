from picounicorn import PicoUnicorn
from picographics import PicoGraphics, DISPLAY_UNICORN_PACK
import time
import math
import random

# Initialize both PicoUnicorn and PicoGraphics
picounicorn = PicoUnicorn()
graphics = PicoGraphics(display=DISPLAY_UNICORN_PACK)

# Get dimensions
w = picounicorn.get_width()
h = picounicorn.get_height()

# Create base colors
BLACK = graphics.create_pen(0, 0, 0)

# TEMPORAL COLOR MIXING AND PERSISTENCE OF VISION EFFECTS

# 1. TEMPORAL DITHERING ENGINE
class TemporalDither:
    """Create colors that don't exist by rapidly switching between others"""
    def __init__(self):
        self.frame = 0
        self.dither_patterns = [
            [1, 0, 1, 0],  # 50%
            [1, 1, 0, 0],  # 50% phase shifted
            [1, 1, 1, 0],  # 75%
            [1, 0, 0, 0],  # 25%
        ]
    
    def get_mixed_color(self, color1, color2, ratio, pixel_phase=0):
        """Mix two colors using temporal dithering"""
        pattern_index = int(ratio * len(self.dither_patterns))
        pattern_index = min(pattern_index, len(self.dither_patterns) - 1)
        pattern = self.dither_patterns[pattern_index]
        
        # Use frame counter and pixel phase for temporal variation
        use_first = pattern[(self.frame + pixel_phase) % len(pattern)]
        return color1 if use_first else color2
    
    def update(self):
        self.frame += 1

# 2. SUBPIXEL RENDERING
def subpixel_shimmer():
    """Exploit rapid color changes to create shimmering effects"""
    dither = TemporalDither()
    phase_offset = [[random.randint(0, 3) for _ in range(w)] for _ in range(h)]
    
    for frame in range(300):
        dither.update()
        t = frame * 0.02
        
        for y in range(h):
            for x in range(w):
                # Base wave pattern
                wave1 = math.sin(x * 0.5 + t) * 0.5 + 0.5
                wave2 = math.sin(y * 0.5 + t * 1.3) * 0.5 + 0.5
                combined = wave1 * wave2
                
                # Create multiple color candidates
                color1 = graphics.create_pen(255, 0, 0)      # Red
                color2 = graphics.create_pen(0, 255, 0)      # Green
                color3 = graphics.create_pen(0, 0, 255)      # Blue
                color4 = graphics.create_pen(255, 255, 0)    # Yellow
                
                # Rapid switching creates color mixing illusion
                if frame % 4 == 0:
                    color = dither.get_mixed_color(color1, color2, combined, phase_offset[y][x])
                elif frame % 4 == 1:
                    color = dither.get_mixed_color(color3, color4, combined, phase_offset[y][x])
                elif frame % 4 == 2:
                    color = dither.get_mixed_color(color1, color3, combined, phase_offset[y][x])
                else:
                    color = dither.get_mixed_color(color2, color4, combined, phase_offset[y][x])
                
                graphics.set_pen(color)
                graphics.pixel(x, y)
        
        picounicorn.update(graphics)
        # No sleep - maximum framerate for persistence of vision!

# 3. CHROMATIC ABERRATION EFFECT
def chromatic_aberration():
    """Simulate color separation by drawing R, G, B channels at different times"""
    for frame in range(200):
        t = frame * 0.02
        
        # Draw only one color channel per frame
        channel = frame % 3
        
        for y in range(h):
            for x in range(w):
                # Create circular pattern
                cx = x - w/2
                cy = y - h/2
                dist = math.sqrt(cx*cx + cy*cy)
                
                # Offset each channel differently
                if channel == 0:  # Red
                    offset_x = x + math.sin(t) * 0.5
                    offset_y = y
                elif channel == 1:  # Green
                    offset_x = x
                    offset_y = y + math.cos(t) * 0.5
                else:  # Blue
                    offset_x = x - math.sin(t) * 0.5
                    offset_y = y - math.cos(t) * 0.5
                
                # Sample pattern at offset position
                pattern = math.sin(dist - t * 5) * 0.5 + 0.5
                
                # Draw only the active channel
                if pattern > 0.3:
                    if channel == 0:
                        color = graphics.create_pen(255, 0, 0)
                    elif channel == 1:
                        color = graphics.create_pen(0, 255, 0)
                    else:
                        color = graphics.create_pen(0, 0, 255)
                    
                    graphics.set_pen(color)
                    graphics.pixel(x, y)
                else:
                    graphics.set_pen(BLACK)
                    graphics.pixel(x, y)
        
        picounicorn.update(graphics)
        # Minimal sleep for persistence effect

# 4. INTERLACED PATTERNS
def interlaced_waves():
    """Use interlacing to create impossible gradients"""
    for frame in range(400):
        t = frame * 0.01
        
        # Even/odd frame interlacing
        interlace = frame % 2
        
        for y in range(h):
            # Only update every other row per frame
            if y % 2 == interlace:
                for x in range(w):
                    # Complex wave interference
                    wave1 = math.sin(x * 0.8 + t * 2)
                    wave2 = math.cos(y * 1.2 + t * 3)
                    wave3 = math.sin((x + y) * 0.5 + t)
                    
                    # Combine waves
                    combined = (wave1 + wave2 + wave3) / 3
                    
                    # Alternate between color sets each frame
                    if interlace == 0:
                        if combined > 0:
                            hue = 0.0  # Red spectrum
                        else:
                            hue = 0.3  # Green spectrum
                    else:
                        if combined > 0:
                            hue = 0.6  # Blue spectrum
                        else:
                            hue = 0.8  # Magenta spectrum
                    
                    brightness = abs(combined)
                    PEN = graphics.create_pen_hsv(hue, 1.0, brightness)
                    graphics.set_pen(PEN)
                    graphics.pixel(x, y)
        
        picounicorn.update(graphics)

# 5. PHASE-SHIFTED COLOR CYCLING
def phase_cycling():
    """Each pixel cycles through colors at different phases"""
    # Initialize phase for each pixel
    phases = [[random.uniform(0, 2 * math.pi) for _ in range(w)] for _ in range(h)]
    frequencies = [[random.uniform(0.5, 2.0) for _ in range(w)] for _ in range(h)]
    
    for frame in range(500):
        t = frame * 0.02
        
        for y in range(h):
            for x in range(w):
                # Each pixel has its own phase and frequency
                phase = phases[y][x]
                freq = frequencies[y][x]
                
                # Calculate color components with different phase offsets
                r = int((math.sin(t * freq + phase) + 1) * 127)
                g = int((math.sin(t * freq + phase + 2.094) + 1) * 127)
                b = int((math.sin(t * freq + phase + 4.189) + 1) * 127)
                
                # Rapid switching between primary colors
                cycle = int(t * 20) % 3
                if cycle == 0:
                    color = graphics.create_pen(r, 0, 0)
                elif cycle == 1:
                    color = graphics.create_pen(0, g, 0)
                else:
                    color = graphics.create_pen(0, 0, b)
                
                graphics.set_pen(color)
                graphics.pixel(x, y)
        
        picounicorn.update(graphics)

# 6. PERSISTENCE TRAILS WITH COLOR MEMORY
def persistence_trails():
    """Use persistence of vision to create color trails"""
    # Color history for each pixel
    history = [[[0, 0, 0] for _ in range(w)] for _ in range(h)]
    
    particles = []
    for _ in range(5):
        particles.append({
            'x': random.uniform(0, w),
            'y': random.uniform(0, h),
            'vx': random.uniform(-1, 1),
            'vy': random.uniform(-1, 1),
            'hue': random.uniform(0, 1)
        })
    
    for frame in range(400):
        # Update particles
        for p in particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            
            # Bounce
            if p['x'] <= 0 or p['x'] >= w-1:
                p['vx'] = -p['vx']
            if p['y'] <= 0 or p['y'] >= h-1:
                p['vy'] = -p['vy']
            
            # Update hue
            p['hue'] = (p['hue'] + 0.01) % 1.0
        
        # Render with temporal effects
        for y in range(h):
            for x in range(w):
                # Check if particle is here
                particle_here = False
                for p in particles:
                    if abs(p['x'] - x) < 1 and abs(p['y'] - y) < 1:
                        particle_here = True
                        # Convert HSV to RGB manually for history
                        r, g, b = hsv_to_rgb(p['hue'], 1.0, 1.0)
                        history[y][x] = [r, g, b]
                        break
                
                if particle_here:
                    # Full brightness
                    r, g, b = history[y][x]
                else:
                    # Fade history
                    history[y][x][0] = max(0, history[y][x][0] - 5)
                    history[y][x][1] = max(0, history[y][x][1] - 5)
                    history[y][x][2] = max(0, history[y][x][2] - 5)
                    r, g, b = history[y][x]
                
                # Temporal dithering for smooth fades
                if frame % 3 == 0:
                    color = graphics.create_pen(r, 0, 0)
                elif frame % 3 == 1:
                    color = graphics.create_pen(0, g, 0)
                else:
                    color = graphics.create_pen(0, 0, b)
                
                graphics.set_pen(color)
                graphics.pixel(x, y)
        
        picounicorn.update(graphics)

# 7. QUANTUM COLOR SUPERPOSITION
def quantum_superposition():
    """Simulate quantum superposition with rapid state changes"""
    for frame in range(300):
        t = frame * 0.02
        
        for y in range(h):
            for x in range(w):
                # Multiple wave functions
                psi1 = math.sin(x * 0.5 + t) * math.cos(y * 0.5 + t)
                psi2 = math.cos(x * 0.7 - t) * math.sin(y * 0.7 - t)
                
                # Probability amplitudes
                prob1 = psi1 * psi1
                prob2 = psi2 * psi2
                
                # Quantum state collapses to different colors
                # based on measurement (frame number)
                measurement = (frame + x + y) % 4
                
                if measurement == 0:
                    # Red state
                    intensity = int(prob1 * 255)
                    color = graphics.create_pen(intensity, 0, 0)
                elif measurement == 1:
                    # Green state
                    intensity = int(prob2 * 255)
                    color = graphics.create_pen(0, intensity, 0)
                elif measurement == 2:
                    # Blue state
                    intensity = int((prob1 + prob2) * 127)
                    color = graphics.create_pen(0, 0, intensity)
                else:
                    # Superposition (yellow)
                    intensity = int(math.sqrt(prob1 * prob2) * 255)
                    color = graphics.create_pen(intensity, intensity, 0)
                
                graphics.set_pen(color)
                graphics.pixel(x, y)
        
        picounicorn.update(graphics)

# 8. RETINAL FATIGUE AFTERIMAGE
def afterimage_effect():
    """Create complementary color afterimages using retinal fatigue"""
    # Show primary image
    primary_frames = 60
    transition_frames = 20
    
    for cycle in range(3):
        # Primary image phase
        for frame in range(primary_frames):
            for y in range(h):
                for x in range(w):
                    # Create a simple pattern
                    if (x // 4 + y // 2) % 2 == 0:
                        if cycle == 0:
                            color = graphics.create_pen(255, 0, 0)  # Red
                        elif cycle == 1:
                            color = graphics.create_pen(0, 255, 0)  # Green
                        else:
                            color = graphics.create_pen(0, 0, 255)  # Blue
                    else:
                        color = BLACK
                    
                    graphics.set_pen(color)
                    graphics.pixel(x, y)
            
            picounicorn.update(graphics)
            time.sleep(0.02)
        
        # Quick transition to complementary
        for frame in range(transition_frames):
            brightness = int(255 * (1 - frame / transition_frames))
            
            for y in range(h):
                for x in range(w):
                    # Invert the pattern with complementary color
                    if (x // 4 + y // 2) % 2 == 1:  # Inverted
                        if cycle == 0:
                            color = graphics.create_pen(0, brightness, brightness)  # Cyan
                        elif cycle == 1:
                            color = graphics.create_pen(brightness, 0, brightness)  # Magenta
                        else:
                            color = graphics.create_pen(brightness, brightness, 0)  # Yellow
                    else:
                        color = BLACK
                    
                    graphics.set_pen(color)
                    graphics.pixel(x, y)
            
            picounicorn.update(graphics)

# Helper function
def hsv_to_rgb(h, s, v):
    i = int(h * 6.0)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6
    
    if i == 0:
        return int(v * 255), int(t * 255), int(p * 255)
    elif i == 1:
        return int(q * 255), int(v * 255), int(p * 255)
    elif i == 2:
        return int(p * 255), int(v * 255), int(t * 255)
    elif i == 3:
        return int(p * 255), int(q * 255), int(v * 255)
    elif i == 4:
        return int(t * 255), int(p * 255), int(v * 255)
    else:
        return int(v * 255), int(p * 255), int(q * 255)

# Main showcase loop
print("Temporal Color Mixing & Persistence of Vision!")
print("These effects exploit your visual system!")

effects = [
    ("Subpixel Shimmer", subpixel_shimmer),
    ("Chromatic Aberration", chromatic_aberration),
    ("Interlaced Waves", interlaced_waves),
    ("Phase-Shifted Cycling", phase_cycling),
    ("Persistence Trails", persistence_trails),
    ("Quantum Superposition", quantum_superposition),
    ("Afterimage Effect", afterimage_effect),
]

current = 0

while True:
    # Button handling
    if picounicorn.is_pressed(picounicorn.BUTTON_A):
        current = (current + 1) % len(effects)
        time.sleep(0.2)
    
    # Run current effect
    name, func = effects[current]
    print(f"Running: {name}")
    func()
    
    # Auto advance
    current = (current + 1) % len(effects)
