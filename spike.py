import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image
import random, math
import time
import os

class QuantumSpikeAnimator:
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 QUANTUM SPIKE ART")
        self.root.configure(bg="#0a0a0a")
        
        # Neural Style Transfer System
        self.style_patterns = {
            "Van Gogh": self.van_gogh_style,
            "Pixel Art": self.pixel_art_style,
            "Cyberpunk": self.cyberpunk_style,
        }
        self.current_style = "Normal"
        
        # Quantum Spike System
        self.quantum_spikes = []
        
        # Animation control
        self.animation_running = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main canvas
        self.canvas = tk.Canvas(self.root, bg="#000010", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Control Panel
        control_frame = tk.Frame(self.root, bg="#001122", relief='ridge', bd=2)
        control_frame.pack(fill="x", padx=10, pady=5)
        
        # Style Transfer
        style_frame = tk.LabelFrame(control_frame, text="🎨 STYLE", 
                                  bg="#001122", fg="#ff00ff", font=("Courier", 10, "bold"))
        style_frame.pack(fill="x", padx=5, pady=2)
        
        self.style_var = tk.StringVar(value="Normal")
        style_combo = ttk.Combobox(style_frame, textvariable=self.style_var,
                                  values=["Normal"] + list(self.style_patterns.keys()),
                                  state="readonly", width=12)
        style_combo.pack(side="left", padx=2)
        style_combo.bind('<<ComboboxSelected>>', self.change_style)
        
        # Spike Animation Controls
        spike_frame = tk.LabelFrame(control_frame, text="⚡ SPIKE ANIMATION", 
                                  bg="#001122", fg="#00ffff", font=("Courier", 10, "bold"))
        spike_frame.pack(fill="x", padx=5, pady=2)
        
        # Animation buttons
        anim_frame = tk.Frame(spike_frame, bg="#001122")
        anim_frame.pack(fill="x", pady=2)
        
        tk.Button(anim_frame, text="🌀 Spiral", command=lambda: self.generate_spikes("spiral"),
                 bg="#004466", fg="white", font=("Arial", 8)).pack(side="left", padx=1)
        tk.Button(anim_frame, text="✨ Shooting", command=lambda: self.generate_spikes("shooting"),
                 bg="#004466", fg="white", font=("Arial", 8)).pack(side="left", padx=1)
        tk.Button(anim_frame, text="🔄 Orbit", command=lambda: self.generate_spikes("orbit"),
                 bg="#004466", fg="white", font=("Arial", 8)).pack(side="left", padx=1)
        tk.Button(anim_frame, text="🎯 Bounce", command=lambda: self.generate_spikes("bounce"),
                 bg="#004466", fg="white", font=("Arial", 8)).pack(side="left", padx=1)
        
        # Parameters
        param_frame = tk.Frame(spike_frame, bg="#001122")
        param_frame.pack(fill="x", pady=5)
        
        tk.Label(param_frame, text="Intensity:", bg="#001122", fg="white").pack(side="left")
        self.intensity_var = tk.DoubleVar(value=0.5)
        intensity_scale = tk.Scale(param_frame, from_=0.1, to=2.0, resolution=0.1,
                                  orient="horizontal", variable=self.intensity_var,
                                  length=80, bg="#220011", fg="#ff00ff")
        intensity_scale.pack(side="left", padx=2)
        
        tk.Label(param_frame, text="Radius:", bg="#001122", fg="white").pack(side="left")
        self.radius_var = tk.DoubleVar(value=50)
        radius_scale = tk.Scale(param_frame, from_=10, to=200, resolution=10,
                               orient="horizontal", variable=self.radius_var,
                               length=80, bg="#002211", fg="#00ff00")
        radius_scale.pack(side="left", padx=2)
        
        # Basic controls
        basic_frame = tk.Frame(control_frame, bg="#001122")
        basic_frame.pack(fill="x", padx=5, pady=2)
        
        tk.Button(basic_frame, text="📁 Upload Image", command=self.select_image,
                 bg="#333333", fg="white").pack(side="left", padx=2)
        tk.Button(basic_frame, text="▶️ Start", command=self.start_animation,
                 bg="#006600", fg="white").pack(side="left", padx=2)
        tk.Button(basic_frame, text="⏹️ Stop", command=self.stop_animation,
                 bg="#660000", fg="white").pack(side="left", padx=2)
        tk.Button(basic_frame, text="❌ Clear", command=self.clear_spikes,
                 bg="#660000", fg="white").pack(side="left", padx=2)
        
        # Status display
        self.status_var = tk.StringVar(value="Ready - Upload image to start")
        status_label = tk.Label(self.root, textvariable=self.status_var,
                              bg="#000000", fg="#00ff00", font=("Courier", 10))
        status_label.pack(side="bottom", fill="x")
        
        self.root.geometry("1000x700")

    # ==================== STYLE TRANSFER ====================
    
    def change_style(self, event=None):
        self.current_style = self.style_var.get()
        self.status_var.set(f"Style: {self.current_style}")
    
    def van_gogh_style(self, r, g, b, x, y, t):
        swirl = math.sin(x * 0.05 + y * 0.03 + t * 2) * 80
        r = (r + swirl * 0.8) % 256
        g = (g + swirl * 0.6) % 256  
        b = (b + swirl * 0.4) % 256
        return int(r), int(g), int(b)
    
    def pixel_art_style(self, r, g, b, x, y, t):
        r = (r // 32) * 32
        g = (g // 32) * 32
        b = (b // 32) * 32
        return r, g, b
    
    def cyberpunk_style(self, r, g, b, x, y, t):
        pulse = (math.sin(t * 4 + x * 0.02) + 1) * 0.5
        r = int(r * 0.2 + 255 * pulse * 0.8)
        g = int(g * 0.3 + 100 * pulse * 0.5)
        b = int(b * 0.1 + 255 * pulse * 0.9)
        return r, g, b
    
    def apply_style_transfer(self, r, g, b, x, y, t):
        if self.current_style == "Normal":
            return r, g, b
        style_function = self.style_patterns.get(self.current_style)
        if style_function:
            return style_function(r, g, b, x, y, t)
        return r, g, b

    # ==================== SPIKE ANIMATION SYSTEM ====================
    
    def generate_spikes(self, animation_type):
        if not self.animation_running:
            messagebox.showinfo("Info", "Please start animation first!")
            return
            
        self.quantum_spikes = []
        num_spikes = 6
        
        center_x, center_y = self.w // 2, self.h // 2
        
        for i in range(num_spikes):
            if animation_type == "spiral":
                spike = self.create_spiral_spike(i, num_spikes, center_x, center_y)
            elif animation_type == "shooting":
                spike = self.create_shooting_spike(i, center_x, center_y)
            elif animation_type == "orbit":
                spike = self.create_orbiting_spike(i, num_spikes, center_x, center_y)
            elif animation_type == "bounce":
                spike = self.create_bouncing_spike(i, center_x, center_y)
            else:
                spike = self.create_spiral_spike(i, num_spikes, center_x, center_y)
                
            self.quantum_spikes.append(spike)
            
        animation_names = {
            "spiral": "Spiral", "shooting": "Shooting Stars", 
            "orbit": "Orbit", "bounce": "Bouncing"
        }
        self.status_var.set(f"{animation_names[animation_type]} - {num_spikes} spikes")

    def create_spiral_spike(self, index, total, center_x, center_y):
        angle = (index / total) * 2 * math.pi
        return {
            'type': 'spiral',
            'x': center_x,
            'y': center_y,
            'angle': angle,
            'radius': 20,
            'speed': 0.5,
            'color_shift': (index / total) * 2 * math.pi,
            'intensity': self.intensity_var.get(),
            'effect_radius': self.radius_var.get(),
        }
    
    def create_shooting_spike(self, index, center_x, center_y):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(50, 150)
        start_x = center_x + math.cos(angle) * distance
        start_y = center_y + math.sin(angle) * distance
        
        dx = center_x - start_x
        dy = center_y - start_y
        length = math.sqrt(dx*dx + dy*dy)
        move_x = dx / length if length > 0 else 0
        move_y = dy / length if length > 0 else 0
        
        return {
            'type': 'shooting',
            'x': start_x,
            'y': start_y,
            'move_x': move_x,
            'move_y': move_y,
            'speed': 1.0,
            'color_shift': random.uniform(0, 2 * math.pi),
            'intensity': self.intensity_var.get() * 1.2,
            'effect_radius': self.radius_var.get() * 0.6,
        }
    
    def create_orbiting_spike(self, index, total, center_x, center_y):
        orbit_radius = 60 + index * 10
        return {
            'type': 'orbit',
            'x': center_x + orbit_radius,
            'y': center_y,
            'orbit_radius': orbit_radius,
            'orbit_angle': (index / total) * 2 * math.pi,
            'speed': 0.2,
            'color_shift': (index / total) * 2 * math.pi,
            'intensity': self.intensity_var.get(),
            'effect_radius': self.radius_var.get() * 0.6,
        }
    
    def create_bouncing_spike(self, index, center_x, center_y):
        start_x = random.uniform(50, self.w - 50)
        start_y = random.uniform(50, self.h - 50)
        angle = random.uniform(0, 2 * math.pi)
        
        return {
            'type': 'bounce',
            'x': start_x,
            'y': start_y,
            'move_x': math.cos(angle),
            'move_y': math.sin(angle),
            'speed': 0.8,
            'color_shift': random.uniform(0, 2 * math.pi),
            'intensity': self.intensity_var.get(),
            'effect_radius': self.radius_var.get() * 0.5,
        }
    
    def clear_spikes(self):
        self.quantum_spikes = []
        self.status_var.set("Spikes cleared")
    
    def update_spike_animations(self, t):
        for spike in self.quantum_spikes:
            if spike['type'] == 'spiral':
                self.update_spiral_spike(spike, t)
            elif spike['type'] == 'shooting':
                self.update_shooting_spike(spike, t)
            elif spike['type'] == 'orbit':
                self.update_orbiting_spike(spike, t)
            elif spike['type'] == 'bounce':
                self.update_bouncing_spike(spike, t)
    
    def update_spiral_spike(self, spike, t):
        spike['radius'] += spike['speed'] * 0.8
        spike['angle'] += 0.05
        spike['x'] = self.w // 2 + math.cos(spike['angle']) * spike['radius']
        spike['y'] = self.h // 2 + math.sin(spike['angle']) * spike['radius']
        spike['color_shift'] += 0.02
    
    def update_shooting_spike(self, spike, t):
        spike['x'] += spike['move_x'] * spike['speed'] * 2
        spike['y'] += spike['move_y'] * spike['speed'] * 2
        spike['color_shift'] += 0.04
        
        if (spike['x'] < -100 or spike['x'] > self.w + 100 or 
            spike['y'] < -100 or spike['y'] > self.h + 100):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(50, 150)
            spike['x'] = self.w // 2 + math.cos(angle) * distance
            spike['y'] = self.h // 2 + math.sin(angle) * distance
    
    def update_orbiting_spike(self, spike, t):
        spike['orbit_angle'] += spike['speed']
        spike['x'] = self.w // 2 + math.cos(spike['orbit_angle']) * spike['orbit_radius']
        spike['y'] = self.h // 2 + math.sin(spike['orbit_angle']) * spike['orbit_radius']
        spike['color_shift'] += 0.015
    
    def update_bouncing_spike(self, spike, t):
        spike['x'] += spike['move_x'] * spike['speed']
        spike['y'] += spike['move_y'] * spike['speed']
        spike['color_shift'] += 0.02
        
        if spike['x'] <= 0 or spike['x'] >= self.w:
            spike['move_x'] *= -1
        if spike['y'] <= 0 or spike['y'] >= self.h:
            spike['move_y'] *= -1

    def apply_spike_effects(self, r, g, b, x, y, t):
        if not self.quantum_spikes:
            return r, g, b
            
        total_effect_r = 0
        total_effect_g = 0  
        total_effect_b = 0
        
        for spike in self.quantum_spikes:
            dx = x - spike['x']
            dy = y - spike['y']
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < spike['effect_radius']:
                intensity = (1 - distance / spike['effect_radius']) * spike['intensity']
                color_shift = spike['color_shift']
                
                r_shift = math.sin(color_shift) * 60 * intensity
                g_shift = math.cos(color_shift) * 60 * intensity
                b_shift = math.sin(color_shift + math.pi/2) * 60 * intensity
                
                total_effect_r += r_shift
                total_effect_g += g_shift
                total_effect_b += b_shift
        
        r = max(0, min(255, r + total_effect_r))
        g = max(0, min(255, g + total_effect_g))
        b = max(0, min(255, b + total_effect_b))
        
        return int(r), int(g), int(b)

    # ==================== CORE SYSTEM ====================
    
    def select_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if not path: 
            return
            
        try:
            self.image = Image.open(path).convert("RGB")
            self.prepare_pixels()
            self.status_var.set(f"Loaded: {os.path.basename(path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def prepare_pixels(self):
        self.canvas.delete("all")
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if w <= 1 or h <= 1:
            w, h = 800, 600
            
        self.pixel_size = max(2, min(8, w // 150))
        
        self.resized = self.image.resize((w//self.pixel_size, h//self.pixel_size))
        self.pixels = self.resized.load()
        self.w, self.h = self.resized.size

        self.pixel_list = []
        self.pixel_objects = {}
        self.pixel_vel = {}
        self.original_positions = {}  # Store original positions
        
        for x in range(self.w):
            for y in range(self.h):
                px, py = float(x), float(y)
                pixel_id = (px, py)
                
                vx = random.uniform(-1, 1)
                vy = random.uniform(-1, 1)
                
                self.pixel_vel[pixel_id] = (vx, vy)
                self.pixel_list.append([px, py])
                self.original_positions[pixel_id] = (px, py)  # Save original position
                
                r, g, b = self.pixels[x, y]
                color = f"#{r:02x}{g:02x}{b:02x}"
                
                rect = self.canvas.create_rectangle(
                    px*self.pixel_size, py*self.pixel_size,
                    px*self.pixel_size+self.pixel_size, 
                    py*self.pixel_size+self.pixel_size,
                    fill=color, outline=color
                )
                self.pixel_objects[pixel_id] = rect

        self.index = 0
        self.pixels_per_frame = min(500, max(50, len(self.pixel_list)//200))
        self.status_var.set(f"{len(self.pixel_list)} pixels ready")

    def start_animation(self):
        if not hasattr(self, 'pixel_list') or not self.pixel_list:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
            
        self.animation_running = True
        self.start_time = time.time()
        self.frame_count = 0
        self.status_var.set("Animation started")
        self.animate()

    def stop_animation(self):
        self.animation_running = False
        self.status_var.set("Animation stopped")
        
        # Reset all pixels to their original positions
        if hasattr(self, 'original_positions'):
            for i in range(len(self.pixel_list)):
                px, py = self.pixel_list[i]
                pixel_id = (px, py)
                if pixel_id in self.original_positions:
                    orig_x, orig_y = self.original_positions[pixel_id]
                    self.pixel_list[i] = [orig_x, orig_y]
                    
                    # Update display immediately
                    if pixel_id in self.pixel_objects:
                        rect = self.pixel_objects[pixel_id]
                        self.canvas.coords(rect, 
                                         orig_x*self.pixel_size, orig_y*self.pixel_size,
                                         orig_x*self.pixel_size+self.pixel_size, 
                                         orig_y*self.pixel_size+self.pixel_size)
                        
                        # Reset to original color
                        x_int, y_int = int(orig_x), int(orig_y)
                        if 0 <= x_int < self.w and 0 <= y_int < self.h:
                            try:
                                r, g, b = self.pixels[x_int, y_int]
                                color = f"#{r:02x}{g:02x}{b:02x}"
                                self.canvas.itemconfig(rect, fill=color)
                            except (IndexError, TypeError):
                                pass

    def animate(self):
        if not self.animation_running:
            return

        current_time = time.time() - self.start_time

        # Update spike animations
        self.update_spike_animations(current_time)

        for _ in range(self.pixels_per_frame):
            if self.index >= len(self.pixel_list):
                self.index = 0

            px, py = self.pixel_list[self.index]
            pixel_id = (px, py)
            x_int, y_int = int(px) % self.w, int(py) % self.h

            try:
                r, g, b = self.pixels[x_int, y_int]
            except (IndexError, TypeError):
                self.index += 1
                continue

            r, g, b = self.apply_style_transfer(r, g, b, px, py, current_time)
            r, g, b = self.apply_spike_effects(r, g, b, px, py, current_time)

            color = f"#{r:02x}{g:02x}{b:02x}"
            
            if pixel_id in self.pixel_objects:
                rect = self.pixel_objects[pixel_id]
                self.canvas.coords(rect, 
                                 px*self.pixel_size, py*self.pixel_size,
                                 px*self.pixel_size+self.pixel_size, 
                                 py*self.pixel_size+self.pixel_size)
                self.canvas.itemconfig(rect, fill=color)

            # Update pixel position
            if pixel_id in self.pixel_vel:
                vx, vy = self.pixel_vel[pixel_id]
                new_x = (px + vx * 0.1) % self.w
                new_y = (py + vy * 0.1) % self.h
                self.pixel_list[self.index] = [new_x, new_y]

            self.index += 1

        self.frame_count += 1
        
        if self.frame_count % 30 == 0:
            spike_info = f"{len(self.quantum_spikes)} spikes" if self.quantum_spikes else "no spikes"
            self.status_var.set(f"Frame {self.frame_count} | Style: {self.current_style} | {spike_info}")

        self.root.after(30, self.animate)


if __name__ == "__main__":
    root = tk.Tk()
    app = QuantumSpikeAnimator(root)
    root.mainloop()