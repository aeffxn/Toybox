"""
toys/particle_burst.py

Toy: Particle Burst.

"""

import tkinter as tk
import random
import math
import theme


class Particle:
    def __init__(self, x, y):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 9)
        self.x = x
        self.y = y
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = 1.0
        self.decay = random.uniform(0.03, 0.07)
        self.radius = random.uniform(2, 5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.92
        self.vy *= 0.92
        self.life -= self.decay

    @property
    def alive(self):
        return self.life > 0


class ParticleBurstToy(tk.Frame):
    FRAME_DELAY_MS = 16
    MAX_PARTICLES = 300

    def __init__(self, parent):
        super().__init__(parent, bg=theme.PANEL)

        theme.toy_title(
            self, "Particle Burst",
            "Click anywhere on the canvas to explode.",
        )

        self.canvas = tk.Canvas(
            self, bg=theme.VOID, highlightthickness=1,
            highlightbackground=theme.PANEL_EDGE,
        )
        self.canvas.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        self.particles = []
        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<B1-Motion>", self._on_click)

        self._running = True
        self._animate()

    def _on_click(self, event):
        new_particles = [Particle(event.x, event.y) for _ in range(25)]
        self.particles.extend(new_particles)
        # Cap total so it can't grind to a halt with thousands of particles.
        if len(self.particles) > self.MAX_PARTICLES:
            self.particles = self.particles[-self.MAX_PARTICLES:]

    def _animate(self):
        if not self._running:
            return

        self.canvas.delete("particle")
        self.particles = [p for p in self.particles if p.alive]

        for p in self.particles:
            p.update()
            # Fade toward void color as life decreases.
            alpha = int(p.life * 255)
            # Interpolate between GLOW (#FFD60A) and a dim version.
            r = int(255 * p.life)
            g = int(214 * p.life)
            b = int(10 * p.life)
            color = f"#{max(0,min(255,r)):02x}{max(0,min(255,g)):02x}{max(0,min(255,b)):02x}"
            r_draw = max(1, p.radius * p.life)
            self.canvas.create_oval(
                p.x - r_draw, p.y - r_draw, p.x + r_draw, p.y + r_draw,
                fill=color, outline="", tags="particle",
            )

        self.after(self.FRAME_DELAY_MS, self._animate)

    def stop(self):
        self._running = False